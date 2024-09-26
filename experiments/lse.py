from math import *
import numpy as np

from scipy.optimize import curve_fit
from tqdm import tqdm

from fractions import Fraction

from ..macro import read
from .share import sampling_rate, expo_time


def check_freq(freqs):
    frac = np.array([Fraction(str(f)).denominator for f in freqs])
    arr = 1e6/(2*freqs*sampling_rate)%1
    temp = []
    for i in freqs[arr == 0]:
        for j in freqs[frac <= 50]:
            if i == j:
                temp.append(i)
    return np.array(temp)


def photons(data):
    data = read(data)
    n = {}
    for k in data.keys():
        n[k] = data[k].sum(axis=1)
    return n


# Normalize the data into (-1, 1).
def norm(data):
    temp = data - data.mean()
    scale = (temp[temp>0].mean() - temp[temp<0].mean()) / 2
    return temp / scale


def norm_phase(phase):
    # Normalize phase to be within [0, 2*pi)
    phase = phase % tau
    # Adjust phase to be within [-pi, pi)
    if phase > pi:
        phase -= tau
    return phase



# Use FFT as pre-estimator.
def fft_est(signal):
    N = len(signal)

    X = np.fft.fft(signal)[:N // 2]
    freq = np.fft.fftfreq(N, expo_time)[:N // 2]
    
    amplitude = np.abs(X)
    phase = np.angle(X)

    peak_freq_idx = np.argmax(amplitude[1:]) + 1
    peak_freq = freq[peak_freq_idx]
    peak_phase = phase[peak_freq_idx]
    
    return peak_freq, peak_phase



# Use LSE as frequency estimator. 
# Note that LSE and MLE are the same in WGN.
def lse(data):
    data = read(data)
    # _, N = data.shape
    N = 50
    n = np.arange(N, dtype=np.float64)

    f_est = {k: [] for k in data.keys()}

    # def s(phi):
    #     def wrapper(n, omega):
    #         return np.sin(omega * n + phi)
    #     return wrapper
    
    def s(n, omega, phi):
        return np.sin(omega * n + phi)

    for k in tqdm(data.keys()):
        data[k] = norm(data[k])
        f_init, phi_init = fft_est(np.ravel(data[k]))
        f_init = tau * f_init * expo_time
        for i, data_ in enumerate(data[k]):
            phi_init = norm_phase((i * f_init * N) + phi_init)
            popt, pcov = curve_fit(s, n, data_, [f_init, phi_init])
            if np.linalg.cond(pcov) <= 1e5:
                # f_est[k].append(popt.item())
                f_est[k].append(popt[0])
            else:
                raise RuntimeError('np.linalg.cond(pcov) > 1e5, the algorithm may not converge')
        f_est[k] = np.array(f_est[k]) / tau
        
    return f_est

