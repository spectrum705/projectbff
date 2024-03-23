from twilio.rest import Client 
import os
from email.message import EmailMessage
import smtplib
import random
from dotenv import load_dotenv
from jobs import Events

load_dotenv()

 






def generate_email_body(event, receiver=None,title=None, password=None,sender=None, link=None, recover_code=None, feedback=None):
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
                                <p style="margin-bottom: 20px;">Have a happy day and take care. See ya :)</p>
                            </div>
                         <a href="{link}" target="_blank" class="button" style="text-decoration: none;display: inline-block;background-color: #172535;color: #fff;padding: 10px 20px;font-size: 18px;font-weight: bold;border: none;cursor: pointer;">Read Now</a>
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
                            <p style="margin-bottom: 20px;"><strong>Password:</strong> [ {password} ]</p>
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


