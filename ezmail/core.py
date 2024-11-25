import os
import json
import base64
import getpass

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from functools import wraps

import os
from ..macro import read
from ..cryptutils import encrypt, decrypt, cpuid


__all__ = ['ezmail_passwd',
           'clear_token',
           'send_email',
           'email_notify']

token_path = os.path.join(os.path.dirname(__file__), 'token.json')
encrypt_key = b'\x82Z\xb7U2\xf0W\x9da\xff\x1eUv\x95S\xa0gAAAAABnRA7GgE1mfqtm1lVXXkgpnQxqGKIQuP-pcXbdu3dqn8ali8ZBmj9hPBBmmfg2XvkdYlLgcBPGgzgIqrySRWzeWBb2VJrthjpOarPuRFucPj6TWMk='


def ezmail_passwd(passwd):
    key = decrypt(encrypt_key, passwd)
    token = {'token': base64.b64encode(encrypt(key, cpuid())).decode('utf-8')}
    with open(token_path, 'w') as f:
        json.dump(token, f, indent=4)
    print('plz restart kernel')


def clear_token():
    if os.path.exists(token_path):
        os.remove(token_path)
        print('done')
    else:
        print(f"token '{token_path}' not exists")


def send_email(subject, message, user):
    sender = 'vxyi@qq.com'
    if os.path.exists(token_path):
        key = decrypt(base64.b64decode(read(token_path)['token']), cpuid())
    else:
        passwd = getpass.getpass('input password: ')
        ezmail_passwd(passwd)
        key = decrypt(encrypt_key, passwd)

    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = formataddr([f'vxyi/myutils: {sender}', sender])
    msg['To'] = formataddr(['User', user])
    msg['Subject'] = subject

    with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
        server.login(sender, key)
        server.sendmail(sender, [user], msg.as_string())
        server.quit()



def email_notify(user):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                send_email(f'{func.__name__} Completed', f'Your function: ***{func.__name__}*** completed successfully.', user)
                return result
            except Exception as e:
                send_email(f'{func.__name__} Error', f'Your function: ***{func.__name__}*** raised an error: {e}', user)
                raise
        return wrapper
    return decorator

