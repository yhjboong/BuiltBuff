from flask import Flask
from models import db, User, WorkoutLog, ExerciseList, WorkoutSession, WorkoutHistory, OneRMRecord, UserPreferences

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///builtbuff.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.drop_all()  # Drop all tables
        db.create_all()  # Recreate tables
        print("All tables dropped and recreated successfully.")