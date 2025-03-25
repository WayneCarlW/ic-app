from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from blueprints.auth.auth import get_mongo_db
from bson import ObjectId
from extensions import mongo, mail
from flask_mail import Message

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    return redirect(url_for('shop.analytics'))

@admin.route('/approve_user/<user_id>', methods=['GET','POST'])
@login_required
def approve_user(user_id):
    if not current_user.is_admin:
        flash('You are not authorized to perform this action.', 'danger')
        return redirect(url_for('admin.dashboard'))

    db = get_mongo_db()
    user = db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        flash("User not found", 'danger')
        return redirect(url_for('admin.manage_manufacturers'))
    
    if user.get("approved"):
        flash("User is already approved", 'info')
        return redirect(url_for('admin.manage_manufacturers'))

    # Approve user
    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"approved": True}})

    # Send approval email
    msg = Message(
        "Your Account Has Been Approved!",
        sender="cwasonga@kabarak.ac.ke",
        recipients=[user["email"]]
    )
    msg.body = f"""
    Hello {user["name"]},

    Your account has been approved! You can now log in to your account.

    Best regards,
    Imitation Control Team
    """
    mail.send(msg)

    flash("User approved and email sent successfully.", 'success')
    return redirect(url_for('admin.manage_manufacturers'))

@admin.route('/manage_manufacturers')
@login_required
def manage_manufacturers():
    db = get_mongo_db()
    if db is None:
        return redirect(url_for('admin.dashboard'))
    manufacturers = db.users.find({'role': 'manufacturer'})
    return render_template('admin/manage_manufacturers.html', user=current_user, manufacturers=manufacturers)