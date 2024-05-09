import numpy as np
import scipy as sp
import pandas as pd
import os
from math import *

import hashlib
from inspect import signature

from numpy.typing import ArrayLike


def whereis_myutils():
    return os.path.dirname(__file__)


def open_myutils():
    import platform
    if platform.system() == 'Windows':
        os.system('start ' + whereis_myutils())
    else:
        os.system('code ' + whereis_myutils())


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


def relu(arr):
    arr[arr<0] = 0 
    return arr


def variables_of(func: callable):
    return len(signature(func).parameters)


def gradient(func: callable, variable=0, epsilon=1e-4):
    def wrapper(*args):
        # if len(args) != variables_of(func):
        #     raise ValueError('specific point to calculate gradient must be provided')
        
        args_1 = list(args[:])
        args_1[variable] = args_1[variable] + epsilon / 2

        args_2 = list(args[:])
        args_2[variable] = args_2[variable] - epsilon / 2

        return (func(*args_1) - func(*args_2)) / epsilon
    return np.vectorize(wrapper)


def pdv(order: int):
    def wrapper(func: callable, variable=0, epsilon=1e-4):
        for _ in range(order):
            func = gradient(func, variable=variable, epsilon=epsilon)
        return func
    return wrapper


def gradient_descent(func: callable, 
                     init: ArrayLike = None, 
                     eta: ArrayLike = None,
                     accuracy: float = None,
                     max_loops:float = inf,
                     epsilon = 1e-4):
    
    variables = variables_of(func)
    if len(init) != variables:
        raise ValueError('specific initial value must be provided')

    gd_result = list(init[:])
    gd_process = list(init[:])

    converged = [False for _ in range(variables)]
    loop = 1

    while(True):
        converged = [False for _ in range(variables)]
        for variable in range(variables):
            update = eta[variable] * gradient(func, variable, epsilon)(*gd_result)
            gd_result[variable] = gd_result[variable] - update
            if (abs(update) <= accuracy):
                converged[variable] = True
            gd_process.append(gd_result[variable])
        loop = loop + 1
        if np.array(converged).all() or (loop >= max_loops):
            break

    if loop >= max_loops:
        print('warning: max_loops has reached, the algorithm might not converged')
    if variables == 1:
        return gd_result, np.array(gd_process)
    else:
        return gd_result, np.array(gd_process).reshape(int(len(gd_process)/variables), variables).T


def gaussian_distribution(mean=0, std=1):
    return lambda x: np.exp(-((x-mean)**2)/(2*std**2))/np.sqrt(tau*std**2)


def poisson_distribution(param):
    return lambda k: np.exp(-param)*param**k/sp.special.factorial(k)


def sha1(file, chunk_size=65535):
    with open(file, 'rb') as file:
        hash = hashlib.sha1()
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            hash.update(chunk)
    return hash.hexdigest()


def sha256(file, chunk_size=65535):
    with open(file, 'rb') as file:
        hash = hashlib.sha256()
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            hash.update(chunk)
    return hash.hexdigest()


def md5(file, chunk_size=65535):
    with open(file, 'rb') as file:
        hash = hashlib.md5()
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            hash.update(chunk)
    return hash.hexdigest()

