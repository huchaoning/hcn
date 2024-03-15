import numpy as np
from math import *
from .equipments import *
from .experiments import *
from .macro import *

sigma = 103 
samples = 1000
sample_rate = 20 
dmd_frequency = 1

spade_total_n = 100 
di_total_n = 500
psf_type = 'gauss'

noise_type = 'poisson'
spade_noise_intensity = 100
spade_noise_std = 4.12
di_noise_intensity = 100
di_noise_std = 4.12

di_roi = 218
zero_point = 107
pixel_size = 4.6

p1 = lambda s: (s+2*sigma)**2*exp(-s**2/(4*sigma**2))/(8*sigma**2)
p2 = lambda s: (s-2*sigma)**2*exp(-s**2/(4*sigma**2))/(8*sigma**2)

def gen_signal(method: str, s):
    if method.lower() == 'spade':
        random_data = np.random.uniform(0, 1, size = spade_total_n)
        return np.histogram(random_data, bins=[0, p1(s), p1(s)+p2(s)])[0]

    if method.lower() == 'di':
        s_ = zero_point - s / qcmos.pixel_size
        sigma_ = sigma / qcmos.pixel_size
        random_data = np.random.normal(s_, sigma_, size=di_total_n)
        return np.histogram(random_data, bins=np.arange(di_roi+1))[0]


def gen_static(s):
    spade_signal, di_signal = [], []
    for _ in range(samples):
        spade_signal.append(gen_signal('spade', s))
        di_signal.append(gen_signal('di', s))
    return np.array(spade_signal), np.array(di_signal)


def gen_dynamic(s):
    spade_signal, di_signal, count, dmd_flip = [], [], 0, True
    for _ in range(samples):
        if dmd_flip:
            spade_signal.append(gen_signal('spade', 0))
            di_signal.append(gen_signal('di', 0))
        else:
            spade_signal.append(gen_signal('spade', s))
            di_signal.append(gen_signal('di', s))
        count = count + 1
        if count == int(sample_rate / dmd_frequency):
            count, dmd_flip = 0, not dmd_flip
    return np.array(spade_signal), np.array(di_signal)


def add_noise(signal, noise_intensity, noise_std):
    if noise_type.lower() == 'poisson':
        noise = np.random.poisson(noise_intensity, size=np.shape(signal))
    if noise_type.lower() == 'gauss':
        def relu_and_round(arr):
            arr[arr < 0] = 0
            return np.round(arr, 0)
        noise = relu_and_round(np.random.normal(noise_intensity, noise_std, size=np.shape(signal)))
    return signal + noise


def estimator(method: str, data: np.ndarray):
    if method.lower() == 'spade':
        k = np.sqrt(data[:, 1] / data[:, 0])
        result = 2 * sigma * (1-k)/(1+k)
        result[np.logical_not(np.isfinite(k))] = -2 * sigma
        return result, data.sum(axis=1)

    if method.lower() == 'di':
        data_sum = data.sum(axis=1)
        index = np.arange(data.shape[1])
        normalized_data = data / data_sum.reshape(samples, 1)
        return (zero_point - normalized_data @ index) * pixel_size, data_sum


