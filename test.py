from mongoengine import Document, StringField
from cryptography.fernet import Fernet
import base64
from message.models import Letters, User
from cryptography.hazmat.primitives import hashes
from passlib.hash import argon2
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# maybe change this to requirements.txt
# TODO
# pip install pyopenssl==22.1.0



# Step 3: Key Derivation Function (KDF) using Argon2 from Passlib
def     derive_key(secret, salt):
    # Convert the salt to bytes
    salt_bytes = salt.to_bytes(16, byteorder='big')  # Assuming a 16-byte salt

    # Hash the secret (password) using Argon2 with the provided salt
    hash_instance = argon2.using(salt=salt_bytes)
    hash_str = hash_instance.hash(secret)

    # Use PBKDF2 to derive a 32-byte key from the Argon2 hash
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        length=32,
        salt=salt_bytes,
        backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(hash_str.encode('utf-8')))
    return key

# Step 2: Define a model with EncryptedField
class EncryptedData(Document):
    encrypted_content = StringField()

# Step 3: Encryption and Decryption functions
def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message.encode('utf-8'))
    return encrypted_message

def decrypt_message(encrypted_message, key):
    cipher_suite = Fernet(key)
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
    return decrypted_message

# Example usage
if __name__ == "__main__":
#     # Step 1: Generate a key
#     # we need the same key for enc and decry
    
    user_secret = "userpassword"

    # User-specific salt (this should be unique for each user)
    user_salt = 379240#os.urandom(16)

    # Derive user-specific key using Argon2
    user_key = derive_key(user_secret, user_salt)
    print(f"User Key: {user_key}")
    
# # b'wyckM32zKHf516M18fXYOqa7Hdy6OshqRfcCobHER2A='

    # Encrypt and store data in MongoDB
    original_message = "its new guggiv h"
    encrypted_message = encrypt_message(original_message, user_key)

    
    
    
    # # encryption_key = generate_key()
    # # print(f"Encryption Key: {encryption_key}")
 
    # # Step 4: Encrypt and store data in MongoDB
    # print(f"Original Message: {original_message}")
 
    # # Encrypt the message
    # print(f"Encrypted Message: {encrypted_message}")
 
    # # Convert the binary data to a string (Base64 encoding)
    # encrypted_message_str = base64.b64encode(encrypted_message).decode('utf-8')
 
    # # goes to MongoDB
    # letter=Letters(title="test",content=encrypted_message_str,author="test",receiver="kirito",status="sent",timestamp="test", myid="test")
    # letter.save()
    # print(f"Encrypted Message (String goes to DB): {encrypted_message_str}")


    # retrieve the encrypted message string in MongoDB
    #mykey=b'umCixoE9AJA05sUhj-ZyaeR66nM5xI8_CUJ4XTTFx7E='
    retrieved_data = Letters.objects(myid="test").first()
    retrieved_message_str = retrieved_data.content
    print(f"Retrieved Message (String): {retrieved_message_str}")
    # Convert the string back to binary (Base64 decoding)
    retrieved_message = base64.b64decode(retrieved_message_str.encode('utf-8'))
    print(f"Retrieved Message: {retrieved_message}")

    # Decrypt the message
    decrypted_message = decrypt_message(retrieved_message, user_key)
    print(f"Decrypted Message (got from DB): {decrypted_message}")

    
    
    # TODO REFER THIS
#     from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives.kdf.argon2 import Argon2KDF
# from cryptography.hazmat.primitives import hashes
# from cryptography.fernet import Fernet
# from mongoengine import Document, StringField
# from message.models import Letters
# import os

# # Step 2: Define a model with EncryptedField
# class EncryptedData(Document):
#     encrypted_content = StringField()

# # Step 3: Key Derivation Function (KDF) using Argon2
# def derive_key(secret, salt):
#     kdf = Argon2KDF(
#         algorithm=hashes.Argon2(),
#         length=32,
#         salt=salt,
#         parallelism=2,
#         memory_cost=102400,
#         time_cost=2,
#     )
#     key = kdf.derive(secret)
#     return key

# # Step 4: Encryption and Decryption functions
# def encrypt_message(message, key):
#     cipher_suite = Fernet(key)
#     encrypted_message = cipher_suite.encrypt(message.encode('utf-8'))
#     return encrypted_message

# def decrypt_message(encrypted_message, key):
#     cipher_suite = Fernet(key)
#     decrypted_message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
#     return decrypted_message

# # Example usage
# if __name__ == "__main__":
#     # User-specific secret (this should be securely stored for each user)
#     user_secret = b'user_specific_secret'

#     # User-specific salt (this should be unique for each user)
#     user_salt = os.urandom(16)

#     # Derive user-specific key using Argon2
#     user_key = derive_key(user_secret, user_salt)
#     print(f"User Key: {user_key}")

#     # Encrypt and store data in MongoDB
#     original_message = "Hello, this is a secret message!"
#     encrypted_message = encrypt_message(original_message, user_key)

#     # Save the encrypted content to MongoDB
#     encrypted_content_str = base64.b64encode(encrypted_message).decode('utf-8')
#     letter = Letters(title="test", content=encrypted_content_str, author="test", receiver="kirito", status="sent", timestamp="test", myid="test")
#     letter.save()

#     # Retrieve and decrypt the message from MongoDB
#     retrieved_data = Letters.objects(myid="test").first()
#     retrieved_message_str = retrieved_data.content
#     retrieved_message = base64.b64decode(retrieved_message_str.encode('utf-8'))
#     decrypted_message = decrypt_message(retrieved_message, user_key)

#     print(f"Original Message: {original_message}")
#     print(f"Decrypted Message: {decrypted_message}")
