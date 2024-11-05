from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    height = db.Column(db.Integer, nullable=True)  # Stored in inches
    gender = db.Column(db.String(10), nullable=True)
    workout_sessions = db.relationship('WorkoutSession', backref='user', lazy=True)

class ExerciseList(db.Model):
    __tablename__ = 'exercise_list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    equipment = db.Column(db.String(100), nullable=False)
    variation = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(500), nullable=True)
    __table_args__ = (
        db.UniqueConstraint('name', 'equipment', 'variation', name='unique_exercise_equipment_variation'),
    )

class WorkoutSession(db.Model):
    __tablename__ = 'workout_sessions'
    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    session_name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(10), default='active')
    workout_logs = db.relationship('WorkoutLog', backref='session', lazy=True)

    def get_total_duration(self):
        return self.end_time - self.start_time if self.end_time else None

class WorkoutLog(db.Model):
    __tablename__ = 'workout_logs'
    workout_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    session_id = db.Column(db.Integer, db.ForeignKey('workout_sessions.session_id'), nullable=False)
    completed_at = db.Column(db.Date)
    intensity_level = db.Column(db.String(10))
    rest_time = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    exercise_name = db.Column(db.String(100))
    equipment = db.Column(db.String(100))
    variation = db.Column(db.String(100))

class WorkoutHistory(db.Model):
    __tablename__ = 'workout_history'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('workout_sessions.session_id'), primary_key=True)
    session_name = db.Column(db.String(100), nullable=False)  # Name of the session
    session_date = db.Column(db.DateTime, nullable=False)  # Date of the session
    session_duration = db.Column(db.Interval)  # Optional: Duration of the session
    total_exercises = db.Column(db.Integer)  # Total number of exercises in the session
    intensity_avg = db.Column(db.Float)  # Optional: Average intensity level if computed

    # Relationships
    user = db.relationship("User", backref="workout_history")
    session = db.relationship("WorkoutSession", backref="workout_history")
