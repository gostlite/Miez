from flask import render_template,redirect, url_for, flash, request
from flask_login import login_user,login_required, current_user, logout_user, UserMixin
from bson.objectid import ObjectId
from miez_app.forms import RegisterForm, LoginForm, UpdateAccountForm
from miez_app import app,bcrypt,login_manager, user_db
from miez_app.model import User, Subscription, Appointment, User1
from datetime import datetime
import json
import os
import secrets



# db = client.get_database('miez')
# subscribe = client.get_database('subscribe')

"""Giving a Usermixin structure to the mongodb str data to work with login manager"""
class MyUser(UserMixin):
    def __init__(self, user_json):
        super().__init__()
        self.user_json = user_json

    def get_id(self):
        object_id = self.user_json.get('_id')
        return str(object_id)



def save_pic(pic):
    randomh = secrets.token_hex(8)
    _, fext = os.path.splitext(pic)
    fname = randomh + fext
    file_path = os.path.join(app.root_path, 'static/profile_pic', fname)
    pic.save(file_path)
    return fname



@login_manager.user_loader
def load_user(user_id):
    user = user_db.find_one({"_id":ObjectId(user_id)})
    return MyUser(user)



@app.route('/')
@app.route('/home')
def home():
    return render_template('landingPage.html')

@app.route('/Miez-sign-up', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if form.validate_on_submit():
        username = form.username.data
        #add logic to go back if uaername exist 
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # new_user = User.copy()
        # new_user['first_name']=form.fname.data
        # new_user['last_name']=form.lname.data
        # new_user['username']=username
        # new_user['email']=form.email.data
        # new_user['password']=hashed_password
        
        myuser = User1(first_name=form.fname.data,last_name=form.lname.data,username=username, email= form.email.data, password=hashed_password )
        user_db.insert_one(myuser.__dict__)

        flash('Successfully created account Created for you', 'success') 
        return redirect(url_for('login'))
    return render_template('sign-up.html', form=form)

@app.route('/sign-in',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = user_db.find_one({'username':form.username.data})
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            flash('Successfully logged in', 'success') 
            userlogin = MyUser(user)
            login_user(user=userlogin, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for(next_page)) if next_page else redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))
    return render_template('sign-in.html', form=form)

@app.route('/miez-membership')
def membership():
    return render_template('membership.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('pages/dashboard.html')


@app.route('/profile')
@login_required
def profile():
    user = current_user.__dict__.get('user_json')
    print(user.get('_id'))
    form = UpdateAccountForm()
    form.username.data = user.get('username')
    form.email.data = user.get('email')
    if form.validate_on_submit:
        if form.img.data:
            user['prof_pic'] = save_pic(form.img.data)
        # user_db.find_one_and_replace({'_id':ObjectId(user.get('_id')),
        #                              'email':form.email.data,
        #                              'username':form.username.data})
        user['username'] = form.username.data
        user['email'] = form.email.data
    print('-----this is the user')
    myImg = url_for('static', filename='profile_pics/'+ user.get('prof_pic'))
    # print(user.get('prof_pic'))
    return render_template('pages/profile.html', img=myImg, form=form) 


@app.route('/map')
@login_required
def map():
    return render_template('pages/map.html')

@app.get('/appointments')
@login_required
def appointment():
    return render_template('pages/appointment.html')


@app.get('/booking')
@login_required
def booking():
    return render_template('pages/bookingForm.html')

@app.get('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))