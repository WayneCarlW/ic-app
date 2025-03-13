from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_login import LoginManager
import gridfs

mongo = PyMongo()
fs = None

def init_app(app):
    global fs
    mongo.init_app(app)

    if mongo.db is None:
        print('Database connection error.')
        raise Exception('Database connection error.')
    
    print(f"Connected to the database: {mongo.db.name}")
    fs = gridfs.GridFS(mongo.db)
    print(f"GridFS initialized:{fs is not None}")
    
mail = Mail()
login_manager = LoginManager()
