from flask import Blueprint, request, redirect, url_for, render_template, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from app.models import (
    db, User, WorkoutLog, ExerciseList, WorkoutSession, 
    WorkoutHistory, OneRMRecord
)
from app.utils.utils import (
    calculate_age_percentile,
    calculate_weight_percentile,
    get_age_category,
    get_weight_class,
)



routes = Blueprint('routes', __name__)

@routes.route('/')
@routes.route('/home')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('routes.login'))
    return redirect(url_for('routes.profile'))

@routes.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        age = request.form['age']
        weight = request.form['weight']
        gender = request.form['gender']
        
        height_foot = int(request.form.get('height_foot', 0))
        height_inch = int(request.form.get('height_inch', 0))
        # total_height_in_inches = height_foot * 12 + height_inch
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User with this email already exists. Please log in.", "info")
            return redirect(url_for('routes.login'))
        
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email, 
            password=password,
            age=age,
            weight=weight,
            gender=gender,
            height_foot=height_foot,
            height_inch=height_inch
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('routes.profile'))
    return render_template('signup.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('routes.profile'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html')

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.home'))

@routes.route('/search_exercises', methods=['GET'])
@login_required
def search_exercises():
    search_term = request.args.get('search_term', '').lower()
    exercises = db.session.query(ExerciseList.name)\
        .filter(ExerciseList.name.ilike(f'%{search_term}%'))\
        .distinct().all()
    results = [{'exercise_name': exercise[0].title()} for exercise in exercises]
    return jsonify({'results': results})

@routes.route('/get_equipment_options', methods=['GET'])
@login_required
def get_equipment_options():
    exercise_name = request.args.get('exercise_name', '').lower()
    equipment_options = ExerciseList.query.filter_by(
        name=exercise_name
    ).with_entities(ExerciseList.equipment).distinct().all()
    options = [equipment[0].title() for equipment in equipment_options if equipment[0]]
    return jsonify({'equipment_options': options})

@routes.route('/add_workout', methods=['POST'])
@login_required
def add_workout():
    if 'active_session_id' not in session:
        flash('No active session found. Please start a workout session.', 'warning')
        return redirect(url_for('routes.startworkout'))
    
    active_session = WorkoutSession.query.filter_by(
        session_id=session['active_session_id'], 
        user_id=current_user.user_id, 
        status='active'
    ).first()
    
    if not active_session:
        flash('No active session found in the database. Please start a workout session.', 'danger')
        return redirect(url_for('routes.startworkout'))
    
    exercise_name = request.form.get('exercise_name', '').lower()
    equipment = request.form.get('equipment', '').lower()
    exercise = ExerciseList.query.filter_by(
        name=exercise_name,
        equipment=equipment
    ).first()
    
    if not exercise:
        flash('Please select a valid exercise and equipment combination', 'danger')
        return redirect(url_for('routes.current_workout'))
    
    workout = WorkoutLog(
        user_id=current_user.user_id,
        session_id=session['active_session_id'],
        exercise_name=exercise_name,
        equipment=equipment,
        weight=request.form.get('weight', type=float),
        reps=request.form.get('reps', type=int)
    )
    db.session.add(workout)
    db.session.commit()
    
    flash('Workout added successfully!', 'success')
    return redirect(url_for('routes.current_workout'))

@routes.route('/get_exercises', methods=['GET'])
@login_required
def get_exercises():
    search_term = request.args.get('search_term', '').lower()
    if search_term:
        exercises = ExerciseList.query.filter(ExerciseList.name.ilike(f'%{search_term}%')).all()
    else:
        exercises = ExerciseList.query.limit(50).all()

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

@routes.route('/search_exercise_names', methods=['GET'])
@login_required
def search_exercise_names():
    search_term = request.args.get('search_term', '').lower()
    if search_term:
        exercises = db.session.query(ExerciseList.name).filter(
            ExerciseList.name.ilike(f'%{search_term}%')
        ).distinct().all()
    else:
        exercises = db.session.query(ExerciseList.name).distinct().limit(50).all()

    results = []
    for exercise_name_tuple in exercises:
        exercise_name = exercise_name_tuple[0].title()
        results.append({"exercise_name": exercise_name})

    return jsonify({"results": results}), 200

