from flask import render_template,redirect, url_for, flash, request
from flask_login import login_user,login_required, current_user, logout_user, UserMixin
from bson.objectid import ObjectId
from miez_app.forms import RegisterForm, LoginForm
from miez_app import app,bcrypt, client, login_manager, user_db
from miez_app.model import User, Subscription, Appointment, User1
from datetime import datetime
import json



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
        myuser = json.dumps(myuser.__dict__)
        user_db.insert_one(myuser)

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
        print(user)
        print(type(user))
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
   return render_template('pages/profile.html') 


@app.route('/map')
def map():
    return render_template('pages/map.html')

@app.get('/appointments')
def appointment():
    return render_template('pages/appointment.html')


@app.get('/booking')
def booking():
    return render_template('pages/bookingForm.html')

@app.get('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))