from flask import Flask, request, redirect, url_for, render_template, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from models import db, User, WorkoutLog, ExerciseList, WorkoutSession
from sqlalchemy import func
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'builtbuff.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

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
        session['user_id'] = new_user.user_id
        return redirect(url_for('profile'))
    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id
            return redirect(url_for('profile'))
        else:
            flash('Login failed. Check your email and password.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/search_exercises', methods=['GET'])
def search_exercises():
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


@app.route('/get_equipment_options', methods=['GET'])
def get_equipment_options():
    if 'user_id' in session:
        exercise_name = request.args.get('exercise_name', '').lower()
        equipment_options = ExerciseList.query.filter_by(name=exercise_name).with_entities(ExerciseList.equipment).distinct()
        equipment_list = sorted([equipment[0] for equipment in equipment_options])
        return jsonify(equipment_list)
    return jsonify({"error": "Unauthorized"}), 401


# @app.route('/search_exercises', methods=['GET'])
# def search_exercises():
#     if 'user_id' in session:
#         search_term = request.args.get('search_term', '')

#         # Fetch all exercises if no search term is provided
#         if search_term:
#             exercises = ExerciseList.query.filter(ExerciseList.name.contains(search_term)).all()
#         else:
#             exercises = ExerciseList.query.all()

#         # Format the response as a list of dictionaries
#         results = [
#             {
#                 "exercise_name": exercise.name,
#                 "equipment": exercise.equipment,
#                 "preparation": exercise.description.split("Preparation: ")[1].split("Execution: ")[0].strip(),
#                 "execution": exercise.description.split("Execution: ")[1].strip()
#             }
#             for exercise in exercises
#         ]

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
def profile():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found.')
            return redirect(url_for('login'))

        height_in_inches = user.height
        height_feet = height_in_inches // 12
        height_inches = height_in_inches % 12
        session_count = WorkoutSession.query.filter_by(user_id=user.user_id).count()
        
        # Use first_name and last_name instead of name
        user_data = {
            "name": f"{user.first_name} {user.last_name}",
            "email": user.email,
            "age": user.age,
            "weight": user.weight,
            "height": f"{height_feet} ft {height_inches} in",
            "gender": user.gender.capitalize(),
            "workout_session_count": session_count
        }
        return render_template('profile.html', user_data=user_data)
    return redirect(url_for('login'))


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
def startworkout():
    if 'user_id' not in session:
        flash('Please log in to start a workout.')
        return redirect(url_for('login'))

    # Check for an existing active session
    active_session = WorkoutSession.query.filter_by(user_id=session['user_id'], status='active').first()
    if active_session:
        session['active_session_id'] = active_session.session_id
        flash("A workout session is already in progress.")
        return redirect(url_for('current_workout'))

    if request.method == 'POST':
        session_name = request.form.get('session_name', 'Workout Session')
        
        # Create a new workout session
        new_session = WorkoutSession(
            user_id=session['user_id'],
            session_name=session_name,
            start_time=datetime.utcnow(),
            status='active'
        )
        db.session.add(new_session)
        db.session.commit()
        session['active_session_id'] = new_session.session_id

        return redirect(url_for('current_workout'))

    return render_template('startworkout.html')


@app.route('/current_workout', methods=['GET', 'POST'])
def current_workout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if 'active_session_id' not in session:
        flash("No active workout session found.", "danger")
        return redirect(url_for('startworkout'))

    session_id = session['active_session_id']
    workout_session = WorkoutSession.query.filter_by(
        session_id=session_id, user_id=session['user_id'], status='active'
    ).first()

    if not workout_session:
        flash("No active workout session found.")
        return redirect(url_for('profile'))

    workout_logs = WorkoutLog.query.filter_by(session_id=session_id).all()

    if request.method == 'POST':
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
            new_log = WorkoutLog(
                user_id=session['user_id'],
                session_id=session_id,
                exercise_name=exercise_name,
                equipment=equipment,
                weight=weight,
                reps=reps
            )
            db.session.add(new_log)
            db.session.commit()
            flash("Workout added successfully!")
        else:
            flash("Please fill out all fields.", "danger")
        return redirect(url_for('current_workout'))

    return render_template('current_workout.html', workout_session=workout_session, workouts=workout_logs)

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

