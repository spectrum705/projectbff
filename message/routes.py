import random
from werkzeug.utils import secure_filename
from message import app, cache
from flask import render_template, redirect, url_for, Flask, flash, session, request
from message.forms import LoginForm, WriteForm, NewUserForm, AddFriendForm, FeedbackForm
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from message import app, bcrypt
from message.models import User, Letters
from message.security import *
import pytz     
import uuid
import string
from datetime import datetime  
from message.notify import send_sms, send_email
from dotenv import load_dotenv
import os
from mongoengine import ValidationError
from cryptography.fernet import Fernet
import base64
import io
from message.utility import compress_image, make_stamp
from message import db

load_dotenv()


# DB_URI = os.getenv('DB_URI') or os.environ["DB_URI"]
# account_sid = os.getenv('account_sid') or os.environ["account_sid"]
# auth_token  = os.getenv('auth_token') or os.environ["auth_token"]
# messaging_service_sid = os.getenv('message_service_sid') or  os.environ["messaging_service_sid"]




@app.route('/', methods=["POST","GET"])
def login():
    # try:
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    # if "user" in session:
    #     return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data.lower().strip()).first()
        # print("user pwd", form.password.data.strip())
    
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data.strip().lower()) :

            session["user"] = user.to_json()#form.username.data
            session.permanent = True
            
            user_key=derive_user_key(form.password.data.strip(),user.myid)
            session["USER_KEY"] = user_key.decode("utf-8")
            # print("user key",user_key)
            
            

            login_user(user)
            # print("logged", current_user.username)
            flash("you are logged in ", "success")
            return redirect(url_for("home"))            
        else:
            flash("Wrong username or password, check again.", "danger") 
    return render_template("login.html", title='Login', form = form)
    # except:
    #     return render_template("error.html")

def search_user(username):
    return User.objects(username=username).first()


@app.route('/add_friend', methods=['GET', 'POST'])
def add_friend():
    try:
        form= AddFriendForm()

        if form.validate_on_submit():
            
            # user=search_user(current_user["username"])  
            code= form.code_firstDigit.data + form.code_secondDigit.data + form.code_thirdDigit.data+form.code_fourthDigit.data  
            # print("TYPE",type(code))
            code=code.upper()
            
            # print("CODE", code)
            friend = User.objects(friend_code=code).first()
            user = User.objects(username=current_user["username"]).first()        
            if friend and (friend not in user.partners) and (friend!=user):
                user.partners.append(friend.username)
                friend.partners.append(user.username)
                user.save()
                friend.save()
                flash(f" Ahoy ! {friend.username} added as your Partner.","success" )
                return redirect(url_for("home"))            
            else:
                flash("Invalid friend Code or User is already your friend", "danger")
                
            
            
        return render_template('new_friend_page.html', form=form)            
    except:
        return render_template("error.html")



@app.route('/create', methods=['GET', 'POST'])
def create():
    # try:
    form = NewUserForm()

    # Populate partner choices from the database
    
    # form.partners.choices = [(user.username, user.username) for user in User.objects()]


    if form.validate_on_submit():
        username = form.username.data.strip().lower()
        password = form.password.data.strip().lower()
        mobile = form.mobile.data.strip()
        email=  form.email.data.strip()
        uid=random.randint(1,10000)
        my_friend_code= ''.join(random.choices(string.ascii_uppercase, k=4))
        entered_friend_code = form.friend_code.data
        # print("BDATA",form.birthday.data)
        # print("PWD",password)
        
        # Check if the username is already taken
        existing_user = User.objects(username=username).first()
        existing_email = User.objects(username=email).first()
        if existing_user:
            flash('Username is already taken. Please choose a different one.', 'danger')
            return redirect(url_for('create'))
        existing_email = User.objects(email=email).first()
        if existing_email:
            flash('Email is already used. Please choose a different one.', 'danger')
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
                        email=email,
                        friend_code=my_friend_code,                        
                        public_key=public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                        ).decode('utf-8'),
                        private_key=encrypted_private_key.decode('utf-8') # Save the encrypted private key as a string

                        )

        # list_of_partners  = form.partners.data
        # print("1>>>>>>>>>", form.partners.data)
        


        if entered_friend_code != "":
            friend = User.objects(friend_code=entered_friend_code.upper()).first()
            if friend and (new_user not in friend.partners):
            # if friend:
                new_user.partners.append(friend.username)
                friend.partners.append(username)
                friend.save()
            else:
                flash("Invalid friend Code ", "danger")
                return(redirect("create"))
        new_user.save()
    
            

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
        
        

    return render_template('create.html', form=form)
    # except:
    #     return render_template("error.html")







