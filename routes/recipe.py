import os
import requests
from dotenv import load_dotenv
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.models import Preferences, Recipe, Ingredient, SearchHistory, SavedRecipe
from my_extensions import db
from datetime import datetime
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables (e.g., API keys)
load_dotenv()
EDAMAM_APP_ID = os.getenv("EDAMAM_APP_ID")
EDAMAM_APP_KEY = os.getenv("EDAMAM_APP_KEY")

# Create the blueprint for recipe-related routes
recipe_bp = Blueprint('recipe', __name__)

# Route for searching and displaying recipes
@recipe_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    query = None
    recipes = []
    error = None

    if request.method == 'POST':
        query = request.form.get('query')
        if not query:
            error = "Please enter a search term."
        else:
            # Save user search to history
            try:
                db.session.add(SearchHistory(UserId=current_user.UserId, Keywords=query))
                db.session.commit()
            except Exception as e:
                logger.warning(f"SearchHistory save failed: {e}")
                db.session.rollback()

            # Prepare Edamam API request
            url = "https://api.edamam.com/search"
            params = {
                'q': query,
                'app_id': EDAMAM_APP_ID,
                'app_key': EDAMAM_APP_KEY,
                'from': 0,
                'to': 10
            }

            try:
                headers = {'User-Agent': 'AllergyFreeRecipeFinder/1.0'}
                response = requests.get(url, params=params, headers=headers, timeout=30)

                # Fallback to new API version if 404 error
                if response.status_code == 404:
                    url = "https://api.edamam.com/api/recipes/v2"
                    headers['Edamam-Account-User'] = 'b265e1fa'
                    params['type'] = 'public'
                    response = requests.get(url, params=params, headers=headers, timeout=30)

                # Parse API response
                data = response.json()
                hits = data.get('hits', [])

                if not hits:
                    error = f"No recipes found for '{query}'. Try another keyword."
                else:
                    # Load current user's allergens and saved recipes
                    user_allergens = [p.Allergen.lower() for p in Preferences.query.filter_by(UserId=current_user.UserId).all()]
                    saved_recipe_ids = {sr.RecipeId for sr in SavedRecipe.query.filter_by(UserId=current_user.UserId).all()}

                    for hit in hits:
                        recipe_data = hit.get('recipe', {})
                        title = recipe_data.get('label')
                        ingredients = recipe_data.get('ingredientLines', [])
                        ingredients_lower = [ing.lower() for ing in ingredients]

                        # Skip if any ingredient contains an allergen
                        if any(allergen in ing for allergen in user_allergens for ing in ingredients_lower):
                            continue

                        # Check if recipe already exists in DB
                        existing = Recipe.query.filter_by(Title=title).first()
                        if not existing:
                            # Create new recipe entry
                            new_recipe = Recipe(
                                Title=title,
                                Ingredients=', '.join(ingredients),
                                CookingTime=recipe_data.get('totalTime') or None,
                                ImageUrl=recipe_data.get('image'),
                                RecipeUrl=recipe_data.get('url')
                            )
                            db.session.add(new_recipe)
                            db.session.commit()

                            # Add new ingredients if not already present
                            for ing in ingredients:
                                ing_name = ing.strip().lower()
                                if len(ing_name) <= 100 and not Ingredient.query.filter_by(Name=ing_name).first():
                                    db.session.add(Ingredient(Name=ing_name))
                            db.session.commit()

                            recipe_id = new_recipe.RecipeId
                        else:
                            recipe_id = existing.RecipeId

                        # Check if user has already saved this recipe
                        is_saved = recipe_id in saved_recipe_ids

                        # Append recipe info for display
                        recipes.append({
                            'id': recipe_id,
                            'title': title,
                            'image_url': recipe_data.get('image'),
                            'cooking_time': recipe_data.get('totalTime') or 'Not specified',
                            'ingredients': ', '.join(ingredients),
                            'recipe_url': recipe_data.get('url'),
                            'is_saved': is_saved
                        })

                    # If no allergy-safe recipes were found
                    if not recipes:
                        error = f"No allergy-safe recipes found!! You are allergy for '{query}'."

            except requests.exceptions.RequestException as req_err:
                error = f"Request error: {req_err}"
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                error = "An unexpected error occurred."

    return render_template("index.html", recipes=recipes, query=query, error=error)

# Route to save or unsave a recipe using its ID
@recipe_bp.route('/recipes/save/<int:recipe_id>', methods=['POST'])
@login_required
def save_recipe_by_id(recipe_id):
    try:
        existing = SavedRecipe.query.filter_by(UserId=current_user.UserId, RecipeId=recipe_id).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
            return jsonify({'success': True, 'saved': False})
        else:
            db.session.add(SavedRecipe(UserId=current_user.UserId, RecipeId=recipe_id))
            db.session.commit()
            return jsonify({'success': True, 'saved': True})
    except Exception as e:
        logger.error(f"Error saving recipe: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Server error'}), 500

# Route to unsave a recipe directly
@recipe_bp.route('/unsave/<int:recipe_id>', methods=['POST'])
@login_required
def unsave_recipe(recipe_id):
    try:
        saved = SavedRecipe.query.filter_by(UserId=current_user.UserId, RecipeId=recipe_id).first()
        if saved:
            db.session.delete(saved)
            db.session.commit()
            return jsonify({'success': True})
        else:
            logger.warning(f"SavedRecipe not found: user={current_user.UserId}, recipe={recipe_id}")
            return jsonify({'success': False, 'message': 'Recipe not found'}), 404
    except Exception as e:
        logger.error(f"Error unsaving recipe: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Server error: {str(e)}'}), 500

# Route to view all saved recipes by the user
@recipe_bp.route('/saved')
@login_required
def saved_recipes():
    saved = (
        db.session.query(Recipe)
        .join(SavedRecipe, Recipe.RecipeId == SavedRecipe.RecipeId)
        .filter(SavedRecipe.UserId == current_user.UserId)
        .all()
    )
    return render_template("saved_recipes.html", recipes=saved)
