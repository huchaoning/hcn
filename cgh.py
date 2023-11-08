import numpy as np

arrizon1 = 1
arrizon2 = 2

class cgh:
    def __init__(self, method):
        self.method = method

    def fx(self, original=False):
        from os import path
        fx = np.load(path.join(path.dirname(__file__), f'fx{self.method}.npy'))
        del path
        if original:
            return fx
        else:
            from scipy.interpolate import interp1d
            fx = interp1d(np.linspace(0, 1, 801), fx)
            del interp1d
            return fx
        
    def gen(self, beam):
        pass

