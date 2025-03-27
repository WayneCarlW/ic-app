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
        return redirect(url_for('shop.home'))
    products = db.products.find()
    products_list = list(products)
    return render_template('shop/shelf.html', user=current_user, products=products_list)

@shop.route('/cart/<product_id>', methods=['GET', 'POST'])
@login_required
def add_to_cart(product_id):
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
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
    return redirect(url_for('shop.view_cart'))

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


@shop.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items_cursor = mongo.db.cart.find({"user_id": current_user.id})  
    cart_items = list(cart_items_cursor)  # Convert cursor to list

    if not cart_items:
        flash('No items in cart!', 'danger')
        return redirect(url_for('shop.view_cart'))

    total = sum(item["price"] * item["quantity"] for item in cart_items)  

    if request.method == "POST":
        order_data = {
            "user_id": current_user.id,  # Store user ID for reference
            "items": cart_items,  # Use the converted list
            "total": total,
            "status": "pending",
            "created_at": datetime.now()
        }

        mongo.db.orders.insert_one(order_data)  # Insert into orders collection
        mongo.db.cart.delete_many({"user_id": current_user.id})  # Clear user's cart

        flash('Order placed successfully!', 'success')
        return redirect(url_for('shop.orders_func'))

    return render_template('shop/checkout.html', user=current_user, cart_items=cart_items, total=total)

@shop.route('/myorders')
@login_required
def orders_func():
    db = get_mongo_db()
    if db is None:
        flash('Database connection error.', 'danger')
        return redirect(url_for('shop.home'))
    
    user_orders = list(db.orders.find({"user_id": current_user.id}))

    if not user_orders:
        flash("You have no orders yet.", "info")

    return render_template('shop/orders.html', user=current_user, orders=user_orders)


@shop.route("/update_order/<order_id>", methods=["POST"])
@login_required
def update_order(order_id):
    if not current_user.is_manufacturer:
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("shop.orders_func"))
    new_status = request.form["status"]
    mongo.db.orders.update_one({"_id": order_id}, {"$set": {"status": new_status}})
    flash("Order updated!", "info")
    return redirect(url_for("order_history"))


@shop.route('/analytics')
def analytics():
    flagged_products_count = mongo.db.products.count_documents({"flags": {"$gt": 0}})
    total_products_count = mongo.db.products.count_documents({})
    farmers_count = mongo.db.users.count_documents({"role": "farmer"})
    manufacturers_count = mongo.db.users.count_documents({"role": "manufacturer"})

    return render_template(
        'shop/analytics.html',
        user=current_user,
        flagged_products_count=flagged_products_count,
        total_products_count=total_products_count,
        farmers_count=farmers_count,
        manufacturers_count=manufacturers_count
    )
@shop.route('/reports')
def reports():
    return render_template('shop/reports.html', user=current_user)

@shop.route('/flag_product/<product_id>', methods=['POST'])
@login_required
def flag_product(product_id):
    order = mongo.db.orders.find_one({
        "user_id": current_user.id,
        "items.product_id": product_id
    })
    if not order:
        flash("You can only flag products you have purchased.", "danger")
        return redirect(url_for('shop.orders_func'))

    mongo.db.reviews.insert_one({
        "product_id": ObjectId(product_id),
        "user_id": current_user.id,
        "flagged": True,
        "comment": request.form.get("comment", ""),
        "created_at": datetime.now()
    })
    
    mongo.db.products.update_one(
        {"_id": ObjectId(product_id)},
        {"$inc": {"flags": 1}}
    )

    flash("Product flagged successfully.", "warning")
    return redirect(url_for('shop.orders_func'))

@shop.route('/flagged_products')
@login_required
def flagged_products():
    if not current_user.is_manufacturer or not current_user.is_admin:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('shop.home'))
    
    flagged_products = mongo.db.products.find({"flags": {"$gt": 0}})
    return render_template('shop/flagged_products.html', products=flagged_products, user=current_user)

@shop.route('/resolve_flag/<product_id>', methods=['POST'])
@login_required
def resolve_flag(product_id):
    if not current_user.is_manufacturer:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('shop.home'))

    action = request.form.get("action")

    if action == "remove":
        mongo.db.products.delete_one({"_id": ObjectId(product_id)})
        mongo.db.reviews.delete_many({"product_id": ObjectId(product_id)})
        flash("Product removed successfully.", "success")

    elif action == "respond":
        response = request.form.get("response")
        mongo.db.reviews.update_many(
            {"product_id": ObjectId(product_id), "flagged": True},
            {"$set": {"manufacturer_response": response}}
        )
        flash("Response added successfully.", "info")

    return redirect(url_for('shop.flagged_products'))

@shop.route('/review_stats')
def review_stats():
    db = get_mongo_db()
    if db is None:
        flash('Database connection error.', 'danger')
        return redirect(url_for('shop.home'))

    # Count flagged products
    flagged_count = db.products.count_documents({"flags": {"$gt": 0}})

    # Calculate average rating
    ratings = list(db.reviews.find({}, {"rating": 1}))
    if ratings:
        avg_rating = sum(rating["rating"] for rating in ratings if "rating" in rating) / len(ratings)
    else:
        avg_rating = None  # No ratings available

    return render_template('shop/review_stats.html', flagged_count=flagged_count, user=current_user, avg_rating=avg_rating)


@shop.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '').strip()
    db = get_mongo_db()
    if db is None:
        flash('Database connection error.', 'danger')
        return redirect(url_for('shop.home'))

    products = []
    if query:
        products = db.products.find({"name": {"$regex": query, "$options": "i"}})
    else:
        products = db.products.find()

    products_list = list(products)
    return render_template('shop/shelf.html', user=current_user, products=products_list, query=query)