@routes.route('/recordworkout', methods=['POST'])
@login_required
def record_workout():
    workout_data = request.get_json()
    session_id = workout_data.get('session_id')
    if not session_id:
        return jsonify({"error": "session_id is required"}), 400

    workout_session = WorkoutSession.query.filter_by(session_id=session_id, user_id=current_user.user_id, status='active').first()
    if not workout_session:
        return jsonify({"error": "No active workout session found with the provided session_id"}), 404

    exercise_name = workout_data.get('exercise_name')
    weight = workout_data.get('weight')
    reps = workout_data.get('reps')
    if not exercise_name or not weight or not reps:
        return jsonify({"error": "exercise_name, weight, and reps are required"}), 400

    new_workout_log = WorkoutLog(
        user_id=current_user.user_id,
        session_id=session_id,
        exercise_name=exercise_name,
        weight=weight,
        reps=reps
    )
    db.session.add(new_workout_log)
    db.session.commit()
    return jsonify({"message": "Workout recorded successfully"}), 201

@routes.route('/update_workout/<int:session_id>/<int:workout_id>', methods=['POST'])
@login_required
def update_workout(session_id, workout_id):
    workout_data = request.get_json()
    workout_log = WorkoutLog.query.filter_by(workout_id=workout_id, session_id=session_id, user_id=current_user.user_id).first()
    if not workout_log:
        return jsonify({"error": "Workout log not found"}), 404

    workout_log.exercise_name = workout_data.get('exercise_name', workout_log.exercise_name)
    workout_log.weight = workout_data.get('weight', workout_log.weight)
    workout_log.reps = workout_data.get('reps', workout_log.reps)
    db.session.commit()
    return jsonify({"message": "Workout updated successfully"}), 200

@routes.route('/delete_workout/<int:session_id>/<int:workout_id>', methods=['DELETE'])
@login_required
def delete_workout(session_id, workout_id):
    workout_log = WorkoutLog.query.filter_by(workout_id=workout_id, session_id=session_id, user_id=current_user.user_id).first()
    if not workout_log:
        return jsonify({"error": "Workout log not found"}), 404

    db.session.delete(workout_log)
    db.session.commit()
    return jsonify({"message": "Workout deleted successfully"}), 200

@routes.route('/profile')
@login_required
def profile():
    recent_sessions = WorkoutSession.query.filter_by(
        user_id=current_user.user_id,
        status='completed'
    ).order_by(WorkoutSession.start_time.desc()).limit(5).all()
    
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

@routes.route('/view_workout/<int:session_id>/<int:workout_id>', methods=['GET'])
@login_required
def view_workout(session_id, workout_id):
    workout_log = WorkoutLog.query.filter_by(workout_id=workout_id, session_id=session_id, user_id=current_user.user_id).first()
    if not workout_log:
        return jsonify({"error": "Workout log not found"}), 404

    workout_data = {
        "exercise_name": workout_log.exercise_name,
        "weight": workout_log.weight,
        "reps": workout_log.reps
    }
    return jsonify(workout_data)

@routes.route('/view_session/<int:session_id>', methods=['GET'])
@login_required
def view_session(session_id):
    workout_session = WorkoutSession.query.filter_by(session_id=session_id, user_id=current_user.user_id).first()
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

@routes.route('/startworkout', methods=['GET', 'POST'])
@login_required
def startworkout():
    active_session = WorkoutSession.query.filter_by(
        user_id=current_user.user_id, 
        status='active'
    ).first()
    
    if active_session:
        session['active_session_id'] = active_session.session_id
        flash("A workout session is already in progress.")
        return redirect(url_for('routes.current_workout'))

    if request.method == 'POST':
        session_name = request.form.get('session_name', 'Workout Session')
        new_session = WorkoutSession(
            user_id=current_user.user_id,
            session_name=session_name,
            start_time=datetime.utcnow(),
            status='active'
        )
        db.session.add(new_session)
        db.session.commit()
        session['active_session_id'] = new_session.session_id
        
        flash("Workout session started successfully!", "success")
        return redirect(url_for('routes.current_workout'))

    return render_template('startworkout.html')

@routes.route('/current_workout')
@login_required
def current_workout():
    if 'active_session_id' not in session or not WorkoutSession.query.filter_by(
        session_id=session.get('active_session_id'),
        user_id=current_user.user_id,
        status='active'
    ).first():
        flash("No active workout session found. Please start a workout session first.", "warning")
        return redirect(url_for('routes.startworkout'))
        
    workout_session = WorkoutSession.query.get(session['active_session_id'])
    workouts = WorkoutLog.query.filter_by(session_id=session['active_session_id']).all()
    
    for workout in workouts:
        workout.one_rm = workout.calculate_1rm()
    
    return render_template('current_workout.html', 
                           workout_session=workout_session, 
                           workouts=workouts)

