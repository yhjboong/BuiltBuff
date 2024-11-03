from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from models import db, User, WorkoutLog, ExerciseCategory, PlannedWorkout, Exercise
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///builtbuff.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db.init_app(app)
@app.route('/')
def home():
    return render_template('home.html')
    return "Welcome to BuiltBuff!"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

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
        new_workout = WorkoutLog(
            user_id=session['user_id'],
            completed_at=date.today(),
            intensity_level=workout_data.get('intensity_level'),
            rest_time=workout_data.get('rest_time')
        )
        db.session.add(new_workout)
        db.session.commit()
        return jsonify({"message": "Workout recorded successfully"}), 201
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/history')
def history():
    if 'user_id' in session:
        user_id = session['user_id']
        workouts = WorkoutLog.query.filter_by(user_id=user_id).all()
        return render_template('history.html', workouts=workouts)
    return redirect(url_for('login'))

@app.route('/update_workout/<int:workout_id>', methods=['POST'])
def update_workout(workout_id):
    workout = WorkoutLog.query.get_or_404(workout_id)
    workout.intensity_level = request.form['intensity_level']
    workout.rest_time = request.form['rest_time']
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


if __name__ == '__main__':
    app.run(debug=True)
