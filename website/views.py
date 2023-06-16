from flask import Blueprint, render_template, flash, session, redirect, request, url_for
from flask_login import login_required, current_user
from .models import User, Product, Order
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'], endpoint='home')
def home():
    # Check if the user is authenticated
    if current_user.is_authenticated:
        # Check if the 'show_flash' flag is not present in the session
        if 'show_flash' not in session:
            # Display a flash message with the name
            flash(f'Logged in as user {current_user.name[0:30]}')
            
            # Set the 'show_flash' flag in the session to True
            # So that the message flashes once on user logging in and redirected here
            session['show_flash'] = True
    
    # Render the home.html template
    return render_template('home.html', user=current_user, endpoint='home')

@views.route('/menu', methods=['GET', 'POST'], endpoint='menu')
def menu():
    if request.method == 'POST':
        pass
    products = Product.query.all()
    context = {'products':products}
    return render_template('menu.html', user=current_user, **context, endpoint='menu')

@views.route('/orders/', methods=['GET', 'POST'])
@login_required
def orders():
    user = current_user
    if user.order:
        order_products = user.order[0].products
    else:
        order_products = []

    return render_template('orders.html', user=user, order_products=order_products, endpoint='order')

@views.route('/order/<int:product_id>', methods=['GET', 'POST'])
@login_required
def order(product_id):
    print(f'POST request received')
    # Gets the current user
    user = current_user
    if request.method == 'POST':
        # Handles if it is a delete request and adds the product to allergic list
        if request.form.get('action') == 'delete':
            pass
        # Handles if it is an order request and adds the product to cart list
        elif request.form.get('action') == 'order':
            amount_in_kg = request.form.get('amount-in-kg')
            customer_price = request.form.get('offer-price')
            # Find the product by ID
            product = Product.query.get(product_id)

            print(f'Product and & price: {product.name} ${product.normal_price}, \t Amount per kg: {amount_in_kg}, \t Price paying: ${customer_price}')

            if product:
                # Create a new order for the user
                print('Product is ')
                order = Order(user_id=user.id, customer_price=customer_price)
                order.products.append(product)
                print(f'New order: {order}')
                db.session.add(order)
                db.session.commit()

                flash(f'Placed a new order on {product.name}', category='success')
                return redirect(url_for('views.orders'))
            
    context = {'order':Order.query.all()}
    return render_template('orders.html', **context, user=current_user)


@views.route('/allergy', methods=['GET', 'POST'])
@login_required
def allergy():
    
    return render_template('allergy.html', user=current_user, endpoint='allergy')

@views.route('/aboutus', methods=['GET', 'POST'], endpoint='aboutus')
def aboutus():
    
    return render_template('aboutus.html', user=current_user, endpoint='aboutus')

@views.route('/privacy', methods=['GET', 'POST'], endpoint='privacy')
def privacy():
    
    return render_template('privacy.html', user=current_user, endpoint='privacy')
