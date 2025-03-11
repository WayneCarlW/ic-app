from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_login import LoginManager

mongo = PyMongo()

def init_app(app):
    mongo.init_app(app)

mail = Mail()
login_manager = LoginManager()