import random
import time
from message import app, cache, Events
from flask import render_template, redirect, url_for, flash, session, request
from message.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from message import app, bcrypt
from message.models import User, Letters
from message.security import *
import pytz     
import uuid
from datetime import datetime  
from message.notify import send_sms, send_email, generate_email_body
from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet
import base64
from wonderwords import RandomSentence
from message.utility import *


load_dotenv()


# TODO emails not getting delivered in deta
# TODO check all try and excepts and add an Error info to the page
@app.route('/', methods=["POST","GET"])
def login():
    # try:
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    # if "user" in session:
    #     return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        if request.form.get(Events.reset_password.value):
            print(request.form.get(Events.reset_password.value))
            user = User.FindUserByEmail(form.email.data.lower().strip())
            if user:
                print("entered if")
                key=  os.getenv('APP_SECRET') or os.environ["APP_SECRET"]
                print("got key")
                
                current_url = os.getenv('CurrentUrl') or os.environ["CurrentUrl"]   
                print("got url")
                        
                reset_link = generate_user_jwt_token(event=Events.reset_password.value,signing_key=key, url=current_url,json_data=user.to_json())
                print("made token")
                
                reset_link = current_url + f"/reset_password/{reset_link}"  
                body = generate_email_body(receiver=user.username, link=reset_link, event=Events.reset_password.value)
                send_email(to=user.email,subject="Reset Password",content=body)
                # try:
                # t1 = Thread(target=send_email, kwargs={"to":user.email,"subject":"Reset Password","content":body})
                # t1.start()
                flash("A link to reset your password will be sent to your Email soon, use it fast","info")
                # except:
                #     pass
                
                print("sent email")
                
                return(redirect(url_for("login")))
            else:
                flash("User with this email doesn't exists, check again", "danger")
            

        else:
            user = User.FindUserByName(form.username.data.lower().strip())
            # print("user pwd", form.password.data.strip())
            if form.username.data == "" or form.password.data == "":
                flash("Fill the details ! baka","danger")
                return redirect(url_for('login'))
        
            if user is not None and bcrypt.check_password_hash(user.password, form.password.data.strip().lower()) :
                if user.verified:
                    session["user"] = user.to_json()#form.username.data
                    session.permanent = True
                    
                    user_key=derive_user_key(form.password.data.strip(),user.myid)
                    session["USER_KEY"] = user_key.decode("utf-8")
                    # print("user key",user_key)
                    login_user(user)
                    # print("logged", current_user.username)
                    flash("you are logged in ! 🫰🏼🫰🏼", "success")
                    return redirect(url_for("home"))         
                else:
                    key=  os.getenv('APP_SECRET') or os.environ["APP_SECRET"]
                    current_url = os.getenv('CurrentUrl') or os.environ["CurrentUrl"]
                    print("USER DATA:",user.to_json(), user.email)
                    user_token= generate_user_jwt_token(json_data=user.to_json(), url= current_url, signing_key=key, event=Events.resend_verify_link.value)
                    verification_link=  current_url + f"/verify_user/{user_token}"

                    body = generate_email_body(receiver=user.username, event=Events.resend_verify_link.value, link=verification_link)
                    send_email(to=user.email,subject="New Verification Link",content=body)
                    # try:
                    #     t1 = Thread(target=send_email, kwargs={"to":user.email,"subject":"New Verification Link","content":body})
                    #     t1.start()
                    # except:
                    #     pass
                    flash("You're account isn't verified, new link will be sent soon. Check your Email ASAP to verify now.", "info")

            else:
                flash("Wrong username or password, check again 🍁🍁🍁 ", "danger") 
    return render_template("login.html", title='Login', form = form)
    # except:
    #     return render_template("error.html")




