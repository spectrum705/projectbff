from flask_login import UserMixin
from message import db, login_manager
import random
# from bson.objectid import ObjectId
import uuid

@login_manager.user_loader
def load_user(user_id):
    return User.objects(myid=int(user_id)).first()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    partner = db.StringField(required=True)
    password = db.StringField(required=True)
    mobile = db.StringField(required=True)
    # _id = ObjectId()#db(required=True,unique=True, default=str(random.randint(1,10000)))
    # myid= db.IntField(db_field='id',unique=True,required=True,default=(random.randint(1,10000)))
    # print uuid.uuid4()
    myid= db.StringField(db_field='id',unique=True,required=True,default=str(uuid.uuid4()))
  
    def to_json(self):
        return {
            "username":self.username,
            "password":self.password,
            "id":self.myid,
            "partner": self.partner
        }
    def __repr__(self):
        return f"User('{self.username}','{self.myid}',{self.partner})"

class Letters(db.Document):
    title=  db.StringField(required=True)
    content = db.StringField(required=True)
    # author = db.ReferenceField(User, dbref=True)  
    author = db.StringField(required=True)
    status = db.StringField(required=True) #draft/sent/seen
    # status = db.StringField()
    timestamp = db.StringField()#default=now)
    myid= db.StringField(db_field='id',unique=True,required=True,default=str(uuid.uuid4()))
    
    # generating random id for each letter
    # _id = db.IntField()


    def to_json(self):
        return {
            "author":self.author,
            "title":self.title,
            "timestamp": self.timestamp,
            # "id": self.myid
            
            # "time":self.timestamp
        }
    def __repr__(self):
        return f"Letters('{self.author}','{self.myid}',{self.timestamp}, {self.title}, {self.status})"




# print(user.get_user("spec"))
# import pytz     
# from datetime import datetime  
# asiaTime= pytz.timezone('Asia/Kolkata')   
# datetime_ind = datetime.now(asiaTime)  
# timeStamp = datetime_ind.strftime("%Y-%m-%d %H:%M:%S.%f")

# dates=["23:40, 19-09-2021", "23:41, 19-09-2021", "04:55, 20-09-2021","00:08, 20-01-2021", "00:01, 21-09-2021","06:17, 20-09-2021"]