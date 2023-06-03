from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from app.models import User
from flask_login import current_user

from . import bp
from app.forms import RegisterForm, SigninForm

@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    # Check if the user is already authenticated and redirect to the home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # Create an instance of the SigninForm
    form = SigninForm()
    
    # Check if the form is submitted and valid
    if form.validate_on_submit():
        # Query the User table for a user with the entered username
        user = User.query.filter_by(username=form.username.data).first()
        
        # Check if the user exists and the entered password is correct
        if user and user.check_password(form.password.data):
            flash(f'{form.username.data} signed in', 'success')
            
            # Log in the user and redirect to the home page
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash(f'{form.username.data} user doesn\'t exist or incorrect password', 'warning')
    
    # Render the signin template with the form
    return render_template('signin.jinja', form=form, title='Drive Archive')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Check if the user is already authenticated and redirect to the home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # Create an instance of the RegisterForm
    form = RegisterForm()
    
    # Check if the form is submitted and valid
    if form.validate_on_submit():
        # Query the User table for a user with the entered username and email
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        
        # Check if the entered username and email are not already taken
        if not email and not user:
            # Create a new User object with the entered username and email
            u = User(username=form.username.data, email=form.email.data)
            
            # Hash the entered password and set it as the user's password
            u.password = u.hash_password(form.password.data)
            
            # Add a token to the user and commit the changes to the database
            u.add_token()
            u.commit()
            
            flash(f"{form.username.data} registered", "success")
            
            # Redirect to the home page
            return redirect(url_for("main.home"))
        
        # Display a flash message if the username or email is already taken
        if user:
            flash(f'{form.username.data} already taken, try again', "warning")
        else:
            flash(f'{form.email.data} already taken, try again', "warning")
    
    # Render the register template with the form
    return render_template('register.jinja', form=form, title='Drive Archive')

@bp.route('/logout')
@login_required
def logout():
    # Log out the current user and redirect to the home page
    logout_user()
    return redirect(url_for('main.home'))
