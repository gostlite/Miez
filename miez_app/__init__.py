from flask import Flask
from flask_bcrypt import Bcrypt
# from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask_login import LoginManager
from dotenv import dotenv_values
from flask_mail import Mail
from flask_jwt_extended import JWTManager

app = Flask(__name__)
# print(dotenv_values('.env').get('SECRET_KEY'))
app.config["SECRET_KEY"] = dotenv_values('.env').get('SECRET_KEY')
app.config['MONGO_URI']= dotenv_values('.env').get('MONGO_URI')
app.config['MAIL_SERVER'] = 'mail.privateemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = dotenv_values('.env').get('USERNAME')
app.config['MAIL_PASSWORD'] = dotenv_values('.env').get('PASSWORD')
app.config["JWT_SECRET_KEY"] = dotenv_values('.env').get('JWT_SECRET_KEY')
# jwt = JWTManager(app)

mail = Mail(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
client = PyMongo(app)
user_db = client.db.users
from miez_app import route
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

