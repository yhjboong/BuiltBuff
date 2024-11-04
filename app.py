import os
from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
from models import db, User, WorkoutLog, ExerciseList, generate_recommendation, WorkoutSession



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

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
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
        name=name, 
        email=email, 
        password=password,
        age=age,
        weight=weight,
        gender=gender,
        height=total_height_in_inches  # Store total height in inches
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User created successfully!"}), 201


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id
            print(f"User logged in with ID: {session['user_id']}")  # Debug line
            # Return JSON response instead of redirecting to profile
            return jsonify({"message": "Login successful", "user_id": user.user_id}), 200
        return jsonify({"error": "Invalid credentials"}), 401
    # If the method is GET, inform that the endpoint is POST-only for login
    return jsonify({"error": "Please use POST to log in"}), 405

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/search_exercises', methods=['GET'])
def search_exercises():
    if 'user_id' in session:
        # Get the partial exercise name from the query parameter
        search_term = request.args.get('exercise_name', '').strip().lower()

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
        exercise_name = workout_data.get('exercise_name', '').strip().lower()
        equipment = workout_data.get('equipment', '').strip().lower()
        variation = workout_data.get('variation', '').strip().lower()

        valid_exercise = ExerciseList.query.filter_by(name=exercise_name, equipment=equipment, variation=variation).first()
        if not valid_exercise:
            return jsonify({"error": "Invalid exercise name, equipment, or variation. Please choose a valid exercise."}), 400

        # Determine the next workout number within this session
        next_workout_number = WorkoutLog.query.filter_by(session_id=session_id).count() + 1

        # Create the new workout log entry
        new_workout = WorkoutLog(
            user_id=session['user_id'],
            session_id=session_id,
            session_workout_number=next_workout_number,
            completed_at=date.today(),
            intensity_level=workout_data.get('intensity_level'),
            rest_time=workout_data.get('rest_time'),
            reps=workout_data.get('reps'),
            sets=workout_data.get('sets'),
            exercise_name=exercise_name,
            equipment=equipment,
            variation=variation
        )

        # Add and commit the new workout to the database
        db.session.add(new_workout)
        db.session.commit()
        return jsonify({"message": "Workout recorded successfully"}), 201
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/update_workout/<int:session_id>/<int:workout_id>', methods=['POST'])
def update_workout(session_id, workout_id):
    if 'user_id' in session:
        workout = WorkoutLog.query.filter_by(session_id=session_id, workout_id=workout_id, user_id=session['user_id']).first()
        if not workout:
            return jsonify({"error": "Workout not found in this session"}), 404

        # Get JSON data from request
        data = request.get_json()

        # Validate the new exercise details against ExerciseList
        exercise_name = data.get('exercise_name', '').strip().lower()
        equipment = data.get('equipment', '').strip().lower()
        variation = data.get('variation', '').strip().lower()
        
        valid_exercise = ExerciseList.query.filter_by(name=exercise_name, equipment=equipment, variation=variation).first()
        if not valid_exercise:
            return jsonify({"error": "Invalid exercise name, equipment, or variation. Please choose a valid exercise."}), 400

        # Update workout fields if valid
        workout.intensity_level = data.get('intensity_level', workout.intensity_level)
        workout.rest_time = data.get('rest_time', workout.rest_time)
        workout.reps = data.get('reps', workout.reps)
        workout.sets = data.get('sets')
        workout.exercise_name = exercise_name
        workout.equipment = equipment
        workout.variation = variation

        db.session.commit()
        return jsonify({"message": "Workout updated successfully"}), 200
    return jsonify({"error": "Unauthorized"}), 401


@app.route('/delete_workout/<int:session_id>/<int:workout_id>', methods=['DELETE'])
def delete_workout(session_id, workout_id):
    if 'user_id' in session:
        # Retrieve the workout based on session_id, workout_id, and user_id
        workout = WorkoutLog.query.filter_by(
            session_id=session_id, 
            workout_id=workout_id, 
            user_id=session['user_id']
        ).first()
        
        if not workout:
            return jsonify({"error": "Workout not found in this session or unauthorized access"}), 404

        # Delete the workout
        db.session.delete(workout)
        db.session.commit()
        
        return jsonify({"message": "Workout deleted successfully"}), 200
    return jsonify({"error": "Unauthorized"}), 401


