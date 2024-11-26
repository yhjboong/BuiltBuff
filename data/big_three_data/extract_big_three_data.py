import pandas as pd

# Data manually extracted from the research paper for squat, bench press, and deadlift percentile tables
squat_data_age = [
    # Squat (Female, Age 12–17)
    {"lift_type": "squat", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 90, "strength_value": 1.95, "lower_bound": 1.94, "upper_bound": 1.96},
    {"lift_type": "squat", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 80, "strength_value": 1.77, "lower_bound": 1.76, "upper_bound": 1.78},
    {"lift_type": "squat", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 70, "strength_value": 1.65, "lower_bound": 1.64, "upper_bound": 1.66},
    {"lift_type": "squat", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 60, "strength_value": 1.55, "lower_bound": 1.54, "upper_bound": 1.56},
    {"lift_type": "squat", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 50, "strength_value": 1.45, "lower_bound": 1.44, "upper_bound": 1.46},
    {"lift_type": "squat", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 40, "strength_value": 1.36, "lower_bound": 1.36, "upper_bound": 1.37},
    {"lift_type": "squat", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 30, "strength_value": 1.26, "lower_bound": 1.26, "upper_bound": 1.27},
    {"lift_type": "squat", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 20, "strength_value": 1.15, "lower_bound": 1.15, "upper_bound": 1.16},
    {"lift_type": "squat", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 10, "strength_value": 1.01, "lower_bound": 1.00, "upper_bound": 1.01},

    # Squat (Female, Age 18–35)
    {"lift_type": "squat", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 90, "strength_value": 2.26, "lower_bound": 2.25, "upper_bound": 2.26},
    {"lift_type": "squat", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 80, "strength_value": 2.07, "lower_bound": 2.06, "upper_bound": 2.07},
    {"lift_type": "squat", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 70, "strength_value": 1.93, "lower_bound": 1.93, "upper_bound": 1.93},
    {"lift_type": "squat", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 60, "strength_value": 1.82, "lower_bound": 1.82, "upper_bound": 1.83},
    {"lift_type": "squat", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 50, "strength_value": 1.72, "lower_bound": 1.72, "upper_bound": 1.72},
    {"lift_type": "squat", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 40, "strength_value": 1.62, "lower_bound": 1.62, "upper_bound": 1.63},
    {"lift_type": "squat", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 30, "strength_value": 1.52, "lower_bound": 1.52, "upper_bound": 1.52},
    {"lift_type": "squat", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 20, "strength_value": 1.40, "lower_bound": 1.39, "upper_bound": 1.40},
    {"lift_type": "squat", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 10, "strength_value": 1.23, "lower_bound": 1.23, "upper_bound": 1.24},
    
    # Squat (Female, Age 36–59)
    {"lift_type": "squat", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 90, "strength_value": 2.05, "lower_bound": 2.04, "upper_bound": 2.06},
    {"lift_type": "squat", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 80, "strength_value": 1.85, "lower_bound": 1.85, "upper_bound": 1.86},
    {"lift_type": "squat", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 70, "strength_value": 1.73, "lower_bound": 1.72, "upper_bound": 1.73},
    {"lift_type": "squat", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 60, "strength_value": 1.61, "lower_bound": 1.60, "upper_bound": 1.61},
    {"lift_type": "squat", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 50, "strength_value": 1.51, "lower_bound": 1.50, "upper_bound": 1.51},
    {"lift_type": "squat", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 40, "strength_value": 1.41, "lower_bound": 1.40, "upper_bound": 1.41},
    {"lift_type": "squat", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 30, "strength_value": 1.30, "lower_bound": 1.29, "upper_bound": 1.30},
    {"lift_type": "squat", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 20, "strength_value": 1.17, "lower_bound": 1.17, "upper_bound": 1.18},
    {"lift_type": "squat", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 10, "strength_value": 1.01, "lower_bound": 1.00, "upper_bound": 1.01},

    # Squat (Female, Age 60–79)
    {"lift_type": "squat", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 90, "strength_value": 1.65, "lower_bound": 1.63, "upper_bound": 1.67},
    {"lift_type": "squat", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 80, "strength_value": 1.48, "lower_bound": 1.47, "upper_bound": 1.50},
    {"lift_type": "squat", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 70, "strength_value": 1.36, "lower_bound": 1.35, "upper_bound": 1.38},
    {"lift_type": "squat", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 60, "strength_value": 1.26, "lower_bound": 1.25, "upper_bound": 1.28},
    {"lift_type": "squat", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 50, "strength_value": 1.17, "lower_bound": 1.15, "upper_bound": 1.18},
    {"lift_type": "squat", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 40, "strength_value": 1.08, "lower_bound": 1.06, "upper_bound": 1.09},
    {"lift_type": "squat", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 30, "strength_value": 0.97, "lower_bound": 0.96, "upper_bound": 0.99},
    {"lift_type": "squat", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 20, "strength_value": 0.87, "lower_bound": 0.85, "upper_bound": 0.89},
    {"lift_type": "squat", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 10, "strength_value": 0.72, "lower_bound": 0.69, "upper_bound": 0.74},

    # Squat (Female, Age 80+)
    {"lift_type": "squat", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 90, "strength_value": 1.01, "lower_bound": 0.95, "upper_bound": 1.21},
    {"lift_type": "squat", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 80, "strength_value": 0.96, "lower_bound": 0.83, "upper_bound": 1.01},
    {"lift_type": "squat", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 70, "strength_value": 0.90, "lower_bound": 0.73, "upper_bound": 0.97},
    {"lift_type": "squat", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 60, "strength_value": 0.78, "lower_bound": 0.58, "upper_bound": 0.94},
    {"lift_type": "squat", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 50, "strength_value": 0.67, "lower_bound": 0.51, "upper_bound": 0.83},
    {"lift_type": "squat", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 40, "strength_value": 0.55, "lower_bound": 0.41, "upper_bound": 0.75},
    {"lift_type": "squat", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 30, "strength_value": 0.49, "lower_bound": 0.30, "upper_bound": 0.62},
    {"lift_type": "squat", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 20, "strength_value": 0.32, "lower_bound": 0.29, "upper_bound": 0.51},
    {"lift_type": "squat", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 10, "strength_value": 0.29, "lower_bound": 0.08, "upper_bound": 0.32},
    
    # Squat (Male, Age 12–17)
    {"lift_type": "squat", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 90, "strength_value": 2.50, "lower_bound": 2.50, "upper_bound": 2.51},
    {"lift_type": "squat", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 80, "strength_value": 2.30, "lower_bound": 2.30, "upper_bound": 2.31},
    {"lift_type": "squat", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 70, "strength_value": 2.16, "lower_bound": 2.16, "upper_bound": 2.17},
    {"lift_type": "squat", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 60, "strength_value": 2.04, "lower_bound": 2.03, "upper_bound": 2.04},
    {"lift_type": "squat", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 50, "strength_value": 1.92, "lower_bound": 1.92, "upper_bound": 1.93},
    {"lift_type": "squat", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 40, "strength_value": 1.80, "lower_bound": 1.80, "upper_bound": 1.81},
    {"lift_type": "squat", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 30, "strength_value": 1.67, "lower_bound": 1.67, "upper_bound": 1.67},
    {"lift_type": "squat", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 20, "strength_value": 1.52, "lower_bound": 1.52, "upper_bound": 1.53},
    {"lift_type": "squat", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 10, "strength_value": 1.32, "lower_bound": 1.31, "upper_bound": 1.33},

    # Squat (Male, Age 18–35)
    {"lift_type": "squat", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 90, "strength_value": 2.83, "lower_bound": 2.83, "upper_bound": 2.83},
    {"lift_type": "squat", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 80, "strength_value": 2.63, "lower_bound": 2.63, "upper_bound": 2.63},
    {"lift_type": "squat", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 70, "strength_value": 2.50, "lower_bound": 2.49, "upper_bound": 2.50},
    {"lift_type": "squat", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 60, "strength_value": 2.38, "lower_bound": 2.38, "upper_bound": 2.38},
    {"lift_type": "squat", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 50, "strength_value": 2.28, "lower_bound": 2.28, "upper_bound": 2.27},
    {"lift_type": "squat", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 40, "strength_value": 2.17, "lower_bound": 2.17, "upper_bound": 2.17},
    {"lift_type": "squat", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 30, "strength_value": 2.06, "lower_bound": 2.05, "upper_bound": 2.06},
    {"lift_type": "squat", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 20, "strength_value": 1.93, "lower_bound": 1.93, "upper_bound": 1.93},
    {"lift_type": "squat", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 10, "strength_value": 1.75, "lower_bound": 1.74, "upper_bound": 1.75},
    
    # Squat (Male, Age 36–59)
    {"lift_type": "squat", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 90, "strength_value": 2.58, "lower_bound": 2.57, "upper_bound": 2.59},
    {"lift_type": "squat", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 80, "strength_value": 2.38, "lower_bound": 2.38, "upper_bound": 2.38},
    {"lift_type": "squat", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 70, "strength_value": 2.24, "lower_bound": 2.24, "upper_bound": 2.25},
    {"lift_type": "squat", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 60, "strength_value": 2.13, "lower_bound": 2.13, "upper_bound": 2.13},
    {"lift_type": "squat", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 50, "strength_value": 2.03, "lower_bound": 2.02, "upper_bound": 2.03},
    {"lift_type": "squat", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 40, "strength_value": 1.91, "lower_bound": 1.91, "upper_bound": 1.92},
    {"lift_type": "squat", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 30, "strength_value": 1.76, "lower_bound": 1.76, "upper_bound": 1.77},
    {"lift_type": "squat", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 20, "strength_value": 1.67, "lower_bound": 1.67, "upper_bound": 1.67},
    {"lift_type": "squat", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 10, "strength_value": 1.48, "lower_bound": 1.48, "upper_bound": 1.48},

    # Squat (Male, Age 60–79)
    {"lift_type": "squat", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 90, "strength_value": 2.16, "lower_bound": 2.15, "upper_bound": 2.18},
    {"lift_type": "squat", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 80, "strength_value": 1.98, "lower_bound": 1.97, "upper_bound": 1.99},
    {"lift_type": "squat", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 70, "strength_value": 1.85, "lower_bound": 1.84, "upper_bound": 1.86},
    {"lift_type": "squat", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 60, "strength_value": 1.73, "lower_bound": 1.72, "upper_bound": 1.75},
    {"lift_type": "squat", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 50, "strength_value": 1.62, "lower_bound": 1.61, "upper_bound": 1.63},
    {"lift_type": "squat", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 40, "strength_value": 1.50, "lower_bound": 1.49, "upper_bound": 1.52},
    {"lift_type": "squat", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 30, "strength_value": 1.38, "lower_bound": 1.37, "upper_bound": 1.39},
    {"lift_type": "squat", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 20, "strength_value": 1.23, "lower_bound": 1.22, "upper_bound": 1.24},
    {"lift_type": "squat", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 10, "strength_value": 1.04, "lower_bound": 1.02, "upper_bound": 1.05},

    # Squat (Male, Age 80+)
    {"lift_type": "squat", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 90, "strength_value": 1.72, "lower_bound": 1.60, "upper_bound": 1.81},
    {"lift_type": "squat", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 80, "strength_value": 1.52, "lower_bound": 1.46, "upper_bound": 1.60},
    {"lift_type": "squat", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 70, "strength_value": 1.37, "lower_bound": 1.27, "upper_bound": 1.47},
    {"lift_type": "squat", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 60, "strength_value": 1.18, "lower_bound": 1.13, "upper_bound": 1.32},
    {"lift_type": "squat", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 50, "strength_value": 1.05, "lower_bound": 0.92, "upper_bound": 1.20},
    {"lift_type": "squat", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 40, "strength_value": 0.90, "lower_bound": 0.83, "upper_bound": 1.03},
    {"lift_type": "squat", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 30, "strength_value": 0.79, "lower_bound": 0.70, "upper_bound": 0.86},
    {"lift_type": "squat", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 20, "strength_value": 0.62, "lower_bound": 0.52, "upper_bound": 0.70},
    {"lift_type": "squat", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 10, "strength_value": 0.52, "lower_bound": 0.47, "upper_bound": 0.68},
]



