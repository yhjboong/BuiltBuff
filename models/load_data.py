import sys
import os
from pathlib import Path

# Get the project root directory
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

import pandas as pd
from datetime import datetime
from app import create_app, db
from app.models import User, WorkoutLog, ExerciseList, WorkoutSession, WorkoutHistory

app = create_app()

def load_exercises_from_csv():
    try:
        # Load exercise CSV file
        df_exercises = pd.read_csv(os.path.join(ROOT_DIR, 'data', 'gym_exercise_dataset.csv'))

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
    # Load the workout sessions CSV file
    df = pd.read_csv(os.path.join(ROOT_DIR, 'data', 'matthew-eleazar-strong.csv'))

    workout_logs = []
    session_mapping = {}

    for _, row in df.iterrows():
        session_key = row['session_key']
        # If session_key is new, create a completed WorkoutSession
        if session_key not in session_mapping:
            session_date = pd.to_datetime(row['Date'])
            new_session = WorkoutSession(
                user_id=1,  # Update as needed for the actual user ID
                session_name=row['Workout Name'],
                start_time=session_date,
                end_time=session_date,  # Temporary, will update after processing all workouts
                status='completed'
            )
            db.session.add(new_session)
            db.session.flush()  # Get the session_id before commit
            session_mapping[session_key] = new_session.session_id

        # Add each workout log entry to the list
        session_id = session_mapping[session_key]
        exercise_name = row['Exercise Name'].lower()
        
        # Handle missing or non-string 'Equipment' values
        equipment = row['Equipment'] if isinstance(row['Equipment'], str) else 'unknown'
        equipment = equipment.lower()

        workout_log = WorkoutLog(
            user_id=1,
            session_id=session_id,
            session_workout_number=row['Set Order'],
            completed_at=pd.to_datetime(row['Date']).date(),
            intensity_level='medium',  # Replace with actual intensity if available
            rest_time=row.get('Seconds', 0),
            reps=row['Reps'],
            sets=row['Set Order'],
            exercise_name=exercise_name,
            equipment=equipment,
            variation='standard',
            weight=row.get('Weight', 0)  # Add weight if present
        )
        workout_logs.append(workout_log)

    # Batch insert all workout logs
    db.session.bulk_save_objects(workout_logs)
    db.session.commit()
    
    # Update each session's end time to the latest workout time in the session
    for session_key, session_id in session_mapping.items():
        last_workout = WorkoutLog.query.filter_by(session_id=session_id).order_by(WorkoutLog.completed_at.desc()).first()
        session = WorkoutSession.query.get(session_id)
        session.end_time = last_workout.completed_at if last_workout else session.start_time
        db.session.commit()
    
    print("Workout sessions and logs loaded as completed history successfully.")


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
