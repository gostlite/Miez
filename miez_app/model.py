# create user model class
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone
from miez_app import client
from bson.objectid import ObjectId
from pydantic import BaseModel , Field
   


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
    time_paid : int = Field(datetime.timestamp(now + timedelta(minutes=30)))
    exp : int = Field()
    
#     id = db.Column(db.Integer, primary_key=True)
#     person_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
#     subcribe = db.Column(db.Boolean, default=False, nullable=True)
#     plan = db.Column(db.String(250), nullable=False)
#     date_started = db.Column(db.String(250), nullable=False)