@app.route('/reset_password/<reset_code>',methods=["POST","GET"])
def reset_password(reset_code):
    reset_code=reset_code
    form = ResetPasswordForm()
    key =  os.getenv('APP_SECRET') or os.environ["APP_SECRET"]

    # if user is not None and bcrypt.check_password_hash(user.password, form.password.data.strip().lower()) :
    token = verify_user_token(token=reset_code,key=key )
    if token["status"]:
        if form.validate_on_submit():
            token_user_details = User.FindUserByName(token["username"])
            if form.username.data.lower().strip() != token_user_details.username:
                flash("This doesn't seem to be your Username, try again..🤔🤔","danger")
                return redirect(url_for("reset_password",reset_code=reset_code))
            
            
          
            if  bcrypt.check_password_hash(token_user_details.password, form.new_password.data.strip().lower()):
                print("CASE 2")
                flash("You can't use the same old password, try a new one 🤷🏼‍♀️ ","danger")
                return redirect(url_for("reset_password",reset_code=reset_code))
            # print(form.new_password.data.strip().lower())
            # print(form.confirm_password.data.strip().lower())
            if form.new_password.data.strip().lower() != form.confirm_password.data.strip().lower():
                print(">>>>>>")
                flash("Confirm your password again, It doesn't match 🤨🤨","danger")
                return redirect(url_for("reset_password",reset_code=reset_code))
                
          
            status = User.ResetPassword(username=token["username"], recovery_code=form.recovery_code.data, new_password=form.new_password.data)
            if  not status:
                flash("Recovery code doesn't match, try again 🤔🤔","danger")
                return redirect(url_for("reset_password",reset_code=reset_code))
        
            
            flash("Your password has been changed successfully(keep it safe), you can log in now 🐋🐋🐋","info")
            return(redirect(url_for("login")))
    
    else:
        
        print("ERRR:", token["info"])
        flash("Invalid or Expired Token, try to request for a new link 🔒", "danger")
        return redirect(url_for('login'))
    

        
                
     
    return render_template("create.html",form=form,event= Events.reset_password.value)
    
    
   

@app.route('/add_friend/<code>', methods=['GET', 'POST'])
@app.route('/add_friend', methods=['GET', 'POST'])
@login_required
def add_friend(code=None):
    # TODO add share friend link
    
    # try:
    if code:
        code=code.upper().strip()
        print("got code from URL:", code)
        
        print("USERname my:",current_user["username"])
        status,f_name = User.AddFriend(my_username=current_user["username"],friends_Code=code)
        if status:
            flash(f" Ahoy ! {f_name} added as your friend 😊🫱🏼‍🫲🏼","success" )
            return redirect(url_for("home"))
        else:
            flash("Invalid friend Code or User is already your friend 🍄🍄", "danger")
            return redirect(url_for("home"))
    
    
    
    
    
    else:
        form= AddFriendForm()

        if form.validate_on_submit():
            
            # user=search_user(current_user["username"])  
            code= form.code_firstDigit.data + form.code_secondDigit.data + form.code_thirdDigit.data+form.code_fourthDigit.data  
            # print("TYPE",type(code))
            code=code.upper()
            
        
            status,f_name = User.AddFriend(my_username=current_user["username"],friends_Code=code)
            if status:
                flash(f" Ahoy ! {f_name} added as your friend 😊🫱🏼‍🫲🏼","success" )
                return redirect(url_for("home"))
            else:
                flash("Invalid friend Code or User is already your friend 🍄🍄", "danger")
                return redirect(url_for("add_friend"))

            
        return render_template('new_friend_page.html', form=form)            
    # except:
    #     return render_template("error.html")


@app.route('/create', methods=['GET', 'POST'])
def create():
    # try:
    form = NewUserForm()
    event = Events.welcome.value
    # Populate partner choices from the database
    
    # form.partners.choices = [(user.username, user.username) for user in User.objects()]


    if form.validate_on_submit():
        username = form.username.data.strip().lower()
        password = form.password.data.strip().lower()
        mobile = form.mobile.data.strip()
        email=  form.email.data.strip()
        if email == "":
            flash("You need to Enter an Email address too ..","danger")
            return redirect(url_for('create'))
    
        existing_user = User.FindUserByName(username)
        existing_email = User.FindUserByEmail(email)
        if existing_user:
            flash('Username is already taken. Please choose a differe one 🏃🏼‍♂️', 'danger')
            return redirect(url_for('create'))
        # existing_email = User.objects(email=email).first()
        if existing_email:
            flash('Email is already used. Please choose a different one.', 'danger')
            return redirect(url_for('create'))
        if form.password.data.strip().lower() != form.confirm_password.data.strip().lower():
            # print(">>>>>>")
            flash("Confirm your password again, It doesn't match .. ","danger")
            return redirect(url_for('create'))

       
        s = RandomSentence()
        # lower case the sentance and join it wirh dash - then send it to model 
        recovery_code = s.sentence()
        print("RECO CODE:",recovery_code)
        recovery_code = recovery_code.replace(" ", "-" )
        recovery_code = recovery_code.lower().strip()
        recovery_code = recovery_code[0:-1]
        
        user = User.Create(username=username,password=form.password.data,mobile=mobile,email=email, recovery_code=recovery_code)

        
        # TODO use more secure key !
        key=  os.getenv('APP_SECRET') or os.environ["APP_SECRET"]
        current_url = os.getenv('CurrentUrl') or os.environ["CurrentUrl"]
        print("USER DATA:",user.to_json())
        user_token= generate_user_jwt_token(json_data=user.to_json(), url= current_url, signing_key=key, event=Events.welcome.value)
        verification_link=  current_url + f"/verify_user/{user_token}"

        body = generate_email_body(receiver=username, event=Events.welcome.value,password=password, link=verification_link, recover_code=recovery_code.lower()                                   )
        send_email(to=email,subject="🌟 Welcome to Project BFF! 🌟",content=body)
        # try:
        #     t1 = Thread(target=send_email, kwargs={"to":email,"subject":"🌟 Welcome to Project BFF! 🌟","content":body})
        #     t1.start()
        # except:
        #     pass
        
        
        flash('Account created successfully! Check your Email ID to verify the account ASAP! 🦚🦚', 'success')
        return redirect(url_for('login'))
        
        

    return render_template('create.html', form=form, event=event)
