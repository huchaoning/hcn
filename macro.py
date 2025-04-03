import numpy as np
import scipy as sp
import pandas as pd
import os
from math import *
from PIL import Image as image
from functools import wraps

from .futils import futils, min_max_normalize
from .cache import cache

from numpy.typing import ArrayLike
from typing import Callable

import inspect
import platform
import subprocess

myutils_path = os.path.dirname(__file__)


def code(input_):
    if inspect.isfunction(input_) or inspect.ismodule(input_) or inspect.isclass(input_):
        file_path = inspect.getfile(input_)
    else:
        file_path = os.path.expanduser(input_)
    if platform.system() == 'Darwin':
        subprocess.run(['code', file_path], check=True)
    elif platform.system() == 'Windows':
        subprocess.run(['powershell.exe', '-Command', f'code {file_path}'], check=True)



def finder(path):
    path = os.path.expanduser(path)
    if platform.system() == 'Darwin':
        subprocess.run(['open', path], check=True)
    elif platform.system() == 'Windows':
        subprocess.run(['start', '', path], shell=True, check=True)



def open_myutils():
    finder(myutils_path)



def square_abs(array):
    return np.square(np.abs(array))



def abs_fft(array):
    return np.abs(np.fft.fft(array))



def fast_meshgrid(h, v, scale = 1):
    return np.meshgrid(np.arange(-h/2, h/2) * scale, -np.arange(-v/2, v/2) * scale)



def load_csv(path=None):
    return np.array(pd.read_csv(path, header=None))



def to_csv(array=None, save=None):
    if array is not None:
        pd.DataFrame(array).to_csv(save, header=None, index=None)
    else:
        raise TypeError('array is None')



def relu(arr):
    np.array(arr)
    arr[arr<0] = 0 
    return arr



def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds * 100) % 100)
    return f'{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:02}'



def gaussian_distribution(mean=0, std=1):
    def wrapper(x):
        return np.exp(-((x-mean)**2)/(2*std**2))/np.sqrt(tau*std**2)
    return futils(wrapper)



def poisson_distribution(lam):
    def wrapper(k):
        return np.exp(-lam)*lam**k/sp.special.factorial(k)
    return futils(wrapper)



def uniform_distribution(a, b):
    def wrapper(x):
        result = np.where((x >= a) & (x <= b), 1 / (b - a), 0)
        return result.item() if result.shape == () else result
    return futils(wrapper)




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




def aviread(avi_path) -> np.ndarray:
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



def load_json(json_path) -> dict:
    import json
    if not os.path.exists(json_path):
        raise FileNotFoundError(f'{json_path} is not exists')
    with open(json_path, 'r') as f:
        dic = json.load(f)
    return dic



def read(input_):
    if inspect.isfunction(input_) or inspect.ismodule(input_) or inspect.isclass(input_):
        code(input_)
        return
    elif isinstance(input_, str):
        extension = os.path.splitext(input_)[-1].lower()[1:]
        if extension == 'npz':
            return load_npz(input_)
        elif extension == 'npy':
            return np.load(input_)
        elif extension == 'avi':
            return aviread(input_)
        elif extension in ['bmp', 'tif']:
            return imread(input_)
        elif extension == 'csv':
            return load_csv(input_)
        elif extension == 'json':
            return load_json(input_)
        elif os.path.exists(input_):
            finder(input_)
            return
        else:
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

        repo = git.Repo(myutils_path)
        repo.git.add(all=True)
        repo.git.commit('-m', commit)
        repo.remotes.origin.push()

    
    def pull():
        repo = git.Repo(myutils_path)
        repo.remotes.origin.pull()

    
    def status():
        repo = git.Repo(myutils_path)
        print(repo.git.status())

except ModuleNotFoundError:
    pass




def empty_list(dimensions):
    if isinstance(dimensions, (tuple, list)):
        raise ValueError('dimensions must a tuple or a list')
    def _create(dimensions):
        if len(dimensions) == 1:
            return [[] for _ in range(dimensions[0])]
        return [_create(dimensions[1:]) for _ in range(dimensions[0])]
    return _create(dimensions)



def closed_range(start, stop, step):
    if step <= 0:
        raise ValueError('step must be positive')
    decimal = max(len(str(start+step).split('.')[1]) if '.' in str(start+step) else 0,
                  len(str(stop-step).split('.')[1]) if '.' in str(stop-step) else 0)
    arr = np.arange(start, stop + 0.1*step, step)
    return np.round(arr, decimal)




# def sinc(x):
#     x = np.array(x)
#     return np.sinc(x / pi)



# def jinc(x):
#     _type_check = False
#     if type(x) in (int, float):
#         x = [x]
#         _type_check = True
#     x = np.abs(np.array(x))

#     from scipy.special import j1
#     with np.errstate(invalid='ignore'):
#         result = 2 * j1(x) / x
        
#     result[np.isnan(result)] = 1

#     if _type_check:
#         return result.item()
#     else:
#         return result



# class psf:
#     def gaus(x, sigma):
#         return np.exp(-(x**2)/(4*sigma**2)) / (tau * sigma**2)**(1/4)

#     def rect(x, sigma):
#         return sinc(x / sigma) / sqrt(pi*sigma)

#     def circ(x, sigma):
#         return jinc(x / sigma) * (sqrt(3*pi)) / (sqrt(32*sigma))


def rgba_in_white_bg(color, alpha=None):
    from matplotlib.colors import to_rgba, to_hex
    color_ = np.array(to_rgba(color)[:-1])
    alpha_ = to_rgba(color)[-1] if not alpha else alpha
    return to_hex(np.array([1, 1, 1]) * (1-alpha_) + color_ * alpha_)