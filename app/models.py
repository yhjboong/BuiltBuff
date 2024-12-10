from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import func, distinct
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

intensity_mapping = {
    'low': 1,
    'medium': 2,
    'high': 3
}

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height_foot = db.Column(db.Integer, nullable=True)
    height_inch = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10))
    workout_sessions = db.relationship('WorkoutSession', backref='user', lazy=True)
    workout_logs = db.relationship('WorkoutLog', backref='user', lazy=True)

    def get_id(self):
        return str(self.user_id)

    def get_activity_analytics(self):
        workout_stats = db.session.query(
            func.count(distinct(WorkoutSession.session_id)).label('total_sessions'),
            func.sum(WorkoutLog.sets).label('total_sets'),
            func.count(distinct(WorkoutLog.exercise_name)).label('unique_exercises'),
            func.avg(WorkoutLog.weight).label('avg_weight')
        ).join(
            WorkoutLog, 
            WorkoutLog.session_id == WorkoutSession.session_id
        ).filter(
            WorkoutSession.user_id == self.user_id,
            WorkoutSession.status == 'completed'
        ).first()

        # Get most frequent exercises
        frequent_exercises = db.session.query(
            WorkoutLog.exercise_name,
            func.count(WorkoutLog.exercise_name).label('count')
        ).filter(
            WorkoutLog.user_id == self.user_id
        ).group_by(
            WorkoutLog.exercise_name
        ).order_by(
            func.count(WorkoutLog.exercise_name).desc()
        ).limit(5).all()

        # Calculate average workout duration
        duration_query = db.session.query(
            func.avg(
                func.strftime('%s', WorkoutSession.end_time) - 
                func.strftime('%s', WorkoutSession.start_time)
            )
        ).filter(
            WorkoutSession.user_id == self.user_id,
            WorkoutSession.status == 'completed'
        ).scalar()

        return {
            'total_sessions': workout_stats[0] or 0,
            'total_sets': workout_stats[1] or 0,
            'unique_exercises': workout_stats[2] or 0,
            'avg_weight': round(workout_stats[3] or 0, 2),
            'frequent_exercises': [{'name': ex[0], 'count': ex[1]} for ex in frequent_exercises],
            'avg_duration_minutes': round((duration_query or 0) / 60, 2)
        }
    def get_workout_streaks(self):
        sessions = WorkoutSession.query.filter_by(
            user_id=self.user_id,
            status='completed'
        ).order_by(WorkoutSession.start_time.desc()).all()
        
        if not sessions:
            return {'current_streak': 0, 'longest_streak': 0, 'badge_level': 'Beginner'}
        
        current_streak = 1
        longest_streak = 1
        current_date = sessions[0].start_time.date()
        
        for i in range(1, len(sessions)):
            session_date = sessions[i].start_time.date()
            diff = (current_date - session_date).days
            
            if diff == 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            elif diff > 1:
                current_streak = 1
            
            current_date = session_date
        
        # Determine badge level
        badge_level = 'Beginner'
        if longest_streak >= 30:
            badge_level = 'Diamond'
        elif longest_streak >= 20:
            badge_level = 'Platinum'
        elif longest_streak >= 14:
            badge_level = 'Gold'
        elif longest_streak >= 7:
            badge_level = 'Silver'
        elif longest_streak >= 3:
            badge_level = 'Bronze'
        
        return {
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'badge_level': badge_level
        }
    

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

    def calculate_1rm(self):
        """Calculate 1RM based on weight and reps"""
        if not (4 <= self.reps <= 6):
            return None
            
        # Define upper body exercises
        upper_body_exercises = {
            'bench press', 'overhead press', 'push up', 'dumbbell press',
            'military press', 'incline bench press', 'decline bench press',
            'shoulder press', 'chest press'
        }
        
        # Check if exercise is upper body
        is_upper = any(exercise in self.exercise_name.lower() for exercise in upper_body_exercises)
        
        if is_upper:
            # Upper body formula: (4-to-6RM x 1.1307) + 0.6998
            return (self.weight * 1.1307) + 0.6998
        else:
            # Lower body formula: (4-to-6RM x 1.09703) + 14.2546
            return (self.weight * 1.09703) + 14.2546

    @staticmethod
    def get_similar_users_1rm(exercise_name, user_weight, user_height, margin=10):
        """Get 1RM data from users with similar weight and height"""
        similar_users = User.query.filter(
            User.weight.between(user_weight - margin, user_weight + margin),
            User.height.between(user_height - margin, user_height + margin)
        ).all()
        
        user_ids = [user.user_id for user in similar_users]
        
        # Get the latest workout logs for the exercise from similar users
        similar_logs = WorkoutLog.query.filter(
            WorkoutLog.user_id.in_(user_ids),
            WorkoutLog.exercise_name.ilike(f'%{exercise_name}%'),
            WorkoutLog.reps.between(4, 6)  # Only consider 4-6 rep sets
        ).all()
        
        # Calculate 1RMs
        one_rms = []
        for log in similar_logs:
            one_rm = log.calculate_1rm()
            if one_rm:
                one_rms.append(one_rm)
        
        if one_rms:
            return {
                'average': sum(one_rms) / len(one_rms),
                'max': max(one_rms),
                'min': min(one_rms)
            }
        return None

    def save(self):
        db.session.add(self)
        db.session.flush()
        return self

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

