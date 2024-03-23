from flask_login import UserMixin
import random
# from bson.objectid import ObjectId
import uuid
import mongoengine as db
import os
from dotenv import load_dotenv
import base64
from jobs import make_stamp, compress_image
load_dotenv()

DB_URI = os.getenv('DB_URI') or os.environ["DB_URI"]



db.connect(host=DB_URI)


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    
    partners = db.ListField(db.StringField())
    password = db.StringField(required=True)
    # birthday = db.DateField(require=True)
    public_key = db.StringField(required=True)
    private_key = db.StringField(required=True)
    backup_key = db.StringField(required=True)
    
    mobile = db.StringField()
    email = db.StringField(unique=True)
    friend_code = db.StringField( unique=True)
    
    myid= db.IntField(db_field='id',primary_key=True, required=True,default=(random.randint(1,10000)))
    
    
    
    
        
        
        
    @staticmethod
    def isVerified(username):
        usr=User.objects(username=username).first()
        print(usr.friend_code)
        if usr.friend_code:
            return True
        else: 
            return False
        
    @staticmethod
    def FindUserByName(username):
        usr=User.objects(username=username).first()
        return usr 
    @staticmethod
    def FindUserByEmail(email):
        usr=User.objects(email=email).first()
        return usr 
    
    def AddFriend(my_username,friends_Code):
        friend = User.objects(friend_code=friends_Code).first()
        user = User.objects(username=my_username).first()
        print(">>",user.partners)        
        if friend and (friend.username not in user.partners) and (friend!=user):
            user.partners.append(friend.username)
            friend.partners.append(user.username)
            user.save()
            friend.save()
            return True, friend.username           
        else:
            return False, None

    def to_json(self):
        return {
            "username":self.username,
            "email":self.email,
            "id":self.myid,
        }
    def __repr__(self):
        return f"User('{self.username}','{self.myid}',{self.partners})"


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
    # stamp_url = db.StringField()
    stamp = db.FileField() #see if we need to add default size limit
    
    myid= db.StringField(db_field='id',primary_key=True, required=True,default=str(uuid.uuid4()))
    
    
    
    
    @staticmethod
    def UserLetterBox(user):
        sortedLetters=sorted(Letters.objects(Q(receiver=user) & (Q(status="sent") | Q(status="read"))), key=lambda letters: datetime.strptime( letters.timestamp, "%H:%M, %d-%m-%Y"), reverse=True)
        return sortedLetters
    
    
    @staticmethod
    def Write(letter_data):
        if type(letter_data['enc_content']) is str:
            enc_content = base64.b64decode(letter_data['enc_content'])
        elif type(letter_data['enc_content']) is bytes:
            enc_content=letter_data['enc_content']
      
        
                # encrypt_symmetric_key = base64.b64decode(letter_data['encrypt_symmetric_key'])
        stamp_url = make_stamp(letter_data["letter_title"])
        print(type(stamp_url))
        stamp_url = compress_image(stamp_url)
        grid_fs_proxy = db.fields.GridFSProxy()
        grid_fs_proxy.put(stamp_url)
        letter_id= str(uuid.uuid4())
        # print(f"name{letter_data['letter_title']}")
        
        letter=Letters(title=letter_data["letter_title"],
                    content=enc_content   ,
                    symmetric_key=letter_data["encrypted_symmetric_key"],
                    author=letter_data["author"],
                    receiver=letter_data["receiver"],
                    status="sent",
                    timestamp=letter_data["timestamp"], 
                    myid=letter_id,
                    stamp=grid_fs_proxy
                    )

        letter.save()
        print( "TASK FINISHED!! ")
        return letter_id
    @staticmethod
    def AddImage(image_data_list, letter_id):
        letter= Letters.objects(myid=letter_id).first()
        for encoded_image in image_data_list:
        # Decode base64 encoded image data
            if type(encoded_image) is str:
                image_data = base64.b64decode(encoded_image)
            elif type(encoded_image) is bytes:
                image_data = encoded_image

            grid_fs_proxy = db.fields.GridFSProxy()

            grid_fs_proxy.put(image_data)
            letter.images.append(grid_fs_proxy)
        letter.attachment = True
        letter.save()# add images here
        return True






    @staticmethod
    def FindLetter(id):
        toRead= Letters.objects(myid=id).first()
        return toRead

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
