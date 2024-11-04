import pandas as pd
from datetime import datetime
from models import db, WorkoutSession, WorkoutLog
from app import app

def load_workout_sessions_from_csv():
    try:
        # First, clear existing data

        db.session.commit()

        # Load CSV file
        df = pd.read_csv('./data/matthew-eleazar-strong.csv')

        # Standardize column names
        df.rename(columns={
            'Date': 'session_date',
            'Workout Name': 'workout_name',
            'Exercise Name': 'exercise_name',
            'Set Order': 'set_order',
            'Weight': 'weight',
            'Reps': 'reps'
        }, inplace=True)

        # Convert date to datetime
        df['session_date'] = pd.to_datetime(df['session_date'])

        # Create a session ID for each unique date + workout name combination
        df['session_key'] = df.groupby(['session_date', 'workout_name']).ngroup() + 1

        # Create sessions first
        unique_sessions = df[['session_date', 'workout_name', 'session_key']].drop_duplicates()
        
        # Store session mapping
        session_mapping = {}
        
        for _, row in unique_sessions.iterrows():
            workout_session = WorkoutSession(
                user_id=1,
                session_name=row['workout_name'],
                start_time=row['session_date'],
                status='completed'
            )
            db.session.add(workout_session)
            db.session.flush()
            session_mapping[row['session_key']] = workout_session.session_id

        # Now create workout logs
        for _, row in df.iterrows():
            # Parse equipment and variation from exercise name
            exercise_name = row['exercise_name']
            equipment = ''
            
            if '(' in exercise_name:
                base_name = exercise_name.split('(')[0].strip()
                equipment = exercise_name.split('(')[1].replace(')', '').strip()
                exercise_name = base_name

            workout_log = WorkoutLog(
                user_id=1,
                session_id=session_mapping[row['session_key']],
                session_workout_number=row['set_order'],
                completed_at=row['session_date'].date(),
                intensity_level='medium',
                rest_time=0,
                reps=row['reps'],
                sets=row['set_order'],
                exercise_name=exercise_name.lower(),
                equipment=equipment.lower() if equipment else 'unknown',
                variation='standard'
            )
            db.session.add(workout_log)

        db.session.commit()
        print("Workout sessions loaded successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error loading workout sessions: {e}")
        raise e

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        load_workout_sessions_from_csv()