@app.route('/profile')
def profile():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        
        # Count the number of workout sessions for this user
        session_count = WorkoutSession.query.filter_by(user_id=user.user_id).count()

        # Format the user data and the session count in a JSON response
        user_data = {
            "profile": {
                "name": user.name,
                "email": user.email,
                "age": user.age,
                "weight": user.weight,
                "height_in_inches": user.height,  # Assuming height is stored in inches
                "gender": user.gender,
            },
            "workout_session_count": session_count
        }
        
        return jsonify(user_data), 200
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/view_workout/<int:session_id>/<int:workout_id>', methods=['GET'])
def view_workout(session_id, workout_id):
    if 'user_id' in session:
        workout = WorkoutLog.query.filter_by(session_id=session_id, workout_id=workout_id, user_id=session['user_id']).first()
        if not workout:
            return jsonify({"error": "Workout not found in this session"}), 404
        
        workout_data = {
            "workout_id": workout.workout_id,
            "session_workout_number": workout.session_workout_number,
            "date": workout.completed_at.strftime("%Y-%m-%d"),
            "intensity_level": workout.intensity_level,
            "rest_time": workout.rest_time,
            "reps": workout.reps,
            "sets": workout.sets,
            "exercise_name": workout.exercise_name,
            "equipment": workout.equipment,
            "variation": workout.variation
        }
        return jsonify(workout_data), 200
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/view_session/<int:session_id>', methods=['GET'])
def view_session(session_id):
    if 'user_id' in session:
        # Ensure that the session is completed
        session_data = WorkoutSession.query.filter_by(session_id=session_id, user_id=session['user_id'], status='completed').first()
        
        if not session_data:
            return jsonify({"error": "Session not found or is still ongoing."}), 404

        # Fetch workouts associated with this completed session
        workouts = WorkoutLog.query.filter_by(session_id=session_id, user_id=session['user_id']).all()

        # If no workouts are found, set workout_list to "N/A"
        if not workouts:
            workout_list = "N/A"
        else:
            workout_list = [
                {
                    "workout_id": log.workout_id,
                    "date": log.completed_at.strftime("%Y-%m-%d"),
                    "intensity_level": log.intensity_level,
                    "rest_time": log.rest_time,
                    "reps": log.reps,
                    "sets": log.sets,
                    "exercise_name": log.exercise_name,
                    "equipment": log.equipment,
                    "variation": log.variation,
                    "prescription": ExerciseList.query.filter_by(
                        name=log.exercise_name,
                        equipment=log.equipment,
                        variation=log.variation
                    ).first().description if log.exercise_name else "N/A"
                }
                for log in workouts
            ]

        return jsonify({
            "session_id": session_id,
            "session_name": session_data.session_name,
            "start_time": session_data.start_time.strftime("%Y-%m-%d %H:%M"),
            "end_time": session_data.end_time.strftime("%Y-%m-%d %H:%M"),
            "workouts": workout_list
        }), 200
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/start_session', methods=['POST'])
def start_session():
    if 'user_id' in session:
        # Check if there is already an active session for this user
        active_session = WorkoutSession.query.filter_by(user_id=session['user_id'], status='active').first()
        if active_session:
            return jsonify({
                "message": "You already have an active session.",
                "session_id": active_session.session_id
            }), 400

        data = request.get_json()
        session_name = data.get('session_name', 'Workout Session')
        
        new_session = WorkoutSession(user_id=session['user_id'], session_name=session_name)
        db.session.add(new_session)
        db.session.commit()
        
        return jsonify({
            "message": "Workout session started successfully",
            "session_id": new_session.session_id
        }), 201
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/view_current_session', methods=['GET'])
def view_current_session():
    if 'user_id' in session:
        # Retrieve the active session for the user
        active_session = WorkoutSession.query.filter_by(user_id=session['user_id'], status='active').first()
        
        if not active_session:
            return jsonify({"message": "No active session found"}), 404

        # Fetch workouts associated with this ongoing session
        workouts = WorkoutLog.query.filter_by(session_id=active_session.session_id).all()

        # If no workouts are found, set workout_list to "N/A"
        if not workouts:
            workout_list = "N/A"
        else:
            workout_list = [
                {
                    "workout_id": workout.workout_id,
                    "date": workout.completed_at.strftime("%Y-%m-%d"),
                    "intensity_level": workout.intensity_level,
                    "rest_time": workout.rest_time,
                    "reps": workout.reps,
                    "sets": workout.sets,
                    "exercise_name": workout.exercise_name,
                    "equipment": workout.equipment,
                    "variation": workout.variation,
                    "prescription": ExerciseList.query.filter_by(
                        name=workout.exercise_name, 
                        equipment=workout.equipment, 
                        variation=workout.variation
                    ).first().description if workout.exercise_name else "N/A"
                }
                for workout in workouts
            ]

        return jsonify({
            "session_id": active_session.session_id,
            "session_name": active_session.session_name,
            "start_time": active_session.start_time.strftime("%Y-%m-%d %H:%M"),
            "workouts": workout_list
        }), 200
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/add_workout', methods=['POST'])
def add_workout():
    if 'user_id' in session:
        workout_data = request.get_json()
        session_id = workout_data.get('session_id')

        # Check if the session exists, belongs to the user, and is active
        workout_session = WorkoutSession.query.filter_by(session_id=session_id, user_id=session['user_id'], status='active').first()
        if not workout_session:
            return jsonify({"error": "Workout session not found, does not belong to this user, or is not active"}), 404

        # Check if the selected exercise is valid
        exercise_name = workout_data.get('exercise_name', '').strip().lower()
        equipment = workout_data.get('equipment', '').strip().lower()
        variation = workout_data.get('variation', '').strip().lower()

        valid_exercise = ExerciseList.query.filter_by(name=exercise_name, equipment=equipment, variation=variation).first()
        if not valid_exercise:
            return jsonify({"error": "Invalid exercise name, equipment, or variation. Please choose a valid exercise."}), 400

        # Determine the next workout number within this session
        next_workout_number = WorkoutLog.query.filter_by(session_id=session_id).count() + 1

        new_workout = WorkoutLog(
            user_id=session['user_id'],
            session_id=session_id,
            session_workout_number=next_workout_number,
            completed_at=date.today(),
            intensity_level=workout_data.get('intensity_level'),
            rest_time=workout_data.get('rest_time'),
            reps=workout_data.get('reps'),
            sets=workout_data.get('sets'),
            exercise_name=exercise_name,
            equipment=equipment,
            variation=variation
        )
        db.session.add(new_workout)
        db.session.commit()
        return jsonify({"message": "Workout added to session successfully"}), 201
    return jsonify({"error": "Unauthorized"}), 401
