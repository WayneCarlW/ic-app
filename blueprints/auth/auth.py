from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import mongo, mail
from flask_mail import Message
from models import User
from bson import ObjectId


auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

def get_mongo_db():
    if mongo is None or mongo.db is None:
        flash('Database connection error.', 'danger')
        return None
    return mongo.db

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = get_mongo_db()
        if db is None:
            return redirect(url_for('auth.register'))
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        user_data = {'email': email, 'password': hashed_password, 'role': "user"}
        db.users.insert_one(user_data)
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', user=current_user, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = get_mongo_db()
        if db is None:
            return redirect(url_for('auth.login'))
        email = request.form['email']
        password = request.form['password']
        user_data = db.users.find_one({'email': email})
        

        if user_data:
            if check_password_hash(user_data['password'], password):
                user = User(str(user_data['_id']), user_data['email'], user_data['password'], user_data['role'])
                login_user(user)
                flash('Logged in successfully!', 'success')

                if user.is_admin():
                    return redirect(url_for('dash.admindash'))
                
                return redirect(url_for('dash.index'))
            else:
                flash('Invalid password', 'danger')
        else:
            flash('Email not found', 'danger')
    return render_template('auth/login.html', user=current_user, title='Login')

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        db = get_mongo_db()
        if db is None:
            return redirect(url_for('auth.forgot_password'))
        email = request.form['email']
        user = db.users.find_one({'email': email})
        if user:
            reset_link = url_for('auth.reset_password', user_id=str(user['_id']), _external=True)
            msg = Message('Password Reset Request',
                          sender=auth.config['MAIL_USERNAME'],
                          recipients=[email])
            msg.body = f"""
            Hello,

            You requested a password reset. Click the link below to reset your password:

            {reset_link}

            If you did not request this, please ignore this email.

            Regards,
            Imitation Control App
            """
            try:
                mail.send(msg)
                flash('Password reset email sent! Check your inbox.', 'info')
                return redirect(url_for('auth.reset_password'))
            except Exception as e:
                flash(f'Error sending email: {str(e)}', 'danger')
        else:
            flash('Email not found.', 'danger')
    return render_template('auth/forgot_pass.html')

@auth.route('/reset-password/<user_id>', methods=['GET', 'POST'])
def reset_password(user_id):
    if request.method == 'POST':
        db = get_mongo_db()
        if db is None:
            return redirect(url_for('auth.reset_password', user_id=user_id))
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        db.users.update_one(
            {'_id': ObjectId(user_id)}, {'$set': {'password': hashed_password}}
        )
        flash('Password has been reset successfully!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
