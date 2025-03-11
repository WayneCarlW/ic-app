from wtforms import Form, StringField, IntegerField, validators


class CheckoutForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150)])
    address = StringField('Address', [validators.Length(min=1, max=150)])
    city = StringField('City', [validators.Length(min=1, max=150)])
    state = StringField('State', [validators.Length(min=1, max=150)])
    country = StringField('Country', [validators.Length(min=1, max=150)])
    zip_code = StringField('Zip Code', [validators.Length(min=1, max=150)])
    phone = StringField('Phone', [validators.Length(min=1, max=150)])
    email = StringField('Email', [validators.Length(min=1, max=150)])
    card_number = StringField('Card Number', [validators.Length(min=1, max=150)])
    card_exp_month = IntegerField('Card Expiration Month', [validators.NumberRange(min=1, max=12)])
    card_exp_year = IntegerField('Card Expiration Year', [validators.NumberRange(min=2017, max=2030)])
    card_cvc = IntegerField('Card CVC', [validators.NumberRange(min=100, max=999)])

class ProductForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150)])
    price = IntegerField('Price', [validators.NumberRange(min=1, max=10000)])
    description = StringField('Description', [validators.Length(min=1, max=150)])
    image = StringField('Image', [validators.Length(min=1, max=150)])
    category = StringField('Category', [validators.Length(min=1, max=150)])
