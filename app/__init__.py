from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-here'

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///builtbuff.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'

    # Register routes blueprint
    from app.routes import routes  # Import blueprint
    app.register_blueprint(routes)

    # Import models and create tables
    with app.app_context():
        from app import models  # Lazy import to prevent circular imports
        db.create_all()

    print(app.config['SQLALCHEMY_DATABASE_URI'])
    
    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
