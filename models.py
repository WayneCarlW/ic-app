from flask_login import UserMixin
class User(UserMixin):
    def __init__(self, user_id, email, password, role, profile_pic):
        self.id = user_id
        self.email = email
        self.password = password
        self.role = role
        self.profile_pic = profile_pic

    def is_admin(self):
        return self.role == 'admin'
    
    def is_farmer(self):
        return self.role == 'farmer'

    def is_manufacturer(self):
        return self.role == 'manufacturer'   
class Product:
    def __init__(self, product_id, name, price, description, image):
        self.id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.image = image
class Farmer(User):
    def __init__(self, farmer_id, name, location, supporting_docs):
        self.id = farmer_id
        self.name = name
        self.location = location
        self.supporting_docs = supporting_docs

class Manufacturer(User):
    def __init__(self, manufacturer_id, kam_id, name, industry_niche, supporting_docs):
        self.id = manufacturer_id
        self.kam_id = kam_id
        self.name = name
        self.industry_niche = industry_niche
        self.supporting_docs = supporting_docs
