import numpy as np

resolution = (1920, 1080)

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
    

