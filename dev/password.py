# By ChatGPT 4o mini

import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# 通过密码生成密钥
def generate_key_from_password(password: str, salt: bytes) -> bytes:
    # 使用PBKDF2HMAC算法将密码转化为加密密钥
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),  # 使用SHA-256散列算法
        length=32,                  # 生成32字节的密钥
        salt=salt,
        iterations=10_000_000,          # 迭代次数
    )
    key = kdf.derive(password.encode())  # 从密码派生出密钥
    return key

# 加密文本
def encrypt_message(message: str, password: str) -> bytes:
    salt = os.urandom(16)  # 生成16字节的随机盐
    key = generate_key_from_password(password, salt)  # 从密码和盐生成密钥
    f = Fernet(base64.urlsafe_b64encode(key))  # 使用从密码派生出的密钥创建Fernet对象
    encrypted_message = f.encrypt(message.encode())  # 加密消息
    return salt + encrypted_message  # 返回盐和加密后的消息，便于解密时使用相同的盐

# 解密文本
def decrypt_message(encrypted_message: bytes, password: str) -> str:
    salt = encrypted_message[:16]  # 从加密数据中提取盐
    encrypted_message = encrypted_message[16:]  # 提取加密的消息
    key = generate_key_from_password(password, salt)  # 从密码和盐生成密钥
    f = Fernet(base64.urlsafe_b64encode(key))  # 使用从密码派生出的密钥创建Fernet对象
    decrypted_message = f.decrypt(encrypted_message).decode()  # 解密消息
    return decrypted_message


# 示例使用
if __name__ == "__main__":
    password = "my_secure_password"  # 用户输入的密码
    original_message = "这是需要保护的秘密信息。"

    # 加密
    encrypted = encrypt_message(original_message, password)
    print(f"加密后的消息: {encrypted}")

    # 解密
    decrypted = decrypt_message(encrypted, password)
    print(f"解密后的消息: {decrypted}")