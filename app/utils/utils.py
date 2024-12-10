import pandas as pd
import os
from app.models import db, AgePercentileData, WeightPercentileData

LBS_PER_KG = 2.2046226218

def load_age_percentile_data(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        age_data = AgePercentileData(
            sex=row['Sex'].lower().strip(),
            age_category=row['Age'],
            percentile=float(str(row['Percentile']).replace('th','')),
            squat=row['Squat'] * LBS_PER_KG,
            squat_ll=row['Squat_LL'] * LBS_PER_KG if not pd.isna(row['Squat_LL']) else None,
            squat_ul=row['Squat_UL'] * LBS_PER_KG if not pd.isna(row['Squat_UL']) else None,
            bench=row['Bench'] * LBS_PER_KG,
            bench_ll=row['Bench_LL'] * LBS_PER_KG if not pd.isna(row['Bench_LL']) else None,
            bench_ul=row['Bench_UL'] * LBS_PER_KG if not pd.isna(row['Bench_UL']) else None,
            deadlift=row['Deadlift'] * LBS_PER_KG,
            deadlift_ll=row['Deadlift_LL'] * LBS_PER_KG if not pd.isna(row['Deadlift_LL']) else None,
            deadlift_ul=row['Deadlift_UL'] * LBS_PER_KG if not pd.isna(row['Deadlift_UL']) else None
        )
        db.session.add(age_data)
    db.session.commit()

def load_weight_percentile_data(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        # Convert weight classes to lbs if numeric:
        weight_class_str = str(row['Weight'])
        # If weight class is like "84+", convert 84 kg to lbs and add "+".
        # Otherwise just convert numeric value from kg to lbs and round:
        if weight_class_str.endswith('+'):
            base_kg = float(weight_class_str.replace('+',''))
            wc_lbs = f"{int(round(base_kg * LBS_PER_KG))}+"
        else:
            base_kg = float(weight_class_str)
            wc_lbs = str(int(round(base_kg * LBS_PER_KG)))

        weight_data = WeightPercentileData(
            sex=row['Sex'].lower().strip(),
            weight_class=wc_lbs,
            percentile=float(str(row['Percentile']).replace('th','')),
            squat=row['Squat'] * LBS_PER_KG,
            squat_ll=row['Squat_LL'] * LBS_PER_KG if not pd.isna(row['Squat_LL']) else None,
            squat_ul=row['Squat_UL'] * LBS_PER_KG if not pd.isna(row['Squat_UL']) else None,
            bench=row['Bench'] * LBS_PER_KG,
            bench_ll=row['Bench_LL'] * LBS_PER_KG if not pd.isna(row['Bench_LL']) else None,
            bench_ul=row['Bench_UL'] * LBS_PER_KG if not pd.isna(row['Bench_UL']) else None,
            deadlift=row['Deadlift'] * LBS_PER_KG,
            deadlift_ll=row['Deadlift_LL'] * LBS_PER_KG if not pd.isna(row['Deadlift_LL']) else None,
            deadlift_ul=row['Deadlift_UL'] * LBS_PER_KG if not pd.isna(row['Deadlift_UL']) else None
        )
        db.session.add(weight_data)
    db.session.commit()

def get_lift_value(row, exercise_name):
    en = exercise_name.lower()
    if 'squat' in en:
        return row.squat, row.squat_ll, row.squat_ul
    elif 'bench' in en:
        return row.bench, row.bench_ll, row.bench_ul
    elif 'deadlift' in en:
        return row.deadlift, row.deadlift_ll, row.deadlift_ul
    return None, None, None

def find_closest_percentile(rows, exercise_name, user_weight):
    values = []
    for r in rows:
        val, ll, ul = get_lift_value(r, exercise_name)
        diff = abs(val - user_weight)
        values.append((diff, r.percentile, val, ll, ul))
    values.sort(key=lambda x: x[0])
    # Return percentile and also LL, UL
    return values[0][1], values[0][3], values[0][4]

def calculate_age_percentile(exercise_name, weight, age, gender):
    gender = gender.lower().strip()
    age_cat = get_age_category(age)
    rows = AgePercentileData.query.filter_by(sex=gender, age_category=age_cat).all()
    if not rows:
        return 50.0, None, None
    percentile, ll, ul = find_closest_percentile(rows, exercise_name, weight)
    return percentile, ll, ul

def calculate_weight_percentile(exercise_name, weight, user_weight, gender):
    gender = gender.lower().strip()
    wc = find_weight_class(gender, user_weight)
    if wc is None:
        return 50.0, None, None
    rows = WeightPercentileData.query.filter_by(sex=gender, weight_class=wc).all()
    if not rows:
        return 50.0, None, None
    percentile, ll, ul = find_closest_percentile(rows, exercise_name, weight)
    return percentile, ll, ul

def parse_weight_classes(sex):
    classes = WeightPercentileData.query.filter_by(sex=sex).distinct(WeightPercentileData.weight_class).all()
    if not classes:
        return []
    distinct_classes = {c.weight_class for c in classes}
    # classes now in lbs, might have a plus sign
    parsed = []
    for wc in distinct_classes:
        if wc.endswith('+'):
            base = float(wc.replace('+',''))
            parsed.append((base, True))
        else:
            parsed.append((float(wc), False))
    parsed.sort(key=lambda x: x[0])
    return parsed

def find_weight_class(gender, user_weight):
    # user_weight in lbs
    parsed = parse_weight_classes(gender)
    if not parsed:
        return None
    if user_weight < parsed[0][0] and not parsed[0][1]:
        chosen = parsed[0]
    else:
        chosen = parsed[-1]
        for w, is_plus in parsed:
            if is_plus and user_weight > w:
                chosen = (w, True)
            elif user_weight <= w:
                chosen = (w, is_plus)
                break
    if chosen[1]:
        return f"{int(chosen[0])}+"
    else:
        return str(int(chosen[0]))

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
    # For display only, no changes needed, just show lightweight/middleweight/heavyweight
    gender = gender.lower().strip()
    if gender == "male":
        if weight < 132: # ~60kg
            return "Lightweight"
        elif weight < 187: # ~85kg
            return "Middleweight"
        else:
            return "Heavyweight"
    else:
        if weight < 110: # ~50kg
            return "Lightweight"
        elif weight < 154: # ~70kg
            return "Middleweight"
        else:
            return "Heavyweight"