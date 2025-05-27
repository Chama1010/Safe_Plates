from flask import Flask, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)
    login_manager.init_app(app)

    # Set the login view route
    login_manager.login_view = 'auth.login'

    # Disable Flask-Login’s default flash message
    login_manager.login_message = None

    # Register blueprints
    from .auth import auth_bp
    from .recipe import recipe_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(recipe_bp)

    return app










