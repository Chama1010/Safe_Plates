from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from my_extensions import db
from models.models import Preferences

# Blueprint for user dashboard and preference management
main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@main_bp.route('/preferences')
@login_required
def preferences():
    return render_template('preferences.html', user=current_user)

# Route to manage user's allergen preferences
@main_bp.route('/manage_allergens', methods=['GET', 'POST'])
@login_required
def manage_allergens():
    # Predefined list of common allergens
    allergen_list = ['Almond', 'Anchovy', 'Apple', 'Apricot', 'Avocado', 'Banana', 'Barley', 'Basil',
        'Beef', 'Bell pepper', 'Blueberry', 'Brazil nut', 'Broccoli', 'Buckwheat', 'Cabbage',
        'Carrot', 'Cashew', 'Cauliflower', 'Celery', 'Cheese', 'Chicken', 'Cilantro',
        'Clam', 'Coconut', 'Corn', 'Crab', 'Cranberry', 'Crustacean', 'Cucumber',
        'Dairy', 'Date', 'Duck', 'Egg', 'Fish', 'Garlic', 'Ginger', 'Gluten',
        'Grape', 'Green bean', 'Green pea', 'Halibut', 'Hazelnut', 'Honey', 'Kiwi', 'Lamb',
        'Lemon', 'Lentil', 'Lettuce', 'Lime', 'Lobster', 'Lupin', 'Macadamia', 'Milk',
        'Mollusc', 'Mushroom', 'Mustard', 'Nectarine', 'Oat', 'Octopus', 'Olive', 'Onion',
        'Orange', 'Papaya', 'Peach', 'Peanut', 'Pear', 'Pecan', 'Pine nut', 'Pineapple',
        'Pistachio', 'Pomegranate', 'Pork', 'Potato', 'Pumpkin', 'Radish', 'Raspberry',
        'Rice', 'Salmon', 'Scallop', 'Seaweed', 'Sesame', 'Shellfish', 'Shrimp',
        'Snap pea', 'Soy', 'Spinach', 'Squash', 'Strawberry', 'Sunflower seed',
        'Sweet potato', 'Tomato', 'Tree nut', 'Trout', 'Tuna', 'Turkey', 'Walnut', 'Watermelon',
        'Wheat', 'Yogurt', 'Zucchini']

    if request.method == 'POST':
        selected_allergens = request.form.getlist('allergens')

        # Remove existing allergen preferences
        Preferences.query.filter_by(UserId=current_user.UserId).delete()

        # Save newly selected allergens
        for allergen in selected_allergens:
            pref = Preferences(UserId=current_user.UserId, Allergen=allergen)
            db.session.add(pref)

        db.session.commit()
        flash('Your allergen preferences have been updated.', 'success')
        return redirect(url_for('main.dashboard'))  

    # Load previously saved allergens for the user
    user_allergens = [p.Allergen for p in Preferences.query.filter_by(UserId=current_user.UserId).all()]

    return render_template('manage_allergens.html', allergen_list=allergen_list, user_allergens=user_allergens, user=current_user)

@main_bp.route('/account')
@login_required
def account():
    preferences = Preferences.query.filter_by(UserId=current_user.UserId).all()
    return render_template('account.html', email=current_user.Email, username=current_user.Name, preferences=preferences)






