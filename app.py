from flask import Flask, request, redirect, url_for, render_template, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
from models import db, User, WorkoutLog, ExerciseList, WorkoutSession
from sqlalchemy import func
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Add Flask-Login initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'builtbuff.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        age = request.form['age']
        weight = request.form['weight']
        gender = request.form['gender']
        
        # Get height in feet and inches, then calculate total height in inches
        height_foot = int(request.form.get('height_foot', 0))
        height_inch = int(request.form.get('height_inch', 0))
        total_height_in_inches = height_foot * 12 + height_inch
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User with this email already exists. Please log in.", "info")
            return redirect(url_for('login'))
        
        # Create a new user
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email, 
            password=password,
            age=age,
            weight=weight,
            gender=gender,
            height=total_height_in_inches
        )
        db.session.add(new_user)
        db.session.commit()
        print(f"Created new user with ID: {new_user.user_id}")  # Debug print
        login_user(new_user)
        return redirect(url_for('profile'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/search_exercises', methods=['GET'])
@login_required
def search_exercises():
    search_term = request.args.get('search_term', '').lower()
    exercises = db.session.query(ExerciseList.name)\
        .filter(ExerciseList.name.ilike(f'%{search_term}%'))\
        .distinct()\
        .all()
    results = [{'exercise_name': exercise[0].title()} for exercise in exercises]
    return jsonify({'results': results})

@app.route('/get_equipment_options', methods=['GET'])
@login_required
def get_equipment_options():
    exercise_name = request.args.get('exercise_name', '').lower()
    equipment_options = ExerciseList.query.filter_by(
        name=exercise_name
    ).with_entities(ExerciseList.equipment).distinct().all()
    options = [equipment[0].title() for equipment in equipment_options if equipment[0]]
    return jsonify({'equipment_options': options})

@app.route('/add_workout', methods=['POST'])
def add_workout():
    if 'user_id' not in session or 'active_session_id' not in session:
        return redirect(url_for('login'))
    
    exercise_name = request.form.get('exercise_name', '').lower()
    equipment = request.form.get('equipment', '').lower()
    
    # Verify the exercise exists in our database
    exercise = ExerciseList.query.filter_by(
        name=exercise_name,
        equipment=equipment
    ).first()
    
    if not exercise:
        flash('Please select a valid exercise and equipment combination', 'danger')
        return redirect(url_for('current_workout'))
    
    # Create the workout log
    workout = WorkoutLog(
        user_id=session['user_id'],
        session_id=session['active_session_id'],
        exercise_name=exercise_name,
        equipment=equipment,
        weight=request.form.get('weight', type=float),
        reps=request.form.get('reps', type=int)
    )
    
    db.session.add(workout)
    db.session.commit()
    
    return redirect(url_for('current_workout'))

@app.route('/get_exercises', methods=['GET'])
def get_exercises():
    if 'user_id' in session:
        search_term = request.args.get('search_term', '').lower()

        # Fetch exercises matching the search term
        if search_term:
            exercises = ExerciseList.query.filter(ExerciseList.name.ilike(f'%{search_term}%')).all()
        else:
            exercises = ExerciseList.query.limit(50).all()

        # Format the response as a list of dictionaries
        results = []
        for exercise in exercises:
            description = exercise.description or ''
            preparation = ''
            execution = ''

            if 'Preparation:' in description and 'Execution:' in description:
                try:
                    preparation = description.split('Preparation:')[1].split('Execution:')[0].strip()
                    execution = description.split('Execution:')[1].strip()
                except IndexError:
                    preparation = description.strip()
            else:
                preparation = description.strip()

            results.append({
                "exercise_name": exercise.name.title(),
                "equipment": exercise.equipment.title() if exercise.equipment else 'N/A',
                "variation": exercise.variation.title() if exercise.variation else 'N/A',
                "preparation": preparation,
                "execution": execution
            })

        return jsonify({"results": results}), 200
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/search_exercise_names', methods=['GET'])
def search_exercise_names():
    if 'user_id' in session:
        search_term = request.args.get('search_term', '').lower()

        # Fetch unique exercise names matching the search term
        if search_term:
            exercises = db.session.query(ExerciseList.name).filter(
                ExerciseList.name.ilike(f'%{search_term}%')
            ).distinct().all()
        else:
            exercises = db.session.query(ExerciseList.name).distinct().limit(50).all()

        # Format the response as a list of unique exercise names
        results = []
        for exercise_name_tuple in exercises:
            exercise_name = exercise_name_tuple[0].title()
            results.append({
                "exercise_name": exercise_name
            })

        return jsonify({"results": results}), 200
    return jsonify({"error": "Unauthorized"}), 401


# @app.route('/search_exercises', methods=['GET'])
# def search_exercises():
#     if 'user_id' in session:
#         search_term = request.args.get('search_term', '').lower()

#         # Fetch exercises matching the search term
#         if search_term:
#             exercises = ExerciseList.query.filter(ExerciseList.name.ilike(f'%{search_term}%')).all()
#         else:
#             exercises = ExerciseList.query.limit(50).all()  # Limit to 50 exercises for performance

#         # Format the response as a list of dictionaries
#         results = []
#         for exercise in exercises:
#             description = exercise.description or ''
#             preparation = ''
#             execution = ''

#             if 'Preparation:' in description and 'Execution:' in description:
#                 try:
#                     preparation = description.split('Preparation:')[1].split('Execution:')[0].strip()
#                     execution = description.split('Execution:')[1].strip()
#                 except IndexError:
#                     preparation = description.strip()
#             else:
#                 preparation = description.strip()

#             results.append({
#                 "exercise_name": exercise.name.title(),
#                 "equipment": exercise.equipment.title(),
#                 "variation": exercise.variation.title(),
#                 "preparation": preparation,
#                 "execution": execution
#             })

#         return jsonify({"results": results}), 200
#     return jsonify({"error": "Unauthorized"}), 401


@app.route('/recordworkout', methods=['POST'])
def record_workout():
    if 'user_id' in session:
        workout_data = request.get_json()
        session_id = workout_data.get('session_id')

        # Check if session_id is provided and if it's an active session for the user
        if not session_id:
            return jsonify({"error": "session_id is required"}), 400

        workout_session = WorkoutSession.query.filter_by(session_id=session_id, user_id=session['user_id'], status='active').first()
        if not workout_session:
            return jsonify({"error": "No active workout session found with the provided session_id"}), 404

        # Verify exercise details
        exercise_name = workout_data.get('exercise_name')
        weight = workout_data.get('weight')
        reps = workout_data.get('reps')
        if not exercise_name or not weight or not reps:
            return jsonify({"error": "exercise_name, weight, and reps are required"}), 400

        # Create a new workout log
        new_workout_log = WorkoutLog(
            user_id=session['user_id'],
            session_id=session_id,
            exercise_name=exercise_name,
            weight=weight,
            reps=reps
        )
        db.session.add(new_workout_log)
        db.session.commit()
        return jsonify({"message": "Workout recorded successfully"}), 201
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/update_workout/<int:session_id>/<int:workout_id>', methods=['POST'])
def update_workout(session_id, workout_id):
    if 'user_id' in session:
        workout_data = request.get_json()
        workout_log = WorkoutLog.query.filter_by(workout_id=workout_id, session_id=session_id, user_id=session['user_id']).first()
        if not workout_log:
            return jsonify({"error": "Workout log not found"}), 404

        workout_log.exercise_name = workout_data.get('exercise_name', workout_log.exercise_name)
        workout_log.weight = workout_data.get('weight', workout_log.weight)
        workout_log.reps = workout_data.get('reps', workout_log.reps)
        db.session.commit()
        return jsonify({"message": "Workout updated successfully"}), 200
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/delete_workout/<int:session_id>/<int:workout_id>', methods=['DELETE'])
def delete_workout(session_id, workout_id):
    if 'user_id' in session:
        workout_log = WorkoutLog.query.filter_by(workout_id=workout_id, session_id=session_id, user_id=session['user_id']).first()
        if not workout_log:
            return jsonify({"error": "Workout log not found"}), 404

        db.session.delete(workout_log)
        db.session.commit()
        return jsonify({"message": "Workout deleted successfully"}), 200
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/profile')
@login_required
def profile():
    # Get user's recent workout sessions
    recent_sessions = WorkoutSession.query.filter_by(
        user_id=current_user.user_id,
        status='completed'
    ).order_by(WorkoutSession.start_time.desc()).limit(5).all()
    
    # Get workout statistics
    workout_stats = db.session.query(
        func.count(WorkoutSession.session_id).label('total_workouts'),
        func.sum(WorkoutLog.sets).label('total_sets'),
        func.count(WorkoutLog.workout_id).label('total_exercises')
    ).join(
        WorkoutLog, 
        WorkoutLog.session_id == WorkoutSession.session_id
    ).filter(
        WorkoutSession.user_id == current_user.user_id,
        WorkoutSession.status == 'completed'
    ).first()
    
    # Get personal records as a dictionary
    pr_query = db.session.query(
        WorkoutLog.exercise_name,
        func.max(WorkoutLog.weight).label('max_weight'),
        func.max(WorkoutLog.reps).label('max_reps')
    ).filter(
        WorkoutLog.user_id == current_user.user_id
    ).group_by(
        WorkoutLog.exercise_name
    ).all()
    
    personal_records = {
        record.exercise_name: {
            'weight': record.max_weight,
            'reps': record.max_reps
        } for record in pr_query
    }
    
    return render_template('profile.html',
                         user=current_user,
                         recent_sessions=recent_sessions,
                         workout_stats=workout_stats,
                         personal_records=personal_records)


@app.route('/view_workout/<int:session_id>/<int:workout_id>', methods=['GET'])
def view_workout(session_id, workout_id):
    if 'user_id' in session:
        workout_log = WorkoutLog.query.filter_by(workout_id=workout_id, session_id=session_id, user_id=session['user_id']).first()
        if not workout_log:
            return jsonify({"error": "Workout log not found"}), 404

        workout_data = {
            "exercise_name": workout_log.exercise_name,
            "weight": workout_log.weight,
            "reps": workout_log.reps
        }
        return jsonify(workout_data)
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/view_session/<int:session_id>', methods=['GET'])
def view_session(session_id):
    if 'user_id' in session:
        workout_session = WorkoutSession.query.filter_by(session_id=session_id, user_id=session['user_id']).first()
        if not workout_session:
            return jsonify({"error": "Workout session not found"}), 404

        workout_logs = WorkoutLog.query.filter_by(session_id=session_id).all()
        session_data = {
            "session_name": workout_session.session_name,
            "start_time": workout_session.start_time,
            "end_time": workout_session.end_time,
            "status": workout_session.status,
            "workouts": [
                {
                    "workout_id": log.workout_id,
                    "exercise_name": log.exercise_name,
                    "weight": log.weight,
                    "reps": log.reps
                }
                for log in workout_logs
            ]
        }
        return jsonify(session_data)
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/startworkout', methods=['GET', 'POST'])
@login_required
def startworkout():
    # Check for an existing active session
    active_session = WorkoutSession.query.filter_by(
        user_id=current_user.user_id, 
        status='active'
    ).first()
    
    if active_session:
        session['active_session_id'] = active_session.session_id
        flash("A workout session is already in progress.")
        return redirect(url_for('current_workout'))

    if request.method == 'POST':
        session_name = request.form.get('session_name', 'Workout Session')
        
        # Create a new workout session
        new_session = WorkoutSession(
            user_id=current_user.user_id,
            session_name=session_name,
            start_time=datetime.utcnow(),
            status='active'
        )
        db.session.add(new_session)
        db.session.commit()
        session['active_session_id'] = new_session.session_id

        return redirect(url_for('current_workout'))

    return render_template('startworkout.html')

@app.route('/current_workout')
@login_required
def current_workout():
    if 'active_session_id' not in session:
        return redirect(url_for('startworkout'))
        
    workout_session = WorkoutSession.query.get(session['active_session_id'])
    workouts = WorkoutLog.query.filter_by(session_id=session['active_session_id']).all()
    
    # Calculate 1RM for each workout
    for workout in workouts:
        workout.one_rm = workout.calculate_1rm()
    
    return render_template('current_workout.html', 
                         workout_session=workout_session, 
                         workouts=workouts)

@app.route('/update_workout_log/<int:log_id>', methods=['POST'])
def update_workout_log(log_id):
    if 'user_id' in session:
        workout_log = WorkoutLog.query.get(log_id)
        if workout_log and workout_log.user_id == session.get('user_id'):
            exercise_name = request.form.get('exercise_name')
            equipment = request.form.get('equipment')
            weight = request.form.get('weight')
            reps = request.form.get('reps')
            if exercise_name and equipment and weight and reps:
                # Verify exercise exists with the specified equipment (case-insensitive)
                exercise = ExerciseList.query.filter(
                    func.lower(ExerciseList.name) == func.lower(exercise_name),
                    func.lower(ExerciseList.equipment) == func.lower(equipment)
                ).first()
                if not exercise:
                    flash("Exercise with specified equipment not found. Please select from suggestions.", "danger")
                    return redirect(url_for('current_workout'))
                workout_log.exercise_name = exercise_name
                workout_log.equipment = equipment
                workout_log.weight = weight
                workout_log.reps = reps
                db.session.commit()
                flash("Workout updated successfully!")
            else:
                flash("Please fill out all fields.", "danger")
            
            if 'current_workout' in request.referrer:
                return redirect(url_for('current_workout'))
            else:
                return redirect(url_for('edit_session', session_id=workout_log.session_id))     
        else:
            flash("Workout log not found or unauthorized.", "danger")
    else:
        flash("Please log in to update workouts.", "danger")
    return redirect(url_for('current_workout'))



@app.route('/delete_workout_log/<int:log_id>', methods=['POST'])
def delete_workout_log(log_id):
    if 'user_id' in session:
        workout_log = WorkoutLog.query.get(log_id)
        if workout_log and workout_log.user_id == session.get('user_id'):
            db.session.delete(workout_log)
            db.session.commit()
            flash("Workout deleted successfully!")
        else:
            flash("Workout log not found or unauthorized.", "danger")
            
        if 'current_workout' in request.referrer:
            return redirect(url_for('current_workout'))
        else:
            return redirect(url_for('edit_session', session_id=workout_log.session_id))
    else:
        flash("Please log in to delete workouts.", "danger")
    return redirect(url_for('current_workout'))

@app.route('/view_current_session', methods=['GET'])
def view_current_session():
    if 'user_id' in session:
        # Retrieve the active session for the user
        active_session = WorkoutSession.query.filter_by(user_id=session['user_id'], status='active').first()
        if not active_session:
            return jsonify({"error": "No active workout session found"}), 404

        workout_logs = WorkoutLog.query.filter_by(session_id=active_session.session_id).all()
        session_data = {
            "session_name": active_session.session_name,
            "start_time": active_session.start_time,
            "end_time": active_session.end_time,
            "status": active_session.status,
            "workouts": [
                {
                    "workout_id": log.workout_id,
                    "exercise_name": log.exercise_name,
                    "weight": log.weight,
                    "reps": log.reps
                }
                for log in workout_logs
            ]
        }
        return jsonify(session_data)
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/exercise_names', methods=['GET'])
def exercise_names():
    if 'user_id' in session:
        exercises = ExerciseList.query.all()
        exercise_list = [
            {"name": exercise.name, "equipment": exercise.equipment} for exercise in exercises
        ]
        return jsonify(exercise_list), 200
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/exercises')
def exercises():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    exercises = ExerciseList.query.all()  # Fetch all exercises initially
    return render_template('exercises.html', exercises=exercises)

# @app.route('/exercises')
# def exercises():
#     exercises = ExerciseList.query.all()  # Fetch all exercises
#     formatted_exercises = [
#         {
#             "exercise_name": exercise.name,
#             "equipment": exercise.equipment,
#             "preparation": exercise.description.split("Preparation: ")[1].split("Execution: ")[0].strip(),
#             "execution": exercise.description.split("Execution: ")[1].strip()
#         }
#         for exercise in exercises
#     ]
#     return render_template('exercises.html', exercises=formatted_exercises)

@app.route('/end_session', methods=['POST'])
def end_session():
    if 'user_id' not in session or 'active_session_id' not in session:
        return redirect(url_for('login'))
    session_id = session.get('active_session_id')
    workout_session = WorkoutSession.query.filter_by(session_id=session_id, user_id=session['user_id'], status='active').first()
    if not workout_session:
        flash("No active workout session found.", "danger")
        return redirect(url_for('current_workout'))

    workout_session.status = 'completed'
    workout_session.end_time = datetime.now(timezone.utc)
    db.session.commit()
    session.pop('active_session_id', None)
    flash("Workout session ended successfully.", "success")
    return redirect(url_for('history'))

@app.route('/edit_session/<int:session_id>', methods=['GET', 'POST'])
def edit_session(session_id):
    if 'user_id' not in session:
        flash('Please log in to edit workouts.', 'danger')
        return redirect(url_for('login'))
    
    workout_session = WorkoutSession.query.filter_by(
        session_id=session_id, 
        user_id=session['user_id']
    ).first_or_404()
    
    workouts = WorkoutLog.query.filter_by(session_id=session_id).all()
    
    # Calculate 1RM for each workout
    for workout in workouts:
        workout.one_rm = workout.calculate_1rm()
    
    return render_template('edit_session.html', 
                         workout_session=workout_session, 
                         workouts=workouts)



@app.route('/history')
@login_required
def history():
    # Get all completed workout sessions for the user
    workout_sessions = WorkoutSession.query.filter_by(
        user_id=current_user.user_id,
        status='completed'
    ).order_by(WorkoutSession.start_time.desc()).all()
    
    # For each session, get its workout logs
    session_data = []
    for session in workout_sessions:
        workout_logs = WorkoutLog.query.filter_by(
            session_id=session.session_id
        ).order_by(WorkoutLog.session_workout_number).all()
        
        # Calculate total sets and PRs
        total_sets = sum(log.sets for log in workout_logs if log.sets)
        
        # Format workout data
        exercises = []
        for log in workout_logs:
            exercises.append({
                'name': log.exercise_name.title(),
                'sets': log.sets,
                'reps': log.reps,
                'weight': log.weight
            })
        
        # Calculate duration
        duration = (session.end_time - session.start_time).total_seconds() / 3600 if session.end_time else 0
        
        session_data.append({
            'id': session.session_id,
            'name': session.session_name,
            'date': session.start_time,
            'duration': f"{int(duration)}h {int((duration % 1) * 60)}m",
            'total_sets': total_sets,
            'exercises': exercises,
            'prs': 0  # You can implement PR detection logic here
        })
    
    return render_template('history.html', workout_sessions=session_data)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user = User.query.get_or_404(session['user_id'])
    
    if request.method == 'POST':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.age = request.form.get('age', type=int)
        user.weight = request.form.get('weight', type=float)
        user.height = request.form.get('height', type=float)
        user.gender = request.form.get('gender')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html', 
                         form_data={
                             "first_name": user.first_name,
                             "last_name": user.last_name,
                             "age": user.age,
                             "weight": user.weight,
                             "height": user.height,
                             "gender": user.gender
                         })

@app.route('/calculate_1rm/<int:workout_id>', methods=['GET'])
def calculate_1rm(workout_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    workout = WorkoutLog.query.get_or_404(workout_id)
    user = User.query.get(session['user_id'])
    
    # Calculate 1RM for current workout
    one_rm = workout.calculate_1rm()
    
    # Get similar users' 1RM data
    similar_users_data = None
    if one_rm:
        similar_users_data = WorkoutLog.get_similar_users_1rm(
            workout.exercise_name,
            user.weight,
            user.height
        )
    
    return jsonify({
        'current_1rm': round(one_rm, 2) if one_rm else None,
        'similar_users': similar_users_data
    })

@app.route('/get_exercise_history', methods=['GET'])
def get_exercise_history():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    exercise_name = request.args.get('exercise_name')
    if not exercise_name:
        return jsonify({'error': 'Exercise name required'}), 400
        
    # Get user's workout history for this exercise
    workout_logs = WorkoutLog.query.filter_by(
        user_id=session['user_id'],
        exercise_name=exercise_name
    ).order_by(WorkoutLog.completed_at.desc()).all()
    
    history = []
    for log in workout_logs:
        one_rm = log.calculate_1rm()
        if one_rm:
            history.append({
                'date': log.completed_at.strftime('%Y-%m-%d') if log.completed_at else None,
                'weight': log.weight,
                'reps': log.reps,
                'one_rm': round(one_rm, 2)
            })
    
    return jsonify({'history': history})

@app.route('/add_workout_to_session/<int:session_id>', methods=['POST'])
def add_workout_to_session(session_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Verify the session belongs to the user
    workout_session = WorkoutSession.query.filter_by(
        session_id=session_id,
        user_id=session['user_id']
    ).first_or_404()
    
    exercise_name = request.form.get('exercise_name', '').lower()
    equipment = request.form.get('equipment', '').lower()
    
    # Verify the exercise exists
    exercise = ExerciseList.query.filter_by(
        name=exercise_name,
        equipment=equipment
    ).first()
    
    if not exercise:
        flash('Please select a valid exercise and equipment combination', 'danger')
        return redirect(url_for('edit_session', session_id=session_id))
    
    # Create the workout log
    workout = WorkoutLog(
        user_id=session['user_id'],
        session_id=session_id,
        exercise_name=exercise_name,
        equipment=equipment,
        weight=request.form.get('weight', type=float),
        reps=request.form.get('reps', type=int),
        completed_at=workout_session.start_time  # Use session start time for consistency
    )
    
    db.session.add(workout)
    db.session.commit()
    
    flash('Exercise added successfully!', 'success')
    return redirect(url_for('edit_session', session_id=session_id))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