@app.route('/end_session', methods=['POST'])
def end_session():
    if 'user_id' in session:
        user_id = session['user_id']
        
        # Retrieve the active session directly
        active_session = WorkoutSession.query.filter_by(user_id=user_id, status='active').first()
        
        if not active_session:
            return jsonify({"error": "No active session found"}), 404

        # Set end_time and mark as completed
        active_session.end_time = datetime.utcnow()
        active_session.status = 'completed'
        db.session.commit()

        return jsonify({
            "message": "Workout session ended",
            "session_id": active_session.session_id,
            "total_duration": str(active_session.get_total_duration())
        }), 200

    return jsonify({"error": "Unauthorized"}), 401


@app.route('/history/<int:user_id>', methods=['GET'])
def history(user_id):

    sessions = WorkoutSession.query.filter_by(user_id=user_id).order_by(WorkoutSession.start_time.desc()).all()
    
    history_data = []
    for session in sessions:

        workouts = WorkoutLog.query.filter_by(
            session_id=session.session_id,
            user_id=user_id
        ).order_by(
            WorkoutLog.completed_at,
            WorkoutLog.exercise_name
        ).all()
        
        if not workouts:
            continue
            
        # Format each workout directly without grouping
        workout_list = []
        for workout in workouts:
            workout_list.append({
                "workout_id": workout.workout_id,
                "exercise_name": workout.exercise_name,
                "equipment": workout.equipment,
                "variation": workout.variation,
                "sets": workout.sets,
                "reps": workout.reps,
                "intensity_level": workout.intensity_level,
                "rest_time": workout.rest_time,
                "completed_at": workout.completed_at.strftime("%Y-%m-%d")
            })
        
        # Add session data
        history_data.append({
            "session_id": session.session_id,
            "session_name": session.session_name,
            "start_time": session.start_time.strftime("%Y-%m-%d %H:%M") if session.start_time else None,
            "end_time": session.end_time.strftime("%Y-%m-%d %H:%M") if session.end_time else None,
            "total_duration": str(session.get_total_duration()) if session.end_time else None,
            "status": session.status,
            "workouts": workout_list
        })
    
    return jsonify(history_data), 200




if __name__ == '__main__':
    app.run(debug=True)
