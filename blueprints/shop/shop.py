from flask import Blueprint
from flask_login import current_user
from flask import render_template


shop = Blueprint('shop', __name__, template_folder='templates', static_folder='static')

@shop.route('/')
def home():
    return render_template('shop/shelf.html', user=current_user)

@shop.route('/cart')
def cart():
    return render_template('shop/cart.html', user=current_user)

@shop.route('/checkout')
def checkout():
    return render_template('shop/checkout.html', user=current_user)

@shop.route('/review')
def review():
    return render_template('shop/review.html', user=current_user)

