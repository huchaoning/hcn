import os
import shutil
import inspect
import pickle
from functools import wraps
from .macro import whereis_myutils, hashsum

CACHE_DIR = os.path.join(whereis_myutils(), '__myutils_cache__/')
if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)


def clear_cache():
    shutil.rmtree(CACHE_DIR)
    os.mkdir(CACHE_DIR)
    print('done')


def cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        cache_key = str(inspect.getsource(func)) + str(func.__name__) + str(args) + str(kwargs)
        cache_key = cache_key.encode('utf-8')
        hash_key = hashsum(cache_key)
        cache_file = os.path.join(CACHE_DIR, f'{hash_key}.pkl')

        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
            
        result = func(*args, **kwargs)
        with open(cache_file, 'wb') as f:
            pickle.dump(result, f)
        return result
    
    return wrapper
        