from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from miez_app import client


class RegisterForm(FlaskForm):
    fname = StringField('First Name',validators=[DataRequired()])
    lname = StringField('Last Name',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password',validators=[DataRequired(), EqualTo('password')])
    submit  = SubmitField('Join us')

    def validate_username(self, username):
        user = client.users.find_one({'username':username})
        if user:
            raise ValidationError('Username already exists, please use another')
        
    def validate_email(self, email):
        user = client.users.find_one({'username':email})
        if user:
            raise ValidationError('Email already exists, please use another')



class LoginForm(FlaskForm):
    
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')
    