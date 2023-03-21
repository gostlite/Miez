from flask import render_template,redirect, url_for, flash, request
from flask_login import login_user,login_required, current_user, logout_user, UserMixin
from bson.objectid import ObjectId
from miez_app.forms import RegisterForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, BookingForm
from miez_app import app,bcrypt,login_manager, user_db, mail, user_bk, user_not
from miez_app.model import User1,  Booking
from datetime import datetime, timedelta, timezone
from jwt import encode, decode, exceptions
import os
import secrets
from PIL import Image
from flask_mail import Message



"""Giving a Usermixin structure to the mongodb str data to work with login manager"""
class MyUser(UserMixin):
    def __init__(self, user_json):
        super().__init__()
        self.user_json = user_json

    def get_id(self):
        object_id = self.user_json.get('_id')
        return str(object_id)
    
    def get_reset_token(self, expires_min=10):
        now = datetime.now(timezone.utc)
        token = encode({'user_id':str(self.get_id()), 'exp':datetime.timestamp(now + timedelta(minutes=expires_min))},app.config["SECRET_KEY"],"HS256")
        print(token)
        print(f"decoded token: {decode(token,app.config['SECRET_KEY'],'HS256')}")
        return token

    @staticmethod
    def verify_reset_token(token):
        now = datetime.timestamp(datetime.now(timezone.utc))
        decoded = decode(token,app.config['SECRET_KEY'],'HS256')
        print(decoded)
        try:
            user_id = decoded['user_id']
            if now > decoded['exp']:
                return None
        except BaseException:
            return None
        return user_id

    def __repr__(self):
        return f"User('{self.user_json['username']}', '{self.user_json['email']}, '{self.user_json['prof_pic']}'')"
    




def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



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
            current_user.user_json["prof_visit"] = int( current_user.user_json["prof_visit"]) + 1
            user_db.find_one_and_update({"_id":user["_id"]}, {"$set":{"prof_visit": current_user.user_json["prof_visit"]}})
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


@app.route('/profile',methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user.user_json
    form = UpdateAccountForm()
    form.username.data = user.get('username')
    form.email.data = user.get('email')
    if form.validate_on_submit:
        # change/ update profile pic
        if form.img.data:
            user['prof_pic'] = save_picture(form.img.data)
            user['username'] = form.username.data
            user["email"] = form.email.data

            user_db.find_one_and_update({'_id':ObjectId(user.get('_id'))},
                                        {'$set': {'email':form.email.data,
                                        'username':form.username.data,"prof_pic":user["prof_pic"]}})
            flash("succefully updated your profile", 'success')
            return redirect(url_for('dashboard'))
     
    print('-----this is the user')
    myImg = url_for('static', filename='profile_pics/'+ user.get('prof_pic'))
    try:
        approved_appointment_list = user_bk.find({"user_id":user['_id']}, {"approved":True})
    except:
        pass
    
    # print(user.get('prof_pic'))
    return render_template('pages/profile.html', img=myImg, form=form, approved=approved_appointment_list) 


@app.route('/map')
@login_required
def map():
    return render_template('pages/map.html')

@app.get('/appointments')
@login_required
def appointment():
    # "accepted":True
    user = current_user.user_json
    try:
        mylist = user_bk.find({"user_id":user["_id"]})
    except BaseException:
        pass
    return render_template('pages/appointment.html', aList=mylist)


@app.get('/notifications')
@login_required
def notification():
    # "accepted":True
    user = current_user.user_json
    try:
        mylist = user_not.find({"user_id":user["_id"]})
    except BaseException:
        pass
    return render_template('pages/notifications.html', aList=mylist)

@app.route('/booking',methods=['GET', 'POST'])
@login_required
def booking():
    user = current_user.user_json
    form = BookingForm()
    # checking the free user
    if user['subscribe'] != "Free" :
        if form.validate_on_submit():    
            bookingsValid(form, user)
            return redirect(url_for('dashboard'))
        return render_template('pages/bookingForm.html', form = form)
    elif user['subscribe']  == 'Free' and int(user['trials']) > 0:
        if form.validate_on_submit():    
            bookingsValid(form, user)
            trials = int(user['trials'])-1
            user['trials'] = trials
            user_db.find_one_and_update({"_id":ObjectId(user['id'])}, {'$set':{"trials":trials}})
            return redirect(url_for('dashboard'))
    flash("Sorry your free trials is exausted, kindly select a plan to enjoy our services", 'danger')
    return redirect(url_for('payment'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = user_db.find_one({'email':form.email.data})
        if not user:
            flash("User was not found, kindly register")
            return redirect(url_for('register'))
        cur_user = MyUser(user)
        send_email(cur_user)
        flash('An email has been sent to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('request_reset.html', form=form)


@app.route('/subscribe')
@login_required
def subscribe():
    return render_template('pages/subscribe.html')

@app.route('/reset_password/<token>',methods=["Get", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    try:
        user_id = MyUser.verify_reset_token(token)
    except (exceptions.ExpiredSignatureError, BaseException):
        user_id = None

    if user_id is None:
        flash('Sorry you have entered an invalid or expired token')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        new_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user_db.find_one_and_update({'_id':ObjectId(str(user_id))},{'$set':{
            "password":new_password
        }})
        return redirect(url_for('login'))
    return render_template('request_token.html', form=form)
 

@app.route('/payment')
@login_required
def payment():
    return render_template('pages/billing.html')

@app.get('/logout')
def logout():
    # add a profile visit increment here
    logout_user()
    return redirect(url_for('home'))


def send_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset Email', recipients=['mrjohn.soft@gmail.com'],sender='support@myhbsconline.com',body= f'''Kindly click on this link
        {url_for('reset_token', token=token, _external=True)}
        to reset your password''')

    mail.send(msg)


def bookingsValid(form, user):
    
    new_booking =Booking(time= form.time.data,
                        date=form.date.data,
                        services=form.services.data,
                        address=form.address.data,details=form.details.data)
    user_bk.insert_one(new_booking)
    flash(f"A new booking has been made for {form.date.data} by {form.time.data}, kindly keep checking your appointment page to see when it is approved")
    #link the bookings to the user
    #increase bookings
    user["booking"] = int(user["booking"]) + 1
    user_db.find_one_and_update({"_id":user["_id"]}, {"$set":{"booking":user["booking"]}})
            