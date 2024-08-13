from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
import os
import bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import cloudinary
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from dotenv import load_dotenv

# :::::::::::::::: Loads the env variables
load_dotenv()

db = SQLAlchemy()
DB_NAME=os.getenv('DB_NAME')
migrate = Migrate()
mail = Mail()

# ::::::::::::::::: create database function
def create_database(app):
    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()

# ::::::::::::::::: create app function
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    migrate.init_app(app, db)

    # Cloudinary configuration
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )

    CORS(app)

    # Mailjet configuration
    app.config['MAIL_SERVER'] = ''
    app.config['MAIL_PORT'] = ''
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = ''
    app.config['MAIL_PASSWORD'] = ''


    from .views import views
    from .auth import auth
    from .admin import admin


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin_panel')


    from .models import User, Product, Order

    # Flask admin configuration
    admin = Admin(app)

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(ModelView(Order, db.session))

    create_database(app)
    with app.app_context():
        if len(User.query.all()) < 1:
                # Create admin user on database initialization
                admin_email=os.getenv('ADMIN_EMAIL')
                admin_password=os.getenv('ADMIN_PASSWORD')
                
                # Encrypts the password and saves it in a variable
                hashed_password = bcrypt.hashpw(
                    admin_password.encode('utf-8'), 
                    bcrypt.gensalt()
                ).decode('utf-8')
                
                # :::::::::::::: Adding admin_user data to the database
                admin_user = User(
                    role='admin', 
                    name='Admin', 
                    email=admin_email, 
                    address='Admin Address', 
                    gender='male', 
                    password=hashed_password
                )
                db.session.add(admin_user)
                db.session.commit()
        
    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        if id == 'None':
            return None
        return User.query.get(int(id))

    return app
