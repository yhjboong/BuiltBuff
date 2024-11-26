import pandas as pd

# Load data once when module is imported
df_age = pd.read_csv('data/big_three_data/Sex_Age_Bigthree.csv')
df_weight = pd.read_csv('data/big_three_data/Sex_Weight_Bigthree.csv')

def get_age_category(age):
    if age < 18:
        return '12-17'
    elif age < 36:
        return '18-35'
    elif age < 60:
        return '36-59'
    elif age < 80:
        return '60-79'
    else:
        return '80+'

def get_weight_class(gender, weight):
    weight_classes = {
        'female': [43, 47, 52, 57, 63, 69, 76, 84],
        'male': [53, 59, 66, 74, 83, 93, 105, 120]
    }
    
    gender = gender.lower()
    classes = weight_classes[gender]
    for wc in classes:
        if weight <= wc:
            return wc
    return f"{classes[-1]}+"

def calculate_percentile(df_filtered, weight):
    if df_filtered.empty:
        return 0
    
    for idx, row in df_filtered.iterrows():
        if weight <= row['Squat']:  # Using Squat as reference
            return float(row['Percentile'].rstrip('th'))
    return 90  # If weight is higher than all records

def calculate_age_percentile(exercise_type, weight, age, gender):
    age_category = get_age_category(age)
    df_filtered = df_age[
        (df_age['Sex'].str.lower() == gender.lower()) &
        (df_age['Age'] == age_category)
    ]
    return calculate_percentile(df_filtered, weight)

def calculate_weight_percentile(exercise_type, weight_lifted, body_weight, gender):
    weight_class = get_weight_class(gender, body_weight)
    df_filtered = df_weight[
        (df_weight['Sex'].str.lower() == gender.lower()) &
        (df_weight['Weight'] == weight_class)
    ]
    return calculate_percentile(df_filtered, weight_lifted)
