# from math import *
# import numpy as np

# from .utils import *
# from tqdm import tqdm

# # Using LSE as frequency estimator. 
# # Note that LSE and MLE are the same in WGN.
# def lse(data, sr=22.17):
#     data = read(data)

#     N = 50
#     n = np.arange(N)

#     f_est = {k: [] for k in data.keys()}
#     phi_est = {k: [] for k in data.keys()}

#     # Define signal and LS loss.
#     def s(n, omega, phi):
#         return np.cos(omega*n + phi)

#     def ls(sample):
#         def wrapper(omega, phi):
#             return (0.5*(sample - s(n, omega, phi))**2).sum()
#         return wrapper
    
#     # Using FFT as pre-estimator.
#     def fft(data):
#         pre_est = np.abs(np.fft.fft(data))
#         f_axis = np.linspace(0, sr, len(pre_est))
#         f = np.argmax(pre_est[1 : len(pre_est) // 2])
#         pre_est = f_axis[f] # +1 is intentionally missed to ensure that the initial value is smaller than true value.
#         return pre_est


#     gdparm = {
#         'eta'      :(1e-5, 1e-2),
#         'accuracy' : 1e-6,
#         'epsilon'  : 1e-8, 
#         'max_loops': 10000,
#         }

#     for k in data.keys():
#         print(f'{k}: ')
#         data[k] = normalize(data[k])
#         f_init = tau*fft(data[k])/sr # Using FFT estimates as initial value of gradient descent algorithm.
#         for data_ in tqdm(data[k].reshape(len(data[k]) // N, N)):
#             # Use homemade gradient descent algorithm to minimize LS loss. 
#             # Because the algorithm shipped with SciPy doesn't converged. (If you know why plz tell me.)
#             gd_result, gd_process, success = gradient_descent(ls(data_), init=(f_init, 0), **gdparm)
#             if success:
#                 f_est[k].append(gd_result[0])
#                 phi_est[k].append(gd_result[1])
            
#         f_est[k] = np.array(f_est[k]) * sr / tau
#         phi_est[k] = np.array(phi_est[k])
#     return f_est, phi_est