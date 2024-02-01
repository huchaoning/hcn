import numpy as np
import scipy as sp
import pandas as pd
import os
from math import *


def where_is_mypy():
    return os.path.dirname(__file__)


def open_mypy():
    import platform
    if platform.system() == 'Windows':
        os.system('start ' + where_is_mypy())
    else:
        os.system('code ' + where_is_mypy())


def square_abs(array):
    return np.square(np.abs(array))


def abs_fft(array):
    return np.abs(np.fft.fft(array))


def max_min_normalization(array):
    return (array - array.min()) / (array.max() - array.min())


def normalization(array):
    return array / array.sum()


def fast_meshgrid(h, v, scale = 1):
    return np.meshgrid(np.arange(-h/2, h/2) * scale, -np.arange(-v/2, v/2) * scale)


def read_csv(path=None):
    return np.array(pd.read_csv(path, header=None))


def to_csv(array=None, save=None):
    if array is not None:
        pd.DataFrame(array).to_csv(save, header=None, index=None)
    else:
        raise TypeError('array is None')
    

def gaussian_distribution(mean=0, std=1):
    return lambda x: np.exp(-((x-mean)**2)/(2*std**2))/np.sqrt(tau*std**2)


def poisson(param):
    return lambda k: np.exp(-param)*param**k/sp.special.factorial(k)


def sha1(file, chunk_size=65535):
    import hashlib
    with open(file, 'rb') as file:
        hash = hashlib.sha1()
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            hash.update(chunk)
    return hash.hexdigest()


def sha256(file, chunk_size=65535):
    import hashlib
    with open(file, 'rb') as file:
        hash = hashlib.sha256()
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            hash.update(chunk)
    return hash.hexdigest()


def md5(file, chunk_size=65535):
    import hashlib
    with open(file, 'rb') as file:
        hash = hashlib.md5()
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            hash.update(chunk)
    return hash.hexdigest()

