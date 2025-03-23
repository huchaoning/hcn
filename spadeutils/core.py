import numpy as np
from scipy.special import hermite, factorial
from scipy.integrate import quad



class _PSF:
    def __init__(self, sigma=1):
        self.sigma = sigma

    def abs_sq(self, x):
        return np.abs(self.psf(x))**2

    def pixelized(self, j_th, pixel_size=1):
        return quad(self.abs_sq, pixel_size*j_th - pixel_size/2, pixel_size*j_th + pixel_size/2, limit=1000)[0]
    
    def prob_table(self, lower_limit: int, upper_limit: int, pixel_size=1):
        return np.array([self.pixelized(j, pixel_size) for j in np.arange(lower_limit, upper_limit + 1, 1)])




class SincPSF(_PSF):
    def psf(self, x, s=0):
        return (self.sigma*np.pi)**-0.5 * np.sinc((x-s) / (self.sigma*np.pi))


class GausPSF(_PSF):
    def psf(self, x, s=0):
        return (2*np.pi*self.sigma**2)**-0.25 * np.exp(-((x-s)**2) / (4*self.sigma**2))


class _Modes:
    def __init__(self, q, sigma=1):
        self.q = q
        self.sigma = sigma

        self._c_term = (2*np.pi*self.sigma**2)**-0.25
        self._exp_term = lambda x: np.exp(-x**2 / (4*self.sigma**2))


class HG(_Modes):
    def __init__(self, q, sigma=1):
        if q % 1 != 0 or q < 0:
            raise ValueError('For HG modes, q must be a natural number.')
        super().__init__(q, sigma)

        if self.q == 0:
            self._term1 = 1
            self._term2 = 1
        else:
            self._term1 = (2**self.q * factorial(self.q))**-0.5
            self._H = hermite(self.q)
            
    def wave_function(self, x):
        _x = x / (2**0.5 * self.sigma)
        if self.q != 0:
            self._term2 = 2*_x if self.q == 1 else self._H(_x)
        return self._c_term * self._term1 * self._term2 * self._exp_term(x)


class PM(_Modes):
    def __init__(self, q, sigma=1):
        if q not in (-1, 1):
            raise ValueError('Fpr PM modes, q must -1 or 1.')
        super().__init__(q, sigma)

    def wave_function(self, x):
        self._term = (1 + self.q * x / self.sigma) * 2**-0.5
        return self._c_term * self._term * self._exp_term(x)



def Born(s, modes: _Modes, psf: _PSF):
    result = []
    for _s in np.atleast_1d(s):
        fun = lambda x: modes.wave_function(x) * psf.psf(x, _s) 
        result.append(np.abs(quad(fun, -np.inf, np.inf)[0])**2)
    return np.array(result)


def FisherInfo(s, modes: _Modes, psf: _PSF, ds=1e-8):
    p1 = Born(s+ds, modes, psf)
    p2 = Born(s-ds, modes, psf)
    dp = p1 - p2
    dv = dp/(2*ds)
    return dv**2 / p1
