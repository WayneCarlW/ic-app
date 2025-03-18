from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required
from bson import ObjectId
from extensions import mongo, fs


dash = Blueprint('dash', __name__, template_folder='templates')

@login_required
@dash.route('/')
def index():
    return render_template('dashboard/dash.html', user=current_user)

@dash.route('/home')
def home():
    return "<h1>Welcome Home!</h1>"

@login_required
@dash.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        if 'image' in request.files:
            image = request.files['image']
            if image.filename == '':
                flash('No selected file', 'danger')
                return redirect(url_for('dash.profile'))
            image_id = fs.put(image, filename=image.filename)
            mongo.db.users.update_one({
                '_id': ObjectId(current_user.id)
            }, {
                '$set': {
                    'profile_pic': str(image_id)
                }
            })
            current_user.profile_pic = str(image_id)
            flash('Profile picture updated successfully!', 'success')
            return redirect(url_for('dash.profile'))
    user = mongo.db.users.find_one({
        '_id': ObjectId(current_user.id)
    })
    image_id = user.get('profile_pic') if user else None
    return render_template('dashboard/profile.html', image_id=image_id, user=current_user)

@dash.route('/image/<image_id>')
def get_image(image_id):
    image = fs.get(ObjectId(image_id))
    return image.read(), 200, {'Content-Type': 'image/jpeg'}

@login_required
@dash.route('/admin')
def admindash():
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect(url_for('auth.login'))
    
    return render_template('dashboard/dash.html', user=current_user)
