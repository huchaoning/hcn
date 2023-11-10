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
        x = np.arange(-h/2, h/2) * slm.pixel_size
        y = np.arange(-v/2, v/2) * slm.pixel_size
        x, y = np.meshgrid(x, -y)
        z = 0.01

        f = fx(method=method)

        a = beam.normalized_amplitude(x, y, z)
        phi = beam.phase_shift(x, y, z) - (np.pi / 4)

        if method == 1:
            img = phi + f(a) * np.sin(phi)
        elif method == 2:
            img = f(a) * np.sin(phi)

        gx = nx / (h * slm.pixel_size)
        gy = ny / (v * slm.pixel_size)
        img = img * np.sin(2*np.pi*(x*gx+y*gy))
        img = img - img.min()
        img = img / img.max() * 255
        return img.astype(np.uint8)

