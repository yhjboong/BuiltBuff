from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
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
        if self.end_time and self.start_time:
            total_duration = self.end_time - self.start_time
            hours, remainder = divmod(total_duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours)}:{int(minutes)}:{int(seconds)}"
        else:
            return "0:0:0"

class WorkoutLog(db.Model):
    __tablename__ = 'workout_logs'
    workout_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    session_id = db.Column(db.Integer, db.ForeignKey('workout_sessions.session_id'), nullable=False)
    session_workout_number = db.Column(db.Integer)  # New field for tracking workout number in the session
    completed_at = db.Column(db.Date)
    intensity_level = db.Column(db.String(10))
    rest_time = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    exercise_name = db.Column(db.String(100))
    equipment = db.Column(db.String(100))
    variation = db.Column(db.String(100))
    weight = db.Column(db.Float)  # Weight used in each exercise


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

def update_workout_history(session_id):
    session = WorkoutSession.query.get(session_id)
    if session:
        total_exercises = WorkoutLog.query.filter_by(session_id=session_id).count()
        
        avg_intensity = db.session.query(
            func.avg(
                func.coalesce(intensity_mapping[WorkoutLog.intensity_level], 2)
            )
        ).filter_by(session_id=session_id).scalar()
        
        history_entry = WorkoutHistory.query.filter_by(session_id=session_id).first()
        if not history_entry:
            history_entry = WorkoutHistory(session_id=session_id, user_id=session.user_id)
            db.session.add(history_entry)
        
        history_entry.total_exercises = total_exercises
        history_entry.intensity_avg = avg_intensity
        db.session.commit()
