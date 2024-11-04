from app import app, db  # Import app and db from app.py

# Create tables within the app context
with app.app_context():
    db.drop_all()  # Drop all tables
    db.create_all()  # Recreate tables
    print("All tables dropped and recreated successfully.")