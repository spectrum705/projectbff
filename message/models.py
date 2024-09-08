from flask_login import UserMixin
from message import db, login_manager,bcrypt

import random
# from bson.objectid import ObjectId
import uuid
from mongoengine.queryset.visitor import Q
from datetime import datetime  
from message.utility import make_stamp, compress_image

import base64
from message.security import serialization, derive_user_key, generate_key_pair, decrypt_private_key, encrypt_private_key

import string


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
    backup_key = db.StringField(required=True)
    
    mobile = db.StringField()
    email = db.StringField(unique=True)
    friend_code = db.StringField( unique=True)
    verified = db.BooleanField(required=True, default=False)
    
    myid= db.IntField(db_field='id',primary_key=True, required=True,default=(random.randint(1,10000)))
    
    
#     
#     
    
    
    @staticmethod
    def Create( username, password, mobile, email,recovery_code):
        uid=random.randint(1,10000)
       
        password_hash=bcrypt.generate_password_hash(password.lower().strip(),10).decode('utf-8') 
        private_key, public_key = generate_key_pair()
        user_key= derive_user_key(password,uid)
        backup_userkey = derive_user_key(recovery_code,uid)
        backup_key = encrypt_private_key(user_key=backup_userkey,private_key=private_key)
        encrypted_private_key = encrypt_private_key(user_key=user_key,private_key=private_key)
        my_friend_code = ''.join(random.choices(string.ascii_uppercase, k=4))
        # backup_key= private_key.private_bytes(
        # encoding=serialization.Encoding.PEM,
        # format=serialization.PrivateFormat.PKCS8,
        # encryption_algorithm=serialization.BestAvailableEncryption(backup_userkey)
        #     )
        # encrypted_private_key = private_key.private_bytes(
        # encoding=serialization.Encoding.PEM,
        # format=serialization.PrivateFormat.PKCS8,
        # encryption_algorithm=serialization.BestAvailableEncryption(user_key)
        #     )
        
        new_user = User(myid=uid,
                            username=username, 
                            password=password_hash,
                            mobile=mobile,
                            email=email,                        
                            public_key=public_key.public_bytes(
                            encoding=serialization.Encoding.PEM,
                            format=serialization.PublicFormat.SubjectPublicKeyInfo
                            ).decode('utf-8'),
                            private_key=encrypted_private_key.decode('utf-8'), # Save the encrypted private key as a string
                            backup_key=backup_key.decode('utf-8'),
                            friend_code = my_friend_code
                            )

            # list_of_partners  = form.partners.data
            # print("1>>>>>>>>>", form.partners.data)

        new_user.save()
        print("üser created !!")
        return new_user
        
        
        
    @staticmethod
    def isVerified(username):
        usr=User.objects(username=username).first()
        return usr.verified        
    @staticmethod
    def FindUserByName(username):
        usr=User.objects(username=username).first()
        return usr 
    @staticmethod
    def FindUserByEmail(email):
        usr=User.objects(email=email).first()
        return usr 
    @staticmethod
    def Verify(username):
        # my_friend_code= ''.join(random.choices(string.ascii_uppercase, k=4))
        usr=User.objects(username=username).first()
        usr.verified = True
        # usr.friend_code=my_friend_code
        usr.save()
        return True 
    @staticmethod
    def ResetPassword(new_password, username,recovery_code) :
       
        user=User.objects(username=username).first()
        new_password = new_password.lower().strip()
        new_password_hash=bcrypt.generate_password_hash(new_password,10).decode('utf-8') 


        backup_userkey=derive_user_key(recovery_code.strip(),user.myid)
        # user_key=user_key.encode('utf-8')
        backup_key = user.backup_key.encode() # Convert the string to a byte string
        # private_key = user.private_key
        
        # Decrypt the symmetric key using the recipient's private key
        # check what happenbs whne using a wrong recovery key....
        
       
        
        status, user_private_key = decrypt_private_key(user_key=backup_userkey,encrypted_key=backup_key)
        if not status:
            return False
        
        
        new_user_key=derive_user_key(new_password.strip(),user.myid)
        
        new_encrypted_private_key = user_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(new_user_key)
            )
        
        user.private_key = new_encrypted_private_key.decode('utf-8')
        user.password = new_password_hash
        user.save()
        

        
        return True 
    
    @staticmethod
    def AddFriend(my_username,friends_Code):
        friend = User.objects(friend_code=friends_Code).first()
        user = User.objects(username=my_username).first()
        # print(">>",user.username)
        # print(">>",friend.username)        
        # TODO make it work with link
        if friend and (friend.username not in user.partners) and (friend!=user):
            print("inside if >>>")
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


# images = fs.Storage('images', fs.IMAGES,
#                     upload_to=lambda o: 'prefix',
#                     basename=lambda o: 'basename')
# TODO add crus operatins as classmethods maybe, checkit out
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
