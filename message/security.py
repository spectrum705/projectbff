import random
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


from message.models import User, Letters
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