bench_data_age = [
    # Bench Press (Female, Age 12–17)
    {"lift_type": "bench_press", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 90, "strength_value": 1.14, "lower_bound": 1.13, "upper_bound": 1.15},
    {"lift_type": "bench_press", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 80, "strength_value": 1.02, "lower_bound": 1.01, "upper_bound": 1.02},
    {"lift_type": "bench_press", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 70, "strength_value": 0.94, "lower_bound": 0.93, "upper_bound": 0.94},
    {"lift_type": "bench_press", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 60, "strength_value": 0.87, "lower_bound": 0.87, "upper_bound": 0.87},
    {"lift_type": "bench_press", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 50, "strength_value": 0.81, "lower_bound": 0.81, "upper_bound": 0.81},
    {"lift_type": "bench_press", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 40, "strength_value": 0.75, "lower_bound": 0.75, "upper_bound": 0.76},
    {"lift_type": "bench_press", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 30, "strength_value": 0.70, "lower_bound": 0.69, "upper_bound": 0.70},
    {"lift_type": "bench_press", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 20, "strength_value": 0.63, "lower_bound": 0.63, "upper_bound": 0.64},
    {"lift_type": "bench_press", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 10, "strength_value": 0.56, "lower_bound": 0.55, "upper_bound": 0.56},

    # Bench Press (Female, Age 18–35)
    {"lift_type": "bench_press", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 90, "strength_value": 1.35, "lower_bound": 1.35, "upper_bound": 1.35},
    {"lift_type": "bench_press", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 80, "strength_value": 1.20, "lower_bound": 1.20, "upper_bound": 1.20},
    {"lift_type": "bench_press", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 70, "strength_value": 1.10, "lower_bound": 1.10, "upper_bound": 1.10},
    {"lift_type": "bench_press", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 60, "strength_value": 1.03, "lower_bound": 1.03, "upper_bound": 1.03},
    {"lift_type": "bench_press", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 50, "strength_value": 0.96, "lower_bound": 0.96, "upper_bound": 0.97},
    {"lift_type": "bench_press", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 40, "strength_value": 0.90, "lower_bound": 0.90, "upper_bound": 0.90},
    {"lift_type": "bench_press", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 30, "strength_value": 0.84, "lower_bound": 0.84, "upper_bound": 0.84},
    {"lift_type": "bench_press", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 20, "strength_value": 0.77, "lower_bound": 0.76, "upper_bound": 0.77},
    {"lift_type": "bench_press", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 10, "strength_value": 0.67, "lower_bound": 0.67, "upper_bound": 0.68},

    # Bench Press (Female, Age 36–59)
    {"lift_type": "bench_press", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 90, "strength_value": 1.28, "lower_bound": 1.28, "upper_bound": 1.29},
    {"lift_type": "bench_press", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 80, "strength_value": 1.14, "lower_bound": 1.14, "upper_bound": 1.14},
    {"lift_type": "bench_press", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 70, "strength_value": 1.04, "lower_bound": 1.04, "upper_bound": 1.05},
    {"lift_type": "bench_press", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 60, "strength_value": 0.97, "lower_bound": 0.97, "upper_bound": 0.97},
    {"lift_type": "bench_press", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 50, "strength_value": 0.90, "lower_bound": 0.90, "upper_bound": 0.90},
    {"lift_type": "bench_press", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 40, "strength_value": 0.84, "lower_bound": 0.83, "upper_bound": 0.84},
    {"lift_type": "bench_press", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 30, "strength_value": 0.77, "lower_bound": 0.77, "upper_bound": 0.77},
    {"lift_type": "bench_press", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 20, "strength_value": 0.70, "lower_bound": 0.70, "upper_bound": 0.70},
    {"lift_type": "bench_press", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 10, "strength_value": 0.62, "lower_bound": 0.61, "upper_bound": 0.62},

    # Bench Press (Female, Age 60–79)
    {"lift_type": "bench_press", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 90, "strength_value": 1.04, "lower_bound": 1.04, "upper_bound": 1.06},
    {"lift_type": "bench_press", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 80, "strength_value": 0.93, "lower_bound": 0.93, "upper_bound": 0.94},
    {"lift_type": "bench_press", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 70, "strength_value": 0.85, "lower_bound": 0.84, "upper_bound": 0.86},
    {"lift_type": "bench_press", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 60, "strength_value": 0.77, "lower_bound": 0.77, "upper_bound": 0.78},
    {"lift_type": "bench_press", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 50, "strength_value": 0.72, "lower_bound": 0.71, "upper_bound": 0.73},
    {"lift_type": "bench_press", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 40, "strength_value": 0.66, "lower_bound": 0.66, "upper_bound": 0.67},
    {"lift_type": "bench_press", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 30, "strength_value": 0.56, "lower_bound": 0.56, "upper_bound": 0.57},
    {"lift_type": "bench_press", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 20, "strength_value": 0.50, "lower_bound": 0.48, "upper_bound": 0.50},
    {"lift_type": "bench_press", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 10, "strength_value": 0.49, "lower_bound": 0.48, "upper_bound": 0.50},

    # Bench Press (Female, Age 80+)
    {"lift_type": "bench_press", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 90, "strength_value": 0.92, "lower_bound": 0.81, "upper_bound": 1.00},
    {"lift_type": "bench_press", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 80, "strength_value": 0.74, "lower_bound": 0.68, "upper_bound": 0.89},
    {"lift_type": "bench_press", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 70, "strength_value": 0.67, "lower_bound": 0.59, "upper_bound": 0.73},
    {"lift_type": "bench_press", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 60, "strength_value": 0.59, "lower_bound": 0.54, "upper_bound": 0.66},
    {"lift_type": "bench_press", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 50, "strength_value": 0.55, "lower_bound": 0.49, "upper_bound": 0.59},
    {"lift_type": "bench_press", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 40, "strength_value": 0.49, "lower_bound": 0.46, "upper_bound": 0.54},
    {"lift_type": "bench_press", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 30, "strength_value": 0.46, "lower_bound": 0.44, "upper_bound": 0.49},
    {"lift_type": "bench_press", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 20, "strength_value": 0.43, "lower_bound": 0.42, "upper_bound": 0.46},
    {"lift_type": "bench_press", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 10, "strength_value": 0.41, "lower_bound": 0.37, "upper_bound": 0.43},
    
    # Bench Press (Male, Age 12–17)
    {"lift_type": "bench_press", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 90, "strength_value": 1.63, "lower_bound": 1.63, "upper_bound": 1.64},
    {"lift_type": "bench_press", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 80, "strength_value": 1.49, "lower_bound": 1.49, "upper_bound": 1.50},
    {"lift_type": "bench_press", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 70, "strength_value": 1.40, "lower_bound": 1.39, "upper_bound": 1.40},
    {"lift_type": "bench_press", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 60, "strength_value": 1.32, "lower_bound": 1.31, "upper_bound": 1.32},
    {"lift_type": "bench_press", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 50, "strength_value": 1.24, "lower_bound": 1.24, "upper_bound": 1.25},
    {"lift_type": "bench_press", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 40, "strength_value": 1.17, "lower_bound": 1.17, "upper_bound": 1.18},
    {"lift_type": "bench_press", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 30, "strength_value": 1.09, "lower_bound": 1.08, "upper_bound": 1.09},
    {"lift_type": "bench_press", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 20, "strength_value": 0.99, "lower_bound": 0.98, "upper_bound": 0.99},
    {"lift_type": "bench_press", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 10, "strength_value": 0.85, "lower_bound": 0.85, "upper_bound": 0.85},

    # Bench Press (Male, Age 18–35)
    {"lift_type": "bench_press", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 90, "strength_value": 1.96, "lower_bound": 1.96, "upper_bound": 1.96},
    {"lift_type": "bench_press", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 80, "strength_value": 1.81, "lower_bound": 1.81, "upper_bound": 1.81},
    {"lift_type": "bench_press", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 70, "strength_value": 1.71, "lower_bound": 1.71, "upper_bound": 1.71},
    {"lift_type": "bench_press", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 60, "strength_value": 1.63, "lower_bound": 1.63, "upper_bound": 1.63},
    {"lift_type": "bench_press", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 50, "strength_value": 1.56, "lower_bound": 1.55, "upper_bound": 1.56},
    {"lift_type": "bench_press", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 40, "strength_value": 1.48, "lower_bound": 1.47, "upper_bound": 1.48},
    {"lift_type": "bench_press", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 30, "strength_value": 1.40, "lower_bound": 1.36, "upper_bound": 1.40},
    {"lift_type": "bench_press", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 20, "strength_value": 1.31, "lower_bound": 1.31, "upper_bound": 1.31},
    {"lift_type": "bench_press", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 10, "strength_value": 1.19, "lower_bound": 1.18, "upper_bound": 1.19},
    
    # Bench Press (Male, Age 36–59)
    {"lift_type": "bench_press", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 90, "strength_value": 1.92, "lower_bound": 1.91, "upper_bound": 1.92},
    {"lift_type": "bench_press", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 80, "strength_value": 1.77, "lower_bound": 1.77, "upper_bound": 1.77},
    {"lift_type": "bench_press", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 70, "strength_value": 1.67, "lower_bound": 1.67, "upper_bound": 1.67},
    {"lift_type": "bench_press", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 60, "strength_value": 1.59, "lower_bound": 1.59, "upper_bound": 1.59},
    {"lift_type": "bench_press", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 50, "strength_value": 1.52, "lower_bound": 1.51, "upper_bound": 1.52},
    {"lift_type": "bench_press", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 40, "strength_value": 1.44, "lower_bound": 1.43, "upper_bound": 1.44},
    {"lift_type": "bench_press", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 30, "strength_value": 1.36, "lower_bound": 1.35, "upper_bound": 1.36},
    {"lift_type": "bench_press", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 20, "strength_value": 1.26, "lower_bound": 1.25, "upper_bound": 1.26},
    {"lift_type": "bench_press", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 10, "strength_value": 1.13, "lower_bound": 1.13, "upper_bound": 1.13},

    # Bench Press (Male, Age 60–79)
    {"lift_type": "bench_press", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 90, "strength_value": 1.60, "lower_bound": 1.60, "upper_bound": 1.61},
    {"lift_type": "bench_press", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 80, "strength_value": 1.46, "lower_bound": 1.46, "upper_bound": 1.48},
    {"lift_type": "bench_press", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 70, "strength_value": 1.38, "lower_bound": 1.37, "upper_bound": 1.38},
    {"lift_type": "bench_press", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 60, "strength_value": 1.30, "lower_bound": 1.29, "upper_bound": 1.30},
    {"lift_type": "bench_press", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 50, "strength_value": 1.23, "lower_bound": 1.23, "upper_bound": 1.24},
    {"lift_type": "bench_press", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 40, "strength_value": 1.16, "lower_bound": 1.15, "upper_bound": 1.16},
    {"lift_type": "bench_press", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 30, "strength_value": 1.00, "lower_bound": 0.99, "upper_bound": 1.00},
    {"lift_type": "bench_press", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 20, "strength_value": 0.88, "lower_bound": 0.87, "upper_bound": 0.88},
    {"lift_type": "bench_press", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 10, "strength_value": 0.88, "lower_bound": 0.87, "upper_bound": 0.88},

    # Bench Press (Male, Age 80+)
    {"lift_type": "bench_press", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 90, "strength_value": 1.31, "lower_bound": 1.28, "upper_bound": 1.34},
    {"lift_type": "bench_press", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 80, "strength_value": 1.21, "lower_bound": 1.17, "upper_bound": 1.23},
    {"lift_type": "bench_press", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 70, "strength_value": 1.10, "lower_bound": 1.06, "upper_bound": 1.12},
    {"lift_type": "bench_press", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 60, "strength_value": 1.00, "lower_bound": 0.98, "upper_bound": 1.02},
    {"lift_type": "bench_press", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 50, "strength_value": 0.93, "lower_bound": 0.90, "upper_bound": 0.96},
    {"lift_type": "bench_press", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 40, "strength_value": 0.86, "lower_bound": 0.84, "upper_bound": 0.88},
    {"lift_type": "bench_press", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 30, "strength_value": 0.80, "lower_bound": 0.77, "upper_bound": 0.82},
    {"lift_type": "bench_press", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 20, "strength_value": 0.73, "lower_bound": 0.70, "upper_bound": 0.75},
    {"lift_type": "bench_press", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 10, "strength_value": 0.61, "lower_bound": 0.57, "upper_bound": 0.63}
]

