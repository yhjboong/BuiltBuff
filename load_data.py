import pandas as pd
from models import db, ExerciseList
from app import app  # Import app to get the app context
from sqlalchemy.exc import IntegrityError  # Add this line

def load_exercises_from_csv():
    try:
        # Load CSV file
        df_exercises = pd.read_csv('./data/gym_exercise_dataset.csv')

        # **Data Cleaning Code (Place here):**
        df_exercises['Exercise Name'] = df_exercises['Exercise Name'].str.strip().str.lower()
        df_exercises['Equipment'] = df_exercises['Equipment'].str.strip().str.lower()
        df_exercises['Variation'] = df_exercises['Variation'].astype(str).str.strip().str.lower()

        # Check if required columns exist
        required_columns = {'Exercise Name', 'Equipment', 'Variation', 'Preparation', 'Execution'}
        if not required_columns.issubset(df_exercises.columns):
            missing = required_columns - set(df_exercises.columns)
            raise ValueError(f"CSV file is missing required columns: {', '.join(missing)}")

        for _, row in df_exercises.iterrows():
            description = f"Preparation: {row['Preparation']}\nExecution: {row['Execution']}"

            # Check if the exercise already exists
            existing_exercise = ExerciseList.query.filter_by(
                name=row['Exercise Name'],
                equipment=row['Equipment'],
                variation=row['Variation']
            ).first()

            if existing_exercise:
                print(f"Exercise '{row['Exercise Name']}' with equipment '{row['Equipment']}' and variation '{row['Variation']}' already exists. Skipping.")
                continue

            # Create new exercise entry
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
        print(f"Error loading exercises: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
        load_exercises_from_csv()
