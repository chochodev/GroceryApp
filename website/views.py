from flask import Blueprint, render_template, flash, session, redirect, request, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Product, Order
from . import db

views = Blueprint('views', __name__)


# FOR HOME PAGE
@views.route('/', methods=['GET', 'POST'])
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


# FOR MENU PAGE
@views.route('/menu', methods=['GET', 'POST'])
def menu():
    products = Product.query.all()

    context = {'products':products}
    return render_template('menu.html', user=current_user, **context, endpoint='menu')


# FOR MENU PAGE
@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_data = request.form.get('search-data')
        results = Product.query.filter((Product.name.ilike(f'%{search_data}%')) | (Product.allergic_desc.ilike(f'%{search_data}%'))).all()

        if results is None:
            flash(f'No product of such description', category='error')
            return redirect('views.home')
            
        context = {'products':results, 'search_return':search_data}
        return render_template('menu.html', **context, user=current_user, endpoint='search')


# FOR ORDERS PAGE
@views.route('/orders/', methods=['GET', 'POST'])
@login_required
def cart():
    # Gets the current user
    user = current_user
    # Gets the variaties of orders
    orders = Order.query.join(Order.user).filter(User.id == user.id).all()
    print(f'Orders: {orders}')
    approved_orders = Order.query.filter_by(user_id=user.id, status='approved').all()
    rejected_orders = Order.query.filter_by(user_id=user.id, status='rejected').all()


    if request.method == 'POST':
        if request.json.get('action') == 'delete':
            # Deletes the order of status='unattended'
            orders = Order.query.filter_by(user_id=user.id, status='unattended').all()
            for order in orders:
                db.session.delete(order)
            # Updates the order into the database
            db.session.commit()

            flash(f'Cart removed', category='error')
            return jsonify({'delete':'success'})
        elif request.json.get('action') == 'order':
            # Sets the status of all orders to 'pending'
            for order in orders:
                order.status = 'pending'
                # Updates the order into the database
                db.session.add(order)
                db.session.commit()

            flash(f'Placed a new order. Await approval', category='success')
            return jsonify({'ordered':'success'})
        
    # For calculating all the order prices
    total_normal_price = 0
    total_customer_price = 0
    for order in orders:
        total_normal_price = float(total_normal_price) + float(order.normal_price)
        print(f'Customer_price: {order.customer_price}')
        total_customer_price = float(total_customer_price) + float(order.customer_price)

    context = {
        'orders':orders, 
        'total_normal_price':total_normal_price, 
        'total_customer_price':total_customer_price, 
        'approved_orders':approved_orders, 
        'rejected_orders':rejected_orders
    }
    return render_template('cart.html', user=user, **context, endpoint='cart')


# FOR ORDER REQUEST
@views.route('/order/<int:product_id>', methods=['GET', 'POST'])
@login_required
def order(product_id):
    # Gets the current user
    user = current_user
    if request.method == 'POST':
        # Gets the product associated with the product_id
        product = Product.query.get(product_id)
        # Handles if it is a delete request and adds the product to allergic list
        if request.form.get('action') == 'delete':
            # Changes the product allergy_status to True
            product.allergy_status = True
            # Updates the product into the database
            db.session.add(product)
            db.session.commit()

            flash(f'Item added to Allergy list {product.allergy_status}', category='success')
            return redirect(url_for('views.menu'))
            
        # Handles if it is an order request and adds the product to cart list
        elif request.form.get('action') == 'order':
            amount_in_kg = request.form.get('amount-in-kg')
            customer_price = request.form.get('offer-price')
            # Find the product by ID

            if product:
                # Create a new order for the user
                normal_price = int(amount_in_kg) * int(product.normal_price)
                order = Order(user_id=user.id, normal_price=normal_price, customer_price=customer_price)
                order.products.append(product)
                # For the normal amount to be paid my the user
                
                db.session.add(order)
                db.session.commit()
                flash(f'Item added to cart, you can now place a new order in cart', category='success')
                return redirect(url_for('views.menu'))


# FOR ALLERGY PAGE 
@views.route('/allergy', methods=['GET', 'POST'])
@login_required
def allergy():
    # Gets all product with allergic_status true
    products = Product.query.filter_by(allergy_status=True).all()
    
    if request.method == 'POST':
        product_id = request.form.get('allergy')
        product = Product.query.filter_by(id=product_id).first()
        if product:
            product.allergy_status = False
            # Updates the database
            db.session.commit()

            flash(f'{product.name} removed from allergy list')
            return jsonify({})
    
    context = {'products':products}
    return render_template('allergy.html', user=current_user, **context, endpoint='allergy')


# FOR ACCOUNT PAGE 
@views.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user = current_user
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        phone = request.form.get('phone')

        user.name = name
        user.email = email
        user.address = address
        user.phone = phone

        db.session.commit()

        flash(f'Account updated successfully', category='success')
        return redirect(url_for('views.home'))
    
    return render_template('account.html', user=current_user, endpoint='account')


# FOR ABOUT US PAGE
@views.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
    
    return render_template('aboutus.html', user=current_user, endpoint='aboutus')


# FOR PRIVACY PAGE
@views.route('/privacy', methods=['GET', 'POST'])
def privacy():
    
    return render_template('privacy.html', user=current_user, endpoint='privacy')
