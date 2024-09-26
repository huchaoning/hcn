from math import *
import numpy as np

from scipy.optimize import curve_fit

from .params import *


__all__ = ['FreqEst']

class FreqEst:
    def __init__(self, est_phi=False, phi=None):
        self.est_phi = est_phi
        if not self.est_phi:
            if type(phi) in (int, float):
                self.phi = phi
            else:
                raise ValueError('phi must be given')


    def _normalize_phase(self, phase):
        # Normalize phase to be within [0, 2*pi)
        phase = phase % tau
        # Adjust phase to be within [-pi, pi)
        if phase > pi:
            phase -= tau
        return phase
    

    # Use FFT as pre-estimator.
    def fft_est(self, signal):
        l = len(signal)

        fft = np.fft.fft(signal)[:l // 2]
        freq = np.fft.fftfreq(l, Expt.expo_time)[:l // 2]
        
        amplitude = np.abs(fft)
        phase = np.angle(fft)

        peak_index = np.argmax(amplitude[1:]) + 1
        freq_est = freq[peak_index]
        phase_est = phase[peak_index]
        
        return freq_est / Expt.sampling_rate, self._normalize_phase(phase_est)
    

    # Use LSE as frequency estimator. 
    # Note that LSE and MLE are the same in WGN.
    # If phi is None, the function estimates both frequency and phase.
    def lse(self, dataset):
        N = dataset.shape[-1]
        n = np.arange(N, dtype=np.float64)
        
        if self.est_phi:
            def s(n, f, phi):
                return np.cos(tau * f * n + phi)
        else:
            def s(n, f):
                return np.cos(tau * f * n + self.phi)

        freq_est, phi_est = [], []
        for group in dataset:
            for data in group:
                f_init, phi_init = self.fft_est(data)
                init = [f_init, phi_init] if self.est_phi else [f_init]
                popt, pcov = curve_fit(s, n, data, init)

                if np.linalg.cond(pcov) <= 5e5:
                    if self.est_phi:
                        freq_est.append(popt[0])
                        phi_est.append(popt[1])
                    else:
                        freq_est.append(popt.item())
                        phi_est.append(phi_init)
                else:
                    raise RuntimeError('np.linalg.cond(pcov) > 50000, the algorithm may not converge')

        return np.array(freq_est).reshape(*dataset.shape[:-1]), np.array(phi_est).reshape(*dataset.shape[:-1])



