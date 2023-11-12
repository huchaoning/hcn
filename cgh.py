import numpy as np
from .equipments import slm
from .laser import laser

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


def gen(beam=None, method=2, nx=500, ny=0):
    if isinstance(beam, laser):

        h, v = slm.resolution
        p = slm.pixel_size

        x, y = np.meshgrid(np.arange(-h/2, h/2)*p, -np.arange(-v/2, v/2)*p)

        f = fx(method=method)

        a = beam.normalized_amplitude(x, y, 0)
        phi = beam.phase_shift(x, y, 0)

        if method == 1:
            img = phi + f(a) * np.sin(phi)
        elif method == 2:
            img = f(a) * np.sin(phi)

        gx = nx / (h * p)
        gy = ny / (v * p)

        img = img * np.sin(2*np.pi*(x*gx+y*gy))
        img = img - img.min()
        img = img / img.max() * 255

        return img.astype(np.uint8)

