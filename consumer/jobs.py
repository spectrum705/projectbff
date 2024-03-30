from PIL import Image
import random
import base64
from io import BytesIO
import requests
import os
import jwt
import hashlib
from notify import *






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
        "prompt": "create  cute cartoon for the following title: "+title
    }
    headers = {
        "content-type": "application/json",
        "Content-Type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "animimagine-ai.p.rapidapi.com"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, proxies={'http':'','https':''})
        print("res:",response.json())
        stamp_url=response.json()["imageUrl"]
    except Exception as e:

        print("ERROR:",e)
        
        stamp_url= random.choice(cute_stamps)

    response = requests.get(stamp_url)
    img = response.content    

    return img

def send_notification(receiver, title, author,link):
    pass
    user = receiver
    text_body = generate_email_body(event=Events.new_letter.value,receiver=user.username,sender=author,link=link, title=title)
    adj=["cute","cute-lika-a-baby","cutest-hooman-in-the-world","pretty-like-the-moon","fluffy-lika-panda","awesome","sweet","amazing","wonderful","lovely","happy", "pretty","adorable", "tinyy","kawaii","cutesy","fluffy","funny", "cute-as-a-penguin", "supercute", "golu-molu-like-a-potato","tiny-like-a-penguin","rarest-gen","shingy-sunshine","melty-icecream", "fluff-ball"]
            
    text_sms = f"""            
        Hi {random.choice(adj)} {user.username}, \n Hope you are smiling. Your precious friend {author} just sent you a letter on ProjectBFF. The title says "{title}". Take a look whenever you want and maybe let them know about it, \n
        have a happy day and take care.
        see ya :)
        """
    
    if user.email:
        try:
            send_email(to=user.email,subject="YOU JUST GOT A NEW LETTER !!",content=text_body)
            print("sent email !")
        except:
            pass
    if user.mobile:
        try:
            send_sms(to=user.mobile,body=text_sms)
            print("sent sms !")
            
        except:
            pass
    return True



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
    # next key is only used when you rerol for a new key
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