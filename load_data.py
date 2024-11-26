import pandas as pd
from datetime import datetime, timedelta
from models import db, ExerciseList, WorkoutSession, WorkoutLog, User, WorkoutHistory
from app import app
from sqlalchemy.exc import IntegrityError

def load_exercises_from_csv():
    try:
        # Load exercise CSV file
        df_exercises = pd.read_csv('./data/gym_exercise_dataset.csv')

        # Data cleaning for exercises
        df_exercises['Exercise Name'] = df_exercises['Exercise Name'].str.strip().str.lower()
        df_exercises['Equipment'] = df_exercises['Equipment'].str.strip().str.lower()
        df_exercises['Variation'] = df_exercises['Variation'].astype(str).str.strip().str.lower()

        # Check required columns
        required_columns = {'Exercise Name', 'Equipment', 'Variation', 'Preparation', 'Execution'}
        if not required_columns.issubset(df_exercises.columns):
            missing = required_columns - set(df_exercises.columns)
            raise ValueError(f"CSV file is missing required columns: {', '.join(missing)}")

        # Load each exercise into the database
        for _, row in df_exercises.iterrows():
            description = f"Preparation: {row['Preparation']}\nExecution: {row['Execution']}"
            existing_exercise = ExerciseList.query.filter_by(
                name=row['Exercise Name'],
                equipment=row['Equipment'],
                variation=row['Variation']
            ).first()

            if existing_exercise:
                print(f"Exercise '{row['Exercise Name']}' with equipment '{row['Equipment']}' and variation '{row['Variation']}' already exists. Skipping.")
                continue

            exercise = ExerciseList(
                name=row['Exercise Name'],
                equipment=row['Equipment'],
                variation=row['Variation'],
                description=description
            )
            db.session.add(exercise)
        db.session.commit()
        print("Exercises loaded successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error loading exercises: {e}")
        raise e

def load_workout_sessions_from_csv():
    try:
        print("Starting to load Matthew's workout data...")
        df = pd.read_csv('./data/matthew-eleazar-strong.csv')
        print(f"Found {len(df)} workout records in CSV")
        
        # Get the test1@test.com user
        user = User.query.filter_by(email='test1@test.com').first()
        if not user:
            print("Error: test1@test.com user not found! Please run test_data.py first")
            return
            
        print(f"Loading workouts for user ID: {user.user_id}")
        
        # Group by session to create workout sessions
        grouped = df.groupby(['session_key', 'Date', 'Workout Name'])
        
        workout_logs = []
        session_mapping = {}
        
        for (session_key, date, workout_name), group in grouped:
            if session_key not in session_mapping:
                session_date = pd.to_datetime(date)
                new_session = WorkoutSession(
                    user_id=user.user_id,  # Use the actual user ID
                    session_name=workout_name,
                    start_time=session_date,
                    end_time=session_date + timedelta(hours=1),
                    status='completed'
                )
                db.session.add(new_session)
                db.session.flush()
                session_mapping[session_key] = new_session.session_id
                
            # Add workout logs for this session
            for _, row in group.iterrows():
                workout_log = WorkoutLog(
                    user_id=user.user_id,  # Use the actual user ID
                    session_id=session_mapping[session_key],
                    completed_at=pd.to_datetime(row['Date']).date(),
                    intensity_level='medium',
                    rest_time=row.get('Seconds', 60),
                    reps=int(row['Reps']),
                    sets=1,
                    exercise_name=row['Exercise Name'].lower(),
                    equipment=row['Equipment'].lower() if isinstance(row['Equipment'], str) else 'barbell',
                    variation='standard',
                    weight=float(row['Weight']) if pd.notna(row['Weight']) else 0
                )
                workout_logs.append(workout_log)
        
        # Batch insert all workout logs
        db.session.bulk_save_objects(workout_logs)
        db.session.commit()
        print(f"Successfully loaded {len(workout_logs)} workout logs across {len(session_mapping)} sessions")
    except Exception as e:
        db.session.rollback()
        print(f"Error loading workout data: {e}")
        raise

def batch_insert_workout_logs(workout_logs):
    try:
        db.session.bulk_save_objects(workout_logs)
        db.session.commit()
        print("Workout logs loaded successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error loading workout logs: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
        load_exercises_from_csv()
        load_workout_sessions_from_csv()
