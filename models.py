from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)

class WorkoutLog(db.Model):
    __tablename__ = 'workout_logs'
    workout_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    completed_at = db.Column(db.Date)
    intensity_level = db.Column(db.String(10))
    rest_time = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    exercise_name = db.Column(db.String(100))  
    equipment = db.Column(db.String(100))
    variation = db.Column(db.String(100))


class ExerciseCategory(db.Model):
    __tablename__ = 'exercise_categories'
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    muscle_group = db.Column(db.String(50))
    exercise_type = db.Column(db.String(50))

class PlannedWorkout(db.Model):
    __tablename__ = 'planned_workouts'
    workout_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    date = db.Column(db.Date)

class Exercise(db.Model):
    __tablename__ = 'exercises'
    exercise_id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout_logs.workout_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('exercise_categories.category_id'))
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

class ExerciseList(db.Model):
    __tablename__ = 'exercise_list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    equipment = db.Column(db.String(100), nullable=False)
    variation = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(500), nullable=True)

    __table_args__ = (
        db.UniqueConstraint('name', 'equipment', 'variation', name='unique_exercise_equipment_variation'),
    )

def generate_recommendation(user_id):
    user = User.query.get(user_id)
    similar_users = User.query.filter(
        User.age.between(user.age - 5, user.age + 5),
        User.weight.between(user.weight - 10, user.weight + 10),
        User.user_id != user.user_id
    ).all()
    
    similar_user_ids = [u.user_id for u in similar_users]
    
    # Get most common exercises for similar users
    recommended_exercises = db.session.query(
        Exercise.category_id, db.func.count(Exercise.category_id).label('popularity')
    ).filter(
        Exercise.user_id.in_(similar_user_ids)
    ).group_by(Exercise.category_id).order_by(db.desc('popularity')).limit(5).all()

    return recommended_exercises
