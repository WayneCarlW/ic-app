from flask import Blueprint, redirect,flash, url_for, Response, request
from flask_login import current_user, login_required
from extensions import mongo
from flask import render_template
from .forms import ProductForm, CheckoutForm, CartForm
from blueprints.auth.auth import get_mongo_db
from bson import ObjectId, Binary
from datetime import datetime


shop = Blueprint('shop', __name__, template_folder='templates', static_folder='static')

@shop.route('/')
def home():
    db = get_mongo_db()
    if db is None:
        return redirect(url_for('shop.shelf'))
    products = db.products.find({'user_id': current_user.id})
    return render_template('shop/shelf.html', user=current_user, products=products)


@shop.route('/cart/<product_id>', methods=['GET', 'POST'])
@login_required
def add_to_cart(product_id):
    product = mongo.db.product_data.find_one({"_id": ObjectId(product_id)})
    if not product:
        return "Product not found", 404
    
    cart_item = {
        "user_id": current_user.id,
        "product_id": product_id,
        "name": product["name"],
        "price": product["price"],
        "quantity": int(request.form["quantity"]),
        "total": product["price"] * int(request.form["quantity"])
    }

    mongo.db.cart.insert_one(cart_item)
    flash('Product added to cart successfully!', 'success')
    return redirect(url_for('shop.cart'))

@shop.route('/cart')
@login_required
def view_cart():
    cart_items = list(mongo.db.cart.find({"user_id": current_user.id}))
    return render_template('shop/cart.html', user=current_user, cart_items=cart_items)

@shop.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    
    if form.validate_on_submit():
        file = form.image.data

        if file:
            image_data = Binary(file.read())
        else:
            image_data = None
        product_data = {
            "name": form.name.data,
            "price": form.price.data,
            "description": form.description.data,
            "image": image_data,
            "category": form.category.data,
            "stock": form.stock.data,
            "user_id": current_user.id
        }

        mongo.db.products.insert_one(product_data)
        flash('Product added successfully!', 'success')
        return redirect(url_for('shop.manage_shelf'))
    
    return render_template('shop/add_product.html', form=form, user=current_user)

@shop.route('/product_image/<product_id>')
def product_image(product_id):
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    if not product or not product.get("image"):
        return "No image found", 404

    return Response(product["image"], mimetype="image/jpeg")

@shop.route('/delete_product/<product_id>', methods=['POST'])
def delete_product(product_id):
    db = get_mongo_db()
    if db is None:
        return redirect(url_for('shop.manage_shelf'))
    db.products.delete_one({'_id': ObjectId(product_id)})
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('shop.manage_shelf'))

@shop.route('/edit_product/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    db = get_mongo_db()
    if db is None:
        return redirect(url_for('shop.manage_shelf'))
    product = db.products.find_one({'_id': ObjectId(product_id)})
    form = ProductForm()
    if form.validate_on_submit():
        file = form.image.data
        if file:
            image_data = Binary(file.read())
        else:
            image_data = product.get('image')

        product_data = {
            "name": form.name.data,
            "price": form.price.data,
            "description": form.description.data,
            "image": image_data,
            "category": form.category.data,
            "stock": form.stock.data,
            "user_id": current_user.id
        }

        db.products.update_one({'_id': ObjectId(product_id)}, {'$set': product_data})
        flash('Product updated successfully!', 'success')
        return redirect(url_for('shop.manage_shelf'))
    form.name.data = product.get('name')
    form.price.data = product.get('price')
    form.description.data = product.get('description')
    form.category.data = product.get('category')
    form.stock.data = product.get('stock')
    return render_template('shop/edit_product.html', form=form, user=current_user)

@shop.route('/manage_shelf')
def manage_shelf():
    db = get_mongo_db()
    if db is None:
        return redirect(url_for('shop.manage_shelf'))
    products = db.products.find({'user_id': current_user.id})
    return render_template('shop/manage_shelf.html', user=current_user, products=products)


@shop.route('/checkout')
def checkout():
    cart_items = list(mongo.db.cart.find({"user_id": current_user.id}))
    if not cart_items:
        flash('No items in cart!', 'danger')
        return redirect(url_for('shop.cart'))
    order_data = {
        "user_id": current_user.id,
        "items": cart_items,
        "total": sum(item["total"] for item in cart_items),
        "status": "pending",
        "created_at": datetime.now()
    }
    order_id = mongo.db.orders.insert_one(order_data).inserted_id
    mongo.db.cart.delete_many({"user_id": current_user.id})
    flash('Order placed successfully!', 'success')
    return redirect(url_for('shop.orders'))

@shop.route('/orders')
def orders():
    orders = list(mongo.db.orders.find({"user_id": current_user.id}))
    return render_template('shop/orders.html', user=current_user, orders=orders)

@shop.route("/update_order/<order_id>", methods=["POST"])
@login_required
def update_order(order_id):
    if not current_user.is_manufacturer:
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("shop.orders"))
    new_status = request.form["status"]
    mongo.db.orders.update_one({"_id": order_id}, {"$set": {"status": new_status}})
    flash("Order updated!", "info")
    return redirect(url_for("order_history"))


@shop.route('/analytics')
def analytics():
    return render_template('shop/analytics.html', user=current_user)

@shop.route('/reports')
def reports():
    return render_template('shop/reports.html', user=current_user)

@shop.route('/review')
def review():
    return render_template('shop/review.html', user=current_user)

