from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the db globally
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Set up the configuration for the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the db with the app
    db.init_app(app)

    # Import blueprints and models within the app context
    with app.app_context():
        from routes import heroes_bp
        from models import Hero, Power, HeroPower  # Import your models here to make sure they are registered with SQLAlchemy
        db.create_all()  # Create tables in the database
    
    # Register the blueprint
    app.register_blueprint(heroes_bp)

    return app