@routes.route('/update_workout_log/<int:log_id>', methods=['POST'])
@login_required
def update_workout_log(log_id):
    workout_log = WorkoutLog.query.get(log_id)
    if workout_log and workout_log.user_id == current_user.user_id:
        exercise_name = request.form.get('exercise_name')
        equipment = request.form.get('equipment')
        weight = request.form.get('weight')
        reps = request.form.get('reps')
        if exercise_name and equipment and weight and reps:
            exercise = ExerciseList.query.filter(
                func.lower(ExerciseList.name) == func.lower(exercise_name),
                func.lower(ExerciseList.equipment) == func.lower(equipment)
            ).first()
            if not exercise:
                flash("Exercise with specified equipment not found. Please select from suggestions.", "danger")
                return redirect(url_for('routes.current_workout'))
            workout_log.exercise_name = exercise_name
            workout_log.equipment = equipment
            workout_log.weight = weight
            workout_log.reps = reps
            db.session.commit()
            flash("Workout updated successfully!")
        else:
            flash("Please fill out all fields.", "danger")
        
        if 'current_workout' in request.referrer:
            return redirect(url_for('routes.current_workout'))
        else:
            return redirect(url_for('routes.edit_session', session_id=workout_log.session_id))
    else:
        flash("Workout log not found or unauthorized.", "danger")
    return redirect(url_for('routes.current_workout'))

@routes.route('/delete_workout_log/<int:log_id>', methods=['POST'])
@login_required
def delete_workout_log(log_id):
    workout_log = WorkoutLog.query.get(log_id)
    if workout_log and workout_log.user_id == current_user.user_id:
        db.session.delete(workout_log)
        db.session.commit()
        flash("Workout deleted successfully!")
    else:
        flash("Workout log not found or unauthorized.", "danger")
        
    if 'current_workout' in request.referrer:
        return redirect(url_for('routes.current_workout'))
    else:
        return redirect(url_for('routes.edit_session', session_id=workout_log.session_id))

@routes.route('/view_current_session', methods=['GET'])
@login_required
def view_current_session():
    active_session = WorkoutSession.query.filter_by(user_id=current_user.user_id, status='active').first()
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

@routes.route('/exercise_names', methods=['GET'])
@login_required
def exercise_names():
    exercises = ExerciseList.query.all()
    exercise_list = [
        {"name": exercise.name, "equipment": exercise.equipment} for exercise in exercises
    ]
    return jsonify(exercise_list), 200

@routes.route('/exercises')
@login_required
def exercises():
    exercises = ExerciseList.query.all()
    return render_template('exercises.html', exercises=exercises)

@routes.route('/end_session', methods=['POST'])
@login_required
def end_session():
    if 'active_session_id' not in session:
        return redirect(url_for('routes.login'))
    session_id = session.get('active_session_id')
    workout_session = WorkoutSession.query.filter_by(session_id=session_id, user_id=current_user.user_id, status='active').first()
    if not workout_session:
        flash("No active workout session found.", "danger")
        return redirect(url_for('routes.current_workout'))

    workout_session.status = 'completed'
    workout_session.end_time = datetime.now(timezone.utc)
    db.session.commit()
    session.pop('active_session_id', None)
    flash("Workout session ended successfully.", "success")
    return redirect(url_for('routes.history'))

@routes.route('/edit_session/<int:session_id>', methods=['GET', 'POST'])
@login_required
def edit_session(session_id):
    workout_session = WorkoutSession.query.filter_by(
        session_id=session_id, 
        user_id=current_user.user_id
    ).first_or_404()
    
    workouts = WorkoutLog.query.filter_by(session_id=session_id).all()
    for workout in workouts:
        workout.one_rm = workout.calculate_1rm()
    
    return render_template('edit_session.html', 
                           workout_session=workout_session, 
                           workouts=workouts)

