from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user

dash = Blueprint('dash', __name__, template_folder='templates')

@dash.route('/')
def index():
    return render_template('dashboard/dash.html', user=current_user)
