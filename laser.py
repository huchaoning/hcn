import numpy as np
from scipy.special import hermite


class laser:
    def __init__(self, wavelength = None, rayleigh_range = None):
        self.wavelength = wavelength
        self.Rayleigh_range = rayleigh_range

    def waist(self, z):
        return z * np.sqrt(self.wavelength * self.Rayleigh_range / np.pi)
    
    def size(self, z):
        return self.waist(z) * np.sqrt(1 + np.square(z / self.Rayleigh_range))


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