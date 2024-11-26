from app import app, db
from models import User, WorkoutSession, WorkoutLog
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def create_test_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Start from user_id 2 to preserve Matthew's data for user_id 1
        for i in range(2, 4):  # Create test data for users 2 and 3
            email = f'test{i}@test.com'
            if not User.query.filter_by(email=email).first():
                user = User(
                    first_name=f'Test User{i}',
                    last_name='Last',
                    email=email,
                    password=generate_password_hash('password'),
                    age=25,
                    weight=180.0,
                    height=70.0,
                    gender='M'
                )
                db.session.add(user)
                db.session.commit()

            # Create workout sessions for this user
            create_test_workouts(user.user_id)

        db.session.commit()
        print("Test data created successfully!")

if __name__ == '__main__':
    create_test_data() 