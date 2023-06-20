from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(route_func):
    @wraps(route_func)
    def decorated_route(*args, **kwargs):
        if current_user.role != 'admin':
            flash('You are not authorized to access this page.', category='error')
            return redirect(url_for('views.home')) 
        return route_func(*args, **kwargs)
    return decorated_route
