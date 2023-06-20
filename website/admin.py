from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User, Product, Order
from flask_login import login_required, current_user
from . import db
from sqlalchemy import func
import cloudinary
from cloudinary import uploader
from .decorators import admin_required

admin = Blueprint('admin_panel', __name__)


@admin.route('/dashboard', methods=['GET', 'POST'])
@login_required
@admin_required
def dashboard():
    customers = User.query.all()
    products = Product.query.all()
    orders = Order.query.all()

    # To find all customer with items in cart
    active_customers = 0
    for customer in customers:
        if len(customer.orders) > 0:
            active_customers = active_customers + 1
    
    # Get all selling products
    selling_products = 0
    for product in products:
        # Get all products associated with the order
        if product.products_in_order:
            selling_products = selling_products + 1

    # To find all pending orders
    pending_orders = 0 
    for order in orders:
        if order.status == 'pending':
            pending_orders = pending_orders + 1
            
    context = {
        'customers':customers, 
        'products':products, 
        'orders':orders,
        'active_customers':active_customers,
        'selling_products':selling_products,
        'pending_orders':pending_orders
    }
    return render_template('/admin/dashboard.html', **context, endpoint='dashboard')


@admin.route('/search', methods=['GET', 'POST'])
@login_required
@admin_required
def search():
    if request.method == 'POST':
        # Gets the search data
        search_data = request.form.get('search-data')
        # Checks if a product has such name or allergic description
        results = Product.query.filter((Product.name.ilike(f'%{search_data}%')) | (Product.allergic_desc.ilike(f'%{search_data}%'))).all()

        if not results:
            flash(f'No product with {search_data} found', category='error')
            return redirect('admin_panel.dashboard')

        context = {'products': results, 'search_return': search_data}
        return render_template('admin/products.html', **context, endpoint='search')


@admin.route('/customers', methods=['GET', 'POST'])
@login_required
@admin_required
def customers():
    customers = User.query.all()

    context = {'customers':customers}
    return render_template('/admin/customers.html', **context, endpoint='customers')

@admin.route('/orders', methods=['GET', 'POST'])
@login_required
@admin_required
def orders():
    # Retrieve all orders from the database
    orders = Order.query.all()
    pending_orders = Order.query.filter_by(status='pending').all()
    approved_orders = Order.query.filter_by(status='approved').all()
        
    context = {'orders':orders, 'pending_orders':pending_orders, 'approved_orders':approved_orders}
    return render_template('/admin/orders.html', **context, endpoint='orders')


@admin.route('/process-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def order(order_id):
    # Gets the order with the id of order_id
    orders = Order.query.filter_by(id=order_id).all()
        
    # For calculating all the order prices
    total_normal_price = 0
    total_customer_price = 0
    for order in orders:
        total_normal_price = float(total_normal_price) + float(order.normal_price)
        total_customer_price = float(total_customer_price) + float(order.customer_price)
    
    if request.method == 'POST':
        # Gets action attribute sent from the page
        if request.form.get('action') == 'approve':
            for order in orders:
                order.status = 'approved'
                # Updates the order status in database
                db.session.add(order)
                db.session.commit()

                flash(f'Order approved, dispatch rider to {order.user.address} for delivery')
                return redirect(url_for('admin_panel.orders'))

        # Gets action attribute sent from the page
        elif request.form.get('action') == 'reject':
            for order in orders:
                order.status = 'rejected'
                # Updates the order status in database
                db.session.add(order)
                db.session.commit()

                flash(f'Order rejected')
                return redirect('admin_panel.orders')
        
    context = {'orders':orders, 'total_normal_price':total_normal_price, 'total_customer_price':total_customer_price}
    return render_template('admin/order.html', **context, endpoint='order')    


@admin.route('/products', methods=['GET', 'POST'])
@login_required
@admin_required
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
@login_required
@admin_required
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

            # Calls and initiates the upload image function
            result = upload_image(image, new_product.id)
            if result:
                new_product.image = result['secure_url']

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
        allergic_desc = request.form.get('allergy')
        normal_price = request.form.get('normal_price')
        min_price = request.form.get('min_price')
        image = request.files.get('image')

        product.name = name
        product.allergic_desc = allergic_desc
        product.normal_price = normal_price
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
@login_required
@admin_required
def delete_product(sent_product_id):
    product = Product.query.get(sent_product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    flash(f'Product with id: {int(sent_product_id)} not found')
    return redirect(url_for('admin_panel.products'))


@admin.route('/validate-order', methods=['GET', 'POST'])
@login_required
@admin_required
def validate_order():
    
    return render_template('admin/validate_order.html', endpoint='validate_order')