@routes.route('/history')
@login_required
def history():
    workout_sessions = WorkoutSession.query.filter_by(
        user_id=current_user.user_id,
        status='completed'
    ).order_by(WorkoutSession.start_time.desc()).all()
    
    session_data = []
    for session_obj in workout_sessions:
        workout_logs = WorkoutLog.query.filter_by(
            session_id=session_obj.session_id
        ).order_by(WorkoutLog.session_workout_number).all()
        
        total_sets = sum(log.sets for log in workout_logs if log.sets)
        
        exercises = []
        for log in workout_logs:
            exercises.append({
                'name': log.exercise_name.title(),
                'sets': log.sets,
                'reps': log.reps,
                'weight': log.weight
            })
        
        duration = (session_obj.end_time - session_obj.start_time).total_seconds() / 3600 if session_obj.end_time else 0
        
        session_data.append({
            'id': session_obj.session_id,
            'name': session_obj.session_name,
            'date': session_obj.start_time,
            'duration': f"{int(duration)}h {int((duration % 1) * 60)}m",
            'total_sets': total_sets,
            'exercises': exercises,
            'prs': 0
        })
    
    return render_template('history.html', workout_sessions=session_data)

@routes.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.get_or_404(current_user.user_id)
    
    if request.method == 'POST':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.age = request.form.get('age', type=int)
        user.weight = request.form.get('weight', type=float)
        user.height_foot = request.form.get('height_foot', type=float)
        user.height_inch = request.form.get('height_inch', type=float)
        user.gender = request.form.get('gender')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('routes.profile'))
    
    return render_template('edit_profile.html', 
                           form_data={
                               "first_name": user.first_name,
                               "last_name": user.last_name,
                               "age": user.age,
                               "weight": user.weight,
                               "height_foot": user.height_foot,
                               "height_inch": user.height_inch,
                               "gender": user.gender
                           })

@routes.route('/calculate_1rm/<int:workout_id>', methods=['GET'])
@login_required
def calculate_1rm(workout_id):
    workout = WorkoutLog.query.get_or_404(workout_id)
    if workout.user_id != current_user.user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.query.get(current_user.user_id)
    one_rm = workout.calculate_1rm()
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

