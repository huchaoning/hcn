import os
import base64
import getpass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# Expose the public functions for encryption and decryption
__all__ = ['encrypt', 'decrypt', 'encrypt_file', 'decrypt_file']

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


def _isNone(password):
    if password is None:
        return getpass.getpass('input password: ')
    else:
        return password


def encrypt(message: str | bytes, password: str = None) -> bytes:
    """
    Encrypts a message using a password and a random salt.

    Args:
        message (str | bytes): The message to be encrypted (can be a string or bytes).
        password (str): The password used to derive the encryption key.

    Returns:
        bytes: The encrypted message concatenated with the salt (used for decryption).
    """
    if isinstance(message, str):
        message = message.encode()  # Convert string to bytes
    
    salt = os.urandom(16)  # Generate a 16-byte random salt
    key = _derive_key(_isNone(password), salt)  # Derive the encryption key from the password and salt
    f = Fernet(base64.urlsafe_b64encode(key))  # Create a Fernet object using the derived key
    encrypted_message = f.encrypt(message)  # Encrypt the message
    return salt + encrypted_message  # Return the salt and the encrypted message


def decrypt(encrypted_message: bytes, password: str = None) -> str | bytes:
    """
    Decrypts an encrypted message using a password and the provided salt.

    Args:
        encrypted_message (bytes): The encrypted message concatenated with the salt.
        password (str): The password used to derive the encryption key.

    Returns:
        str | bytes: The decrypted plaintext message (either a string or binary data).
    """
    salt = encrypted_message[:16]  # Extract the salt from the encrypted data
    encrypted_message = encrypted_message[16:]  # Extract the actual encrypted message
    key = _derive_key(_isNone(password), salt)  # Derive the encryption key from the password and salt
    f = Fernet(base64.urlsafe_b64encode(key))  # Create a Fernet object using the derived key
    
    try:
        # Try to decode as a string (for text files)
        return f.decrypt(encrypted_message).decode()  # Try to return as string
    except UnicodeDecodeError:
        # If decoding fails, return the original binary data
        return f.decrypt(encrypted_message)  # If it's binary data, return the raw binary data


def encrypt_file(filename: str, password: str = None):
    """Encrypt any file and save it with the '.locked' extension, then delete the original file."""
    with open(filename, 'rb') as infile:
        file_content = infile.read()  # Read file content in binary mode

    encrypted_content = encrypt(file_content, _isNone(password))  # Encrypt the file content

    locked_filename = filename + '.locked'  # The filename for the encrypted file
    with open(locked_filename, 'wb') as outfile:
        outfile.write(encrypted_content)  # Write the encrypted content to the file

    os.remove(filename)  # Delete the original file


def decrypt_file(filename: str, password: str = None):
    """Decrypt a '.locked' file and restore the original file."""
    if not filename.endswith('.locked'):
        raise ValueError("The file must have a '.locked' extension")

    with open(filename, 'rb') as infile:
        encrypted_content = infile.read()  # Read the encrypted binary content

    decrypted_content = decrypt(encrypted_content, _isNone(password))  # Decrypt the content

    original_filename = filename[:-7]  # Remove the '.locked' extension to get the original filename
    with open(original_filename, 'wb') as outfile:
        outfile.write(decrypted_content)  # Write the decrypted content to the file

    os.remove(filename)  # Delete the encrypted file
