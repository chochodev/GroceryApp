from flask import current_app
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous import URLSafeTimedSerializer as Serializer


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    products = db.relationship('Product', backref='order')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    allergic_desc = db.Column(db.String(350), nullable=False)
    normal_price = db.Column(db.String(150), nullable=False)
    min_price = db.Column(db.String(150), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    def __init__(self):
        self.name = name
    
    def __repr__(self):
        return f"User('{self.name}', '{self.allergic_desc[0:30]}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    phone = db.Column(db.Integer, unique=True)
    gender = db.Column(db.String(15))
    password = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    
    def __repr__(self):
        return f"User('{self.name}', '{self.username}', '{self.email}')"