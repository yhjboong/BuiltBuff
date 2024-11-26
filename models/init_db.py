import sys
import os
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys
from pathlib import Path
from app import create_app
from models import db, User, ExerciseList, WorkoutSession, WorkoutLog, WorkoutHistory


# Create the Flask application
app = Flask(__name__)

# Use absolute path for database
db_path = os.path.join(ROOT_DIR, 'builtbuff.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define models here instead of importing
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    gender = db.Column(db.String(10))
    workout_sessions = db.relationship('WorkoutSession', backref='user', lazy=True)
    workout_logs = db.relationship('WorkoutLog', backref='user', lazy=True)

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
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(10), default='active')
    workout_logs = db.relationship('WorkoutLog', backref='session', lazy=True)

class WorkoutLog(db.Model):
    __tablename__ = 'workout_logs'
    workout_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    session_id = db.Column(db.Integer, db.ForeignKey('workout_sessions.session_id'), nullable=False)
    session_workout_number = db.Column(db.Integer)
    completed_at = db.Column(db.Date)
    intensity_level = db.Column(db.String(10))
    rest_time = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    exercise_name = db.Column(db.String(100))
    equipment = db.Column(db.String(100))
    variation = db.Column(db.String(100))
    weight = db.Column(db.Float)

class WorkoutHistory(db.Model):
    __tablename__ = 'workout_history'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('workout_sessions.session_id'), primary_key=True)
    session_name = db.Column(db.String(100), nullable=False)
    session_date = db.Column(db.DateTime, nullable=False)
    session_duration = db.Column(db.Interval)
    total_exercises = db.Column(db.Integer)
    intensity_avg = db.Column(db.Float)
    user = db.relationship("User", backref="workout_history")
    session = db.relationship("WorkoutSession", backref="workout_history")
    
app = create_app()

# Create tables within the app context
if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # Drop all tables
        db.create_all()  # Recreate tables
        print("All tables dropped and recreated successfully.")