import numpy as np


def fx(method=2, original=False):
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


def gen(complex_amplitude=None, method=2, nx=500, ny=0): 
    v, h = np.shape(complex_amplitude)
    x, y = np.meshgrid(np.arange(-h/2, h/2), -np.arange(-v/2, v/2))

    f = fx(method=method)

    a = np.abs(complex_amplitude) / np.abs(complex_amplitude).max()
    phi = np.angle(complex_amplitude)

    if method == 1:
        img = phi + f(a) * np.sin(phi + (2*np.pi*(x*nx/h+y*ny/v)))
    elif method == 2:
        img = f(a) * np.sin(phi + (2*np.pi*(x*nx/h+y*ny/v)))

    from .__init__ import max_min_normalization as nl
    img = nl(img) * 255
    del nl

    return img

