import time
import jwt
import uuid
import json
import hashlib
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
import base64
from cryptography.hazmat.primitives import hashes
from passlib.hash import argon2
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import datetime
from message import Events


def derive_user_key(secret, salt):
    # Convert the salt to bytes
    salt_bytes = salt.to_bytes(16, byteorder='big')  # Assuming a 16-byte salt

    # Hash the secret (password) using Argon2 with the provided salt
    hash_instance = argon2.using(salt=salt_bytes)
    hash_str = hash_instance.hash(secret)

    # Use PBKDF2 to derive a 32-byte key from the Argon2 hash
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=200000,
        length=32,
        salt=salt_bytes,
        backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(hash_str.encode('utf-8')))
    return key

# Function to generate an RSA key pair
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key



# Function to encrypt the symmetric key using the recipient's public key
def encrypt_symmetric_key(symmetric_key, recipient_public_key):
    encrypted_key = recipient_public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key
# Function to decrypt the symmetric key using the recipient's private key
def decrypt_symmetric_key(encrypted_key, recipient_private_key):
    decrypted_key = recipient_private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_key



def encrypt_message_chunked(message, key):
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message.encode('utf-8'))
    return encrypted_message
#
def decrypt_message_chunked(encrypted_message, key):
    cipher_suite = Fernet(key)
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
    return decrypted_message


def encrypt_file_chunked(message, key):
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message)
    return encrypted_message
#
def decrypt_file_chunked(encrypted_message, key):
    cipher_suite = Fernet(key)
    decrypted_message = cipher_suite.decrypt(encrypted_message)
    return decrypted_message


def encrypt_private_key(user_key, private_key):
    enc_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(user_key)
            )
    return enc_key



def decrypt_private_key(user_key, encrypted_key):
    try:
        user_private_key = serialization.load_pem_private_key(
                encrypted_key,
                password=user_key,
                backend=default_backend()
            )
        return True, user_private_key
    except:
        return False, None
   

# Function to generate the JWT token
def generate_user_jwt_token(url, signing_key,json_data, event):
    current_time = int(time.time())
    # expiration_time = current_time + (10 * 365 * 24 * 60 * 60)  # TODO make it 2 mins

    # expiration_time = current_time + 300  # JWT expiration time (5 minutes)
    jti = str(uuid.uuid4())

    payload = {
        "iss": "ProjectBff",
        "sub": url,
        "iat": current_time,
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=40),
        "jti": jti,  # Unique ID for the token
        "username": json_data["username"],
        "event":event
         
    }
    jwt_token = jwt.encode(payload, signing_key, algorithm='HS256')
    return jwt_token

def verify_user_token(token, key):
    valid_events = [Events.welcome.value,Events.resend_verify_link.value,Events.reset_password.value]
    try:
        decoded_token = jwt.decode(token, key, algorithms=['HS256'], )
        print("DECODED:",decoded_token)
    except jwt.ExpiredSignatureError:
        return {'status': False, "info":'ExpiredSignatureError'}

    except Exception as e:
        print("ERROR:",e)
        return {'status': False, "info":'Invalid token'}
    if decoded_token['iss'] != 'ProjectBff':
        print(decoded_token['iss'])
        print("invalid publisher")
    if  "event" not in decoded_token or decoded_token['event'] not in valid_events:
        print("invalid event")

        return {'status': False,'info': 'Issuer mismatch'}
    
    return {'status': True, "info":"Token is valid", "username":decoded_token["username"], "event":decoded_token["event"]}


def validate_request(signature,key,url,body):
    try:
        decoded_token = jwt.decode(signature, key, algorithms=['HS256'], verify_exp=False)
        # print("decoded:",decoded_token)
        # TODO remove prints

    except jwt.ExpiredSignatureError:
        return {'status': False, "info":'ExpiredSignatureError'}

    except Exception as e:
        print("ERROR:",e)
        return {'status': False, "info":'Invalid token'}

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