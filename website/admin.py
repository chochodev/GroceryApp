from flask import Blueprint, render_template
from .models import User, Product, Order

admin = Blueprint('admin', __name__)

@admin.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    
    return render_template('/admin/dashboard.html', endpoint='dashboard')

@admin.route('/customers', methods=['GET', 'POST'])
def customers():
    
    return render_template('/admin/customers.html', endpoint='customers')

@admin.route('/orders', methods=['GET', 'POST'])
def orders():
    
    return render_template('/admin/orders.html', endpoint='orders')

@admin.route('/products', methods=['GET', 'POST'])
def products():

    return render_template('/admin/products.html', endpoint='products')

@admin.route('/product', methods=['GET', 'POST'])
def product():

    return render_template('/admin/create_product.html', endpoint='product')

@admin.route('/edit-product', methods=['GET', 'POST'])
def edit_product():

    return render_template('admin/edit_product.html', endpoint='edit_product')

@admin.route('/validate-order', methods=['GET', 'POST'])
def validate_order():
    
    return render_template('admin/validate_order.html', endpoint='validate_order')