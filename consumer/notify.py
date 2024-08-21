from twilio.rest import Client 
import os
from email.message import EmailMessage
import smtplib
import random
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

 
class Tasks(Enum):  
    make_letter = "MAKE_LETTER"


  
class Events(Enum):
    new_letter = "NEW_LETTER"
    feedback = "FEEDBACK"
    welcome = "WELCOME"
    resend_verify_link = "RESEND_TOKEN"
    reset_password = "RESET_PASSWORD"

    
cute_stamps  = [
    "https://i.pinimg.com/originals/83/cd/ef/83cdef4f9b31d3aa9da285d1219a4d7b.jpg",
    "https://i.pinimg.com/originals/e9/64/9d/e9649d32c643667a909890d3fabba102.jpg",
    "https://i.pinimg.com/originals/94/d1/5a/94d15a107aa83ca743898a4e910fc6e3.png",
    "https://i.pinimg.com/originals/84/fb/ae/84fbaec5983044aa2d8cf288ca1a5f4a.jpg",
    "https://i.pinimg.com/originals/46/9e/30/469e3005a3a77c89a6c3960fa80f549a.jpg",
    "https://i.pinimg.com/originals/95/45/94/9545948df1a2498bb332a06878d10cca.jpg",
    "https://i.pinimg.com/originals/d9/7d/6a/d97d6a823f10713620589bcb6b7842c7.jpg",
    "https://i.pinimg.com/564x/9d/c8/92/9dc892fe84e6eaf70c7d0bb082869687.jpg",
    "https://i.pinimg.com/originals/c9/17/51/c91751068aaadfc668829af7e8db8ff5.jpg",
    "https://i.pinimg.com/originals/db/d6/4f/dbd64f8b5f641068c191d01ad49d56c9.jpg",
    "https://i.pinimg.com/originals/c9/85/e7/c985e77036a7fb3a505800fff6949efc.jpg",
    "https://i.pinimg.com/originals/7f/43/50/7f4350279f26a6884bf69da5ef6cc454.jpg",
    "https://i.pinimg.com/564x/65/2e/98/652e98feb0c98b929ddd210c20f89ea1.jpg",
    "https://i.pinimg.com/originals/06/62/38/0662383e4c551fd7bf2b4c60a89f7af2.jpg",
    "https://i.pinimg.com/564x/33/88/e9/3388e92c75cc478a79009bd7b2b7880e.jpg",
    "https://i.pinimg.com/originals/f6/77/cc/f677cc00f0d4f90bd46e5f5cbbd86777.jpg",
    "https://i.pinimg.com/564x/b3/21/19/b32119df3d5fa4b2748f811995826b20.jpg",
    "https://i.pinimg.com/564x/0a/8e/49/0a8e494b87b822c06fe849a34210f42d.jpg",
    "https://i.pinimg.com/564x/25/ab/6f/25ab6f6ad6d553e850d422dd47664aaf.jpg",
    "https://i.pinimg.com/originals/35/bb/57/35bb57f1400d301a51607f5bed4a0e35.jpg",
    "https://i.pinimg.com/564x/f5/19/52/f519526d3dbbcf9de52989cf97d54902.jpg",
    "https://i.pinimg.com/originals/fd/ed/82/fded82c1d80785ccae330d0a8b06f6ea.jpg",
    "https://i.pinimg.com/564x/cf/f1/4e/cff14e0ec5d744df10e0d5e77d270811.jpg",
    "https://i.pinimg.com/originals/a4/72/77/a472775c17dc1a9a695191e11eabb6af.jpg",
    "https://i.pinimg.com/originals/1a/77/a6/1a77a63b3fea144b96033c308252b801.jpg",
    "https://i.pinimg.com/564x/ca/11/00/ca11000e7286c959f82d893dcbb8592b.jpg",
    "https://i.pinimg.com/564x/6d/45/04/6d450440f1b0d13f5ed296b7b8077403.jpg",
    "https://i.pinimg.com/564x/6b/99/4f/6b994ff4e96b124f50a58b574253eaa5.jpg",
    "https://i.pinimg.com/564x/87/03/a3/8703a370b6b99bf251f1b429ea8513bb.jpg",
    "https://i.pinimg.com/564x/bd/df/76/bddf763f975d852b61d50542d95a285c.jpg",
    "https://i.pinimg.com/564x/bd/df/76/bddf763f975d852b61d50542d95a285c.jpg",
    "https://i.pinimg.com/564x/66/91/31/669131eb2279630358efd5418c1405c0.jpg"
]





