from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Storing hashed password

class WorkoutLog(db.Model):
    __tablename__ = 'workout_logs'
    workout_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    completed_at = db.Column(db.Date)
    intensity_level = db.Column(db.String(10))
    rest_time = db.Column(db.Integer)

class ExerciseCategory(db.Model):
    __tablename__ = 'exercise_categories'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    muscle_group = db.Column(db.String(50))
    exercise_type = db.Column(db.String(50))

class PlannedWorkout(db.Model):
    __tablename__ = 'planned_workouts'
    workout_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    date = db.Column(db.Date)

class Exercise(db.Model):
    __tablename__ = 'exercises'
    exercise_id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout_logs.workout_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('exercise_categories.category_id'))
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
