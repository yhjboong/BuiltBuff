from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from pathlib import Path

# Initialize Flask-SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    
    # Get the project root directory
    ROOT_DIR = Path(__file__).parent
    
    # Configure database
    db_path = os.path.join(ROOT_DIR, 'builtbuff.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    return app