dead_data_age = [
    # Deadlift (Female, Age 12–17)
    {"lift_type": "deadlift", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 90, "strength_value": 2.30, "lower_bound": 2.29, "upper_bound": 2.31},
    {"lift_type": "deadlift", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 80, "strength_value": 2.11, "lower_bound": 2.10, "upper_bound": 2.12},
    {"lift_type": "deadlift", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 70, "strength_value": 1.98, "lower_bound": 1.97, "upper_bound": 1.98},
    {"lift_type": "deadlift", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 60, "strength_value": 1.87, "lower_bound": 1.86, "upper_bound": 1.88},
    {"lift_type": "deadlift", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 50, "strength_value": 1.76, "lower_bound": 1.76, "upper_bound": 1.77},
    {"lift_type": "deadlift", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 40, "strength_value": 1.66, "lower_bound": 1.66, "upper_bound": 1.67},
    {"lift_type": "deadlift", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 30, "strength_value": 1.55, "lower_bound": 1.55, "upper_bound": 1.56},
    {"lift_type": "deadlift", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 20, "strength_value": 1.43, "lower_bound": 1.42, "upper_bound": 1.43},
    {"lift_type": "deadlift", "sex": "female", "age_category": "12-17", "weight_class": "all", "percentile": 10, "strength_value": 1.26, "lower_bound": 1.25, "upper_bound": 1.26},

    # Deadlift (Female, Age 18–35)
    {"lift_type": "deadlift", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 90, "strength_value": 2.66, "lower_bound": 2.66, "upper_bound": 2.67},
    {"lift_type": "deadlift", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 80, "strength_value": 2.45, "lower_bound": 2.45, "upper_bound": 2.46},
    {"lift_type": "deadlift", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 70, "strength_value": 2.30, "lower_bound": 2.30, "upper_bound": 2.30},
    {"lift_type": "deadlift", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 60, "strength_value": 2.17, "lower_bound": 2.17, "upper_bound": 2.18},
    {"lift_type": "deadlift", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 50, "strength_value": 2.06, "lower_bound": 2.05, "upper_bound": 2.06},
    {"lift_type": "deadlift", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 40, "strength_value": 1.94, "lower_bound": 1.94, "upper_bound": 1.94},
    {"lift_type": "deadlift", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 30, "strength_value": 1.82, "lower_bound": 1.82, "upper_bound": 1.83},
    {"lift_type": "deadlift", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 20, "strength_value": 1.68, "lower_bound": 1.68, "upper_bound": 1.68},
    {"lift_type": "deadlift", "sex": "female", "age_category": "18-35", "weight_class": "all", "percentile": 10, "strength_value": 1.49, "lower_bound": 1.48, "upper_bound": 1.49},

    # Deadlift (Female, Age 36–59)
    {"lift_type": "deadlift", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 90, "strength_value": 2.51, "lower_bound": 2.50, "upper_bound": 2.51},
    {"lift_type": "deadlift", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 80, "strength_value": 2.28, "lower_bound": 2.28, "upper_bound": 2.29},
    {"lift_type": "deadlift", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 70, "strength_value": 2.13, "lower_bound": 2.12, "upper_bound": 2.13},
    {"lift_type": "deadlift", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 60, "strength_value": 2.00, "lower_bound": 1.99, "upper_bound": 2.00},
    {"lift_type": "deadlift", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 50, "strength_value": 1.86, "lower_bound": 1.85, "upper_bound": 1.86},
    {"lift_type": "deadlift", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 40, "strength_value": 1.76, "lower_bound": 1.75, "upper_bound": 1.76},
    {"lift_type": "deadlift", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 30, "strength_value": 1.64, "lower_bound": 1.63, "upper_bound": 1.64},
    {"lift_type": "deadlift", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 20, "strength_value": 1.50, "lower_bound": 1.49, "upper_bound": 1.50},
    {"lift_type": "deadlift", "sex": "female", "age_category": "36-59", "weight_class": "all", "percentile": 10, "strength_value": 1.32, "lower_bound": 1.31, "upper_bound": 1.32},

    # Deadlift (Female, Age 60–79)
    {"lift_type": "deadlift", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 90, "strength_value": 2.19, "lower_bound": 2.17, "upper_bound": 2.20},
    {"lift_type": "deadlift", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 80, "strength_value": 1.97, "lower_bound": 1.97, "upper_bound": 2.00},
    {"lift_type": "deadlift", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 70, "strength_value": 1.85, "lower_bound": 1.82, "upper_bound": 1.86},
    {"lift_type": "deadlift", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 60, "strength_value": 1.71, "lower_bound": 1.70, "upper_bound": 1.72},
    {"lift_type": "deadlift", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 50, "strength_value": 1.60, "lower_bound": 1.59, "upper_bound": 1.61},
    {"lift_type": "deadlift", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 40, "strength_value": 1.48, "lower_bound": 1.47, "upper_bound": 1.51},
    {"lift_type": "deadlift", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 30, "strength_value": 1.37, "lower_bound": 1.34, "upper_bound": 1.40},
    {"lift_type": "deadlift", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 20, "strength_value": 1.27, "lower_bound": 1.26, "upper_bound": 1.28},
    {"lift_type": "deadlift", "sex": "female", "age_category": "60-79", "weight_class": "all", "percentile": 10, "strength_value": 1.11, "lower_bound": 1.09, "upper_bound": 1.13},

    # Deadlift (Female, Age 80+)
    {"lift_type": "deadlift", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 90, "strength_value": 1.68, "lower_bound": 1.63, "upper_bound": 1.73},
    {"lift_type": "deadlift", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 80, "strength_value": 1.61, "lower_bound": 1.49, "upper_bound": 1.66},
    {"lift_type": "deadlift", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 70, "strength_value": 1.47, "lower_bound": 1.28, "upper_bound": 1.58},
    {"lift_type": "deadlift", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 60, "strength_value": 1.28, "lower_bound": 1.16, "upper_bound": 1.45},
    {"lift_type": "deadlift", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 50, "strength_value": 1.11, "lower_bound": 0.97, "upper_bound": 1.28},
    {"lift_type": "deadlift", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 40, "strength_value": 0.97, "lower_bound": 0.85, "upper_bound": 1.16},
    {"lift_type": "deadlift", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 30, "strength_value": 0.70, "lower_bound": 0.62, "upper_bound": 0.82},
    {"lift_type": "deadlift", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 20, "strength_value": 0.61, "lower_bound": 0.55, "upper_bound": 0.67},
    {"lift_type": "deadlift", "sex": "female", "age_category": "80+", "weight_class": "all", "percentile": 10, "strength_value": 0.31, "lower_bound": 0.08, "upper_bound": 0.43},
    
    # Deadlift (Male, Age 12–17)
    {"lift_type": "deadlift", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 90, "strength_value": 2.90, "lower_bound": 2.89, "upper_bound": 2.90},
    {"lift_type": "deadlift", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 80, "strength_value": 2.69, "lower_bound": 2.68, "upper_bound": 2.69},
    {"lift_type": "deadlift", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 70, "strength_value": 2.53, "lower_bound": 2.53, "upper_bound": 2.54},
    {"lift_type": "deadlift", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 60, "strength_value": 2.41, "lower_bound": 2.40, "upper_bound": 2.41},
    {"lift_type": "deadlift", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 50, "strength_value": 2.28, "lower_bound": 2.27, "upper_bound": 2.28},
    {"lift_type": "deadlift", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 40, "strength_value": 2.15, "lower_bound": 2.14, "upper_bound": 2.15},
    {"lift_type": "deadlift", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 30, "strength_value": 2.01, "lower_bound": 2.01, "upper_bound": 2.02},
    {"lift_type": "deadlift", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 20, "strength_value": 1.85, "lower_bound": 1.84, "upper_bound": 1.85},
    {"lift_type": "deadlift", "sex": "male", "age_category": "12-17", "weight_class": "all", "percentile": 10, "strength_value": 1.61, "lower_bound": 1.61, "upper_bound": 1.62},

    # Deadlift (Male, Age 18–35)
    {"lift_type": "deadlift", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 90, "strength_value": 3.25, "lower_bound": 3.25, "upper_bound": 3.25},
    {"lift_type": "deadlift", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 80, "strength_value": 3.03, "lower_bound": 3.03, "upper_bound": 3.03},
    {"lift_type": "deadlift", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 70, "strength_value": 2.87, "lower_bound": 2.87, "upper_bound": 2.87},
    {"lift_type": "deadlift", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 60, "strength_value": 2.75, "lower_bound": 2.74, "upper_bound": 2.75},
    {"lift_type": "deadlift", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 50, "strength_value": 2.63, "lower_bound": 2.62, "upper_bound": 2.63},
    {"lift_type": "deadlift", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 40, "strength_value": 2.51, "lower_bound": 2.51, "upper_bound": 2.51},
    {"lift_type": "deadlift", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 30, "strength_value": 2.38, "lower_bound": 2.38, "upper_bound": 2.39},
    {"lift_type": "deadlift", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 20, "strength_value": 2.24, "lower_bound": 2.23, "upper_bound": 2.24},
    {"lift_type": "deadlift", "sex": "male", "age_category": "18-35", "weight_class": "all", "percentile": 10, "strength_value": 2.03, "lower_bound": 2.02, "upper_bound": 2.03},
    
    # Deadlift (Male, Age 36–59)
    {"lift_type": "deadlift", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 90, "strength_value": 2.98, "lower_bound": 2.97, "upper_bound": 2.99},
    {"lift_type": "deadlift", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 80, "strength_value": 2.75, "lower_bound": 2.74, "upper_bound": 2.75},
    {"lift_type": "deadlift", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 70, "strength_value": 2.59, "lower_bound": 2.58, "upper_bound": 2.59},
    {"lift_type": "deadlift", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 60, "strength_value": 2.46, "lower_bound": 2.46, "upper_bound": 2.47},
    {"lift_type": "deadlift", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 50, "strength_value": 2.34, "lower_bound": 2.33, "upper_bound": 2.34},
    {"lift_type": "deadlift", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 40, "strength_value": 2.22, "lower_bound": 2.21, "upper_bound": 2.22},
    {"lift_type": "deadlift", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 30, "strength_value": 2.08, "lower_bound": 2.07, "upper_bound": 2.09},
    {"lift_type": "deadlift", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 20, "strength_value": 1.95, "lower_bound": 1.94, "upper_bound": 1.95},
    {"lift_type": "deadlift", "sex": "male", "age_category": "36-59", "weight_class": "all", "percentile": 10, "strength_value": 1.75, "lower_bound": 1.74, "upper_bound": 1.75},

    # Deadlift (Male, Age 60–79)
    {"lift_type": "deadlift", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 90, "strength_value": 2.64, "lower_bound": 2.63, "upper_bound": 2.65},
    {"lift_type": "deadlift", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 80, "strength_value": 2.44, "lower_bound": 2.42, "upper_bound": 2.44},
    {"lift_type": "deadlift", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 70, "strength_value": 2.26, "lower_bound": 2.25, "upper_bound": 2.28},
    {"lift_type": "deadlift", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 60, "strength_value": 2.14, "lower_bound": 2.13, "upper_bound": 2.15},
    {"lift_type": "deadlift", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 50, "strength_value": 2.00, "lower_bound": 2.00, "upper_bound": 2.03},
    {"lift_type": "deadlift", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 40, "strength_value": 1.89, "lower_bound": 1.87, "upper_bound": 1.90},
    {"lift_type": "deadlift", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 30, "strength_value": 1.75, "lower_bound": 1.74, "upper_bound": 1.76},
    {"lift_type": "deadlift", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 20, "strength_value": 1.61, "lower_bound": 1.60, "upper_bound": 1.62},
    {"lift_type": "deadlift", "sex": "male", "age_category": "60-79", "weight_class": "all", "percentile": 10, "strength_value": 1.42, "lower_bound": 1.41, "upper_bound": 1.44},

    # Deadlift (Male, Age 80+)
    {"lift_type": "deadlift", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 90, "strength_value": 2.30, "lower_bound": 2.24, "upper_bound": 2.39},
    {"lift_type": "deadlift", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 80, "strength_value": 2.07, "lower_bound": 1.99, "upper_bound": 2.14},
    {"lift_type": "deadlift", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 70, "strength_value": 1.81, "lower_bound": 1.73, "upper_bound": 1.93},
    {"lift_type": "deadlift", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 60, "strength_value": 1.63, "lower_bound": 1.57, "upper_bound": 1.69},
    {"lift_type": "deadlift", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 50, "strength_value": 1.42, "lower_bound": 1.36, "upper_bound": 1.45},
    {"lift_type": "deadlift", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 40, "strength_value": 1.24, "lower_bound": 1.19, "upper_bound": 1.34},
    {"lift_type": "deadlift", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 30, "strength_value": 1.12, "lower_bound": 1.09, "upper_bound": 1.17},
    {"lift_type": "deadlift", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 20, "strength_value": 0.96, "lower_bound": 0.93, "upper_bound": 1.03},
    {"lift_type": "deadlift", "sex": "male", "age_category": "80+", "weight_class": "all", "percentile": 10, "strength_value": 0.93, "lower_bound": 0.90, "upper_bound": 0.96}
]

