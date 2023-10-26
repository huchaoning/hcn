import numpy as np
from scipy.special import hermite


class laser:
    def __init__(self, wavelength = None, rayleigh_range = None):
        self.wavelength = wavelength
        self.rayleigh_range = rayleigh_range

    def waist(self, z):
        return z * (self.wavelength * self.rayleigh_range / np.pi)**0.5
    
    def size(self, z):
        return self.waist(z) * (1 + (z / self.rayleigh_range)**2)**0.5


class HG:
    def __init__(self, m, n, beam):
        self.m = m 
        self.n = n
        self.beam = beam

    def amplitude(self, x, y, z):
        return
    
    def phase(self, x, y, z):
        return



if __name__ == "__main__":
    main()