from shop import shop
from flask import render_template
from models import Product
from bson import ObjectId
from auth import get_mongo_db

@shop.route('/')
def home():
    return render_template('shop/shelf.html')

@shop.route('/cart')
def cart():
    return render_template('shop/cart.html')

@shop.route('/checkout')
def checkout():
    return render_template('shop/checkout.html')

@shop.route('review')
def review():
    return render_template('shop/review.html')