# @login_required #works use this
@app.route('/home')
@login_required
def home():
    
   
    #  after we add reciever field in letter we need to sort letters by that instead of author
    # try:
    if "USER_KEY" not in session:   
        flash("Your session has expired, please Re-login","info")
        return redirect(url_for("logout"))
    sortedLetters=sorted(Letters.objects(receiver=current_user["username"]), key=lambda letters: datetime.strptime( letters.timestamp, "%H:%M, %d-%m-%Y"), reverse=True)

    # sortedLetters=None
    return render_template("index.html", letters = sortedLetters)
    # except:        
    #     return render_template("error.html")

   
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



# # Generate a secret key for Fernet
# key = Fernet.generate_key()
# cipher_suite = Fernet(key)
@app.route('/email/<con>')
def email(con):
    return render_template('email.html',content=con)

@app.route('/write',methods=["POST","GET"])
@login_required
def write():
    #TODO
   
    try:
        if current_user["partners"] != []:
            # draftLetters =Letters.objects(author=current_user["username"], status = "draft")
            
            form = WriteForm()
            #making a button to get draft item if exist
            #mention NOte for save later
            #after sending the draft status should change too
            #fix updateing letter object
            #form should fill from db not local storage
            # should work cross platform
            #no multiple letter objects should be formed    
            
            #for saving to drafts
            # if draftLetters :
            #     print(draftLetters.author)
            #     print(draftLetters.status)
            #     print(draftLetters.title)
            #     print("block 1")
            #     form.title.data =draftLetters.title
            #     form.content.data=draftLetters.content


            # if request.method == "POST":
            #     print("block 2")

            #     if request.form.get("save") == "yes":
            #         print("hm it worked")
            #         draftMessage(title=form.title.data, content=form.content.data)
            #         flash("okay, it's saved you can finish later :)" , "info")
            #         return redirect(url_for("home"))

            # list of partners
            PreSelect = request.args.get('PreSelect')
            form.receiver.choices = [(PreSelect, PreSelect)] + [(partner, partner) for partner in current_user['partners'] if partner != PreSelect] if PreSelect else  [(partner, partner) for partner in current_user['partners']]




            # print("choices:", form.receiver.choices)
            # print("PRESELECT in write page got it from the reply button:",PreSelect, type(PreSelect))

            if form.validate_on_submit():
                asiaTime= pytz.timezone('Asia/Kolkata')   
                datetime_ind = datetime.now(asiaTime)  
                now = datetime_ind.strftime("%H:%M, %d-%m-%Y")
                # print("block 3")

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
                # TODO comment these
                # print("receiver:", form.receiver.data)
                # print("1. recipient public key:", recipient_public_key)
                # print("title:",  form.title.data, type(form.title.data))
                # print("content:", form.content.data, type(form.content.data))
                # print("author:", current_user["username"])
                # print("status:", "sent")
                # print("timestamp:", now)
                # print("receiver:", form.receiver.data, type(form.receiver.data))

                symmetric_key = Fernet.generate_key()
                # print("2. symmentric key used on letter for enc:", symmetric_key)
                title=form.title.data
                # content=form.content.data
                encrypted_content = encrypt_message_chunked( form.content.data, symmetric_key)
                encrypted_symmetric_key = encrypt_symmetric_key(symmetric_key, recipient_public_key)
                stamp_url=make_stamp(title)
                # print("4. encrypted symmetric key:",encrypted_symmetric_key)

                author=current_user["username"] 
                
                
                letter=Letters(title=title,
                                content=encrypted_content,
                                symmetric_key=base64.b64encode(encrypted_symmetric_key).decode('utf-8'),
                                author=author,
                                receiver=receiver.username,
                                status="sent",
                                timestamp=now, 
                                myid=str(uuid.uuid4()),
                                stamp_url=stamp_url
                                )
                
            

                # OG veriosn
                if all((item.filename != '') for item in form.images.data):      
                
                    # upload_images.delay(form.images.data)                  
                    for file in form.images.data:
                        
                        # print("file type",type(file))
                        filename = secure_filename(file.filename)
                    
                        grid_fs_proxy = db.fields.GridFSProxy()
                        img=compress_image(file)               
                        enc_img=encrypt_file_chunked(img,symmetric_key)
                        # print("ENC IMAGE",type(enc_img))
                        
                        grid_fs_proxy.put(enc_img)
                        letter.images.append(grid_fs_proxy)
                        letter.attachment = True
                    # print("filename", filename)
                    
                

                    # print(">>>> got an image ")
                    # print(file.filename)
                flash(f'Letter sent, Thank you for making {selected_partner} Happy :)',"info")
                letter.save()
                # print("LETTERRRR SAVED !!!")
                # print(letter.to_json())
                
                adj=["cute","cute-lika-a-baby","cutest-hooman-in-the-world","pretty-like-the-moon","fluffy-lika-panda","awesome","sweet","amazing","wonderful","lovely","happy", "pretty","adorable", "tinyy","kawaii","cutesy","fluffy","funny", "cute-as-a-penguin", "supercute", "golu-molu-like-a-potato","tiny-like-a-penguin","rarest-gen","shingy-sunshine","melty-icecream", "fluff-ball"]
                url="https://tinyurl.com/projectbffs"
                    
                notification_body = f"""            
                    Hi {random.choice(adj)} {receiver.username}, \n Hope you are smiling. Your precious friend {current_user['username']} just sent you a letter on ProjectBFF. The title says "{form.title.data}". Take a look whenever you want and maybe let them know about it, \n
                    have a happy day and take care.
                    see ya :)
                """

                
                # notify partner about new letter via email
                if receiver.email != "":
                    # print("EMAIL:",User.objects(username=receiver.username).first().email)
                    send_email(to=User.objects(username=receiver.username).first().email,subject="YOU JUST GOT A NEW LETTER !!",content=notification_body)        
                    
                
                # notify the partner with sms
                # make a list of cute adjectives
                if receiver.mobile != "":
                    
                    # generate random word from list
                    to=User.objects(username=receiver.username).first().mobile 
                    # print("to:",to)
                    # need to change partner into specific reciver
                    # print('>> before sms function call')
                    send_sms(to=to, body=notification_body)
                    # print(">sent sms!")
                return redirect(url_for("home"))
            # print('>>>>>USR ID',current_user["myid"])
            #for draft testing
            # content_fill= "test content meow meow meow"
            return render_template("write.html", form = form, userId=current_user["myid"], PreSelect=PreSelect )
        else:
            flash("you need to add a friend :(","danger")
            return redirect(url_for('home'))
    except:
        return render_template("error.html")
        
