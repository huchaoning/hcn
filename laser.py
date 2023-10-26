import numpy as np
from math import factorial
from scipy.special import hermite, laguerre


class hermite_gauss:
    def __init__(self, n, m):
        self.n = n
        self.m = m

    @classmethod
    def is_what(self):
        return 'Hermite Gauss {}, {}'.format(self.n, self.m)
    

class laguerre_gauss:
    def __init__(self, n, m):
        self.n = n
        self.m = m

    @classmethod
    def is_what(self):
        return 'Laguerre Gauss {}, {}'.format(self.n, self.m)


class laser:
    def __init__(self, wavelength = None, rayleigh_range = None, mode = None):
        self.wavelength = wavelength
        self.wave_number = 2 * np.pi / self.wavelength
        self.rayleigh_range = rayleigh_range

        if isinstance(mode, (hermite_gauss, laguerre_gauss)):
            self.mode = mode
        else:
            self.mode = None

    def beam_waist(self, z):
        return z * (self.wavelength * self.rayleigh_range / np.pi)**0.5
    
    def beam_size(self, z):
        return self.waist(z) * (1 + (z / self.rayleigh_range)**2)**0.5

    def radial_beam_coordinate(self, x, y):
        return (x**2 + y**2)**0.5

    def gouy_phase(self, z):
        return np.arctan(z / self.rayleigh_range)

    def wave_radius_of_curvature(self, z):
        return z * (1 + np.square(self.rayleigh_range / z))


    def amplitude_term(self, x, y, z):
        n = self.mode.n
        m = self.mode.m
        k = self.wave_number

        rho = self.radial_beam_coordinate(x, y)
        w = self.beam_size(z)
        r = self.wave_radius_of_curvature(z)
        w0 = self.beam_waist(z)
        xi = self.gouy_phase(z)

        if isinstance(self.mode, hermite_gauss):
            return (1/w)*((2**(1-n-m))/(np.pi*factorial(n)*factorial(m)))*hermite()
        elif isinstance(self.mode, laguerre_gauss):
            return
    

    def phase_term(self, x, y, z):
        n = self.mode.n
        m = self.mode.m
        k = self.wave_number

        rho = self.radial_beam_coordinate(x, y)
        w = self.beam_size(z)
        r = self.wave_radius_of_curvature(z)
        w0 = self.beam_waist(z)
        xi = self.gouy_phase(z)

        if isinstance(self.mode, hermite_gauss):
            return np.exp(1j(n+m+1)*xi)*np.exp(-1j(k*rho**2/(2*r)))*np.exp(-1j(k*z))
        elif isinstance(self.mode, laguerre_gauss):
            return



if __name__ == "__main__":
    main()