class OneRMRecord(db.Model):
    __tablename__ = 'one_rm_records'
    
    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    exercise_type = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    date_recorded = db.Column(db.DateTime, nullable=False)
    age_percentile = db.Column(db.Float)
    weight_percentile = db.Column(db.Float)

    def __repr__(self):
        return f'<OneRMRecord {self.exercise_type} {self.weight}kg>'

class StrengthPercentile(db.Model):
    __tablename__ = 'strength_percentiles'
    
    percentile_id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10), nullable=False)
    exercise_type = db.Column(db.String(20), nullable=False)
    age_group = db.Column(db.String(20))
    weight_class = db.Column(db.Float)
    percentile = db.Column(db.Integer, nullable=False)
    strength_value = db.Column(db.Float, nullable=False)

class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    
    preference_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    comparison_type = db.Column(db.String(10), default='both')  # 'age', 'weight', or 'both'
    
    user = db.relationship('User', backref='preferences')

class AgePercentileData(db.Model):
    __tablename__ = 'age_percentile_data'
    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.String(10), nullable=False)
    age_category = db.Column(db.String(50), nullable=False)
    percentile = db.Column(db.Float, nullable=False)
    squat = db.Column(db.Float, nullable=False)
    squat_ll = db.Column(db.Float, nullable=True)
    squat_ul = db.Column(db.Float, nullable=True)
    bench = db.Column(db.Float, nullable=False)
    bench_ll = db.Column(db.Float, nullable=True)
    bench_ul = db.Column(db.Float, nullable=True)
    deadlift = db.Column(db.Float, nullable=False)
    deadlift_ll = db.Column(db.Float, nullable=True)
    deadlift_ul = db.Column(db.Float, nullable=True)

class WeightPercentileData(db.Model):
    __tablename__ = 'weight_percentile_data'
    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.String(10), nullable=False)
    weight_class = db.Column(db.String(50), nullable=False)
    percentile = db.Column(db.Float, nullable=False)
    squat = db.Column(db.Float, nullable=False)
    squat_ll = db.Column(db.Float, nullable=True)
    squat_ul = db.Column(db.Float, nullable=True)
    bench = db.Column(db.Float, nullable=False)
    bench_ll = db.Column(db.Float, nullable=True)
    bench_ul = db.Column(db.Float, nullable=True)
    deadlift = db.Column(db.Float, nullable=False)
    deadlift_ll = db.Column(db.Float, nullable=True)
    deadlift_ul = db.Column(db.Float, nullable=True)