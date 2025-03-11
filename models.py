from flask_login import UserMixin
class User(UserMixin):
    def __init__(self, user_id, email, password):
        self.id = user_id
        self.email = email
        password = password
class Product:
    def __init__(self, product_id, name, price, description, image):
        self.id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.image = image
