from math import *
import numpy as np

from ..macro import read
from fractions import Fraction
from scipy.optimize import curve_fit
from tqdm import tqdm

sigma = 103

expo_time = 0.0451
sampling_rate = 1 / expo_time

# freq_list = np.array([0.1, 0.125, 0.15625, 0.2, 0.22, 0.25, 0.275, 0.3125, 0.34375, 0.4])
freq_list = np.array([0.1, 0.125, 0.15625, 0.2, 0.22, 0.25, 0.3125, 0.34375, 0.4])
pic_time = 1e6 / (2*freq_list*sampling_rate)

samples_pre_cycle = np.array([Fraction(str(f)).denominator for f in freq_list]).astype(int)
samples_length = ((np.ceil(50 / samples_pre_cycle) * samples_pre_cycle) * 200).astype(int)

cut_point = np.ceil(50 / samples_pre_cycle) * samples_pre_cycle

del Fraction


def check_freq(freqs):
    from fractions import Fraction
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



# def lse(data, sr=22.17):
#     data = read(data)

#     N = 50
#     n = np.arange(N, dtype=np.float64)

#     f_est = {k: [] for k in data.keys()}
#     phi_est = {k: [] for k in data.keys()}

#     # Define signal and LS loss.
#     def s(n, omega, phi):
#         return np.cos(omega*n + phi)
    
#     # Using FFT as pre-estimator.
#     def fft(data):
#         pre_est = np.abs(np.fft.fft(data))
#         f_axis = np.linspace(0, sr, len(pre_est))
#         f = np.argmax(pre_est[1 : len(pre_est) // 2])
#         pre_est = f_axis[f] # +1 is intentionally missed to ensure that the initial value is smaller than true value.
#         return pre_est

#     for k in data.keys():
#         print(f'{k}: ')
#         data[k] = normalize(data[k])
#         f_init = tau*fft(data[k])/sr
#         for data_ in tqdm(data[k].reshape(len(data[k]) // N, N)):
            
#             popt, pcov = curve_fit(s, n, data_, [f_init, 0])
#             if np.linalg.cond(pcov) <= 1e15:
#                 f_est[k].append(popt[0])
#                 phi_est[k].append(popt[1])
#             else:
#                 raise RuntimeError('np.linalg.cond(pcov) > 1e15, the algorithm may not converge')
                
#         f_est[k] = np.array(f_est[k]) * sr / tau
#         phi_est[k] = np.array(phi_est[k])
#     return f_est, phi_est

