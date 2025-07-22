from flask import Flask, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize SQLAlchemy and Flask-Login
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Create the Flask application instance
    app = Flask(__name__)

    # Set secret key and database URI
    app.config['SECRET_KEY'] = 'my_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    # Initialize database and login manager with the app
    db.init_app(app)
    login_manager.init_app(app)

    # Set the route name for the login page
    login_manager.login_view = 'auth.login'

    # Disable default login message from Flask-Login
    login_manager.login_message = None

    # Import and register blueprints
    from .auth import auth_bp
    from .recipe import recipe_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(recipe_bp)

    return app
