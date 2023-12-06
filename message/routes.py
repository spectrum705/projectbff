import random
from flask import render_template, redirect, url_for, Flask, flash, session, request
from message.forms import LoginForm, WriteForm, NewUserForm
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from message import app
from message.models import User, Letters
import pytz     
import uuid
from datetime import datetime  
from message.notify import send_sms
from dotenv import load_dotenv
import os
from mongoengine import ValidationError

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
        # print("urs:",form.username.data)
        # print("pwd:", form.password.data)
        # print("userinDb",user)
        # print("pwd:",user.password)
        if user is not None and form.password.data.strip() == user.password:
            session["user"] = user.to_json()#form.username.data
            session.permanent = True

            login_user(user)
            # print("logged", current_user.username)
            flash("you are logged in ", "success")
            return redirect(url_for("home"))            
        else:
            flash("Wrong username or password, check again.", "danger") 
    return render_template("login.html", title='Login', form = form)


def SearchUser(username):
    return User.objects(username=username).first()

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = NewUserForm()

    # Populate partner choices from the database
    form.partners.choices = [(user.username, user.username) for user in User.objects()]


    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        mobile = form.mobile.data
        
        # Check if the username is already taken
        existing_user = User.objects(username=username).first()
        if existing_user:
            flash('Username is already taken. Please choose a different one.', 'danger')
            return redirect(url_for('create'))

        # Hash the password before storing it
        # hashed_password = generate_password_hash(password, method='sha256')

        # Create a new user
        new_user = User(myid=random.randint(1,10000),username=username, password=password, mobile=mobile)

        list_of_partners  = form.partners.data
        print("1>>>>>>>>>", form.partners.data)
        


        new_user.partners=list_of_partners
        new_user.save()
        #TODO update the partner for other user too (append i think)
        for each_selected_user in list_of_partners:
            user=SearchUser(each_selected_user)
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
    # sortedLetters=sorted(Letters.objects(reciever=current_user), key=lambda letters: datetime.strptime( letters.timestamp, "%H:%M, %d-%m-%Y"), reverse=True)
    
    sortedLetters="hi"
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
@app.route('/write',methods=["POST","GET"])
@login_required
def write():
    
    try:
        # prevLetter =Letters.objects(author=session["user"]["username"], status = "draft").first()
        prevLetter =Letters.objects(author=current_user["username"], status = "draft").first()
        
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
            print("title:", form.title.data)
            print("content:", form.content.data)
            flash(f'Letter sent, Thank you for making {current_user["partner"]} Happy :)',"info")
            letter=Letters(title=form.title.data, 
            content=form.content.data,
            author=current_user["username"],
            status="sent", myid=str(uuid.uuid4()) ,timestamp=now)

            letter.save()
            print(letter.to_json())
            # notify the partner with sms
            # make a list of cute adjectives
            
            adj=["cute","cute-lika-a-baby","cutest-hooman-in-the-world","pretty-like-the-moon","fluffy-lika-panda","awesome","sweet","amazing","wonderful","lovely","princess","happy", "pretty","adorable", "tinyy","kawaii","cutesy","fluffy","funny", "cute-as-a-penguin", "pouty","supercute", "golu-molu-like-a-potato"]
            
            # generate random word from list
            to=User.objects(username=current_user["partner"]).first().mobile 
            url="https://tinyurl.com/projectbffs"
            print("to:",to)
            # need to change partner into specific reciver
            body = f"Hi {random.choice(adj)} {session['user']['partner']}, Hope you are smiling. {current_user['username']} just sent you a letter in ProjectBFF. The title says '{form.title.data}'. Take a read whenever you want, here's the link {url}. see ya :)"
            print('>> before sms function call')
            send_sms(to=to, body=body)
            print(">sent sms!")
            return redirect(url_for("home"))

        return render_template("write.html", form = form, userId=current_user["id"] )
    except:
        return redirect(url_for("login"))

@app.route('/letter/<string:id>')
@login_required
def letter(id):
    # print(id)
    try:
        toRead= Letters.objects(myid=id).first()
        # print(toRead)
        #make status to read !
        print(toRead.author)
        print("username:",current_user['username'])
        print(current_user["partner"])
        if current_user['username'] != toRead.author:
            if toRead.author == current_user["partner"] and toRead.status == "sent":
                Letters.objects(myid=id).update(status="read")
            para = toRead.content.split('\n')
            para = [x for x in para if x]
            print(toRead.status)
            return render_template("letter.html", message=toRead, content=para)
        else:
            return redirect(url_for("home"))
    except:
        return redirect(url_for("login"))

@app.route('/about')
# @login_required
def about():
    
    return render_template("about.html")



@app.route('/logout')
def logout():
    # session.pop("user",None)
    logout_user()

    return redirect(url_for(("login")))


@app.route('/sw.js', methods=['GET'])
def sw():
    return app.send_static_file('sw.js')
