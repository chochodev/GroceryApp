from flask import Blueprint, render_template, flash, session
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'], endpoint='home')
def home():
    # Check if the user is authenticated
    if current_user.is_authenticated:
        # Check if the 'show_flash' flag is not present in the session
        if 'show_flash' not in session:
            # Display a flash message with the username
            flash(f'Logged in as user {current_user.username}')
            
            # Set the 'show_flash' flag in the session to True
            # So that the message flashes once on user logging in and redirected here
            session['show_flash'] = True
    
    # Render the home.html template
    return render_template('home.html', user=current_user, endpoint='home')

@views.route('/menu', methods=['GET', 'POST'], endpoint='menu')
def menu():
    
    return render_template('menu.html', user=current_user, endpoint='menu')

@views.route('/cart', methods=['GET', 'POST'], endpoint='cart')
@login_required
def cart():
    
    return render_template('cart.html', user=current_user, endpoint='cart')

@views.route('/allergy', methods=['GET', 'POST'], endpoint='allergy')
@login_required
def allergy():
    
    return render_template('allergy.html', user=current_user, endpoint='allergy')

@views.route('/aboutus', methods=['GET', 'POST'], endpoint='aboutus')
def aboutus():
    
    return render_template('aboutus.html', user=current_user, endpoint='aboutus')

@views.route('/privacy', methods=['GET', 'POST'], endpoint='privacy')
def privacy():
    
    return render_template('privacy.html', user=current_user, endpoint='privacy')
