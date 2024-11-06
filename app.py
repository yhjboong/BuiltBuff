from flask import Flask, request, redirect, url_for, render_template, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db, User, WorkoutLog, ExerciseList, WorkoutSession
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
            return jsonify({
                "message": "User with this email already exists. Please log in.",
                "login_url": url_for('login')
            }), 400
        
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
    return redirect(url_for('login'))

@app.route('/search_exercises', methods=['GET'])
def search_exercises():
    if 'user_id' in session:
        search_term = request.args.get('search_term', '')
        if not search_term:
            return jsonify({"error": "Please provide an exercise name to search."}), 400

        # Filter the exercises in ExerciseList by matching the search term in the exercise name
        exercises = ExerciseList.query.filter(ExerciseList.name.contains(search_term)).all()

        # Collect unique combinations of exercise_name, equipment, and variation
        unique_exercises = {
            (exercise.name, exercise.equipment, exercise.variation)
            for exercise in exercises
        }

        # Format the response as a list of dictionaries
        results = [
            {"exercise_name": name, "equipment": equipment, "variation": variation}
            for name, equipment, variation in unique_exercises
        ]

        return jsonify({"results": results}), 200
    return jsonify({"error": "Unauthorized"}), 401

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

    if request.method == 'POST':
        # Extract form data (ensure your form fields match these names)
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

        flash('Workout session started successfully!')
        return redirect(url_for('profile'))

    # For GET request, render the startworkout.html template
    return render_template('startworkout.html')

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

        workout_session = WorkoutSession.query.filter_by(session_id=session_id, user_id=session['user_id'], status='active').first()
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
    if 'user_id' in session:
        session_id = request.json.get('session_id')
        workout_session = WorkoutSession.query.filter_by(session_id=session_id, user_id=session['user_id'], status='active').first()
        if not workout_session:
            return jsonify({"error": "No active workout session found with the provided session_id"}), 404

        workout_session.status = 'completed'
        workout_session.end_time = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Workout session ended successfully"}), 200
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/history', methods=['GET'])
def history():
    if 'user_id' in session:
        user_id = session['user_id']
        workout_sessions = WorkoutSession.query.filter_by(user_id=user_id).order_by(WorkoutSession.start_time.desc()).all()

        # Prepare the history data with formatted date details and workout logs
        history_data = []
        for workout_session in workout_sessions:  # Renamed to avoid conflict with Flask session
            workouts = WorkoutLog.query.filter_by(session_id=workout_session.session_id, user_id=user_id).order_by(WorkoutLog.completed_at, WorkoutLog.exercise_name).all()

            if not workouts:
                continue
            
            # Format dates for display
            start_time = workout_session.start_time
            formatted_date = {
                'month_year': start_time.strftime("%B %Y"),
                'day_name': start_time.strftime("%A"),
                'short_date': start_time.strftime("%b %d"),
                'full_date': start_time.strftime("%Y-%m-%d %H:%M")
            }
            
            workout_list = [
                {
                    "workout_id": workout.workout_id,
                    "exercise_name": workout.exercise_name,
                    "equipment": workout.equipment,
                    "variation": workout.variation,
                    "sets": workout.sets,
                    "reps": workout.reps,
                    "intensity_level": workout.intensity_level,
                    "rest_time": workout.rest_time,
                    "completed_at": workout.completed_at.strftime("%Y-%m-%d")
                }
                for workout in workouts
            ]
            
            history_data.append({
                "session_id": workout_session.session_id,
                "session_name": workout_session.session_name,
                "formatted_date": formatted_date,
                "start_time": start_time.strftime("%Y-%m-%d %H:%M") if start_time else None,
                "end_time": workout_session.end_time.strftime("%Y-%m-%d %H:%M") if workout_session.end_time else None,
                "total_duration": str(workout_session.get_total_duration()) if workout_session.end_time else None,
                "status": workout_session.status,
                "workouts": workout_list
            })

        return jsonify(history_data), 200
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == '__main__':
    app.run(debug=True)