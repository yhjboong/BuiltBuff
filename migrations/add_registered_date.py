from datetime import datetime
from app import db
from models import User

def upgrade():
    # Add registered_date column
    with app.app_context():
        db.session.execute('ALTER TABLE user ADD COLUMN registered_date DATETIME')
        # Set default value for existing users
        db.session.execute(
            'UPDATE user SET registered_date = ? WHERE registered_date IS NULL',
            [datetime.utcnow()]
        )
        db.session.commit()

if __name__ == '__main__':
    upgrade() 