from twilio.rest import Client 
import os
from dotenv import load_dotenv
from flask import render_template
from email.message import EmailMessage
import smtplib

# DB_URI = os.getenv('DB_URI')  or os.environ["DB_URI"]
load_dotenv()


account_sid = os.getenv('account_sid') or os.environ["account_sid"]
auth_token  = os.getenv('auth_token') or os.environ["auth_token"]
messaging_service_sid = os.getenv('message_service_sid') or  os.environ["messaging_service_sid"]
gmail_id=os.getenv('gmail_id') or os.environ["gmail_id"]
gmail_password = os.getenv('gmail_password') or os.environ["gmail_password"]



def send_sms(to, body):
    sms_client = Client(account_sid, auth_token) 
    message = sms_client.messages.create(  
                            messaging_service_sid=messaging_service_sid, 
                            body=body,      
                            to=to 
                        ) 

def send_email(to, content, subject):
  # yag = yagmail.SMTP(gmail_id, gmail_password)
  msg = EmailMessage()
  msg['Subject'] = subject
  msg['From'] = gmail_id
  msg['To'] = to
  if subject == "PROJECTBFF USER FEEDBACK":
      msg.set_content( content)
  else:  
    msg.set_content(f"""
                    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Notification</title>
    </head>

    <body style="margin: 0; padding: 0; font-family: 'Arial', sans-serif; background-color: #f0f0f0;">

        <div class="container" style="display: flex; justify-content: space-between; align-items: center; height: 100vh; background-color: #f0f0f0; flex-wrap: wrap;">

            <div class="cats" style="display: grid; grid-auto-flow: dense; overflow: hidden; flex: 1;">
                <div class="cat cat--1" style="background-color: #abe7db; grid-column-start: 1; grid-column-end: 2; grid-row-start: 1; grid-row-end: 2;">
                    <img src="https://cdn.dribbble.com/users/218750/screenshots/2090988/sleeping_beauty.gif" alt="" style="width: 80%;">
                </div>
                <div class="cat cat--2" style="background-color: #f67c61; grid-column-start: 1; grid-column-end: 2; grid-row-start: 2; grid-row-end: 3;">
                    <img src="https://cdn.dribbble.com/users/6191/screenshots/1192777/catpurr.gif" alt="" style="width: 80%;">
                </div>
                <div class="cat cat--3" style="background-color: #fff9e8; grid-column-start: 1; grid-column-end: 2; grid-row-start: 3; grid-row-end: 4;">
                    <img src="https://cdn.dribbble.com/users/6191/screenshots/2211315/meal.gif" alt="" style="width: 80%;">
                </div>
                <div class="cat cat--4" style="background-color: #58a5a3; grid-column-start: 2; grid-column-end: 3; grid-row-start: 1; grid-row-end: 3;">
                    <img src="https://cdn.dribbble.com/users/6191/screenshots/1189704/walkingcat.gif" alt="" style="width: 80%;">
                </div>
                <div class="cat cat--5" style="background-color: #172535; grid-column-start: 2; grid-column-end: 3; grid-row-start: 2; grid-row-end: 4;">
                    <img src="https://cdn.dribbble.com/users/6191/screenshots/3661586/cat_sleep_dribbble.gif" alt="" style="width: 80%;">
                </div>
            </div>

            <div class="center-box" style="border: 2px dashed #172535; padding: 40px; box-sizing: border-box; background-color: #fff; text-align: left; flex: 1; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); position: relative;">

                <p style="font-size: 22px; font-weight: bold; line-height: 1.5em; margin-bottom: 30px; color: #333;">
                    {content}
                </p>

                <a href="https://tinyurl.com/projectbffs" target="_blank" style="text-decoration: none; display: inline-block; background-color: #172535; color: #fff; padding: 10px 20px; font-size: 18px; font-weight: bold; border: none; cursor: pointer;">Read Now</a>

                <img src="https://lh3.googleusercontent.com/drive-viewer/AEYmBYSSkkeUFNvXcLA7oGy-caihWfOv9ROh2ZOsq0APDpVVzf2XLt6TYBQEpls5HXMQILCUDeiqGCMf_vsYbD36MIqgMmDwDQ=s2560" alt="Logo" style="width: 80px; height: 80px; border-radius: 50%; border: 4px solid #172535; object-fit: cover; position: absolute; bottom: 20px; right: 20px;">

            </div>
        </div>
        <p style="text-align: center; font-size: 14px; margin-top: 20px;">To view this page externally, <a href="https://tinyurl.com/projectbffs/email/{content}" target="_blank" style="text-decoration: none; display: inline-block; background-color: #172535; color: #fff; padding: 10px 20px; font-size: 15px; font-weight: bold; border: none; cursor: pointer;">View Externally</a>
.</p>
    </body>

    </html>

                    """
        ,subtype='html')
  # email_content=render_template("cat_email.html", content=content)
  with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(gmail_id, gmail_password)
    smtp.send_message(msg)


  # yag.send(to, subject, msg)