@app.route('/add_workout', methods=['POST'])
def add_workout():
    if 'user_id' in session:
        workout_data = request.get_json()
        session_id = workout_data.get('session_id')
        exercise_name = workout_data.get('exercise_name')
        weight = workout_data.get('weight')
        reps = workout_data.get('reps')

        if not session_id or not exercise_name or not weight or not reps:
            return jsonify({"error": "session_id, exercise_name, weight, and reps are required"}), 400

        workout_session = WorkoutSession.query.filter_by(
            session_id=session_id, user_id=session['user_id'], status='active'
        ).first()
        
        if not workout_session:
            return jsonify({"error": "No active workout session found with the provided session_id"}), 404

        new_workout_log = WorkoutLog(
            user_id=session['user_id'],
            session_id=session_id,
            exercise_name=exercise_name,
            weight=weight,
            reps=reps
        )
        db.session.add(new_workout_log)
        db.session.commit()
        return jsonify({"message": "Workout added successfully"}), 201
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/end_session', methods=['POST'])
def end_session():
    if 'user_id' in session and 'active_session_id' in session:
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
    flash("You need to be logged in to end a session.", "danger")
    return redirect(url_for('login'))

@app.route('/edit_session/<int:session_id>', methods=['GET', 'POST'])
def edit_session(session_id):
    if 'user_id' not in session:
        flash('Please log in to edit workouts.', 'danger')
        return redirect(url_for('login'))
    # Fetch the session and workouts
    workout_session = WorkoutSession.query.filter_by(session_id=session_id, user_id=session['user_id']).first()
    if not workout_session:
        flash('Workout session not found.', 'danger')
        return redirect(url_for('history'))
    workouts = WorkoutLog.query.filter_by(session_id=session_id).all()
    if request.method == 'POST':
        if 'session_name' in request.form:
            # Update session name
            session_name = request.form.get('session_name')
            if session_name:
                workout_session.session_name = session_name
                db.session.commit()
                flash('Session name updated successfully!', 'success')
                return redirect(url_for('edit_session', session_id=session_id))
        else:
            # Add new workout
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
                    return redirect(url_for('edit_session', session_id=session_id))
                new_log = WorkoutLog(
                    user_id=session['user_id'],
                    session_id=session_id,
                    exercise_name=exercise_name,
                    equipment=equipment,
                    weight=weight,
                    reps=reps
                )
                db.session.add(new_log)
                db.session.commit()
                flash("Workout added successfully!", "success")
            else:
                flash("Please fill out all fields.", "danger")
            return redirect(url_for('edit_session', session_id=session_id))
    return render_template('edit_session.html', session=workout_session, workouts=workouts)



@app.route('/history', methods=['GET'])
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    workout_sessions = WorkoutSession.query.filter_by(user_id=user_id).order_by(WorkoutSession.start_time.desc()).all()

    # Process the workout sessions for display
    history_data = []
    for workout_session in workout_sessions:
        workouts = WorkoutLog.query.filter_by(session_id=workout_session.session_id, user_id=user_id).order_by(WorkoutLog.completed_at, WorkoutLog.exercise_name).all()
        
        start_time = workout_session.start_time
        formatted_date = {
            'month_year': start_time.strftime("%B %Y"),
            'day_name': start_time.strftime("%A"),
            'short_date': start_time.strftime("%b %d"),
            'full_date': start_time.strftime("%Y-%m-%d %H:%M")
        }
        
        workout_list = [
            {
                "exercise_name": workout.exercise_name,
                "sets": workout.sets,
                "reps": workout.reps,
                "weight": workout.weight,
                "completed_at": workout.completed_at.strftime("%Y-%m-%d") if workout.completed_at else "N/A"
            }
            for workout in workouts
        ]

        history_data.append({
            "session_id": workout_session.session_id,
            "session_name": workout_session.session_name,
            "formatted_date": formatted_date,
            "workouts": workout_list,
            "status": workout_session.status,
            "start_time": start_time.strftime("%Y-%m-%d %H:%M") if start_time else None,
            "end_time": workout_session.end_time.strftime("%Y-%m-%d %H:%M") if workout_session.end_time else None,
            "total_duration": str(workout_session.get_total_duration()) if workout_session.end_time else None,
        })

    return render_template('history.html', workout_sessions=history_data)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash('Please log in to edit your profile.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        # Get updated data from form
        first_name = request.form.get('first_name', user.first_name)
        last_name = request.form.get('last_name', user.last_name)
        age = request.form.get('age', user.age)
        weight = request.form.get('weight', user.weight)
        gender = request.form.get('gender', user.gender)
        height_foot = int(request.form.get('height_foot', user.height // 12))
        height_inch = int(request.form.get('height_inch', user.height % 12))
        total_height_in_inches = height_foot * 12 + height_inch

        # Update user data
        user.first_name = first_name
        user.last_name = last_name
        user.age = age
        user.weight = weight
        user.gender = gender
        user.height = total_height_in_inches

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    # For GET request, render the edit profile page
    height_foot = user.height // 12
    height_inch = user.height % 12
    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "age": user.age,
        "weight": user.weight,
        "height_foot": height_foot,
        "height_inch": height_inch,
        "gender": user.gender,
    }
    return render_template('edit_profile.html', user_data=user_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
