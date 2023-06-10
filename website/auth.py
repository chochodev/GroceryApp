from flask import Flask, Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from .models import User
import bcrypt
from . import db, mail
from flask_login import login_required, login_user, logout_user, current_user
from flask_login import LoginManager
from datetime import timedelta
from flask_mail import Message
from itsdangerous import URLSafeSerializer as Serializer


# Create Flask app instance
app = Flask(__name__)

# Initialize LoginManager
login_manager = LoginManager(app)

# Create auth Blueprint
auth = Blueprint('auth', __name__)

def send_confirmation_email(user):
    serializer = Serializer(app.config['SECRET_KEY'])
    token = serializer.dumps(user)
    confirm_url = url_for('auth.signup', token=token, _external=True)
    
    subject = 'Confirm Your Email Address'
    body = f'''Please click the following link to confirm your email address: 

    {confirm_url}

    If you didn't request this email, please ignore this message.
    
    '''
    
    # Create a message instance
    message = Message(subject=subject, body=body, recipients=[user.email])
    
    # Send the email
    mail.send(message)

@auth.route('/signup/<token>', methods=['GET'])
def confirm_email(token):
    try:
        new_user = Serializer.loads(token, max_age=86400)
    except:
        flash('The confirmation link is invalid or has expired.', category='error')
        return redirect(url_for('auth.signin'))
    
    # new_user = User.query.filter_by(email=user.email).first()
    if new_user:
        # Adds the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Flashes success message and redirects to home page
        flash('Account created for ' + new_user.username, category='success')
        login_user(new_user)
        return redirect(url_for('views.home'))

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
            
            # Send the confirmation email
            send_confirmation_email(new_user)

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
                flash(f'Logged in successfully as {user.username}', category='success')

                # Checks if user choose to stay logged in
                if remember:
                    # Logs in user and stay logged in for 7 days
                    login_manager.remember_cookie_duration = timedelta(days=7)
                    login_user(user)
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
    serial = Serializer(app.config['SECRET_KEY'], expires_sec=300)
    token = serial.dumps({user.id}).decode('utf-8')
    msg = Message('Password Reset Sent', recipients=[user.email], sender='')
    msg.body = f'''
    To reset Password, please follow the link below.

    {url_for('auth.forgetpassword', token=token, _external=True)}
    
    If you didn't send a reset password request, please ignore this message.
    '''
    mail.send(msg)


@auth.route('/forgetpassword', methods=['POST'], endpoint='forgetpassword')
def forgetpassword():
    # Retrieves data from Javascript fetch api
    email = request.form.get('forget_password_email')

    # Gets user with the email if they exist and assign a storage value
    user = User.query.filter_by(email=email).first()
    
    # Handles if User associated with the email does exist
    if user:
        send_mail(user)

        flash('Password reset link has been sent! Check your email and click on it to proceed.', category='success')

    # Handles if User associated with the email does not exist
    elif not user:
        flash('User with this email does not exist!', category='error')
        return render_template('auth.html')
    
    return render_template('auth.html')

@auth.route('/forgetpassword/<token>', methods=['GET', 'POST'])
def reset_token(token):
    password = request.form.get('password')
    password2 = request.form.get('password2')

    user = User.verify_token(token)
    if user is None:
        flash('Invalid token or token has expired, please try again', category='error')
        return redirect(url_for('auth.forgetpassword'))
    
    if password != password2:
        flash('Password are not the same!', category='error')
        return render_template('change_password.html', token=token)
    elif password == password2:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password changed successfully! Login now to continue shopping')
        return redirect(url_for('auth.signin'))
    
    return render_template('change_password.html')