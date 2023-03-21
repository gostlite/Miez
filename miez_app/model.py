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