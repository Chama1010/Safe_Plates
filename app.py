from flask import Flask
from flask_login import LoginManager
from my_extensions import db
import os
from dotenv import load_dotenv
from flask_migrate import Migrate


# updated with the second code 
# load_dotenv()
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

def create_app():
    # app = Flask(__name__)
    app = Flask(__name__, template_folder='templates', static_folder='static')

    
    # Debug environment variables
    db_url = os.getenv('DATABASE_URL')
    secret_key = os.getenv('SECRET_KEY')
    print(f"DATABASE_URL: {'*' * (len(db_url) - 10) + db_url[-10:] if db_url else 'None'}")
    print(f"SECRET_KEY: {'*' * (len(secret_key) - 5) + secret_key[-5:] if secret_key else 'None'}")
    
    # Configure app
    if not secret_key:
        app.config['SECRET_KEY'] = 'dev-key-for-testing-only'
        print("WARNING: Using default SECRET_KEY!")
    else:
        app.config['SECRET_KEY'] = secret_key
    
    if not db_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
        print("WARNING: Using SQLite database fallback!")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)

    # Initialize migrate
    migrate = Migrate(app, db)
    
    # Setup login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from models.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Import blueprints
    from routes.recipe import recipe_bp
    from routes.auth import auth_bp
    from routes.main import main_bp  
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(recipe_bp)
    app.register_blueprint(main_bp)  
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    #remove this if db connect
    print("SQLAlchemy URI in use:", app.config['SQLALCHEMY_DATABASE_URI'])

    return app















