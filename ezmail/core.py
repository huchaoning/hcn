import os
import json

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from functools import wraps

import os
from ..macro import read


__all__ = ['email_passwd',
           'email_send',
           'email_notify']

passwd_path = os.path.join(os.path.dirname(__file__), 'passwd.json')


def email_passwd(passwd):
    dic = {'passwd': passwd}
    with open(passwd_path, 'w') as json_file:
        json.dump(dic, json_file, indent=4)
    print('plz restart kernel')



def email_send(subject, message, user):
    sender = 'vxyi@qq.com'
    if os.path.exists(passwd_path):
        passwd = read(passwd_path)['passwd']
    else:
        passwd = input('password: ')
        email_passwd(passwd)

    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = formataddr([f'vxyi/myutils: {sender}', sender])
    msg['To'] = formataddr(['User', user])
    msg['Subject'] = subject

    with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
        server.login(sender, passwd)
        server.sendmail(sender, [user], msg.as_string())
        server.quit()



def email_notify(user):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                email_send(f'{func.__name__} Completed', f'Your function: ***{func.__name__}*** completed successfully.', user)
                return result
            except Exception as e:
                email_send(f'{func.__name__} Error', f'Your function: ***{func.__name__}*** raised an error: {e}', user)
                raise
        return wrapper
    return decorator

