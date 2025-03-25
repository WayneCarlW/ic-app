from flask import Blueprint, render_template, url_for, redirect, request, flash,send_file, Response
import io
import gridfs
from flask_login import current_user, login_required
from bson import ObjectId, Binary
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
            file = request.files['image']
            if file.filename == '':
                flash('No selected file', 'danger')
                return redirect(url_for('dash.profile'))
            if file:
                image_data = Binary(file.read())
            else:
                image_data = None
            print(f"File Size: {len(image_data)} bytes")
            file.seek(0)
            
            # if fs is None:
            #     flash('File storage system is not initialized.', 'danger')
            #     return redirect(url_for('dash.profile'))
            
            mongo.db.users.update_one({
                '_id': ObjectId(current_user.id)
            }, {
                '$set': {
                    'profile_pic': image_data
                }
            })
            # current_user.profile_pic = str(image_id)
            flash('Profile picture updated successfully!', 'success')
            return redirect(url_for('dash.profile'))
    user = mongo.db.users.find_one({
        '_id': ObjectId(current_user.id)
    })
    image_id = user.get('profile_pic') if user else None
    return render_template('dashboard/profile.html', user_id=image_id, user=current_user)


@dash.route('/image/<user_id>')
def get_image(user_id):
    user = mongo.db.users.find_one({
        '_id': ObjectId(user_id)
    })
    if user is None:
        return "Image not found",
    return Response(user['profile_pic'], mimetype='image/jpeg')

@login_required
@dash.route('/admin')
def admindash():
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect(url_for('auth.login'))
    
    return render_template('dashboard/dash.html', user=current_user)
