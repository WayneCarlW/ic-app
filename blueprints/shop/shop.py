from flask import Blueprint, redirect,flash, url_for
from flask_login import current_user, login_required
from extensions import mongo
from flask import render_template
from .forms import ProductForm


shop = Blueprint('shop', __name__, template_folder='templates', static_folder='static')

@shop.route('/')
def home():
    return render_template('shop/shelf.html', user=current_user)

@shop.route('/cart')
def cart():
    return render_template('shop/cart.html', user=current_user)

@shop.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    
    if form.validate_on_submit():
        product_data = {
            "name": form.name.data,
            "price": form.price.data,
            "description": form.description.data,
            "image": form.image.data,
            "category": form.category.data,
            "stock": form.stock.data,
            "user_id": current_user.id
        }

        mongo.db.products.insert_one(product_data)
        flash('Product added successfully!', 'success')
        return redirect(url_for('shop.add_product'))
    
    return render_template('shop/add_product.html', form=form, user=current_user)

@shop.route('/manage_shelf')
def manage_shelf():
    return render_template('shop/manage_shelf.html', user=current_user)


@shop.route('/checkout')
def checkout():
    return render_template('shop/checkout.html', user=current_user)


@shop.route('/reports')
def reports():
    return render_template('shop/reports.html', user=current_user)

@shop.route('/review')
def review():
    return render_template('shop/review.html', user=current_user)

