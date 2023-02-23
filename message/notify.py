from twilio.rest import Client 
import os
from dotenv import load_dotenv
# DB_URI = os.getenv('DB_URI')  or os.environ["DB_URI"]
load_dotenv()


account_sid = os.getenv('account_sid') or os.environ["account_sid"]
auth_token  = os.getenv('auth_token') or os.environ["auth_token"]
messaging_service_sid = os.getenv('message_service_sid') or  os.environ["messaging_service_sid"]



def send_sms(to, body):
    sms_client = Client(account_sid, auth_token) 
    message = sms_client.messages.create(  
                            messaging_service_sid=messaging_service_sid, 
                            body=body,      
                            to=to 
                        ) 


