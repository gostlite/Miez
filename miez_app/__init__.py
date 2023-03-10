from flask import Flask
from flask_bcrypt import Bcrypt
# from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask_login import LoginManager
from dotenv import dotenv_values

app = Flask(__name__)
# print(dotenv_values('.env').get('SECRET_KEY'))
app.config["SECRET_KEY"] = dotenv_values('.env').get('SECRET_KEY')
app.config['MONGO_URI']= dotenv_values('.env').get('MONGO_URI')
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
client = PyMongo(app)
user_db = client.db.users
from miez_app import route
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