female_data_weight = [
        # Squat (Female, 43 kg)
    {"lift_type": "squat", "sex": "female", "weight_class": "43 kg", "percentile": 10, "strength_value": 1.00, "lower_bound": 0.95, "upper_bound": 1.03},
    {"lift_type": "squat", "sex": "female", "weight_class": "43 kg", "percentile": 20, "strength_value": 1.13, "lower_bound": 1.11, "upper_bound": 1.16},
    {"lift_type": "squat", "sex": "female", "weight_class": "43 kg", "percentile": 30, "strength_value": 1.23, "lower_bound": 1.18, "upper_bound": 1.26},
    {"lift_type": "squat", "sex": "female", "weight_class": "43 kg", "percentile": 40, "strength_value": 1.33, "lower_bound": 1.29, "upper_bound": 1.36},
    {"lift_type": "squat", "sex": "female", "weight_class": "43 kg", "percentile": 50, "strength_value": 1.43, "lower_bound": 1.38, "upper_bound": 1.46},
    {"lift_type": "squat", "sex": "female", "weight_class": "43 kg", "percentile": 60, "strength_value": 1.53, "lower_bound": 1.51, "upper_bound": 1.56},
    {"lift_type": "squat", "sex": "female", "weight_class": "43 kg", "percentile": 70, "strength_value": 1.64, "lower_bound": 1.61, "upper_bound": 1.69},
    {"lift_type": "squat", "sex": "female", "weight_class": "43 kg", "percentile": 80, "strength_value": 1.76, "lower_bound": 1.74, "upper_bound": 1.81},
    {"lift_type": "squat", "sex": "female", "weight_class": "43 kg", "percentile": 90, "strength_value": 2.01, "lower_bound": 1.94, "upper_bound": 2.05},

    # Bench Press (Female, 43 kg)
    {"lift_type": "bench_press", "sex": "female", "weight_class": "43 kg", "percentile": 10, "strength_value": 0.63, "lower_bound": 0.62, "upper_bound": 0.65},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "43 kg", "percentile": 20, "strength_value": 0.70, "lower_bound": 0.69, "upper_bound": 0.71},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "43 kg", "percentile": 30, "strength_value": 0.76, "lower_bound": 0.74, "upper_bound": 0.77},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "43 kg", "percentile": 40, "strength_value": 0.82, "lower_bound": 0.80, "upper_bound": 0.83},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "43 kg", "percentile": 50, "strength_value": 0.87, "lower_bound": 0.83, "upper_bound": 0.90},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "43 kg", "percentile": 60, "strength_value": 0.93, "lower_bound": 0.92, "upper_bound": 0.95},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "43 kg", "percentile": 70, "strength_value": 1.00, "lower_bound": 0.96, "upper_bound": 1.02},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "43 kg", "percentile": 80, "strength_value": 1.11, "lower_bound": 1.07, "upper_bound": 1.14},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "43 kg", "percentile": 90, "strength_value": 1.25, "lower_bound": 1.22, "upper_bound": 1.29},

    # Deadlift (Female, 43 kg)
    {"lift_type": "deadlift", "sex": "female", "weight_class": "43 kg", "percentile": 10, "strength_value": 1.30, "lower_bound": 1.25, "upper_bound": 1.33},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "43 kg", "percentile": 20, "strength_value": 1.65, "lower_bound": 1.48, "upper_bound": 1.56},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "43 kg", "percentile": 30, "strength_value": 1.78, "lower_bound": 1.74, "upper_bound": 1.81},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "43 kg", "percentile": 40, "strength_value": 1.88, "lower_bound": 1.82, "upper_bound": 1.92},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "43 kg", "percentile": 50, "strength_value": 1.98, "lower_bound": 1.92, "upper_bound": 2.00},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "43 kg", "percentile": 60, "strength_value": 2.09, "lower_bound": 2.04, "upper_bound": 2.13},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "43 kg", "percentile": 70, "strength_value": 2.24, "lower_bound": 2.21, "upper_bound": 2.28},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "43 kg", "percentile": 80, "strength_value": 2.48, "lower_bound": 2.41, "upper_bound": 2.54},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "43 kg", "percentile": 90, "strength_value": 2.83, "lower_bound": 2.62, "upper_bound": 2.90},
    
    # Squat (Female, 47 kg)
    {"lift_type": "squat", "sex": "female", "weight_class": "47 kg", "percentile": 10, "strength_value": 1.20, "lower_bound": 1.15, "upper_bound": 1.24},
    {"lift_type": "squat", "sex": "female", "weight_class": "47 kg", "percentile": 20, "strength_value": 1.40, "lower_bound": 1.39, "upper_bound": 1.42},
    {"lift_type": "squat", "sex": "female", "weight_class": "47 kg", "percentile": 30, "strength_value": 1.67, "lower_bound": 1.66, "upper_bound": 1.68},
    {"lift_type": "squat", "sex": "female", "weight_class": "47 kg", "percentile": 40, "strength_value": 1.81, "lower_bound": 1.80, "upper_bound": 1.83},
    {"lift_type": "squat", "sex": "female", "weight_class": "47 kg", "percentile": 50, "strength_value": 1.92, "lower_bound": 1.91, "upper_bound": 1.93},
    {"lift_type": "squat", "sex": "female", "weight_class": "47 kg", "percentile": 60, "strength_value": 2.05, "lower_bound": 2.03, "upper_bound": 2.06},
    {"lift_type": "squat", "sex": "female", "weight_class": "47 kg", "percentile": 70, "strength_value": 2.19, "lower_bound": 2.18, "upper_bound": 2.21},
    {"lift_type": "squat", "sex": "female", "weight_class": "47 kg", "percentile": 80, "strength_value": 2.40, "lower_bound": 2.37, "upper_bound": 2.42},

    # Bench Press (Female, 47 kg)
    {"lift_type": "bench_press", "sex": "female", "weight_class": "47 kg", "percentile": 10, "strength_value": 0.74, "lower_bound": 0.72, "upper_bound": 0.75},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "47 kg", "percentile": 20, "strength_value": 0.83, "lower_bound": 0.82, "upper_bound": 0.85},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "47 kg", "percentile": 30, "strength_value": 0.93, "lower_bound": 0.92, "upper_bound": 0.94},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "47 kg", "percentile": 40, "strength_value": 1.00, "lower_bound": 0.98, "upper_bound": 1.02},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "47 kg", "percentile": 50, "strength_value": 1.14, "lower_bound": 1.13, "upper_bound": 1.16},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "47 kg", "percentile": 60, "strength_value": 1.25, "lower_bound": 1.23, "upper_bound": 1.27},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "47 kg", "percentile": 70, "strength_value": 1.35, "lower_bound": 1.34, "upper_bound": 1.38},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "47 kg", "percentile": 80, "strength_value": 1.42, "lower_bound": 1.41, "upper_bound": 1.44},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "47 kg", "percentile": 90, "strength_value": 1.58, "lower_bound": 1.56, "upper_bound": 1.60},

    # Deadlift (Female, 47 kg)
    {"lift_type": "deadlift", "sex": "female", "weight_class": "47 kg", "percentile": 10, "strength_value": 1.68, "lower_bound": 1.62, "upper_bound": 1.70},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "47 kg", "percentile": 20, "strength_value": 1.86, "lower_bound": 1.84, "upper_bound": 1.88},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "47 kg", "percentile": 30, "strength_value": 2.05, "lower_bound": 2.04, "upper_bound": 2.06},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "47 kg", "percentile": 40, "strength_value": 2.16, "lower_bound": 2.15, "upper_bound": 2.17},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "47 kg", "percentile": 50, "strength_value": 2.29, "lower_bound": 2.27, "upper_bound": 2.31},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "47 kg", "percentile": 60, "strength_value": 2.42, "lower_bound": 2.40, "upper_bound": 2.44},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "47 kg", "percentile": 70, "strength_value": 2.56, "lower_bound": 2.54, "upper_bound": 2.57},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "47 kg", "percentile": 80, "strength_value": 2.72, "lower_bound": 2.71, "upper_bound": 2.74},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "47 kg", "percentile": 90, "strength_value": 2.96, "lower_bound": 2.93, "upper_bound": 2.98},
    
    # Squat (Female, 52 kg)
    {"lift_type": "squat", "sex": "female", "weight_class": "52 kg", "percentile": 10, "strength_value": 1.27, "lower_bound": 1.26, "upper_bound": 1.28},
    {"lift_type": "squat", "sex": "female", "weight_class": "52 kg", "percentile": 20, "strength_value": 1.45, "lower_bound": 1.44, "upper_bound": 1.46},
    {"lift_type": "squat", "sex": "female", "weight_class": "52 kg", "percentile": 30, "strength_value": 1.59, "lower_bound": 1.58, "upper_bound": 1.59},
    {"lift_type": "squat", "sex": "female", "weight_class": "52 kg", "percentile": 40, "strength_value": 1.80, "lower_bound": 1.79, "upper_bound": 1.81},
    {"lift_type": "squat", "sex": "female", "weight_class": "52 kg", "percentile": 50, "strength_value": 1.93, "lower_bound": 1.91, "upper_bound": 1.94},
    {"lift_type": "squat", "sex": "female", "weight_class": "52 kg", "percentile": 60, "strength_value": 2.04, "lower_bound": 2.02, "upper_bound": 2.05},
    {"lift_type": "squat", "sex": "female", "weight_class": "52 kg", "percentile": 70, "strength_value": 2.18, "lower_bound": 2.17, "upper_bound": 2.19},
    {"lift_type": "squat", "sex": "female", "weight_class": "52 kg", "percentile": 80, "strength_value": 2.39, "lower_bound": 2.37, "upper_bound": 2.40},

    # Bench Press (Female, 52 kg)
    {"lift_type": "bench_press", "sex": "female", "weight_class": "52 kg", "percentile": 10, "strength_value": 0.74, "lower_bound": 0.74, "upper_bound": 0.74},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "52 kg", "percentile": 20, "strength_value": 0.83, "lower_bound": 0.83, "upper_bound": 0.84},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "52 kg", "percentile": 30, "strength_value": 0.91, "lower_bound": 0.91, "upper_bound": 0.92},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "52 kg", "percentile": 40, "strength_value": 1.04, "lower_bound": 1.03, "upper_bound": 1.04},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "52 kg", "percentile": 50, "strength_value": 1.14, "lower_bound": 1.11, "upper_bound": 1.14},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "52 kg", "percentile": 60, "strength_value": 1.19, "lower_bound": 1.18, "upper_bound": 1.20},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "52 kg", "percentile": 70, "strength_value": 1.28, "lower_bound": 1.28, "upper_bound": 1.30},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "52 kg", "percentile": 80, "strength_value": 1.45, "lower_bound": 1.44, "upper_bound": 1.46},

    # Deadlift (Female, 52 kg)
    {"lift_type": "deadlift", "sex": "female", "weight_class": "52 kg", "percentile": 10, "strength_value": 1.66, "lower_bound": 1.64, "upper_bound": 1.67},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "52 kg", "percentile": 20, "strength_value": 1.86, "lower_bound": 1.85, "upper_bound": 1.86},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "52 kg", "percentile": 30, "strength_value": 2.00, "lower_bound": 1.99, "upper_bound": 2.01},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "52 kg", "percentile": 40, "strength_value": 2.13, "lower_bound": 2.12, "upper_bound": 2.14},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "52 kg", "percentile": 50, "strength_value": 2.25, "lower_bound": 2.24, "upper_bound": 2.25},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "52 kg", "percentile": 60, "strength_value": 2.36, "lower_bound": 2.35, "upper_bound": 2.37},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "52 kg", "percentile": 70, "strength_value": 2.49, "lower_bound": 2.49, "upper_bound": 2.52},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "52 kg", "percentile": 80, "strength_value": 2.65, "lower_bound": 2.64, "upper_bound": 2.66},
    
    # Squat (Female, 57 kg)
    {"lift_type": "squat", "sex": "female", "weight_class": "57 kg", "percentile": 10, "strength_value": 1.26, "lower_bound": 1.25, "upper_bound": 1.27},
    {"lift_type": "squat", "sex": "female", "weight_class": "57 kg", "percentile": 20, "strength_value": 1.44, "lower_bound": 1.43, "upper_bound": 1.46},
    {"lift_type": "squat", "sex": "female", "weight_class": "57 kg", "percentile": 30, "strength_value": 1.57, "lower_bound": 1.56, "upper_bound": 1.58},
    {"lift_type": "squat", "sex": "female", "weight_class": "57 kg", "percentile": 40, "strength_value": 1.78, "lower_bound": 1.78, "upper_bound": 1.79},
    {"lift_type": "squat", "sex": "female", "weight_class": "57 kg", "percentile": 50, "strength_value": 1.99, "lower_bound": 1.99, "upper_bound": 2.00},
    {"lift_type": "squat", "sex": "female", "weight_class": "57 kg", "percentile": 60, "strength_value": 2.13, "lower_bound": 2.12, "upper_bound": 2.14},
    {"lift_type": "squat", "sex": "female", "weight_class": "57 kg", "percentile": 70, "strength_value": 2.32, "lower_bound": 2.31, "upper_bound": 2.33},

    # Bench Press (Female, 57 kg)
    {"lift_type": "bench_press", "sex": "female", "weight_class": "57 kg", "percentile": 10, "strength_value": 0.72, "lower_bound": 0.72, "upper_bound": 0.73},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "57 kg", "percentile": 20, "strength_value": 0.83, "lower_bound": 0.82, "upper_bound": 0.85},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "57 kg", "percentile": 30, "strength_value": 0.89, "lower_bound": 0.89, "upper_bound": 0.90},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "57 kg", "percentile": 40, "strength_value": 1.02, "lower_bound": 1.01, "upper_bound": 1.02},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "57 kg", "percentile": 50, "strength_value": 1.15, "lower_bound": 1.15, "upper_bound": 1.16},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "57 kg", "percentile": 60, "strength_value": 1.24, "lower_bound": 1.23, "upper_bound": 1.25},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "57 kg", "percentile": 70, "strength_value": 1.40, "lower_bound": 1.39, "upper_bound": 1.41},

    # Deadlift (Female, 57 kg)
    {"lift_type": "deadlift", "sex": "female", "weight_class": "57 kg", "percentile": 10, "strength_value": 1.64, "lower_bound": 1.63, "upper_bound": 1.65},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "57 kg", "percentile": 20, "strength_value": 1.97, "lower_bound": 1.96, "upper_bound": 1.97},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "57 kg", "percentile": 30, "strength_value": 2.20, "lower_bound": 2.19, "upper_bound": 2.21},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "57 kg", "percentile": 40, "strength_value": 2.31, "lower_bound": 2.31, "upper_bound": 2.32},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "57 kg", "percentile": 50, "strength_value": 2.44, "lower_bound": 2.44, "upper_bound": 2.45},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "57 kg", "percentile": 60, "strength_value": 2.58, "lower_bound": 2.57, "upper_bound": 2.59},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "57 kg", "percentile": 70, "strength_value": 2.77, "lower_bound": 2.76, "upper_bound": 2.78},
    
    # Squat (Female, 63 kg)
    {"lift_type": "squat", "sex": "female", "weight_class": "63 kg", "percentile": 10, "strength_value": 1.22, "lower_bound": 1.22, "upper_bound": 1.23},
    {"lift_type": "squat", "sex": "female", "weight_class": "63 kg", "percentile": 20, "strength_value": 1.40, "lower_bound": 1.39, "upper_bound": 1.40},
    {"lift_type": "squat", "sex": "female", "weight_class": "63 kg", "percentile": 30, "strength_value": 1.52, "lower_bound": 1.52, "upper_bound": 1.52},
    {"lift_type": "squat", "sex": "female", "weight_class": "63 kg", "percentile": 40, "strength_value": 1.73, "lower_bound": 1.72, "upper_bound": 1.73},
    {"lift_type": "squat", "sex": "female", "weight_class": "63 kg", "percentile": 50, "strength_value": 1.83, "lower_bound": 1.83, "upper_bound": 1.84},
    {"lift_type": "squat", "sex": "female", "weight_class": "63 kg", "percentile": 60, "strength_value": 1.93, "lower_bound": 1.92, "upper_bound": 1.94},
    {"lift_type": "squat", "sex": "female", "weight_class": "63 kg", "percentile": 70, "strength_value": 2.07, "lower_bound": 2.06, "upper_bound": 2.07},
    {"lift_type": "squat", "sex": "female", "weight_class": "63 kg", "percentile": 80, "strength_value": 2.24, "lower_bound": 2.23, "upper_bound": 2.24},

    # Bench Press (Female, 63 kg)
    {"lift_type": "bench_press", "sex": "female", "weight_class": "63 kg", "percentile": 10, "strength_value": 0.70, "lower_bound": 0.69, "upper_bound": 0.70},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "63 kg", "percentile": 20, "strength_value": 0.86, "lower_bound": 0.85, "upper_bound": 0.86},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "63 kg", "percentile": 30, "strength_value": 0.92, "lower_bound": 0.92, "upper_bound": 0.92},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "63 kg", "percentile": 40, "strength_value": 1.02, "lower_bound": 1.01, "upper_bound": 1.02},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "63 kg", "percentile": 50, "strength_value": 1.09, "lower_bound": 1.08, "upper_bound": 1.09},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "63 kg", "percentile": 60, "strength_value": 1.20, "lower_bound": 1.20, "upper_bound": 1.20},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "63 kg", "percentile": 70, "strength_value": 1.33, "lower_bound": 1.32, "upper_bound": 1.33},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "63 kg", "percentile": 80, "strength_value": 1.58, "lower_bound": 1.58, "upper_bound": 1.60},

    # Deadlift (Female, 63 kg)
    {"lift_type": "deadlift", "sex": "female", "weight_class": "63 kg", "percentile": 10, "strength_value": 1.59, "lower_bound": 1.58, "upper_bound": 1.60},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "63 kg", "percentile": 20, "strength_value": 1.86, "lower_bound": 1.85, "upper_bound": 1.87},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "63 kg", "percentile": 30, "strength_value": 2.00, "lower_bound": 2.00, "upper_bound": 2.01},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "63 kg", "percentile": 40, "strength_value": 2.22, "lower_bound": 2.21, "upper_bound": 2.23},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "63 kg", "percentile": 50, "strength_value": 2.35, "lower_bound": 2.34, "upper_bound": 2.35},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "63 kg", "percentile": 60, "strength_value": 2.46, "lower_bound": 2.45, "upper_bound": 2.47},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "63 kg", "percentile": 70, "strength_value": 2.65, "lower_bound": 2.64, "upper_bound": 2.65},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "63 kg", "percentile": 80, "strength_value": 2.98, "lower_bound": 2.93, "upper_bound": 2.98},
    
    # Squat (Female, 69 kg)
    {"lift_type": "squat", "sex": "female", "weight_class": "69 kg", "percentile": 10, "strength_value": 1.18, "lower_bound": 1.17, "upper_bound": 1.18},
    {"lift_type": "squat", "sex": "female", "weight_class": "69 kg", "percentile": 20, "strength_value": 1.35, "lower_bound": 1.34, "upper_bound": 1.36},
    {"lift_type": "squat", "sex": "female", "weight_class": "69 kg", "percentile": 30, "strength_value": 1.47, "lower_bound": 1.46, "upper_bound": 1.48},
    {"lift_type": "squat", "sex": "female", "weight_class": "69 kg", "percentile": 40, "strength_value": 1.67, "lower_bound": 1.66, "upper_bound": 1.67},
    {"lift_type": "squat", "sex": "female", "weight_class": "69 kg", "percentile": 50, "strength_value": 1.76, "lower_bound": 1.75, "upper_bound": 1.76},
    {"lift_type": "squat", "sex": "female", "weight_class": "69 kg", "percentile": 60, "strength_value": 1.86, "lower_bound": 1.85, "upper_bound": 1.86},
    {"lift_type": "squat", "sex": "female", "weight_class": "69 kg", "percentile": 70, "strength_value": 1.98, "lower_bound": 1.97, "upper_bound": 1.99},
    {"lift_type": "squat", "sex": "female", "weight_class": "69 kg", "percentile": 80, "strength_value": 2.16, "lower_bound": 2.15, "upper_bound": 2.17},

    # Deadlift (Female, 69 kg)
    {"lift_type": "deadlift", "sex": "female", "weight_class": "69 kg", "percentile": 10, "strength_value": 1.52, "lower_bound": 1.51, "upper_bound": 1.52},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "69 kg", "percentile": 20, "strength_value": 1.76, "lower_bound": 1.75, "upper_bound": 1.76},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "69 kg", "percentile": 30, "strength_value": 2.01, "lower_bound": 2.00, "upper_bound": 2.02},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "69 kg", "percentile": 40, "strength_value": 2.20, "lower_bound": 2.19, "upper_bound": 2.21},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "69 kg", "percentile": 50, "strength_value": 2.42, "lower_bound": 2.41, "upper_bound": 2.43},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "69 kg", "percentile": 60, "strength_value": 2.58, "lower_bound": 2.57, "upper_bound": 2.59},
    {"lift_type": "deadlift", "sex": "female", "weight_class": "69 kg", "percentile": 70, "strength_value": 2.77, "lower_bound": 2.76, "upper_bound": 2.78},
    
    # Squat (Female, 76 kg)
    {"lift_type": "squat", "sex": "female", "weight_class": "76 kg", "percentile": 10, "strength_value": 1.15, "lower_bound": 1.15, "upper_bound": 1.16},
    {"lift_type": "squat", "sex": "female", "weight_class": "76 kg", "percentile": 20, "strength_value": 1.32, "lower_bound": 1.31, "upper_bound": 1.32},
    {"lift_type": "squat", "sex": "female", "weight_class": "76 kg", "percentile": 30, "strength_value": 1.43, "lower_bound": 1.42, "upper_bound": 1.43},
    {"lift_type": "squat", "sex": "female", "weight_class": "76 kg", "percentile": 40, "strength_value": 1.62, "lower_bound": 1.61, "upper_bound": 1.62},
    {"lift_type": "squat", "sex": "female", "weight_class": "76 kg", "percentile": 50, "strength_value": 1.71, "lower_bound": 1.72, "upper_bound": 1.72},
    {"lift_type": "squat", "sex": "female", "weight_class": "76 kg", "percentile": 60, "strength_value": 1.82, "lower_bound": 1.81, "upper_bound": 1.83},
    {"lift_type": "squat", "sex": "female", "weight_class": "76 kg", "percentile": 70, "strength_value": 1.94, "lower_bound": 1.93, "upper_bound": 1.94},
    {"lift_type": "squat", "sex": "female", "weight_class": "76 kg", "percentile": 80, "strength_value": 2.11, "lower_bound": 2.10, "upper_bound": 2.12},
    
    # Bench Press (Female, 76 kg)
    {"lift_type": "bench_press", "sex": "female", "weight_class": "76 kg", "percentile": 10, "strength_value": 0.64, "lower_bound": 0.64, "upper_bound": 0.65},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "76 kg", "percentile": 20, "strength_value": 0.73, "lower_bound": 0.72, "upper_bound": 0.73},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "76 kg", "percentile": 30, "strength_value": 0.85, "lower_bound": 0.84, "upper_bound": 0.85},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "76 kg", "percentile": 40, "strength_value": 0.90, "lower_bound": 0.90, "upper_bound": 0.90},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "76 kg", "percentile": 50, "strength_value": 1.03, "lower_bound": 1.02, "upper_bound": 1.03},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "76 kg", "percentile": 60, "strength_value": 1.11, "lower_bound": 1.11, "upper_bound": 1.12},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "76 kg", "percentile": 70, "strength_value": 1.24, "lower_bound": 1.23, "upper_bound": 1.24},
    {"lift_type": "bench_press", "sex": "female", "weight_class": "76 kg", "percentile": 80, "strength_value": 1.41, "lower_bound": 1.40, "upper_bound": 1.42},
]


# Convert to a DataFrame
df = pd.DataFrame(data)

# Save to a CSV file
csv_file_path = '/mnt/data/strength_norms.csv'
df.to_csv(csv_file_path, index=False)

csv_file_path
