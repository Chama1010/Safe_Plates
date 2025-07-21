from my_extensions import db
from flask_login import UserMixin
from datetime import datetime
from flask_login import LoginManager
from my_extensions import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

# User model to store basic user information and relationships
class User(UserMixin, db.Model):
    __tablename__ = 'User'
    UserId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(150), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    RegistrationDate = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships to other tables
    preferences = db.relationship('Preferences', backref='user', lazy=True)
    search_history = db.relationship('SearchHistory', backref='user', lazy=True)
    ratings = db.relationship('RatingsFeedback', backref='user', lazy=True)

    # Method to set a hashed password
    def set_password(self, password):
        self.Password = generate_password_hash(password)

    # Method to check if the entered password is correct
    def check_password(self, password):
        return check_password_hash(self.Password, password)

    # Flask-Login requires a method to return the user ID
    def get_id(self):  
        return str(self.UserId)

# Load user from the database using user ID (required by Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Stores allergen and dietary preferences for a user
class Preferences(db.Model):
    __tablename__ = 'Preferences'
    PreferenceId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.UserId', ondelete='CASCADE'))
    Allergen = db.Column(db.String(100))
    DietaryPreference = db.Column(db.String(100))

# Stores recipes fetched from Edamam API
class Recipe(db.Model):
    __tablename__ = 'Recipe'
    RecipeId = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    Ingredients = db.Column(db.Text, nullable=False)
    CookingTime = db.Column(db.Integer)
    ImageUrl = db.Column(db.String(2048))
    RecipeUrl = db.Column(db.String(2048))

    # Relationships for recipe ratings and tags
    ratings = db.relationship('RatingsFeedback', backref='recipe', lazy=True)
    tags = db.relationship('RecipeTag', backref='recipe', lazy=True)

# Optional table to list known ingredients
class Ingredient(db.Model):
    __tablename__ = 'Ingredient'
    IngredientId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    IsAllergen = db.Column(db.Boolean, default=False)

# Tags for categorizing recipes (e.g., Vegan, Low-carb)
class Tags(db.Model):
    __tablename__ = 'Tags'
    TagId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)

# Association table for many-to-many relationship between Recipe and Tags
class RecipeTag(db.Model):
    __tablename__ = 'RecipeTag'
    RecipeId = db.Column(db.Integer, db.ForeignKey('Recipe.RecipeId', ondelete='CASCADE'), primary_key=True)
    TagId = db.Column(db.Integer, db.ForeignKey('Tags.TagId', ondelete='CASCADE'), primary_key=True)

# Stores user's search history with keywords and timestamp
class SearchHistory(db.Model):
    __tablename__ = 'SearchHistory'
    SearchId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.UserId', ondelete='CASCADE'))
    Keywords = db.Column(db.String(255), nullable=False)
    SearchDate = db.Column(db.DateTime, default=datetime.utcnow)

# Stores user ratings and feedback on recipes
class RatingsFeedback(db.Model):
    __tablename__ = 'RatingsFeedback'
    RatingId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.UserId', ondelete='SET NULL'))
    RecipeId = db.Column(db.Integer, db.ForeignKey('Recipe.RecipeId', ondelete='CASCADE'))
    Rating = db.Column(db.Integer)
    Comment = db.Column(db.Text)
    FeedbackDate = db.Column(db.DateTime, default=datetime.utcnow)

# Stores recipes saved by users
class SavedRecipe(db.Model):
    __tablename__ = 'SavedRecipe'
    SavedRecipeId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.UserId', ondelete='CASCADE'), nullable=False)
    RecipeId = db.Column(db.Integer, db.ForeignKey('Recipe.RecipeId', ondelete='CASCADE'), nullable=False)
    SavedDate = db.Column(db.DateTime, default=datetime.utcnow)

    # Establish relationships to User and Recipe
    user = db.relationship('User', backref=db.backref('saved_recipes', cascade='all, delete-orphan'))
    recipe = db.relationship('Recipe', backref=db.backref('saved_by_users', cascade='all, delete-orphan'))