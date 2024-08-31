import numpy as np
import scipy as sp
import pandas as pd
import os
from math import *
from PIL import Image as image
from .futils import min_max_normalize

from numpy.typing import ArrayLike
from typing import Callable

import inspect


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


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds * 100) % 100)
    return f'{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:02}'



def gaussian_distribution(mean=0, std=1):
    return lambda x: np.exp(-((x-mean)**2)/(2*std**2))/np.sqrt(tau*std**2)



def poisson_distribution(param):
    return lambda k: np.exp(-param)*param**k/sp.special.factorial(k)



def pwm(A, omega):
    k = np.arange(1, 1e4)
    def wrapper(n):
        result = [A/2 + 2*A/pi * np.sum(np.sin(k*pi/2) * np.cos(k*omega*n_) / k)
                  for n_ in [[n] if isinstance(n, (int, float)) else n][0]]
        return np.array(result)
    return wrapper



def hashsum(file, algorithm='all', chunk_size=65535):
    import hashlib

    def _core(file, algorithm, chunk_size):
        if algorithm.lower() == 'md5':
            hash = hashlib.md5()
        elif algorithm.lower() == 'sha1':
            hash = hashlib.sha1()
        elif algorithm.lower() == 'sha256':
            hash = hashlib.sha256()
        else:
            raise ValueError('Unsupported hash algorithm. Use md5, sha1, or sha256')
        
        with open(file, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                hash.update(chunk)
        return hash.hexdigest()
        
    if isinstance(file, bytes):
        return hashlib.md5(file).hexdigest()
    elif algorithm.lower() == 'all' or algorithm is None:
        return {k: _core(file, k, chunk_size) for k in ('md5', 'sha1', 'sha256')}
    else:
        return _core(file, algorithm, chunk_size)



def aviread(avi_path):
    try:
        import cv2
    except ImportError:
        raise ImportError('import cv2 failed, try pip install opencv-python')
    if not os.path.exists(avi_path):
        raise FileNotFoundError(f'{avi_path} is not exists')
    avi = cv2.VideoCapture(avi_path)
    arr = []
    while True:
        ret, frame = avi.read()
        if not ret:
            break
        arr.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    avi.release()
    return np.array(arr).astype(float)



def imread(img_path) -> np.ndarray:
    if not os.path.exists(img_path):
        raise FileNotFoundError(f'{img_path} is not exists')
    img = image.open(img_path)
    array = []
    for i in range(img.n_frames):
        img.seek(i)
        array.append(np.array(img))
    array = np.array(array, dtype=float)
    if np.shape(array)[0] == 1:
        return array[0]
    else:
        return array



def gifshow(array, auto_contrast=True, loops=0, fps=30, save=None, override=False):
    import io
    from IPython.display import display, Image as IPImage
    
    array = read(array)
    if array.ndim != 3:
        raise ValueError('array must be 3-d')
        
    duration = int(1000 / fps)
    if auto_contrast:
        images = [image.fromarray(min_max_normalize(frame, min_=0, max_=255)) 
                  for frame in array]
    else:
        images = [image.fromarray(frame)for frame in array]
    gif_buffer = io.BytesIO()

    if loops == 1:
        loop = None
    elif loops in (0, inf):
        loop = 0
    else:
        loop = loops - 1

    images[0].save(gif_buffer, 
                   format='GIF', 
                   save_all=True, 
                   append_images=images[1:], 
                   duration=duration, 
                   loop=loop)
    
    gif_buffer.seek(0)

    if save is not None:
        if os.path.exists(save):
            if override:
                os.remove(save)
            elif not override:
                raise FileExistsError('file already exists')
        else:
            with open(save, 'wb') as f:
                f.write(gif_buffer.getvalue())

    display(IPImage(data=gif_buffer.getvalue(), format='gif'))
     


def imwrite(array=None, save=None, convert=False):
    if array is not None:
        if array.dtype == np.uint8:
            image.fromarray(array).save(save)
        elif not (array.dtype == np.uint8) and convert:
            image.fromarray(array.astype(np.uint8)).save(save)
        else:
            raise TypeError('array.dtype must be np.uint8')
    else:
        raise TypeError('array is None')
    


def load_npz(npz_path) -> dict:
    if not os.path.exists(npz_path):
        raise FileNotFoundError(f'{npz_path} is not exists')
    dic = dict(np.load(npz_path))
    for key in dic.keys():
        dic[key] = dic[key].astype(float)
    return dic



def read(input_):
    if isinstance(input_, str):
        extension = os.path.splitext(input_)[-1].lower()
        if extension == '.npz':
            return load_npz(input_)
        elif extension == '.npy':
            return np.load(input_)
        elif extension == '.avi':
            return aviread(input_)
        elif extension in ['bmp', 'tif']:
            return imread(input_)
        elif extension == 'csv':
            return read_csv(input_)
        else:
            print('warning: this file format is not supported')
            return input_
    else:
        return input_



try:
    import git
    def push(commit: str = None):
        if commit is None:
            auto = input('commit is None, do you wish to generate an auto commit ([y]/n)? ')
            while True:
                if auto == '' or auto.lower() == 'y' or auto.lower() == 'yes':
                    commit = 'An auto commit.'
                    break
                elif auto.lower() == 'n' or auto.lower() == 'no':
                    commit = input('enter the commit message for your changes')
                    break
                else:
                    auto = input('invalid input, do you wish to generate an auto commit ([y]/n)? ')

        while True:
            if type(commit) == str:
                break
            else:
                commit = input('commit must be a str, enter the commit message for your changes')

        repo = git.Repo(whereis_myutils())
        repo.git.add(all=True)
        repo.git.commit('-m', commit)
        repo.remotes.origin.push()

    def pull():
        repo = git.Repo(whereis_myutils())
        repo.remotes.origin.pull()

    def status():
        repo = git.Repo(whereis_myutils())
        print(repo.git.status())

except ModuleNotFoundError:
    pass


def code(module):
    os.system(f'code {inspect.getfile(module)}')


def empty_list(dimensions):
    if isinstance(dimensions, (tuple, list)):
        raise ValueError('dimensions must a tuple or a list')
    def _create(dimensions):
        if len(dimensions) == 1:
            return [[] for _ in range(dimensions[0])]
        return [_create(dimensions[1:]) for _ in range(dimensions[0])]
    return _create(dimensions)


# from inspect import signature
# 由于自己写的算法效率低, 计算速度慢, 弃用

# def variables_of(func: Callable):
#     return len(signature(func).parameters)

# 
# def gradient(func: Callable, variable=0, epsilon=1e-4):
#     def wrapper(*args):
#         # if len(args) != variables_of(func):
#         #     raise ValueError('specific point to calculate gradient must be provided')
        
#         args_1 = list(args[:])
#         args_1[variable] = args_1[variable] + epsilon / 2

#         args_2 = list(args[:])
#         args_2[variable] = args_2[variable] - epsilon / 2

#         return (func(*args_1) - func(*args_2)) / epsilon
#     return np.vectorize(wrapper)


# def pdv(order: int):
#     def wrapper(func: Callable, variable=0, epsilon=1e-4):
#         for _ in range(order):
#             func = gradient(func, variable=variable, epsilon=epsilon)
#         return func
#     return wrapper


# def gradient_descent(func: Callable, 
#                      init: ArrayLike = None, 
#                      eta: ArrayLike = None,
#                      accuracy: float = None,
#                      max_loops:float = inf,
#                      epsilon = 1e-4):
    
#     variables = variables_of(func)
#     if len(init) != variables:
#         raise ValueError('specific initial value must be provided')

#     gd_result = list(init[:])
#     gd_process = list(init[:])

#     converged = [False for _ in range(variables)]
#     loop = 1

#     while(True):
#         converged = [False for _ in range(variables)]
#         for variable in range(variables):
#             update = eta[variable] * gradient(func, variable, epsilon)(*gd_result)
#             gd_result[variable] = gd_result[variable] - update
#             if (abs(update) <= accuracy):
#                 converged[variable] = True
#             gd_process.append(gd_result[variable])
#         loop = loop + 1
#         if np.array(converged).all() or (loop >= max_loops):
#             break

#     if loop >= max_loops:
#         print('warning: max_loops has reached, the algorithm might not converged')
#     if variables == 1:
#         return gd_result, np.array(gd_process)
#     else:
#         return gd_result, np.array(gd_process).reshape(int(len(gd_process)/variables), variables).T

