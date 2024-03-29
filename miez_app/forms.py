from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TimeField, DateField, FieldList,SelectField, FormField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_login import current_user

from miez_app import user_db


class RegisterForm(FlaskForm):
    fname = StringField('First Name',validators=[DataRequired()])
    lname = StringField('Last Name',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password',validators=[DataRequired(), EqualTo('password')])
    submit  = SubmitField('Join us')

    def validate_username(self, username):
        user = user_db.find_one({'username':username.data})
        if user:
            raise ValidationError('Username already exists, please use another')
        
    def validate_email(self, email):
        user = user_db.find_one({'username':email.data})
        if user:
            raise ValidationError('Email already exists, please use another')



class LoginForm(FlaskForm):
    
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')
    


class UpdateAccountForm(FlaskForm):
    # fname = StringField('First Name',validators=[DataRequired()])
    # lname = StringField('Last Name',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    img = FileField(label='profile_pic', validators=[FileAllowed(['jpg','png'])])
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit  = SubmitField('update')

    def validate_username(self, username):
        if username.data != current_user.get('user_json').get('username'):
            user = user_db.find_one({'username':username.data})
            if user:
                raise ValidationError('Username already exists, please use another')
        
    def validate_email(self, email):
        if email.data != current_user.get('user_json').get('email'):
            user = user_db.find_one({'email':email.data})
            if user:
                raise ValidationError('Email already exists, please use another')
            

class RequestResetForm(FlaskForm):
        email = StringField('Email',
                        validators=[DataRequired(), Email()])
        submit = SubmitField('Request Password Reset')

        def validate_email(self, email):
            user = user_db.find_one({'email':email.data})
            if user is None:
                raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class BookingForm(FlaskForm):
    time = TimeField('Time')
    date = DateField('Date')
    services= SelectField(label='services', choices=["nailbar", "haircut/hairsaloon", "facials", "tatooing"], validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired("Please put in an address")])
    details = TextAreaField('Anything else')
    submit = SubmitField('Submit')
