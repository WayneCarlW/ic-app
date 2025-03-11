from flask_login import UserMixin
from bson import ObjectId

class User(UserMixin):
    def __init__(self, user_id, email, password):
        self.id = user_id
        self.email = email