def generate_email_body(event, receiver=None,title=None, sender=None, link=None, recover_code=None, feedback=None):
    if event==Events.new_letter.value:
        adj=["cute","cute-lika-a-baby","cutest-hooman-in-the-world","pretty-like-the-moon","fluffy-lika-panda","awesome","sweet","amazing","wonderful","lovely","happy", "pretty","adorable", "tinyy","kawaii","cutesy","fluffy","funny", "cute-as-a-penguin", "supercute", "golu-molu-like-a-potato","tiny-like-a-penguin","rarest-gen","shingy-sunshine","melty-icecream", "fluff-ball"]
        notification_body = f"""            
                    <!DOCTYPE html>
                        <html>
                        <head>
                            
                        </head>
                        <body style="font-family: Arial, sans-serif;font-size: 16px;line-height: 1.6;">
                            <div class="container" style="max-width: 600px;margin: 0 auto;padding: 20px;border: 1px solid #ccc;border-radius: 10px;">
                                <h1 style="color: #333;text-align: center;">New Letter on ProjectBFF!</h1>
                                <p style="margin-bottom: 20px;">Hi <strong>{random.choice(adj)} {receiver}</strong>,</p>
                                <p style="margin-bottom: 20px;">Hope you are smiling. Your precious friend <strong>{sender}</strong> just sent you a letter on ProjectBFF. The title says "<strong>{title}</strong>". Take a look whenever you want and maybe let them know about it.</p>
                                <p style="margin-bottom: 20px;">Have a happy day and take care. </p>
                                <p style="margin-bottom: 20px;">See ya :) </p>
                                
                         <a href="{link}" target="_blank" class="button" style="text-decoration: none;display: inline-block;background-color: #172535;color: #fff;padding: 10px 20px;font-size: 18px;font-weight: bold;border: none;cursor: pointer;">Read Now</a>
                            </div>
                        </body>
                        </html>

        """
    elif event == Events.resend_verify_link.value:
        notification_body = f"""
                                <!DOCTYPE html>
                                    <html>
                                    <head>
                                        
                                    </head>
                                    <body style="font-family: Arial, sans-serif;font-size: 16px;line-height: 1.6;color: #333;">
                                        <div class="container" style="max-width: 600px;margin: 0 auto;padding: 20px;border: 1px solid #ccc;border-radius: 10px;">
                                            <h1 style="text-align: center;">Verify Your Email Address</h1>
                                            <p style="margin-bottom: 20px;">Hey <strong>{receiver}</strong>,</p>
                                            <p style="margin-bottom: 20px;">Click the button below to verify your email quickly and start using ProjectBFF 🎉. If you need any help, feel free to contact me(from feedback page or discord).</p>
                                            <p style="margin-bottom: 20px;">Regards,<br>
                                            Spectrum <a href="https://discord.com/users/558700192992591883">(contact)</a><br>
                                            ProjectBff</p>
                                            <a href="{link}" target="_blank" class="button" style="text-decoration: none;display: inline-block;background-color: #172535;color: #fff;padding: 10px 20px;font-size: 18px;font-weight: bold;border: none;cursor: pointer;">Verify Now</a>
                                        </div>
                                    </body>
                                    </html>

        
                            """ 
    elif event == Events.feedback.value:
        notification_body = f"""
                                <!DOCTYPE html>
                                    <html>
                                    <head>
                                        
                                    </head>
                                    <body style="font-family: Arial, sans-serif;font-size: 16px;line-height: 1.6;color: #333;">
                                        <div class="container" style="max-width: 600px;margin: 0 auto;padding: 20px;border: 1px solid #ccc;border-radius: 10px;">
                                            <h1 style="text-align: center;">{title}</h1>
                                            <p style="margin-bottom: 20px;">{feedback}</p>
                                           
                                        </div>
                                    </body>
                                    </html>

        
                            """ 
                            
    elif event == Events.reset_password.value:
        notification_body = f"""
                                <!DOCTYPE html>
                                    <html>
                                    <head>
                                        
                                    </head>
                                    <body style="font-family: Arial, sans-serif;font-size: 16px;line-height: 1.6;color: #333;">
                                        <div class="container" style="max-width: 600px;margin: 0 auto;padding: 20px;border: 1px solid #ccc;border-radius: 10px;">
                                            <h1 style="text-align: center;">You can change your Password Now</h1>
                                            <p style="margin-bottom: 20px;">Hey <strong>{receiver}</strong>,</p>
                                            <p style="margin-bottom: 20px;">Here's  your reset link, it expires in 5 minutes. Click the button below to change your password to a new one. If you need any help, feel free to contact me(from feedback page or discord).</p>
                                            <p style="margin-bottom: 20px;">Regards,<br>
                                            Spectrum <a href="https://discord.com/users/558700192992591883">(contact)</a><br>
                                            ProjectBff</p>
                                            <a href="{link}" target="_blank" class="button" style="text-decoration: none;display: inline-block;background-color: #172535;color: #fff;padding: 10px 20px;font-size: 18px;font-weight: bold;border: none;cursor: pointer;">Reset</a>
                                        </div>
                                    </body>
                                    </html>

        
                            """ 
    elif event==Events.welcome.value:
        notification_body=f"""
                                            
                                        
                <!DOCTYPE html>
                <html>
                <head>
                    
                </head>
                <body style="font-family: Arial, sans-serif;font-size: 16px;line-height: 1.6;">
                    <div class="container" style="max-width: 600px;margin: 0 auto;padding: 20px;border: 1px solid #ccc;border-radius: 10px;">
                        <h1 style="color: #333;text-align: center;">Welcome to Project BFF!</h1>
                        <p style="margin-bottom: 20px;">Hey <strong>{receiver}</strong>! 🎉</p>
                        <p style="margin-bottom: 20px;">Welcome to the Project BFF! I am super happy to have you on board. 🥳</p>
                        <p style="margin-bottom: 20px;">Your account has been successfully created, and we're excited for the beautiful journey ahead. Here are your login details:</p>
                        <div class="note" style="background-color: #f8f8f8;padding: 10px;border-radius: 5px;">
                            <p style="margin-bottom: 20px;"><strong>Username:</strong> [ {receiver} ]</p>
                            <p style="margin-bottom: 20px;"><strong>Recovery Code:</strong> [ {recover_code} ]</p>
                            <p style="margin-bottom: 20px;"><strong>In case you ever forget your password you'll be able to reset it using the recovery code. So keep it really safe, I suggest you write it down somewhere.</strong></p>
                            <p style="margin-bottom: 20px;">Keep these really safe in your secret stash! 💌</p>
                            <p style="margin-bottom: 20px;"><strong>(Note: Before you can start, you need to verify your email. Use the link we sent below to verify yourself your email, The verification Link is only valid for 2 minuts so. In case the link expires, you can try to login again and we'll send you another link to verify ASAP)</strong></p>
                        </div>
                        <p style="margin-bottom: 20px;">And Get ready to embark on a magical journey where heartfelt letters bring friends closer together. 🌈 Share your thoughts, dreams, and adventures with your besties, and let the joy of friendship fill your heart.</p>
                        <p style="margin-bottom: 20px;">We can't wait to see the wonderful letters you'll write and receive! ✨</p>
                        <p style="margin-bottom: 20px;">If you ever need a sprinkle of magic or just want to share a smile, remember, I am always here for you. 🌟(You can reach me from the feedback page or discord)</p>
                        
                        <p style="margin-bottom: 20px;">Cheers to new beginnings and everlasting friendships!</p>
                        <p style="margin-bottom: 20px;">Sending you happy Smiles and Warmest hugs,</p>
                        <p style="margin-bottom: 20px;">Spectrum <a href="https://discord.com/users/558700192992591883">(contact)</a>,<br>ProjectBff,</p>
                        <a href="{link}" target="_blank" style="text-decoration: none; display: inline-block; background-color: #172535; color: #fff; padding: 10px 20px; font-size: 18px; font-weight: bold; border: none; cursor: pointer;">Verify Now</a>
                    </div>
                </body>
                </html>

                        """
                                
    return notification_body


def send_sms(to, body):
    messaging_service_sid = os.getenv('message_service_sid') or  os.environ["messaging_service_sid"]

    account_sid = os.getenv('account_sid') or os.environ["account_sid"]
    auth_token  = os.getenv('auth_token') or os.environ["auth_token"]
    sms_client = Client(account_sid, auth_token) 
    message = sms_client.messages.create(  
                            messaging_service_sid=messaging_service_sid, 
                            body=body,      
                            to=to 
                        ) 

def send_email(to, content, subject ):
    
    gmail_id=os.getenv('gmail_id') or os.environ["gmail_id"]
    gmail_password = os.getenv('gmail_password') or os.environ["gmail_password"]
  
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = gmail_id
    msg['To'] = to
    
  
    msg.set_content(content
        ,subtype='html')

   
        
    # email_content=render_template("cat_email.html", content=content)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(gmail_id, gmail_password)
        smtp.send_message(msg)


