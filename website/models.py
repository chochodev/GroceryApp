from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous import URLSafeTimedSerializer as Serializer


cart_product_association = db.Table('cart_product_association',
    db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

user_allergy_association = db.Table('user_allergy_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('allergy_id', db.Integer, db.ForeignKey('allergy.id'), primary_key=True)
)


class Allergy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    products = db.relationship('Product', secondary=cart_product_association, backref=db.backref('carts', lazy='dynamic'))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    price = db.Column(db.String(150))
    allergy_desc = db.Column(db.String(300))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    gender = db.Column(db.String(15))
    password = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    allergies = db.relationship('Allergy', secondary=user_allergy_association, backref=db.backref('users', lazy='dynamic'))

    def get_token(self, expires_sec=300):
        serial = Serializer(current_app.config['SECRET_KEY'], expires_sec=expires_sec)
        return serial.dumps({'user_id':user.id}).decode('utf-8')
    
    @staticmethod
    def verify_token(token):
        serial = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.name}', '{self.username}', '{self.email}')"