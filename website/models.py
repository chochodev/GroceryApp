from flask import current_app
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import backref
from itsdangerous import URLSafeTimedSerializer as Serializer


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    normal_price = db.Column(db.String(20), nullable=False)
    customer_price = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='unattended', nullable=False)
    # allergy_status = db.Column(db.Boolean, default=False)

    date = db.Column(db.DateTime(timezone=True), default=func.now())

    # For customers associated with an order
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    customer = db.relationship('User', backref=backref('orders', cascade="all, delete"))

    # For products associated with an order
    products = db.relationship('Product', secondary='order_product', backref=backref('products_in_order', cascade='all, delete'))

    def __repr__(self):
        user = User.query.get(self.user_id)
        user_name = user.name if user else "Unknown User"
        product_names = [product.name for product in self.products]
        return f"Order_id: '{self.id}', User: '{user_name}', Products: {product_names}'"

# Define the association table for the many-to-many relationship
order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    allergic_desc = db.Column(db.String(350), nullable=False)
    allergy_status = db.Column(db.Boolean, default=False)
    normal_price = db.Column(db.String(150), nullable=False)
    min_price = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(225))

    # Add the relationship with the Order model
    orders = db.relationship('Order', secondary='order_product', backref='products_in_order')

    def __repr__(self):
        return f"Product ('{self.name}', '{self.allergic_desc[0:30]}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10), default='customer')
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.Integer, unique=True)
    gender = db.Column(db.String(15))
    password = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    # Define the relationship with the Order model
    order = db.relationship('Order', backref='user', overlaps="customer,orders")

    def __repr__(self):
        return f"User ('{self.name}', '{self.email}')"
