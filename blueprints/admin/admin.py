from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('admin/admin.html', user=current_user)