from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer, nullable=True)        # Add age field
    weight = db.Column(db.Float, nullable=True)       # Add weight field
    height = db.Column(db.Integer, nullable=True)     # Store height as total inches
    gender = db.Column(db.String(10), nullable=True)  # Add gender field


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
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

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

from datetime import datetime, timedelta

class WorkoutSession(db.Model):
    __tablename__ = 'workout_sessions'
    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    session_name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)  # End time when session is completed
    status = db.Column(db.String(10), default='active')  # 'active' or 'completed'

    # This line establishes the relationship and should remain as is
    workout_logs = db.relationship('WorkoutLog', backref='session', lazy=True)

    def get_total_duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None  # Ongoing session

class WorkoutLog(db.Model):
    __tablename__ = 'workout_logs'
    workout_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    session_id = db.Column(db.Integer, db.ForeignKey('workout_sessions.session_id'), nullable=False)
    session_workout_number = db.Column(db.Integer, nullable=False)  # Workout number within the session
    completed_at = db.Column(db.Date)
    intensity_level = db.Column(db.String(10))
    rest_time = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    exercise_name = db.Column(db.String(100))  
    equipment = db.Column(db.String(100))
    variation = db.Column(db.String(100))



def generate_recommendation(user_id):
    user = User.query.get(user_id)
    similar_users = User.query.filter(
        User.age.between(user.age - 5, user.age + 5),
        User.weight.between(user.weight - 10, user.weight + 10),
        User.user_id != user.user_id
    ).all()
    
    similar_user_ids = [u.user_id for u in similar_users]
    
    # Get most common exercises for similar users
    recommended_exercises = db.session.query(
        Exercise.category_id, db.func.count(Exercise.category_id).label('popularity')
    ).filter(
        Exercise.user_id.in_(similar_user_ids)
    ).group_by(Exercise.category_id).order_by(db.desc('popularity')).limit(5).all()

    return recommended_exercises
