from math import *
import numpy as np
from scipy.optimize import curve_fit

from tqdm import tqdm

from .common import *

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
    n = np.arange(N, dtype=np.float64)

    f_est = {k: [] for k in data.keys()}

    def s(phi):
        def wrapper(n, omega):
            return np.cos(omega * n + phi)
        return wrapper

    for k in tqdm(data.keys()):
        data[k] = norm(data[k])
        f_init, phi_init = fft_est(data[k])
        f_init = tau * f_init * expo_time
        for i, data_ in enumerate(data[k].reshape(len(data[k]) // N, N)):
            phi = norm_phase((i * f_init * N) + phi_init)
            popt, pcov = curve_fit(s(phi), n, data_, [f_init])
            if np.linalg.cond(pcov) <= 1e5:
                f_est[k].append(popt.item())
            else:
                raise RuntimeError('np.linalg.cond(pcov) > 1e5, the algorithm may not converge')
        f_est[k] = np.array(f_est[k]) * sampling_rate / tau
        
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
