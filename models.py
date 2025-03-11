from flask_login import UserMixin
class User(UserMixin):
    def __init__(self, user_id, email, password, role):
        self.id = user_id
        self.email = email
        password = password
        role = role

    def is_admin(self):
        return self.role == 'admin'    
class Product:
    def __init__(self, product_id, name, price, description, image):
        self.id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.image = image
