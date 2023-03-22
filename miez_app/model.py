# create user model class
from datetime import datetime, timedelta, timezone
from miez_app import client, user_db
from miez_app import login_manager,app
from bson.objectid import ObjectId
from pydantic import BaseModel , Field
from jwt import encode, decode, exceptions
from flask_login import UserMixin
   


class User1(BaseModel):
    # id: str = Field(default_factory=uuid.uuid4, alias="_id")    # _id = ObjectId(primary_key=True)
    first_name: str = Field()
    last_name : str = Field()
    email : str = Field(unique=True)
    prof_pic : str = Field(default='default.png')
    username : str = Field(unique=True)
    password : str = Field()
    booking : int = Field(default=0) 
    appointment : int = Field(default=0) 
    prof_visit : int = Field(default=0) 
    membership : str = Field(default="Free")
    trials : int = Field(default=3)
    admin: bool = Field(default=False, nullable=True)
    num_of_visit: int = Field(default=0, nullable=True)

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

now = datetime.now(timezone.utc)
class Member(BaseModel):
    plan: str = Field()
    time_paid : int = Field(now)
    exp : int = Field(datetime.timestamp(now + timedelta(days=30)))


class Booking(BaseModel):  
    user_id :str= Field()
    time: str = Field()
    date : str = Field()
    services: str = Field()
    address : str = Field()
    details : str = Field()
    accepted : bool = Field(default=False)

  
class Notication(BaseModel):
    user_id: str = Field()
    title: str = Field()
    message: str = Field()

@login_manager.user_loader
def load_user(user_id):
    user = user_db.find_one({"_id":ObjectId(user_id)})
    return MyUser(user)


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
    