# except:
    #     return render_template("error.html")

#TODO check and read all the readme and infos onnce
@app.route('/pinned_view',methods=["GET","POST"])
def pinned_view():
    # 99a74794-3194-44fc-8957-053ed2036fdc
    # t=render_template("pinned_letter.html")
    # print(t,type(t))
    # TODO can try 2 ways
    # this way of extending htmls 
    # second using derive 2 render temoplats here and send for both sources from here on. (the problem is that base tempalte gets loaded 2 times)
    form = WriteForm()
    PreSelect = request.args.get('PreSelect')
    form.receiver.choices = [(PreSelect, PreSelect)] + [(partner, partner) for partner in current_user['partners'] if partner != PreSelect] if PreSelect else  [(partner, partner) for partner in current_user['partners']]

    if PreSelect:
        form.receiver.data=PreSelect
        selected_partner = form.receiver.data
    id = "03b9c827-2ffd-4cac-a5c4-1588339170b1"

    toRead=Letters.FindLetter(id=id)
    from message.test import words
    test_text= words
    para = test_text.split('\n')
    para = [x for x in para if x]
    stamp_data = toRead.stamp.read()
    stamp_data = base64.b64encode(stamp_data).decode('utf-8')
    
    
    
    return render_template("pinned_letter.html", form=form,PreSelect=PreSelect,userId=3214, message=toRead, content=para,stamp=stamp_data )








# TODO aadd cure emojies to all flash messages
@app.route('/verify_user/<token>')
def verify_user(token):
    key=  os.getenv('APP_SECRET') or os.environ["APP_SECRET"]
    token = verify_user_token(token,key=key )
    print("GOT TOKEN:",token)
    if token["status"]:
        user = User.FindUserByName(token["username"])
        if not user.verified :
            User.Verify(str(token['username']))
            flash("Yeyy! Your Email is verified, You can login. You're one of us now! 😇🎉", "info")
            return redirect(url_for('login'))
        else:
            flash("Hey ! Your Email is already verified .... :O", "info")
            return redirect(url_for('login'))

                
        # elif token["event"] == Events.reset_password.value:
        #     flash("Let's secure your account with a new passoword🗝️", "info")
        #     return redirect(url_for('reset_password'))

            
    else:
        print("ERRR:", token["info"])
        flash("Invalid or Expired Token, try to login again to get a new verfication link🔒🔒", "danger")
        return redirect(url_for('login'))

            
    




# @login_required #works use this
@app.route('/home')
@login_required
def home():
    
   
    #  after we add reciever field in letter we need to sort letters by that instead of author
    # try:
    if "USER_KEY" not in session:   
        flash("Your session has expired, please Re-login 🐶🐶","info")
        return redirect(url_for("logout"))
    # filter it by status other than draft
    sortedLetters= Letters.UserLetterBox(user=current_user["username"])
    
    current_link = os.getenv('CurrentUrl') or os.environ["CurrentUrl"]
    # sortedLetters=None
    return render_template("index.html", letters = sortedLetters, link=current_link)
    # except:        
    #     return render_template("error.html")

   


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


