from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(password):
    """Generate a 32-byte key from the given password"""
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key[:32])  

def encrypt_text(password, text):
    """Encrypt the text using the given password"""
    key = generate_key(password)
    cipher = Fernet(key)
    encrypted_text = cipher.encrypt(text.encode()).decode()
    return encrypted_text

def decrypt_text(password, encrypted_text):
    """Decrypt the text using the given password"""
    key = generate_key(password)
    cipher = Fernet(key)
    try:
        decrypted_text = cipher.decrypt(encrypted_text.encode()).decode()
        return decrypted_text
    except:
        return "Incorrect password or data is corrupted."
