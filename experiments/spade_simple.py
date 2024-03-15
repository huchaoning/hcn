import numpy as np
from math import sqrt, exp
import os 
from ..plotter import imread
from .__init__ import sigma

point_1 = (91, 110)
point_2 = (91, 404)
characteristic_width = sigma

def photon_number(img):
    if type(img) == str and os.path.exists(img):
        img = imread(img)
    return img[:, point_1[1], point_1[0]] + img[:, point_2[1], point_2[0]]


def estimator(img, output_photon_number=True):
    if type(img) == str and os.path.exists(img):
        img = imread(img)

    k = np.sqrt(img[:, point_1[1], point_1[0]] / img[:, point_2[1], point_2[0]])
    result = 2 * characteristic_width * (1-k)/(1+k)
    result[np.logical_not(np.isfinite(k))] = -2 * characteristic_width

    if output_photon_number:
        return result, photon_number(img)
    else:
        return result


def p1(s, sigma):
    return (s+2*sigma)**2*exp(-s**2/(4*sigma**2))/(8*sigma**2)

def p2(s, sigma):
    return (s-2*sigma)**2*exp(-s**2/(4*sigma**2))/(8*sigma**2)

def gen_signal(s, resource):
    random_data = np.random.uniform(0, 1, size = resource)
    return np.histogram(random_data, bins=[0, p1(s), p1(s)+p2(s)])[0]