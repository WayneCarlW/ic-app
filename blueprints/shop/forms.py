from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange

class CheckoutForm(FlaskForm):
    name = StringField('Name', [Length(min=1, max=150)])
    address = StringField('Address', [Length(min=1, max=150)])
    city = StringField('City', [Length(min=1, max=150)])
    state = StringField('State', [Length(min=1, max=150)])
    country = StringField('Country', [Length(min=1, max=150)])
    zip_code = StringField('Zip Code', [Length(min=1, max=150)])
    phone = StringField('Phone', [Length(min=1, max=150)])
    email = StringField('Email', [Length(min=1, max=150)])
    card_number = StringField('Card Number', [Length(min=1, max=150)])
    card_exp_month = IntegerField('Card Expiration Month', [NumberRange(min=1, max=12)])
    card_exp_year = IntegerField('Card Expiration Year', [NumberRange(min=2017, max=2030)])
    card_cvc = IntegerField('Card CVC', [NumberRange(min=100, max=999)])

class ProductForm(FlaskForm):
    name = StringField('Name', [Length(min=1, max=150)])
    price = IntegerField('Price', [NumberRange(min=1, max=10000)])
    description = TextAreaField('Description', [Length(min=1, max=150)])  # Changed to TextAreaField
    image = FileField('Image', [DataRequired()])
    category = StringField('Category', [Length(min=1, max=150)])
    stock = IntegerField('Stock', [NumberRange(min=1, max=10000)])
    submit = SubmitField('Submit')
