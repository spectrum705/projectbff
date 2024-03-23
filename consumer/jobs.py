from PIL import Image

import base64
from io import BytesIO
import requests
import os
# from models import Letters, db, User
import time
import jwt
import hashlib
from enum import Enum
from cryptography.fernet import Fernet


class Tasks(Enum):  
    make_letter = "MAKE_LETTER"


  
class Events(Enum):
    new_letter = "NEW_LETTER"
    feedback = "FEEDBACK"
    welcome = "WELCOME"
    resend_verify_link = "RESEND_TOKEN"
    reset_password = "RESET_PASSWORD"

    

def encrypt_file_chunked(message, key):
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message)
    return encrypted_message
#
def decrypt_file_chunked(encrypted_message, key):
    cipher_suite = Fernet(key)
    decrypted_message = cipher_suite.decrypt(encrypted_message)
    return decrypted_message



def compress_image(file, max_width=1024, max_height=1024):
    """
    Compresses an image without cropping.

    Parameters:
        file: FileStorage object or file-like object
            The image file to compress.
        max_width: int, optional
            The maximum width of the compressed image.
        max_height: int, optional
            The maximum height of the compressed image.

    Returns:
        bytes: The compressed image data.
    """
    # Open the image using PIL
    if type(file) is bytes:
        file = BytesIO(file)
    image_file = Image.open(file)
    image = image_file.convert('RGB')
    # Calculate the aspect ratio of the original image
    aspect_ratio = image.width / image.height

    # Calculate the new dimensions to fit within the maximum dimensions while preserving aspect ratio
    new_width = min(max_width, image.width)
    new_height = min(max_height, image.height)
    if aspect_ratio > 1:
        # Landscape orientation
        new_height = int(new_width / aspect_ratio)
    else:
        # Portrait or square orientation
        new_width = int(new_height * aspect_ratio)

    # Resize the image without cropping
    resized_image = image.resize((new_width, new_height))

    # Create a BytesIO object to store the compressed image
    compressed_image = BytesIO()

    # Save the compressed image to the BytesIO object
    resized_image.save(compressed_image, format='JPEG')

    # Get the compressed image data as bytes
    compressed_image_data = compressed_image.getvalue()

    return compressed_image_data





# Using AI GEN
def make_stamp(title):
   
    url = "https://animimagine-ai.p.rapidapi.com/generateImage"
    RAPID_API_KEY = os.getenv('RAPID_API_KEY') or os.environ["RAPID_API_KEY"]


    payload = {
        "selected_model_id": "anything-v5",
        "selected_model_bsize": "512",
        "prompt": "create an beautiful art for the following title: "+title
    }
    headers = {
        "content-type": "application/json",
        "Content-Type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "animimagine-ai.p.rapidapi.com"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        stamp_url=response.json()["imageUrl"]
    # print(response.json())
    except:
        stamp_url="https://i.pinimg.com/originals/83/cd/ef/83cdef4f9b31d3aa9da285d1219a4d7b.jpg"

    response = requests.get(stamp_url)
    # print(response.content)
    # img = Image.open(BytesIO(response.content))
    img = response.content    

    return img

def send_notification(receiver, title, author):
    pass
    # user=User.objects(username=receiver).first()
    # text_body=generate_notification_body(receiver=receiver, sender=author, title=title)
    # if user.mobile:
    #     send_sms(to=user.mobile,body=text_body)
    # if user.email:
    #     send_email(to=user.email,subject="YOU JUST GOT A NEW LETTER !!",content=text_body)
    # return True


# def make_letter(letter_data):
#     print(type(letter_data['enc_content']))
#     enc_content = base64.b64decode(letter_data['enc_content'])
#     print(type(enc_content))
#             # encrypt_symmetric_key = base64.b64decode(letter_data['encrypt_symmetric_key'])
#     stamp_url=make_stamp(letter_data["letter_title"])
#     # print(f"name{letter_data['letter_title']}")
    
#     letter=Letters(title=letter_data["letter_title"],
#                 content=enc_content   ,
#                 symmetric_key=letter_data["encrypted_symmetric_key"],
#                 author=letter_data["author"],
#                 receiver=letter_data["receiver"],
#                 status="sent",
#                 timestamp=letter_data["timestamp"], 
#                 myid=letter_data["letter_id"],
#                 stamp_url=stamp_url
#                 )
   
#     # letter.save()
#     print( "TASK FINISHED!! ")
#     return True

# def add_images(image_data_list, letter_id):
#     letter= Letters.objects(myid=letter_id).first()
#     print(type(image_data_list[0]))
#     print(type(base64.b64decode(image_data_list[0])))
    
#     for encoded_image in image_data_list:
# # Decode base64 encoded image data

#         image_data = base64.b64decode(encoded_image)
       
#         grid_fs_proxy = db.fields.GridFSProxy()

#         grid_fs_proxy.put(image_data)
#         letter.images.append(grid_fs_proxy)
#     letter.attachment = True
#     # letter.save()# add images here
#     return True


def validate_with_key(key, signature, url, body):
    try:
        decoded_token = jwt.decode(signature, key, algorithms=['HS256'], verify_exp=False)
        # print("decoded:",decoded_token)
        # TODO remove prints
    
    except jwt.ExpiredSignatureError:
          return {'status': False, "info":'ExpiredSignatureError'}

    except Exception as e:
        print("ERROR:",e)
        return {'status': False, "info":f'{e}'}

    # Validate the claims in the JWT token
    if decoded_token['iss'] != 'Upstash':
        print(decoded_token['iss'])
        print("invalid publisher")

        return {'status': False,'info': 'Issuer mismatch'}
    
    if  (decoded_token["sub"] != url):
        print("taskURL:",url)
        print("decodedSUB:",decoded_token["sub"] )
        print("STT:",{ "Invalid subject": {decoded_token['sub']}, "want": {'url'}},type({ "Invalid subject": {decoded_token['sub']}, "want": {url}}))
        info= f"Invalid subject: {decoded_token['sub']}, want: {'url'}"
        return {        'status': False, "info":info}
        
    body_hash = hashlib.sha256(body).digest()
    body_hash_b64 = base64.urlsafe_b64encode(body_hash).decode().rstrip("=")

    if decoded_token["body"].rstrip("=") != body_hash_b64:
        print("decoded bodu:",decoded_token["body"].rstrip("="))
        print("body hash:",body_hash_b64)
        info=f"Invalid body hash: {decoded_token['body']}, want: {body_hash_b64}"
        return {'status': False, "info":info}
    
    
    return {'status': True, "info":"Token is valid"}
    
def verify_request(signature,current_key, next_key,url,body):
    # print("task:",task)
    
    # print("signature:",signature)
    # print("boduy",body)
    # TODO make it abstract 
    
    result = validate_with_key(signature=signature,key=current_key,url=url,body=body)
    print(f"in try part:{result}")
    if not result["status"]: 
        result = validate_with_key(signature=signature,key=next_key,url=url,body=body)
        print(f"in except part:{result}")
    
    return result
        
    # return result