import pandas as pd
import os
from app.models import db, AgePercentileData, WeightPercentileData

def load_age_percentile_data(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        age_data = AgePercentileData(
            sex=row['Sex'],
            age_category=row['Age'],
            percentile=float(str(row['Percentile']).replace('th','')),
            squat=row['Squat'],
            squat_ll=row['Squat_LL'],
            squat_ul=row['Squat_UL'],
            bench=row['Bench'],
            bench_ll=row['Bench_LL'],
            bench_ul=row['Bench_UL'],
            deadlift=row['Deadlift'],
            deadlift_ll=row['Deadlift_LL'],
            deadlift_ul=row['Deadlift_UL']
        )
        db.session.add(age_data)
    db.session.commit()

def load_weight_percentile_data(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        weight_data = WeightPercentileData(
            sex=row['Sex'],
            weight_class=str(row['Weight']),
            percentile=float(str(row['Percentile']).replace('th','')),
            squat=row['Squat'],
            squat_ll=row['Squat_LL'],
            squat_ul=row['Squat_UL'],
            bench=row['Bench'],
            bench_ll=row['Bench_LL'],
            bench_ul=row['Bench_UL'],
            deadlift=row['Deadlift'],
            deadlift_ll=row['Deadlift_LL'],
            deadlift_ul=row['Deadlift_UL']
        )
        db.session.add(weight_data)
    db.session.commit()

def get_lift_value(row, exercise_name):
    if exercise_name == 'Squat':
        return row.squat
    elif exercise_name == 'Bench Press':
        return row.bench
    elif exercise_name == 'Deadlift':
        return row.deadlift
    return None

def find_closest_percentile(rows, exercise_name, user_weight):
    # rows: list of model objects with percentile and lift values
    # user_weight: user's 1RM
    # Return closest percentile
    values = []
    for r in rows:
        val = get_lift_value(r, exercise_name)
        values.append((abs(val - user_weight), r.percentile))
    # Sort by difference
    values.sort(key=lambda x: x[0])
    # Return percentile of the closest value
    return values[0][1]

def calculate_age_percentile(exercise_name, weight, age, gender):
    gender = gender.lower().strip()
    age_cat = get_age_category(age)
    # Query AgePercentileData
    rows = AgePercentileData.query.filter_by(sex=gender, age_category=age_cat).all()
    if not rows:
        # If no data, return a default percentile
        return 50.0
    return find_closest_percentile(rows, exercise_name, weight)

def parse_weight_classes(sex):
    # Return sorted classes from WeightPercentileData
    classes = WeightPercentileData.query.filter_by(sex=sex).distinct(WeightPercentileData.weight_class).all()
    # Extract distinct classes
    distinct_classes = {c.weight_class for c in classes}
    # Convert them to numeric or handle '+' classes
    # weight classes like '43', '84+', '120'
    parsed = []
    for wc in distinct_classes:
        if wc.endswith('+'):
            base = float(wc.replace('+',''))
            parsed.append((base, True))  # (weight, is_plus)
        else:
            parsed.append((float(wc), False))
    # Sort by weight
    parsed.sort(key=lambda x: x[0])
    return parsed

def find_weight_class(gender, user_weight):
    # Find best matching weight_class from the database
    gender = gender.lower().strip()
    parsed = parse_weight_classes(gender)
    # If user_weight is less than first class and not plus, choose first class
    if user_weight < parsed[0][0] and not parsed[0][1]:
        chosen = parsed[0]
    else:
        chosen = parsed[-1]  # by default last
        for i, (w, is_plus) in enumerate(parsed):
            if is_plus and user_weight > w:
                chosen = (w, True)
            elif user_weight <= w:
                # user fits into this class or next lower
                chosen = (w, is_plus)
                break
    # Reconstruct string
    if chosen[1]:
        return f"{int(chosen[0])}+"
    else:
        return str(int(chosen[0]))

def calculate_weight_percentile(exercise_name, weight, user_weight, gender):
    gender = gender.lower().strip()
    wc = find_weight_class(gender, user_weight)
    rows = WeightPercentileData.query.filter_by(sex=gender, weight_class=wc).all()
    if not rows:
        return 50.0
    return find_closest_percentile(rows, exercise_name, weight)

def get_age_category(age):
    if age < 18:
        return "12-17"
    elif age <= 35:
        return "18-35"
    elif age <= 59:
        return "36-59"
    elif age <= 79:
        return "60-79"
    else:
        return "80+"

def get_weight_class(gender, weight):
    # This is replaced by a more dynamic find_weight_class logic in calculations,
    # but we keep this function since code may depend on it.
    # Just return a generic class or a simplified logic:
    # We'll map a few classes from the logic above:
    gender = gender.lower().strip()
    # For display only, pick simple logic:
    if gender == "male":
        if weight < 60:
            return "Lightweight"
        elif weight < 85:
            return "Middleweight"
        else:
            return "Heavyweight"
    else:
        if weight < 50:
            return "Lightweight"
        elif weight < 70:
            return "Middleweight"
        else:
            return "Heavyweight"
