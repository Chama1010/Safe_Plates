from flask import Flask
from flask_login import LoginManager
from my_extensions import db
import os
from dotenv import load_dotenv
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Load environment variables
    db_url = os.getenv('DATABASE_URL')
    secret_key = os.getenv('SECRET_KEY')
    
    # Print masked values for debugging
    print(f"DATABASE_URL: {'*' * (len(db_url) - 10) + db_url[-10:] if db_url else 'None'}")
    print(f"SECRET_KEY: {'*' * (len(secret_key) - 5) + secret_key[-5:] if secret_key else 'None'}")
    
    # Set Flask secret key
    if not secret_key:
        app.config['SECRET_KEY'] = 'dev-key-for-testing-only'
        print("WARNING: Using default SECRET_KEY!")
    else:
        app.config['SECRET_KEY'] = secret_key
    
    # Set database connection
    if not db_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
        print("WARNING: Using SQLite database fallback!")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database extension
    db.init_app(app)

    # Set up database migration tool
    migrate = Migrate(app, db)
    
    # Initialize Flask-Login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Redirect to login page if not logged in
    login_manager.init_app(app)
    
    # Load user from database (used by Flask-Login)
    from models.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Import blueprints
    from routes.recipe import recipe_bp
    from routes.auth import auth_bp
    from routes.main import main_bp  
    
    # Register blueprints to the app
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(recipe_bp)
    app.register_blueprint(main_bp)
    
    # Create all database tables
    with app.app_context():
        db.create_all()

    return app
