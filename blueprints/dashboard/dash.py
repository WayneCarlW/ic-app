from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import current_user, login_required

dash = Blueprint('dash', __name__, template_folder='templates')

@login_required
@dash.route('/')
def index():
    return render_template('dashboard/dash.html', user=current_user)

@login_required
@dash.route('/admin')
def admindash():
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect(url_for('auth.login'))
    
    return render_template('dashboard/dash.html', user=current_user)
