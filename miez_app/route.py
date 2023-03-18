from flask import render_template,redirect, url_for, flash, request
from flask_login import login_user,login_required, current_user, logout_user, UserMixin
from bson.objectid import ObjectId
from miez_app.forms import RegisterForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, BookingForm
from miez_app import app,bcrypt,login_manager, user_db, mail, jwt
from flask_jwt_extended import create_access_token, get_jwt_identity
from miez_app.model import User1
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
import os
import secrets
from PIL import Image
from flask_mail import Message


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
    
    def get_reset_token(self, expires_sec=50):
        # s = Serializer(app.config['SECRET_KEY'], expires_sec)
        # return s.dumps({'user_id': self.get_id()}).decode('utf-8')
        token = create_access_token(identity=self.get_id(),expires_delta=int(datetime.strftime(datetime.now())) + expires_sec).encode('utf-8')
        print(token)
        return token

    # @staticmethod
    # def verify_reset_token(self,token):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except:
    #         return None
    #     user = user_db.find_one({'_id':ObjectId(user_id)})
    #     return MyUser(user)

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
    print(current_user.user_json['prof_pic'])
    # print(current_user.prof_pic)
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


@app.route('/booking',methods=['GET', 'POST'])
@login_required
def booking():
    form = BookingForm()
    if form.validate_on_submit:
        print(form.data)
        pass
    return render_template('pages/bookingForm.html', form = form)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = user_db.find_one({'email':form.email.data})
        if not user:
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

@app.route('/reset_password/<token>')
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    user = MyUser.get_reset_token(token)
    if user is None:
        flash('Sorry you have entered an invalid or expired token')
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    # return render_template('')
 

@app.route('/payment')
@login_required
def payment():
    return render_template('pages/billing.html')

@app.get('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def send_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset Email', recipients=['mrjohn.soft@gmail.com'],sender='support@myhbsconline.com',body= f'''Kindly click on this link
        {url_for('reset_token', token=token)}
        to reset your password''')

    print(mail.send(msg))


