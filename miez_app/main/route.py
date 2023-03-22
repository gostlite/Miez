from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint("main", __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('landingPage.html')




@main.route('/map')
@login_required
def map():
    return render_template('pages/map.html')