@routes.route('/get_exercise_history', methods=['GET'])
@login_required
def get_exercise_history():
    exercise_name = request.args.get('exercise_name')
    if not exercise_name:
        return jsonify({'error': 'Exercise name required'}), 400
        
    workout_logs = WorkoutLog.query.filter_by(
        user_id=current_user.user_id,
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

@routes.route('/add_workout_to_session/<int:session_id>', methods=['POST'])
@login_required
def add_workout_to_session(session_id):
    workout_session = WorkoutSession.query.filter_by(
        session_id=session_id,
        user_id=current_user.user_id
    ).first_or_404()
    
    exercise_name = request.form.get('exercise_name', '').lower()
    equipment = request.form.get('equipment', '').lower()
    exercise = ExerciseList.query.filter_by(
        name=exercise_name,
        equipment=equipment
    ).first()
    
    if not exercise:
        flash('Please select a valid exercise and equipment combination', 'danger')
        return redirect(url_for('routes.edit_session', session_id=session_id))
    
    workout = WorkoutLog(
        user_id=current_user.user_id,
        session_id=session_id,
        exercise_name=exercise_name,
        equipment=equipment,
        weight=request.form.get('weight', type=float),
        reps=request.form.get('reps', type=int),
        completed_at=workout_session.start_time
    )
    
    db.session.add(workout)
    db.session.commit()
    flash('Exercise added successfully!', 'success')
    return redirect(url_for('routes.edit_session', session_id=session_id))

@routes.route('/one_rm_tracker', methods=['GET', 'POST'])
@login_required
def one_rm_tracker():
    user = current_user
    try:
        user_age = int(user.age)
    except ValueError:
        flash("Invalid age format. Please update your profile.", "danger")
        return redirect(url_for('routes.edit_profile'))

    if request.method == 'POST':
        try:
            exercise_raw = request.form.get('exercise')
            weight = float(request.form.get('weight'))
            date_recorded = datetime.now()

            exercise_mapping = {
                'Bench Press': 'Bench Press',
                'Squat': 'Squat',
                'Deadlift': 'Deadlift'
            }
            exercise_name = exercise_mapping.get(exercise_raw)
            if not exercise_name:
                flash(f"Invalid exercise type: {exercise_raw}", "danger")
                return redirect(url_for('routes.one_rm_tracker'))

            # Get percentiles and extract the first element of the tuple
            age_percentile_tuple = calculate_age_percentile(exercise_name, weight, user_age, user.gender)
            weight_percentile_tuple = calculate_weight_percentile(exercise_name, weight, user.weight, user.gender)

            age_percentile = age_percentile_tuple[0]  # Extract the percentile value
            weight_percentile = weight_percentile_tuple[0]  # Extract the percentile value

            new_record = OneRMRecord(
                user_id=user.user_id,
                exercise_type=exercise_name,
                weight=weight,
                date_recorded=date_recorded,
                age_percentile=age_percentile,
                weight_percentile=weight_percentile
            )

            db.session.add(new_record)
            db.session.commit()

            flash("Record added successfully!", "success")
            return redirect(url_for('routes.one_rm_tracker'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error saving record: {e}", "danger")
            return redirect(url_for('routes.one_rm_tracker'))


    # On GET: Retrieve existing records for display
    records = OneRMRecord.query.filter_by(user_id=user.user_id).order_by(OneRMRecord.date_recorded.desc()).all()
    records_dict = [{
        'exercise_type': record.exercise_type,
        'weight': record.weight,
        'date_recorded': record.date_recorded.strftime('%Y-%m-%d'),
        'age_percentile': record.age_percentile,
        'weight_percentile': record.weight_percentile
    } for record in records]
    def combine_intervals(ll1, ul1, ll2, ul2):
        # Combine by averaging if both available
        def avg(a, b):
            if a is not None and b is not None:
                return (a + b) / 2.0
            return a if a is not None else b

        combined_ll = avg(ll1, ll2)
        combined_ul = avg(ul1, ul2)
        return combined_ll, combined_ul

    records_dict_with_ll = []
    for r in records:
        ex_name = r.exercise_type
        w = r.weight
        age_pct, age_ll, age_ul = calculate_age_percentile(ex_name, w, user_age, user.gender)
        wt_pct, wt_ll, wt_ul = calculate_weight_percentile(ex_name, w, user.weight, user.gender)

        # Compute combined intervals
        combined_ll, combined_ul = combine_intervals(age_ll, age_ul, wt_ll, wt_ul)

        rec = {
            'exercise_type': r.exercise_type,
            'weight': r.weight,
            'date_recorded': r.date_recorded.strftime('%Y-%m-%d'),
            'age_percentile': r.age_percentile,
            'weight_percentile': r.weight_percentile,
            'age_ll': age_ll,
            'age_ul': age_ul,
            'weight_ll': wt_ll,
            'weight_ul': wt_ul,
            'record_id': r.record_id,
            'combined_ll': combined_ll,
            'combined_ul': combined_ul,
        }
        records_dict_with_ll.append(rec)

    records_dict = records_dict_with_ll

    # Default values for advanced analysis
    advanced_analysis = {
        'exercise': None,
        'weight': None,
        'age_percentile': None,
        'age_ll': None,
        'age_ul': None,
        'weight_percentile': None,
        'weight_ll': None,
        'weight_ul': None
    }

    # Calculate advanced analysis if records exist
    if records_dict:
        last_record = records_dict[0]
        ex_name = last_record['exercise_type']
        w = last_record['weight']

        age_pct, age_ll, age_ul = calculate_age_percentile(ex_name, w, user_age, user.gender)
        wt_pct, wt_ll, wt_ul = calculate_weight_percentile(ex_name, w, user.weight, user.gender)

        advanced_analysis.update({
            'exercise': ex_name,
            'weight': w,
            'age_percentile': age_pct,
            'age_ll': age_ll,
            'age_ul': age_ul,
            'weight_percentile': wt_pct,
            'weight_ll': wt_ll,
            'weight_ul': wt_ul
        })

    return render_template(
        'one_rm_tracker.html',
        user=user,
        records=records_dict,
        age_category=get_age_category(user_age),
        weight_class=get_weight_class(user.gender, user.weight),
        advanced_analysis=advanced_analysis
    )



@routes.route('/debug_one_rm_records', methods=['GET'])
@login_required
def debug_one_rm_tracker():
    user = current_user
    records = OneRMRecord.query.filter_by(user_id=user.user_id).order_by(OneRMRecord.date_recorded.desc()).all()
    records_dict = [{
        'exercise_type': record.exercise_type,
        'weight': record.weight,
        'date_recorded': record.date_recorded.strftime('%Y-%m-%d'),
        'age_percentile': record.age_percentile,
        'weight_percentile': record.weight_percentile
    } for record in records]
    return jsonify(records_dict)

@routes.route('/debug_one_rm', methods=['GET'])
@login_required
def debug_one_rm():
    records = OneRMRecord.query.filter_by(user_id=current_user.user_id).all()
    records_dict = [
        {
            'exercise_type': record.exercise_type,
            'weight': record.weight,
            'date_recorded': record.date_recorded.strftime('%Y-%m-%d'),
            'age_percentile': record.age_percentile,
            'weight_percentile': record.weight_percentile
        }
        for record in records
    ]
    return jsonify(records_dict), 200
