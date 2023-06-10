from flask import Flask, Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from .models import User
import bcrypt
from . import db, mail
from flask_login import login_required, login_user, logout_user, current_user
from flask_login import LoginManager
from datetime import timedelta


# Create Flask app instance
app = Flask(__name__)

# Initialize LoginManager
login_manager = LoginManager(app)

# Create auth Blueprint
auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'], endpoint='signup')
def signup():
    # Checks if request is POST
    if request.method == 'POST':
        if request.is_json:
            # Retrieves data from Postman payload
            data = request.get_json()
            name = data.get('name')
            username = data.get('username')
            email = data.get('email')
            gender = data.get('gender')
            password = data.get('password')
            return jsonify({'message': 'Post request was received successfully'})

        else:
            # Retrieves data from HTML form
            email = request.form.get('email')
            name = request.form.get('name')
            username = request.form.get('username')
            gender = request.form.get('gender')
            password = request.form.get('password')


        # Validation checks
        # Checks if user email exists
        if User.query.filter_by(email=email).first():
            flash(f'User with {email} already exist', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name or username) < 2:
            flash('Name and Username must be greater than 1 character.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Encrypts the password and saves it in a variable
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            # Saves user with the retrieved data to a variable
            new_user = User(email=email, name=name, username=username, gender=gender, password=hashed_password)
            # Adds the new user to the database
            db.session.add(new_user)
            db.session.commit()

            # Flashes success message and redirects to home page
            flash('Account created for ' + new_user.username, category='success')
            return redirect(url_for('views.home'))

    return render_template('auth.html')


@auth.route('/signin', methods=['GET', 'POST'], endpoint='signin')
def signin():
    if request.method == 'POST':
        # Retrieves data from HTML form
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('login-remember'))

        # Checks if user email exists
        user = User.query.filter_by(email=email).first()
        # Proceeds if email from user variable exists
        if user:
            # Validates the encrypted password
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                flash('Logged in successfully!', category='success')

                # Checks if user choose to stay logged in
                if remember:
                    # Logs in user and stay logged in for 7 days
                    login_manager.remember_cookie_duration = timedelta(days=7)
                    login_user(user, remember=False)
                else:
                    # Logs in user
                    login_user(user, remember=False)
                # Redirects to home page
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password!', category='error')

        # Flashes error message if email does not exist
        else:
            flash('User with email does not exist!', category='error')
    return render_template('auth.html')

@auth.route('/logout')
@login_required
def logout():
    # Gets logged in user and flashes a message
    user = current_user
    flash(f'Logged out from {user.username}', category='success')
    # Logs out user
    logout_user()
    # Redirect the user to signin page
    return redirect(url_for('auth.signin'))


def send_mail(user):
    token = user.get_token()
    msg = Message('Password Reset Sent', recipients=[user.email], sender='')
    msg.body = f'''
    To reset Password, please follow the link below.

    {url_for()}
    
    If you didn't send a reset password request, please ignore this message.
    '''


@auth.route('/forgetpassword', methods=['POST'], endpoint='forgetpassword')
def forgetpassword():
    # Retrieves data from Javascript fetch api
    email = request.form.get('forget_password_email')
    print(f'Email: {email}')

    # Gets user with the email if they exist and assign a storage value
    user = User.query.filter_by(email=email).first()
    
    # Handles if User associated with the email does exist
    if user:
        print(f'Email: {email}')
        send_mail(user)

        flash('Password reset link has been sent! Check your email and click on it to proceed.', category='success')

    # Handles if User associated with the email does not exist
    elif not user:
        flash('User with this email does not exist!', category='error')
        return render_template('auth.html')
    
    return render_template('auth.html')

@auth.route('/forgetpassword/<token>', methods=['GET', 'POST'])
def verify_token():
    user = User.verify_token(token)
    if user is None:
        flash('Invalid token or token has expired, please try again', category='error')
        return redirect(url_for('views.forgetpassword'))
    
    return render_template('change_password.html')