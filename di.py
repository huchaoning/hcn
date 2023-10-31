import numpy as np
from math import log10


zero_point = 0
pixel_size = 1
axis = 'y'


def photon_number(img):
    return img.sum()


def estimator(img, axis = axis):

    if axis == 'x':
        img = np.sum(img, axis=0)
        img = img / img.sum()
        index = np.arange(len(img))
        return (zero_point - index @ img) * pixel_size
    
    elif axis == 'y':
        img = np.sum(img, axis=1)
        img = img / img.sum()
        index = np.arange(len(img))
        return (zero_point - index @ img) * pixel_size


def signal_to_noise_ratio(signal=None, noise=None):
    return 10 * log10(sum(photon_number(signal)) / sum(photon_number(noise)))