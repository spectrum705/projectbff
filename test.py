# from mongoengine import Document, StringField
# from cryptography.fernet import Fernet
# import base64
# from message.models import Letters, User
# from cryptography.hazmat.primitives import hashes
# from passlib.hash import argon2
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# import base64




# # Step 3: Key Derivation Function (KDF) using Argon2 from Passlib
# def     derive_key(secret, salt):
#     # Convert the salt to bytes
#     salt_bytes = salt.to_bytes(16, byteorder='big')  # Assuming a 16-byte salt

#     # Hash the secret (password) using Argon2 with the provided salt
#     hash_instance = argon2.using(salt=salt_bytes)
#     hash_str = hash_instance.hash(secret)

#     # Use PBKDF2 to derive a 32-byte key from the Argon2 hash
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA256(),
#         iterations=100000,
#         length=32,
#         salt=salt_bytes,
#         backend=default_backend())
#     key = base64.urlsafe_b64encode(kdf.derive(hash_str.encode('utf-8')))
#     return key

# # Step 2: Define a model with EncryptedField
# class EncryptedData(Document):
#     encrypted_content = StringField()

# # Step 3: Encryption and Decryption functions
# def generate_key():
#     return Fernet.generate_key()

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
# #     # Step 1: Generate a key
# #     # we need the same key for enc and decry
    
#     user_secret = "userpassword"

#     # User-specific salt (this should be unique for each user)
#     user_salt = 379240#os.urandom(16)

#     # Derive user-specific key using Argon2
#     user_key = derive_key(user_secret, user_salt)
#     print(f"User Key: {user_key}")
    
# # # b'wyckM32zKHf516M18fXYOqa7Hdy6OshqRfcCobHER2A='

#     # Encrypt and store data in MongoDB
#     original_message = "its new guggiv h"
#     encrypted_message = encrypt_message(original_message, user_key)


#     retrieved_data = Letters.objects(myid="test").first()
#     retrieved_message_str = retrieved_data.content
#     print(f"Retrieved Message (String): {retrieved_message_str}")
#     # Convert the string back to binary (Base64 decoding)
#     retrieved_message = base64.b64decode(retrieved_message_str.encode('utf-8'))
#     print(f"Retrieved Message: {retrieved_message}")

#     # Decrypt the message
#     decrypted_message = decrypt_message(retrieved_message, user_key)
#     print(f"Decrypted Message (got from DB): {decrypted_message}")

 