@app.route('/write',methods=["POST","GET"])
@login_required
def write():
 
    # try:
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
            main_start = time.perf_counter()
            
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
            # receiver=search_user(selected_partner)
            receiver=User.FindUserByName(selected_partner)
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
            # title=form.title.data
            # content=form.content.data
            encrypted_content = encrypt_message_chunked( form.content.data, symmetric_key)
            print(type(encrypted_content))
            encrypted_symmetric_key = encrypt_symmetric_key(symmetric_key, recipient_public_key)
            # print("4. encrypted symmetric key:",encrypted_symmetric_key)

            author=current_user["username"]
            task=make_letter_json(title=form.title.data,content=encrypted_content, timestamp=now,key=encrypted_symmetric_key,author=author,receiver=receiver.username)
            # TODO put all the keys to enc
            
            # # send_to_queue(task)
            
            
            
           
                
            start = time.perf_counter()
            if all((item.filename != '') for item in form.images.data):  
                # print("FILE TYPE 1!:",type(form.images.data[0]))

                process_images(letter_content=task,image_data_list=form.images.data,symmetric_key=symmetric_key)
                # final_image_list=[]
                # for file in form.images.data:
                # #     # print("file type",type(file))
                # # filename = secure_filename(file.filename)

                # # grid_fs_proxy = db.fields.GridFSProxy()
                #     img=compress_image(file)    
                #     enc_img=encrypt_file_chunked(img,symmetric_key)
                #     encoded_image = base64.b64encode(enc_img).decode('utf-8')
                #     final_image_list.append(encoded_image)
                # task["attached"] = True
                # task["image_data_list"] = final_image_list
                # send_to_queue(task)   
               
               
            # TODO limit single pic size, giving error in deta deployemnt
            else:
               
                # when the letter doesnt have images 
                send_to_queue(task=task)
                     
                   
                    
                    # image_list.append(enc_img)
                    # final_image_list = []
                    # for img in encrypted_images:
                    
                
                
                
                
                # print("FORMDATA:",form.images.data,type(form.images.data))
                # image_list=[]
                # for file in form.images.data:
                # #     # print("file type",type(file))
                #     filename = secure_filename(file.filename)
                
                #     grid_fs_proxy = db.fields.GridFSProxy()
                #     img=compress_image(file)    
                #     enc_img=encrypt_file_chunked(img,symmetric_key)
                   
                    
                #     image_list.append(enc_img)           
                #     # print("ENC IMAGE",type(enc_img))
                    
                #     grid_fs_proxy.put(enc_img)
                #     letter.images.append(grid_fs_proxy)
                #     letter.attachment = True
                # print("filename", filename)
                # p1=Thread(target=attach_images,kwargs={"letter_id":letter_id,"image_data_list":form.images.data,"key":symmetric_key})
                # TODO maybe try creating 3 different threads for compression, enc, and queue
                # p1=Thread(target= attach_images,kwargs={  "content":task,"image_data_list":form.images.data,"key":symmetric_key})
                # p1.start()
                # TIME TAKEN FOR IMAGE STUFF!!:2.44s
                # process_images(content=task,image_data_list=form.images.data,key=symmetric_key)
                # TIME TAKEN FOR IMAGE STUFF!!:2.12s
                # process_images_threads(letter_content=task,image_data_list=form.images.data,symmetric_key=symmetric_key)
                # img= Thread(target= process_images,kwargs={  "letter_content":task,"image_data_list":form.images.data,"symmetric_key":symmetric_key})
                # img.start()
              

                # print(">>>> got an image ")
                # print(file.filename)
            finish=time.perf_counter()
            print(f"TIME TAKEN FOR IMAGE STUFF!!:{round(finish-start,2)}s")

            flash(f'Letter will be delivered soon, Thank you for making {selected_partner} Happyy 👉🏼👈🏼',"info")
            # letter.save()
            main_end = time.perf_counter()
            print("LETTERRRR SAVED !!!")
            print(f"TIME TAKEN FOR whole  STUFF!!:{round(main_end-main_start,2)}s")
            
            # print(letter.to_json())
            
            adj=["cute","cute-lika-a-baby","cutest-hooman-in-the-world","pretty-like-the-moon","fluffy-lika-panda","awesome","sweet","amazing","wonderful","lovely","happy", "pretty","adorable", "tinyy","kawaii","cutesy","fluffy","funny", "cute-as-a-penguin", "supercute", "golu-molu-like-a-potato","tiny-like-a-penguin","rarest-gen","shingy-sunshine","melty-icecream", "fluff-ball"]
            url="https://tinyurl.com/projectbffs"
                
            notification_body = f"""            
                Hi {random.choice(adj)} {receiver.username}, \n Hope you are smiling. Your precious friend {current_user['username']} just sent you a letter on ProjectBFF. The title says "{form.title.data}". Take a look whenever you want and maybe let them know about it, \n
                have a happy day and take care.
                see ya :)
            """

            # notify partner about new letter via email
            # if receiver.email != "":
            #     send_email(to=User.objects(username=receiver.username).first().email,subject="YOU JUST GOT A NEW LETTER !!",content=notification_body)        
                
            
            # # notify the partner with sms
            # # make a list of cute adjectives
            # if receiver.mobile != "":
                
            #     # generate random word from list
            #     to=User.objects(username=receiver.username).first().mobile 
              
            #     send_sms(to=to, body=notification_body)
                # print(">sent sms!")
            return redirect(url_for("home"))
      
        return render_template("write.html", form = form, userId=current_user["myid"], PreSelect=PreSelect )
    else:
        flash("you need to add a friend 🥺🥺","danger")
        return redirect(url_for('home'))
    
    # except:
    #     return render_template("error.html")

