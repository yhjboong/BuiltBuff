import os
from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from models import db, User, WorkoutLog, ExerciseList, generate_recommendation

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
    
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({
            "message": "User with this email already exists. Please log in.",
            "login_url": url_for('login')
        }), 400
    
    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User created successfully!"}), 201

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.user_id
            return redirect(url_for('profile'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/recordworkout', methods=['POST'])
def record_workout():
    if 'user_id' in session:
        workout_data = request.get_json()
        exercise_name = workout_data.get('exercise_name')
        equipment = workout_data.get('equipment')
        variation = workout_data.get('variation')
        
        valid_exercise = ExerciseList.query.filter_by(name=exercise_name, equipment=equipment, variation=variation).first()
        if not valid_exercise:
            return jsonify({"error": "Invalid exercise name, equipment, or variation. Please choose a valid exercise."}), 400

        new_workout = WorkoutLog(
            user_id=session['user_id'],
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
        return jsonify({"message": "Workout recorded successfully"}), 201
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/update_workout/<int:workout_id>', methods=['POST'])
def update_workout(workout_id):
    workout = WorkoutLog.query.get_or_404(workout_id)

    # Get JSON data from request
    data = request.get_json()

    # Check if data is received
    if not data:
        return jsonify({"error": "No data provided or invalid JSON format."}), 400

    # Normalize input fields
    exercise_name = data.get('exercise_name', '').strip().lower()
    equipment = data.get('equipment', '').strip().lower()
    variation = data.get('variation', '').strip().lower()

    intensity_level = data.get('intensity_level')
    rest_time = data.get('rest_time')
    reps = data.get('reps')
    sets = data.get('sets')

    # Debugging output for input values
    print(f"Update Request: exercise_name='{exercise_name}', equipment='{equipment}', variation='{variation}'")

    # Query for the valid exercise with normalized fields
    valid_exercise = ExerciseList.query.filter(
        ExerciseList.name == exercise_name,
        ExerciseList.equipment == equipment,
        ExerciseList.variation == variation
    ).first()

    # Debugging output for database match
    if valid_exercise:
        print(f"Matched Exercise in DB: {valid_exercise.id} - {valid_exercise.name}, {valid_exercise.equipment}, {valid_exercise.variation}")
    else:
        print("No matching exercise found in database.")

    if not valid_exercise:
        return jsonify({"error": "Invalid exercise name, equipment, or variation. Please choose a valid exercise."}), 400

    # Update workout fields
    workout.intensity_level = intensity_level
    workout.rest_time = rest_time
    workout.reps = reps
    workout.sets = sets

    # Update exercise details in workout log
    workout.exercise_name = exercise_name
    workout.equipment = equipment
    workout.variation = variation

    db.session.commit()
    return jsonify({"message": "Workout updated successfully"}), 200

@app.route('/delete_workout/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    workout = WorkoutLog.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted successfully"}), 200

@app.route('/profile')
def profile():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('profile.html', user=user)
    return redirect(url_for('login'))

@app.route('/view_workouts', methods=['GET'])
def view_workouts():
    if 'user_id' in session:
        user_id = session['user_id']
        workouts = WorkoutLog.query.filter_by(user_id=user_id).all()

        if not workouts:
            # If there are no workouts, provide a message and link to record a workout
            return jsonify({
                "message": "No workouts to view. Click the link below to record a new workout.",
                "record_workout_url": url_for('record_workout')  # Assumes there's a route named 'record_workout'
            }), 200

        # Otherwise, format the workouts with details
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

        return jsonify(workout_list), 200
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == '__main__':
    app.run(debug=True)
