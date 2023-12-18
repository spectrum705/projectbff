import random
from flask import render_template, redirect, url_for, Flask, flash, session, request
from message.forms import LoginForm, WriteForm, NewUserForm
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from message import app, bcrypt
from message.models import User, Letters
from message.security import *
import pytz     
import uuid
from datetime import datetime  
from message.notify import send_sms
from dotenv import load_dotenv
import os
from mongoengine import ValidationError
from cryptography.fernet import Fernet


load_dotenv()


# DB_URI = os.getenv('DB_URI') or os.environ["DB_URI"]
# account_sid = os.getenv('account_sid') or os.environ["account_sid"]
# auth_token  = os.getenv('auth_token') or os.environ["auth_token"]
# messaging_service_sid = os.getenv('message_service_sid') or  os.environ["messaging_service_sid"]




@app.route('/', methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    # if "user" in session:
    #     return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data.lower().strip()).first()
       
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data.strip()) :

            session["user"] = user.to_json()#form.username.data
            session.permanent = True
            user_key=derive_user_key(form.password.data.strip(),user.myid)
            session["USER_KEY"] = user_key.decode("utf-8")
            print("user key",user_key)
            
            

            login_user(user)
            # print("logged", current_user.username)
            flash("you are logged in ", "success")
            return redirect(url_for("home"))            
        else:
            flash("Wrong username or password, check again.", "danger") 
    return render_template("login.html", title='Login', form = form)


def search_user(username):
    return User.objects(username=username).first()

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = NewUserForm()

    # Populate partner choices from the database
    form.partners.choices = [(user.username, user.username) for user in User.objects()]

  
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()
        mobile = form.mobile.data.strip()
        uid=random.randint(1,10000)
        
        # Check if the username is already taken
        existing_user = User.objects(username=username).first()
        if existing_user:
            flash('Username is already taken. Please choose a different one.', 'danger')
            return redirect(url_for('create'))


        password_hash=bcrypt.generate_password_hash(password,10).decode('utf-8') 
        private_key, public_key = generate_key_pair()
        user_key= derive_user_key(password,uid)
        encrypted_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(user_key)
        )
        # Create a new user
        new_user = User(myid=uid,
                        username=username, 
                        password=password_hash,
                        mobile=mobile,
                         public_key=public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                        ).decode('utf-8'),
                        private_key=encrypted_private_key.decode('utf-8') # Save the encrypted private key as a string

                        )

        list_of_partners  = form.partners.data
        print("1>>>>>>>>>", form.partners.data)
        


        new_user.partners=list_of_partners
        new_user.save()
        #update the partner for other user too (append i think)
        for each_selected_user in list_of_partners:
            user=search_user(each_selected_user)
            user.partners.append(username)
            user.save()
            

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
        
         

    return render_template('create.html', form=form)






# @login_required #works use this
@app.route('/home')
@login_required
def home():
    
    # if "user" not in session:
    #     return redirect(url_for("login"))
    # current_user = session["user"]
    
    # eariler the letters were retrieved by author field
    # sortedLetters=sorted(Letters.objects(author=current_user["partners"] ), key=lambda letters: datetime.strptime( letters.timestamp, "%H:%M, %d-%m-%Y"), reverse=True)
    
    #  after we add reciever field in letter we need to sort letters by that instead of author
    if "USER_KEY" not in session:   
        return redirect(url_for("logout"))
    sortedLetters=sorted(Letters.objects(receiver=current_user["username"]), key=lambda letters: datetime.strptime( letters.timestamp, "%H:%M, %d-%m-%Y"), reverse=True)

    # sortedLetters=None
    return render_template("index.html", letters = sortedLetters)
   
    #uncomment these later
    # if "user" in session:
    #     return render_template("index.html")
    # else:
    #     return redirect("login")