@app.route("/feedback",methods=["POST","GET"])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        #user_email=form.title.data
        title=form.subject.data
        feedback=form.feedback.data
        admin_id=os.getenv('admin_id') or os.environ["admin_id"]
        feedback= feedback+f"  \n\n USER_DETAILS \n NAME:{current_user['username']}, \n  EMAIL: {current_user['email']}"
        # TODO threads not working in deta !
        body = generate_email_body(event=Events.feedback.value,feedback=feedback,title= title)
        send_email(to=admin_id, subject="ProjectBff UserFeedback", content=body)
        # TODO testing without thread for senind emails
        # t1 = Thread(target=send_email, kwargs={"to":admin_id,"subject":"ProjectBff UserFeedback","content":body})
        # t1.start()

        
        flash("Your Feedback is important, Thank you 🫡🫡", "info")
        return redirect(url_for('home'))
        
    
    return render_template("feedback.html",form=form)

# 
@app.route('/process',methods=["GET,POST"])
def process_letter():
    
    
    
    task=request.get_json()
    signature = request.headers 
    print(">>>>>>>>>>tgot callback url :", signature)
    print(">>>>>>>>>>tgot callback url :", task)
    
    return "GOT CALL BACK URL"
    

@app.route('/letter/<string:id>')
@login_required
@cache.cached(timeout=9000)
def letter(id):
    # print(id)
    # try:
    toRead=Letters.FindLetter(id=id)
    

    if current_user['username'] == toRead.receiver:
        if toRead.author in current_user["partners"] and toRead.status == "sent":
           
           
            Letters.objects(myid=id).update(status="read")#, stamp_url=stamp_url)
        # converting string to bytes
        user_key=session["USER_KEY"].encode('utf-8')
        # test for wrong user key
        encrypted_private_key = current_user.private_key.encode() # Convert the string to a byte string

        # Decrypt the symmetric key using the recipient's private key
        status, recipient_private_key = decrypt_private_key(user_key=user_key   ,encrypted_key=encrypted_private_key)

        # recipient_private_key = serialization.load_pem_private_key(
        #     encrypted_private_key,
        #     password=user_key,
        #     backend=default_backend()
        # )
        #TODO remove all prints 
        # print("5. user private key:",recipient_private_key)
        print("in the mid of letter route!")
        encrypted_symmetric_key = base64.b64decode(toRead.symmetric_key.encode())
        
        symmetric_key = decrypt_symmetric_key(encrypted_symmetric_key, recipient_private_key)
       
        # stamp_data = base64.b64encode(toRead.stamp.read().decode('utf-8'))
        stamp_data = toRead.stamp.read()
        stamp_data = base64.b64encode(stamp_data).decode('utf-8')
        # if toRead.images != []: #
        if toRead.attachment:
            
            attached_images = toRead.images 
            
            image_data_list=[base64.b64encode(decrypt_file_chunked(photo.read(),symmetric_key)).decode('utf-8') for photo in attached_images]  
            
          
                
        else:
            print("no imge field:")
            
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
        return render_template("letter.html", message=toRead, content=para, PreSelect=PreSelect, img_data=image_data_list, stamp=stamp_data)
    else:
        return redirect(url_for("home"))
    # except:
    #     return render_template("error.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/features')
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

