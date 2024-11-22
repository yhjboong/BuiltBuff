from app import app, db
from models import User, WorkoutSession, WorkoutLog
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def create_test_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create test users with similar weights/heights
        users = [
            User(
                first_name='Test',
                last_name='User1',
                email='test1@test.com',
                password=generate_password_hash('password'),
                age=25,
                weight=180,  # in lbs
                height=70,   # in inches
                gender='male'
            ),
            User(
                first_name='Test',
                last_name='User2',
                email='test2@test.com',
                password=generate_password_hash('password'),
                age=27,
                weight=175,
                height=71,
                gender='male'
            ),
            User(
                first_name='Test',
                last_name='User3',
                email='test3@test.com',
                password=generate_password_hash('password'),
                age=24,
                weight=185,
                height=69,
                gender='male'
            )
        ]
        
        for user in users:
            db.session.add(user)
        db.session.commit()

        # Create workout sessions and logs for each user
        exercises = [
            ('bench press', 'upper'),
            ('squat', 'lower'),
            ('deadlift', 'lower')
        ]

        for user in users:
            # Create sessions over the past week
            for days_ago in range(7):
                session_date = datetime.now() - timedelta(days=days_ago)
                session = WorkoutSession(
                    user_id=user.user_id,
                    session_name=f'Workout {days_ago + 1}',
                    start_time=session_date,
                    end_time=session_date + timedelta(hours=1),
                    status='completed'
                )
                db.session.add(session)
                db.session.flush()

                # Add workout logs for each exercise
                for exercise_name, _ in exercises:
                    # Add a 4-6 rep set (for 1RM calculation)
                    WorkoutLog(
                        user_id=user.user_id,
                        session_id=session.session_id,
                        exercise_name=exercise_name,
                        weight=185 - days_ago,  # Decreasing weight to show progression
                        reps=5,
                        completed_at=session_date,
                        equipment='barbell',
                        variation='standard'
                    ).save()

                    # Add additional sets with different rep ranges
                    WorkoutLog(
                        user_id=user.user_id,
                        session_id=session.session_id,
                        exercise_name=exercise_name,
                        weight=165 - days_ago,
                        reps=8,
                        completed_at=session_date,
                        equipment='barbell',
                        variation='standard'
                    ).save()

        db.session.commit()
        print("Test data created successfully!")

if __name__ == '__main__':
    create_test_data() 