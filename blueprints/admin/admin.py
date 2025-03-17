from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from blueprints.auth.auth import get_mongo_db
from bson import ObjectId

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('admin/admin.html', user=current_user)

@admin.route('/approve_user/<user_id>', methods=['PUT'])
def approve_user(user_id):
    db = get_mongo_db()
    if db is None:
        return redirect(url_for('admin.dashboard'))
    db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'approved': True}})
    flash('User approved successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/manage_manufacturers')
def manage_manufacturers():
    db = get_mongo_db()
    if db is None:
        return redirect(url_for('admin.dashboard'))
    manufacturers = db.users.find({'role': 'manufacturer'})
    return render_template('admin/manage_manufacturers.html', user=current_user, manufacturers=manufacturers)