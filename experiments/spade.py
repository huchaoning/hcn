import numpy as np
from math import sqrt
import os 
from ..plotter import imread

point_1 = (91, 110)
point_2 = (91, 404)
characteristic_width = 103

mode = '+-'
batch = True

def photon_number(img):
    if type(img) == str and os.path.exists(img):
        img = imread(img)
    if batch and (mode != '+-'):
        raise('if batch is True, mode must be +-')
    if batch:
        return img[:, point_1[1], point_1[0]] + img[:, point_2[1], point_2[0]]
    else:
        return img[point_1[1], point_1[0]] + img[point_2[1], point_2[0]]

def estimator(img, mode = mode):
    if type(img) == str and os.path.exists(img):
        img = imread(img)
    if batch and (mode != '+-'):
        raise('if batch is True, mode must be +-')
    if batch:
        k = np.sqrt(img[:, point_1[1], point_1[0]] / img[:, point_2[1], point_2[0]])
        result = 2 * characteristic_width * (1-k)/(1+k)
        result[np.logical_not(np.isfinite(k))] = -2 * characteristic_width
        return result
    else:
        if img[point_2[1], point_2[0]] == 0:
            return -2 * characteristic_width
        elif mode == '+-':
            k = sqrt(img[point_1[1], point_1[0]] / img[point_2[1], point_2[0]])
            return 2 * characteristic_width * (1-k)/(1+k)
        elif mode == '0001':
            return 2 * characteristic_width * sqrt(img[point_1[1], point_1[0]] / img[point_2[1], point_2[0]])

