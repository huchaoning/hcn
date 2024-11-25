# Code by ChatGPT
# Python module for message encryption and decryption using PBKDF2 and Fernet
# This module allows encrypting and decrypting messages with a password.

import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# Expose the public functions for encryption and decryption
__all__ = ['encrypt', 'decrypt']

# Internal function to derive the encryption key from the password
def _derive_key(password: str, salt: bytes) -> bytes:
    """
    Derives a key from the password using PBKDF2-HMAC-SHA256.

    Args:
        password (str): The password used to derive the key.
        salt (bytes): The salt value added to the password to prevent rainbow table attacks.

    Returns:
        bytes: The derived encryption key (32 bytes).
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),  # Using SHA-256 as the hash algorithm
        length=32,                  # The length of the derived key (32 bytes)
        salt=salt,
        iterations=2_000_000,       # Number of iterations (to slow down brute force)
    )
    key = kdf.derive(password.encode())  # Derive the key from the password
    return key


def encrypt(message: str, password: str) -> bytes:
    """
    Encrypts a message using a password and a random salt.

    Args:
        message (str): The plaintext message to be encrypted.
        password (str): The password used to derive the encryption key.

    Returns:
        bytes: The encrypted message concatenated with the salt (used for decryption).
    """
    salt = os.urandom(16)  # Generate a 16-byte random salt
    key = _derive_key(password, salt)  # Derive the encryption key from the password and salt
    f = Fernet(base64.urlsafe_b64encode(key))  # Create a Fernet object using the derived key
    encrypted_message = f.encrypt(message.encode())  # Encrypt the message
    return salt + encrypted_message  # Return the salt and the encrypted message


def decrypt(encrypted_message: bytes, password: str) -> str:
    """
    Decrypts an encrypted message using a password and the provided salt.

    Args:
        encrypted_message (bytes): The encrypted message concatenated with the salt.
        password (str): The password used to derive the encryption key.

    Returns:
        str: The decrypted plaintext message.
    """
    salt = encrypted_message[:16]  # Extract the salt from the encrypted data
    encrypted_message = encrypted_message[16:]  # Extract the actual encrypted message
    key = _derive_key(password, salt)  # Derive the encryption key from the password and salt
    f = Fernet(base64.urlsafe_b64encode(key))  # Create a Fernet object using the derived key
    decrypted_message = f.decrypt(encrypted_message).decode()  # Decrypt the message
    return decrypted_message
