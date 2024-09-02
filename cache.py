import os
import shutil
import inspect
import pickle
import time

from functools import wraps
from hashlib import md5


cache_dir = os.path.join(os.path.dirname(__file__), '__myutils_cache__/')
expiration_time = 2 * 24 * 60 * 60

if not os.path.exists(cache_dir):
    os.mkdir(cache_dir)


__all__ = [
    'clean_all_cache',
    'clean_expired_cache',
    'open_cache_dir',
    'cache'
]


def open_cache_dir():
    import platform
    if platform.system() == 'Windows':
        os.system('start ' + cache_dir)
    else:
        os.system('open ' + cache_dir)


def clean_all_cache():
    shutil.rmtree(cache_dir)
    os.mkdir(cache_dir)
    print('done')


def clean_expired_cache():
    current_time = time.time()
    for filename in os.listdir(cache_dir):
        file_path = os.path.join(cache_dir, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'rb') as f:
                    metadata = pickle.load(f)
                    last_access_time = metadata['last_access_time']
                    if current_time - last_access_time > expiration_time:
                        os.remove(file_path)
            except (EOFError, pickle.UnpicklingError):
                os.remove(file_path)


def cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        cache_key = str(inspect.getsource(func)) + str(func.__name__) + str(args) + str(kwargs)
        cache_key = cache_key.encode('utf-8')
        hash_key = md5(cache_key).hexdigest()
        cache_file = os.path.join(cache_dir, f'{hash_key}.pkl')

        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                metadata = pickle.load(f)
                metadata['last_access_time'] = time.time()
                with open(cache_file, 'wb') as f:
                    pickle.dump(metadata, f)
                return metadata['result']
            
        result = func(*args, **kwargs)
        metadata = {'result': result, 'last_access_time': time.time()}
        with open(cache_file, 'wb') as f:
            pickle.dump(metadata, f)
        return result
    
    return wrapper
