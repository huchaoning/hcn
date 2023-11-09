import numpy as np
from .equipments import slm

arrizon1 = 1
arrizon2 = 2

method = 1

def fx(method=method, original=False):
    from os import path
    fx = np.load(path.join(path.dirname(__file__), f'fx{method}.npy'))
    del path
    if original:
        return fx
    else:
        from scipy.interpolate import interp1d
        fx = interp1d(np.linspace(0, 1, 801), fx)
        del interp1d
        return fx

def meshgrid(resolution, pixel_size):
    x = np.arange(-resolution[0]/2, resolution[0]/2) / pixel_size
    y = np.arange(-resolution[1]/2, resolution[1]/2) / pixel_size
    return np.meshgrid(x, -y)