#making a draft feature (saving messages by default to db)
# def draftMessage(title, content):
#     prevLetter =Letters.objects(author=session["user"]["username"], status = "draft").first()
#     asiaTime= pytz.timezone('Asia/Kolkata')   
#     datetime_ind = datetime.now(asiaTime)  
#     now = datetime_ind.strftime("%H:%M, %d-%m-%Y")
#     if prevLetter:
#         print("draft already exits so updataing that")
#         # try to fix this update thing
#         #its giving some id error from dm side

#         prevLetter.update(title=title, content=content, timestamp=now )

#     else:
        
#         letter=Letters(title=title, 
#         content=content,
#         author=session["user"]["username"],
#         status="draft", 
#         timestamp=now,
#         myid=str(uuid.uuid4()))
#         letter.save()
#         print("saved in draft")


@app.route('/test',methods=["POST","GET"])
def test():
    form= WriteForm()
    userId=7242
    return render_template("write.html", form = form, userId=userId )


# Generate a secret key for Fernet
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/write',methods=["POST","GET"])
@login_required
def write():
    
    # try:
    # prevLetter =Letters.objects(author=current_user["username"], status = "draft").first()
    
    form = WriteForm()   
    #making a button to get draft item if exist
    #mention NOte for save later
    #after sending the draft status should change too
    #fix updateing letter object
    #form should fill from db not local storage
    # should work cross platform
    #no multiple letter objects should be formed    
    
    #for saving to drafts
    # if prevLetter :
    #     print(prevLetter.author)
    #     print(prevLetter.status)
    #     print(prevLetter.title)
    #     print("block 1")
    #     form.title.data =prevLetter.title
    #     form.content.data=prevLetter.content


    # if request.method == "POST":
    #     print("block 2")

    #     if request.form.get("save") == "yes":
    #         print("hm it worked")
    #     draftMessage(title=form.title.data, content=form.content.data)
    #     flash("okay, it's saved you can finish later ;)" , "info")
    #     return redirect(url_for("home"))

    # list of partners
    PreSelect = request.args.get('PreSelect')
    form.receiver.choices = [(PreSelect, PreSelect)] + [(partner, partner) for partner in current_user['partners'] if partner != PreSelect] if PreSelect else  [(partner, partner) for partner in current_user['partners']]




    print("choices:", form.receiver.choices)
    print("PRESELECT in write page got it from the reply button:",PreSelect, type(PreSelect))

    if form.validate_on_submit():
        asiaTime= pytz.timezone('Asia/Kolkata')   
        datetime_ind = datetime.now(asiaTime)  
        now = datetime_ind.strftime("%H:%M, %d-%m-%Y")
        print("block 3")

        #fill the form if there's a letter in draft
        # if prevLetter:
        #     prevLetter.update(title=form.title.data, 
        #     content=form.content.data,status="sent",timestamp=now, myid=str(uuid.uuid4()))
        #     return redirect(url_for("home"))

        # else:
        if PreSelect:
            form.receiver.data=PreSelect
        selected_partner = form.receiver.data
        receiver=search_user(selected_partner)
        recipient_public_key_str = receiver.public_key#selected_partner.public_key#
        recipient_public_key = serialization.load_pem_public_key(
                recipient_public_key_str.encode(),
                backend=default_backend()
            )
        # print("receiver:", form.receiver.data)
        print("1. recipient public key:", recipient_public_key)
        print("title:",  form.title.data, type(form.title.data))
        print("content:", form.content.data, type(form.content.data))
        print("author:", current_user["username"])
        print("status:", "sent")
        print("timestamp:", now)
        print("receiver:", form.receiver.data, type(form.receiver.data))

        symmetric_key = Fernet.generate_key()
        print("2. symmentric key used on letter for enc:", symmetric_key)
        title=form.title.data
        # content=form.content.data
        encrypted_content = encrypt_message_chunked( form.content.data, symmetric_key)
        encrypted_symmetric_key = encrypt_symmetric_key(symmetric_key, recipient_public_key)
        print("4. encrypted symmetric key:",encrypted_symmetric_key)

        author=current_user["username"] 
         
        letter=Letters(title=title,
                        content=encrypted_content,
                        symmetric_key=base64.b64encode(encrypted_symmetric_key).decode('utf-8'),
                        author=author,
                        receiver=receiver.username,
                        status="sent",
                        timestamp=now, 
                        myid=str(uuid.uuid4())
                        )

        letter.save()
        print("LETTERRRR SAVED !!!")
        flash(f'Letter sent, Thank you for making {selected_partner} Happy :)',"info")
        print(letter.to_json())
        
        
        # notify the partner with sms
        # make a list of cute adjectives
        if receiver.mobile != "":
            adj=["cute","cute-lika-a-baby","cutest-hooman-in-the-world","pretty-like-the-moon","fluffy-lika-panda","awesome","sweet","amazing","wonderful","lovely","princess","happy", "pretty","adorable", "tinyy","kawaii","cutesy","fluffy","funny", "cute-as-a-penguin", "pouty","supercute", "golu-molu-like-a-potato"]
            
            # generate random word from list
            to=User.objects(username=receiver).first().mobile 
            url="https://tinyurl.com/projectbffs"
            print("to:",to)
            # need to change partner into specific reciver
            body = f"Hi {random.choice(adj)} {receiver}, Hope you are smiling. {current_user['username']} just sent you a letter in ProjectBFF. The title says '{form.title.data}'. Take a read whenever you want, here's the link {url}. see ya :)"
            print('>> before sms function call')
            send_sms(to=to, body=body)
            print(">sent sms!")
        return redirect(url_for("home"))
    print('>>>>>USR ID',current_user["myid"])
    return render_template("write.html", form = form, userId=current_user["myid"], PreSelect=PreSelect )
    # except:
        # return redirect(url_for("login"))