@app.route("/feedback",methods=["POST","GET"])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        #user_email=form.title.data
        title=form.subject.data
        feedback=form.feedback.data
        admin_id=os.getenv('admin_id') or os.environ["admin_id"]
        
        feedback= f"TITLE: {title}\n  " +feedback+f"  \n USER_DETAILS \n NAME:{current_user['username']}, \n  EMAIL: {current_user['email']}"
        send_email(to=admin_id, subject="PROJECTBFF USER FEEDBACK", content=feedback)
        flash("Your Feedback is important, Thank you :)", "info")
        return redirect(url_for('home'))
        
    
    return render_template("feedback.html",form=form)

# 
@app.route('/test')
def test():
    return render_template('stamp2.html')


@app.route('/letter/<string:id>')
@login_required
@cache.cached(timeout=9000)
def letter(id):
    # print(id)
    try:
        toRead= Letters.objects(myid=id).first()
        
        # print(toRead)
        
        # print(toRead.author)
        # print("username:",current_user['username'])
        # print(current_user["partners"])
        
        
            
    

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
            #TODO remove all prints 
            # print("5. user private key:",recipient_private_key)
            
            encrypted_symmetric_key = base64.b64decode(toRead.symmetric_key.encode())
            
            symmetric_key = decrypt_symmetric_key(encrypted_symmetric_key, recipient_private_key)
            if toRead.attachment:
                attached_images = toRead.images 
                
                image_data_list=[base64.b64encode(decrypt_file_chunked(photo.read(),symmetric_key)).decode('utf-8') for photo in attached_images]  
                
                # this one is working
                # image_data_list=[base64.b64encode(photo.read()).decode('utf-8') for photo in attached_images] 
                
                
                # image_data_list=[]
                # for  photo in attached_images:
                #     print("PHOTO TYP:",type(photo))
                #     dec_img= decrypt_file_chunked(photo.read(),symmetric_key)
                #     print("Dec TYP:",type(dec_img))
                #     fin_img= base64.b64encode(dec_img).decode('utf-8')
                #     print("FIN",type(fin_img))
                #     image_data_list.append(fin_img)
                    
            else:
                image_data_list=None
            # print("6. decrypted symmetric key used on Letter:",symmetric_key)
            
            decrypted_content = decrypt_message_chunked(toRead.content, symmetric_key)
            # print("7. decrypted contet:",decrypted_content)
            
            para = decrypted_content.split('\n')
            para = [x for x in para if x]
            # para = list(filter(lambda x : x != '', decrypted_content.split('\n\n')))

            print(toRead.status)
            PreSelect=toRead.author
            # print("preselect from letter page:",PreSelect)
            # print(toRead.images.read())
            # image=toRead.images.read()
            return render_template("letter.html", message=toRead, content=para, PreSelect=PreSelect, img_data=image_data_list)
        else:
            return redirect(url_for("home"))
    except:
        return render_template("error.html")

@app.route('/about')
# @login_required
def about():
    return render_template("about.html")

@app.route('/features')
# @login_required
def features():
    return render_template("features.html")



@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("USER_KEY",None)
    logout_user()

    return redirect(url_for(("login")))


@app.route('/sw.js', methods=['GET'])
def sw():
    return app.send_static_file('sw.js')


# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('error.html'),404
 
# #Handling error 500 and displaying relevant web page
# @app.errorhandler(500)
# def internal_error(error):
#     return render_template('error.html'),500

