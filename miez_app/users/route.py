from flask import Blueprint, render_template,flash, redirect, url_for, request
from miez_app.model import MyUser, exceptions, User1
from miez_app.forms import LoginForm, RegisterForm, ResetPasswordForm, UpdateAccountForm, RequestResetForm
from flask_login import login_user,login_required, current_user, logout_user
from miez_app.util import save_picture, send_email
from miez_app import bcrypt, user_db, user_bk
from bson.objectid import ObjectId

users = Blueprint("users", __name__)

@users.route('/subscribe')
@login_required
def subscribe():
    return render_template('pages/subscribe.html')

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = user_db.find_one({'email':form.email.data})
        if not user:
            flash("User was not found, kindly register")
            return redirect(url_for('users.register'))
        cur_user = MyUser(user)
        send_email(cur_user)
        flash('An email has been sent to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('request_reset.html', form=form)

@users.route('/reset_password/<token>',methods=["Get", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    try:
        user_id = MyUser.verify_reset_token(token)
    except (exceptions.ExpiredSignatureError, BaseException):
        user_id = None

    if user_id is None:
        flash('Sorry you have entered an invalid or expired token')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        new_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user_db.find_one_and_update({'_id':ObjectId(str(user_id))},{'$set':{
            "password":new_password
        }})
        return redirect(url_for('users.login'))
    return render_template('request_token.html', form=form)
 

@users.route('/payment')
@login_required
def payment():
    return render_template('pages/billing.html')

@users.get('/logout')
def logout():
    # add a profile visit increment here
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/Miez-sign-up', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    if form.validate_on_submit():
        username = form.username.data
        #add logic to go back if uaername exist 
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
   
        
        myuser = User1(first_name=form.fname.data,last_name=form.lname.data,username=username, email= form.email.data, password=hashed_password )
        user_db.insert_one(myuser.__dict__)

        flash('Successfully created account Created for you', 'success') 
        return redirect(url_for('users.login'))
    return render_template('sign-up.html', form=form)

@users.route('/sign-in',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    
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
            return redirect(url_for(next_page)) if next_page else redirect(url_for('users.dashboard'))
        else:
            return redirect(url_for('users.login'))
    return render_template('sign-in.html', form=form)

@users.route('/miez-membership')
def membership():
    return render_template('membership.html')


@users.route('/dashboard')
@login_required
def dashboard():
    user = current_user.user_json
    try:
        mylist = list(user_bk.find({"user_id":str(user["_id"]), "accepted":True}))
    except BaseException:
        pass
    return render_template('pages/dashboard.html', bookings=mylist)


@users.route('/profile',methods=['GET', 'POST'])
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
            return redirect(url_for('users.dashboard'))
     
    myImg = url_for('static', filename='profile_pics/'+ user.get('prof_pic'))
    try:
        approved_appointment_list = user_bk.find({"user_id":user['_id']}, {"approved":True})
    except:
        pass
    
    # print(user.get('prof_pic'))
    return render_template('pages/profile.html', img=myImg, form=form, approved=approved_appointment_list) 