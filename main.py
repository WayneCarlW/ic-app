from flask import Flask, render_template, request, redirect, url_for, flash, session
from blueprints.auth.auth import auth
from blueprints.dashboard.dash import dash
from blueprints.shop.shop import shop
from flask_mail import Mail
from flask_pymongo import PyMongo
from extensions import login_manager
from flask_login import LoginManager
from models import User
import os
from extensions import init_app
from bson import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ic-app'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'cwasonga@kabarak.ac.ke'
app.config['MAIL_PASSWORD'] = '123456:::::number'


mongo = PyMongo(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(str(user_data['_id']), user_data['email'], user_data['password'])
    return None

@app.before_request
def permanent_session():
    session.permanent = True

@app.route('/')
def home():
    return render_template('index.html')

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(dash, url_prefix='/dashboard')
app.register_blueprint(shop, url_prefix='/shop')

if __name__ == '__main__':
    app.run(debug=True)