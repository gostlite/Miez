# create user model class
from werkzeug.security import generate_password_hash
from datetime import datetime
from miez_app import client
from bson.objectid import ObjectId
from pydantic import BaseModel , Field
# import http



# def create_app():
    # return app

# client = MongoClient("mongodb+srv://mrjohnsoft:tEkuXpWYs8UJHHc2@cluster0.b8d55ly.mongodb.net/?retryWrites=true&w=majority")
# db = client.get_database('miez')
# db = client.db
# print(list(db))
# subscribe = client.get_database('subscribe')
# print(list(db.users.find()))

User = dict(first_name='',
       last_name='',
        email='',
         username='',
          password='',
           admin=False)

Subscription = dict(

    person_id = '',
    subcribe = False,
    plan = '',
    date_started = datetime.utcnow(),
    # date_end = (datetime(int(datetime.now())) + 2592000)
    )

Appointment= dict(
    person_id = '',
    time = datetime.now(),
    plan ='' )
def get_dict():
    return dict(email='',
         username='')


# db.users.insert_one(test)

##CREATE DATABASE
#Optional: But it will silence the deprecation warning in the console.
# def validate_user(username):
#     client.users.






# class User(UserMixin,db.Document):
#     # id = db.String(db.Integer, primary_key=True)
#     _id = ObjectId (primary_key=True)
#     first_name = db.Column(db.String(250), unique=True, nullable=False)
#     last_name = db.Column(db.String(250), nullable=False)
#     email = db.Column(db.String(80),unique=True, nullable=False)
#     username = db.Column(db.String(120),unique=True, nullable=False)
#     password = db.Column(db.String(250), nullable=False)
#     admin = db.Column(db.Boolean, default=False, nullable=True)
#     subscriptions = db.relationship('Subscription', backref='user', lazy=True)
   


class User1(BaseModel):
    # id: str = Field(default_factory=uuid.uuid4, alias="_id")    # _id = ObjectId(primary_key=True)
    first_name: str = Field()
    last_name : str = Field()
    email : str = Field(unique=True)
    prof_pic : str = Field(default='default.png')
    username : str = Field(unique=True)
    password : str = Field()
    admin: bool = Field(default=False, nullable=True)

    def __repr__(self):
        return f'{self.username} has been created'

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "first_name": "Don",
                "last_namer": "Quixote",
                "email": "mail@mail.com",
                "username": "dove234",
            }
        }
    # subscriptions = db.relationship('Subscription', backref='user', lazy=True)
#     #Optional: this will allow each book object to be identified by its title when printed.
#     def __repr__(self):
#         sub = "Subcribed" if self.subscribe else "Not subscribed"
#         return f"<Miez User {self.username}"


 
# class Subscription(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     person_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
#     subcribe = db.Column(db.Boolean, default=False, nullable=True)
#     plan = db.Column(db.String(250), nullable=False)
#     date_started = db.Column(db.String(250), nullable=False)

# db.create_all()




class Myuser:
    _username = ''
    # _password = ''
    _subscribed = False
    email = ''
    admin = False
    def __init__(self,userName, email, password):
        self._username = userName
        self.email = email
        self._password = password

    """check if paswword matches"""
   

    @property 
    def password(self):
        return self._password
    
    @password.setter
    def password(self,val):
        self._password = val
        
        # print(val)
        






    
        

 
    # def user_details(self):
    #     return self.__owner



# """The views"""
# def home(render, page):
#     return render_(page)
