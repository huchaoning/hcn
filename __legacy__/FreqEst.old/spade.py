import numpy as np

from .common import *
from ..cache import cache
from ..macro import read

# SPADE's hyperparameter
point1 = (119, 91)
point2 = (407, 91)


def reader(arr, point1, point2):
    arr = np.array(arr)
    if len(arr.shape) == 3:
        return arr[:, point1[0], point1[1]], arr[:, point2[0], point2[1]]
    elif len(arr.shape) == 2:
        return arr[point1[0], point1[1]], arr[point2[0], point2[1]]
    else:
        raise ValueError('arr must be 2-d or 3-d')
    

# param pixels is used here only for convince
def cropper(file, pixels=None):
    data = read(file)

    def _crop(data):
        temp = data[:, :-4, :]
        copped = reader(temp, point1, point2)
        noise = (temp[:, :5, :5].mean((1,2)) + temp[:, -5:, :5].mean((1,2)) + 
                 temp[:, :5, -5:].mean((1,2)) + temp[:, -5:, -5:].mean((1,2))) / 4
        return np.array(copped).T, noise
    
    if isinstance(data, dict):
        copped, noise = {}, {}
        for k in data.keys():
            copped[k], noise[k] = _crop(data[k])
        return copped, noise
    
    else:
        return _crop(data)
    

def reshape(file, pixels=None):
    raw = read(file)

    for i, key in enumerate(freq_list):
        key = str(key)
        raw[key] = raw[key][:samples_length[i], :]
        raw[key] = raw[key].reshape(200, -1, 2)
        raw[key] = raw[key][:, :50, :]

    return raw


# SPADE's time domain estmator is extremely simple.
def estimator(data):
    data = read(data)
    time_domain = {}
    for k in data.keys():
        time_domain[k] = data[k][:, :, 0] - data[k][:, :, 1]
    return time_domain


def gen(s_list, photons, noise=0):

    def p1(s):
        return (s+2*sigma)**2*np.exp(-s**2/(4*sigma**2))/(8*sigma**2)
    def p2(s):
        return (s-2*sigma)**2*np.exp(-s**2/(4*sigma**2))/(8*sigma**2)

    data = [np.histogram(np.random.uniform(0, 1, photons), 
            bins=[0, p1(s), p1(s)+p2(s)])[0] for s in s_list]

    return (np.array(data) + np.random.poisson(noise, 2)).astype(float)

