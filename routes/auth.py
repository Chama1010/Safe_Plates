from flask import Blueprint, render_template, redirect, url_for, flash, request
from my_extensions import db
from models.models import User, Preferences
from flask_login import login_user, logout_user, login_required, current_user
from forms import LoginForm, RegisterForm

# Blueprint for authentication-related routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect authenticated users to homepage
    if current_user.is_authenticated:
        return redirect(url_for('recipe.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower().strip()
        password = form.password.data

        # Check if email is already registered
        if User.query.filter_by(Email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('auth.register'))

        # Create and save new user
        user = User(Name=name, Email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect authenticated users to homepage
    if current_user.is_authenticated:
        return redirect(url_for('recipe.index'))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        password = form.password.data
        user = User.query.filter_by(Email=email).first()

        # Check credentials and login
        if user and user.check_password(password):
            login_user(user)

            # Redirect to allergen management if not set
            has_allergens = Preferences.query.filter_by(UserId=user.UserId).first()
            if not has_allergens:
                return redirect(url_for('main.manage_allergens'))

            return redirect(url_for('recipe.index'))

        flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    # Logout the user
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))
