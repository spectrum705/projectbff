from flask_login import UserMixin
from message import db, login_manager
import random
# from bson.objectid import ObjectId
import uuid
from wtforms import StringField

@login_manager.user_loader
def load_user(user_id):
    return User.objects(myid=int(user_id)).first()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    
    partners = db.ListField(db.StringField())
    password = db.StringField(required=True)
    # birthday = db.DateField(require=True)
    public_key = db.StringField(required=True)
    private_key = db.StringField(required=True)
    mobile = db.StringField()
    email = db.StringField(unique=True)
    friend_code = db.StringField(required=True, unique=True)
    # _id = ObjectId()#db(required=True,unique=True, default=str(random.randint(1,10000)))
    myid= db.IntField(db_field='id',primary_key=True, required=True,default=(random.randint(1,10000)))
    # print uuid.uuid4()
    # myid= db.StringField(db_field='id',unique=True,required=True,default=str(uuid.uuid4()))
    # _id=db.IntField(db_field='id', required=True,default=(random.randint(1,10000)))

    def to_json(self):
        return {
            "username":self.username,
            "password":self.password,
            "id":self.myid,
            "partner": self.partners
        }
    def __repr__(self):
        return f"User('{self.username}','{self.myid}',{self.partners})"


# images = fs.Storage('images', fs.IMAGES,
#                     upload_to=lambda o: 'prefix',
#                     basename=lambda o: 'basename')
class Letters(db.Document):
    title=  db.StringField(required=True)
    content = db.StringField(required=True)
    author = db.StringField(required=True)
    receiver = db.StringField(required=True)
    status = db.StringField(required=True) #draft/sent/seen
    timestamp = db.StringField()#default=now)
    symmetric_key = db.StringField()
    attachment= db.BooleanField(required=True, default=False)
    images = db.ListField(db.FileField()) #see if we need to add default size limit
    # images = db.FileField()
    myid= db.StringField(db_field='id',primary_key=True, required=True,default=str(uuid.uuid4()))

    
    # generating random id for each letter
    # _id = db.IntField()


    def to_json(self):
        return {
            "author":self.author,
            "title":self.title,
            "timestamp": self.timestamp,
            "status": self.status,
            "receiver":self.receiver,
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

#How to add new user
#do inside main.py
# from message.models import User, Letter
# new=User(username='kirito',partner='asuna',password='test')
# new.save()

# letter=Letters(title=form.title.data, 
#             content=form.content.data,
#             author=current_user["username"],
#             status="sent", myid=str(uuid.uuid4()) ,timestamp=now,
#             receiver=selected_partner)
# l=Letters(title="test",content="test",author="test",receiver="test",status="test",timestamp="test",myid="test")
