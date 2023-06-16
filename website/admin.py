from flask import Flask, Blueprint, render_template, redirect, url_for, request, current_app, jsonify, flash, send_from_directory
from .models import User, Product, Order
from werkzeug.utils import secure_filename
from . import db
import cloudinary
import json
from cloudinary import uploader

admin = Blueprint('admin_panel', __name__)

# User roles
ROLES = {
    'admin': 1,
    'customer': 2
}

#################### yet to be implemented ####################
@admin.route('/admin/create/<int:user_id>', methods=['POST'])
def create_admin(user_id):
    # Gets the user with the id
    user = User.query.get(user_id)
        
    if user:
        # Assign the admin role to the user
        user.role = ROLES['admin']
        # Commit the changes to the database
        db.session.commit()
        
        flash(f'User {user.name[0:30]} has been assigned the admin role.', category='success')
    else:
        flash(f'User with ID {user_id} not found.', category='error')
    
    # Redirect to a suitable location (e.g., admin dashboard)
    return redirect(url_for('admin.dashboard'))

@admin.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    customers = User.query.all()
    products = Product.query.all()
    orders = Order.query.all()
    
    print(len(orders))
    context = {'customers':customers, 'products':products, 'orders':orders}
    return render_template('/admin/dashboard.html', **context, endpoint='dashboard')

@admin.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        pass
    customers = User.query.all()
    context = {'customers':customers}
    return render_template('/admin/customers.html', **context, endpoint='customers')

@admin.route('/orders', methods=['GET', 'POST'])
def orders():
    # Retrieve all orders from the database
    orders = Order.query.all()
    
    context = {'orders':orders}
    return render_template('/admin/orders.html', **context, endpoint='orders')

@admin.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        pass
    else:
        products = Product.query.all()

        context = {'products':products}
        return render_template('/admin/products.html', **context, endpoint='products')

def upload_image(image, product_id):
    if image:
        # Upload the image to Cloudinary
        result = cloudinary.uploader.upload(image, public_id=f'product_images/{product_id}')
        return result
    return None

@admin.route('/create-product', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        # Retrieves data from HTML form
        name = request.form.get('name')
        desc = request.form.get('desc')
        price_per_kg = request.form.get('price_per_kg')
        min_price = request.form.get('min_price')
        image = request.files.get('image')

        if Product.query.filter_by(name=name).first():
            flash(f'Product {name} already exist', category='error')
        else:
            new_product = Product(name=name, allergic_desc=desc, normal_price=price_per_kg, min_price=min_price)

            db.session.add(new_product)
            db.session.commit()

            print(f'upload function about to be called')

            # Calls and initiates the upload image function
            result = upload_image(image, new_product.id)
            if result:
                new_product.image = result['secure_url']
                print('Image URL: ' + result['secure_url'])
                # Flashes success message and redirects to home page
                flash(f'New product {new_product.name} successfully created', category='success')
                db.session.commit()
                return render_template('/admin/create_product.html')
            else:
                flash('Image upload failed')

            return redirect(url_for('admin_panel.products'))
    
    return render_template('/admin/create_product.html', endpoint='create_product')


@admin.route('/edit-product/<int:sent_product_id>', methods=['GET', 'POST', 'PUT'])
def edit_product(sent_product_id):
    if request.method == 'POST':
        product_id = int(sent_product_id)
        product = Product.query.get(product_id)

        if not product:
            flash('Product not found', category='error')
            return redirect(url_for('admin_panel.products'))

        # Retrieves data from HTML form
        name = request.form.get('name')
        desc = request.form.get('desc')
        price_per_kg = request.form.get('price_per_kg')
        min_price = request.form.get('min_price')
        image = request.files.get('image')

        product.name = name
        product.allergic_desc = desc
        product.normal_price = price_per_kg
        product.min_price = min_price
        db.session.commit()

        # Calls and initiates the upload image function
        if image:
            result = upload_image(image, product.id)
            if result:
                product.image = result['secure_url']
                # Flashes success message and redirects to home page
                flash(f'Product {product.name} successfully edited', category='success')
                db.session.add(product)
                db.session.commit()
                return redirect(url_for('admin_panel.products'))
            else:
                flash('Image upload failed')

        db.session.add(product)
        db.session.commit()
        return redirect(url_for('admin_panel.products'))
    
    product_id = int(sent_product_id)
    product = Product.query.filter_by(id=product_id).first()
    context = {'product':product}
    return render_template('admin/edit_product.html', **context, endpoint='edit_product')


@admin.route('/delete-product/<int:sent_product_id>', methods=['POST'])
def delete_product(sent_product_id):
    product = Product.query.get(sent_product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    flash(f'Product with id: {int(sent_product_id)} not found')
    return redirect(url_for('admin_panel.products'))


@admin.route('/validate-order', methods=['GET', 'POST'])
def validate_order():
    
    return render_template('admin/validate_order.html', endpoint='validate_order')