@app.route('/letter/<string:id>')
@login_required
def letter(id):
    # print(id)
    #TODO uncomment try catchpyton3 
    # try:
    toRead= Letters.objects(myid=id).first()
    
    # print(toRead)
    #make status to read !
    print(toRead.author)
    print("username:",current_user['username'])
    print(current_user["partners"])
    if current_user['username'] == toRead.receiver:
        if toRead.author in current_user["partners"] and toRead.status == "sent":
            Letters.objects(myid=id).update(status="read")
        # converting string to bytes
        user_key=session["USER_KEY"].encode('utf-8')
        
        encrypted_private_key = current_user.private_key.encode() # Convert the string to a byte string

        # Decrypt the symmetric key using the recipient's private key
        recipient_private_key = serialization.load_pem_private_key(
            encrypted_private_key,
            password=user_key,
            backend=default_backend()
        )
        print("5. user private key:",recipient_private_key)
        
        encrypted_symmetric_key = base64.b64decode(toRead.symmetric_key.encode())
        
        symmetric_key = decrypt_symmetric_key(encrypted_symmetric_key, recipient_private_key)
        
        print("6. decrypted symmetric key used on Letter:",symmetric_key)
        
        decrypted_content = decrypt_message_chunked(toRead.content, symmetric_key)
        print("7. decrypted contet:",decrypted_content)
        
        para = decrypted_content.split('\n')
        para = [x for x in para if x]
        print(toRead.status)
        PreSelect=toRead.author
        print("preselect from letter page:",PreSelect)
        return render_template("letter.html", message=toRead, content=para, PreSelect=PreSelect)
    else:
        return redirect(url_for("home"))
# except:
    #     return redirect(url_for("login"))

@app.route('/about')
# @login_required
def about():
    
    return render_template("about.html")



@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("USER_KEY",None)
    logout_user()

    return redirect(url_for(("login")))


@app.route('/sw.js', methods=['GET'])
def sw():
    return app.send_static_file('sw.js')
