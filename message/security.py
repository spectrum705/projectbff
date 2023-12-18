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


# TODO test the word limit of encryption
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


# In your user creation route or method
def create(username):
    # Store the public key in the user model
    #this is the unhashed pwd that user enters
    # TODO ENCRYPT PWD WITH FERRET KEY AND STORE IN THE SESSION AND STORE HALF THE KEY IN SESSION AND HALF IN CODE
    
    password=derive_user_key("test",2242)
    print("password:",password,type(password))
    private_key, public_key = generate_key_pair()
    # password= f'b{pwd}'
    encrypted_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(password)
)
    print("0. user private key:", private_key)
    print("0. user public key:", public_key)
    new_user = User(
        myid=random.randint(1, 10000),
        username=username,
        password="test",#password_hash,
        mobile="testpwd",
        public_key=public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8'),
            private_key=encrypted_private_key.decode('utf-8') # Save the encrypted private key as a string

    )
    # new_user.save()

# Update the write function
def write():
    # Get the recipient's public key
    selected_partner=User.objects(username="bob").first()

    recipient_public_key_str = selected_partner.public_key#get_public_key(selected_partner)
    recipient_public_key = serialization.load_pem_public_key(
        recipient_public_key_str.encode(),
        backend=default_backend()
    )
    print("1. recipient public key:", recipient_public_key)

    # Generate a symmetric key for the message
    symmetric_key = Fernet.generate_key()
    print("2. symmentric key used on letter for enc:", symmetric_key)
    # Encrypt the message with chunked encryption
    test_content=" the secret letter i send you"
    
    encrypted_content = encrypt_message_chunked(test_content, symmetric_key)
    # print("3. encrypted content:",encrypted_content)
    # Encrypt the symmetric key with the recipient's public key
    encrypted_symmetric_key = encrypt_symmetric_key(symmetric_key, recipient_public_key)

    print("4. encrypted symmetric key:",encrypted_symmetric_key)
    
    
    letter = Letters(
        title="testing encryption",
        content=encrypted_content,
        symmetric_key=base64.b64encode(encrypted_symmetric_key).decode('utf-8'),
        author="admin",
        # signature=base64.b64encode(signature).decode('utf-8'), # Save the signature as a string
        receiver="kirito",
        status="sent",
        timestamp="test",
        myid=str("test2_enc")
    )
    letter.save()
    print("LETTER SAVED !!!")

# Update the letter retrieval function
def letter():
    toRead = Letters.objects(myid="test2_enc").first()

    # ... existing code ...
    test_user=User.objects(username="bob").first()
    print("test user:",test_user)
    password=b"this-is-a-secure-pass-phrase"
 # Use the same password as before maybe from session
    encrypted_private_key = test_user.private_key.encode() # Convert the string to a byte string

    # Decrypt the symmetric key using the recipient's private key
    recipient_private_key = serialization.load_pem_private_key(
        encrypted_private_key,
        password=password,
        backend=default_backend()
    )
    
    print("5. user private key:",recipient_private_key)
    encrypted_symmetric_key = base64.b64decode(toRead.symmetric_key.encode())
    symmetric_key = decrypt_symmetric_key(encrypted_symmetric_key, recipient_private_key)
    print("6. decrypted symmetric key used on Letter:",symmetric_key)

    # Decrypt the message using chunked decryption
    decrypted_content = decrypt_message_chunked(toRead.content, symmetric_key)
    print("7. decrypted contet:",decrypted_content)
   