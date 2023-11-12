import numpy as np
from math import *
from scipy.special import hermite, laguerre


class hermite_gauss:
    def __init__(self, n, m):
        self.n = n
        self.m = m

    def pattern(self, scale=30):
        from .__init__ import fast_meshgrid, square_abs, imshow
        from .__init__ import max_min_normalization as nl
        n, m = self.n, self.m
        x, y = fast_meshgrid(300, 300, 1 / scale)
        rho = np.square(x) + np.square(y)
        img = hermite(n)(x) * hermite(m)(y) * np.exp(-rho/2)
        imshow(nl(square_abs(img)), title=r'$\rm HG_{'+f'{n},{m}'+'}$')


class laguerre_gauss:
    def __init__(self, n, m):
        self.n = n
        self.m = m


class laser:
    def __init__(self, wavelength = None, beam_waist = None, mode = None):
        self.wavelength = wavelength
        self.wave_number = tau / self.wavelength
        self.beam_waist = beam_waist
        self.rayleigh_range = (pi * (2*self.beam_waist)**2) / self.wavelength
        if isinstance(mode, (hermite_gauss, laguerre_gauss)):
            self.mode = mode
        elif mode is None:
            self.mode = None
        else:
            raise TypeError
    
    def beam_size(self, z):
        return self.beam_waist * sqrt(1 + (z / self.rayleigh_range)**2)

    def gouy_phase(self, z):
        return atan(z / self.rayleigh_range)

    def wave_radius_of_curvature(self, z):
        if z == 0:
            return inf
        else:
            return z * (1 + (self.rayleigh_range / z)**2)

    def amplitude(self, x, y, z):
        rho = np.square(x) + np.square(y)

        # w0 = self.beam_waist
        w = self.beam_size(z)

        if isinstance(self.mode, hermite_gauss):
            n = self.mode.n
            m = self.mode.m
            hx = hermite(n)(sqrt(2)*x/w)
            hy = hermite(m)(sqrt(2)*y/w)
            return sqrt(2**(1-n-m)/(pi*factorial(n)*factorial(m)))*hx*hy*np.exp(-rho/(w**2)) / w
        elif isinstance(self.mode, laguerre_gauss):
            pass # LG 模式的振幅, 待补充

    def phase(self, x, y, z):
        n = self.mode.n
        m = self.mode.m
    
        rho = np.square(x) + np.square(y)
        xi = self.gouy_phase(z)

        k = self.wave_number
        r = self.wave_radius_of_curvature(z)

        if isinstance(self.mode, hermite_gauss):
            return np.exp(1j*(k*(rho**2/(2*r)+z)-xi*(n+m+1)))
        elif isinstance(self.mode, laguerre_gauss):
            pass # LG 模式的相位, 待补充

    def complex_amplitude(self, x, y, z):
        return self.amplitude(x, y, z) * self.phase(x, y, z)

    def intensity(self, x, y, z):
        return np.square(np.abs(self.complex_amplitude(x, y, z))) 

    def phase_shift(self, x, y, z):
        return np.angle(self.complex_amplitude(x, y, z))

    def normalized_amplitude(self, x, y, z):
        amplitude = np.abs(self.amplitude(x, y, z))
        return amplitude / amplitude.max()

    def normalized_complex_amplitude(self, x, y, z):
        return self.normalized_amplitude(x, y, z)*np.exp(1j*self.phase_shift(x, y, z))

    def normalized_intensity(self, x, y, z):
        return np.square(np.abs(self.normalized_complex_amplitude(x, y, z)))

