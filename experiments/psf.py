import numpy as np
from math import *


def sinc(x):
    x = np.array(x)
    return np.sinc(x / pi)


def jinc(x):
    _type_check = False
    if type(x) in (int, float):
        x = [x]
        _type_check = True

    x = np.abs(np.array(x))
    from scipy.special import j1

    with np.errstate(invalid='ignore'):
        result = 2 * j1(x) / x
        
    result[np.isnan(result)] = 1

    if _type_check:
        return result.item()
    else:
        return result



def gaus(x, sigma):
    return  np.exp(-(x**2)/(4*sigma**2)) / (tau * sigma**2)**(1/4)


def rect(x, sigma):
    return sinc(x / sigma) / sqrt(pi*sigma)


def circ(x, sigma):
    return jinc(x / sigma) * (sqrt(3*pi)) / (sqrt(32*sigma))