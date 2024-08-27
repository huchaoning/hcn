import numpy as np

def fim(s, params, N=50, sigma=103):

    size = len(params)
    fim_ = np.zeros((size, size))

    def grad(p):
        eps = np.sqrt(np.finfo(float).eps)
        params_ = np.copy(params)
        params_[p] = params_[p] + eps
        return (s(np.arange(N), *params_) - s(np.arange(N), *params)) / eps

    for i in range(size):
        for j in range(size):
            fim_[i, j] = np.sum(grad(i) * grad(j))

    return fim_ / sigma**2


# def s(A, omega, phi, c):
#     def wrapper(n):
#         return A * np.cos(omega * n + phi) + c
#     return wrapper

# def fim(s: Callable, N: int, sigma):
#     def s_(*args, **kargs):
#         return s(*args, **kargs)(np.arange(N))
    
#     def wrapper(*args, **kargs):
#         params = variables_of(s)
#         fim_ = np.zeros((params, params))
#         for i in range(params):
#             for j in range(params):
#                 fim_[i, j] = np.sum(grad(s_, i)(*args, **kargs) * 
#                                     grad(s_, j)(*args, **kargs))
#         return fim_ / sigma**2
    
#     return wrapper


#########################
# Requires modification #
#########################

# from math import *
# import numpy as np
# import os

# from .utils import *

# from numpy.linalg import inv
# from scipy.interpolate import interp1d

# # The CFIM of DI is given by below. 
# def cfim_di(A, w, omega, roi, N=50):
#     A = A / 2 * dmd / 4.6 
#     sigma = 103 / 4.6

#     omega_ = omega / 22.17
#     phi_ = 0

#     epsilon = 1e-8

#     def p(x, n, w, omega=omega_, phi=phi_):
#         s = A * np.cos(omega * n + phi)
#         return (1-w)/np.sqrt(2*pi*sigma**2)*np.exp(-(x-s)**2/(2*sigma**2)) + w/roi 

#     def part_omega(x, n, w):
#         return (p(x, n, w, omega=omega_+epsilon) - p(x, n, w)) / epsilon
    
#     def part_phi(x, n, w):
#         return (p(x, n, w, phi=phi_+epsilon) - p(x, n, w)) / epsilon

#     def fi11(n, w):
#         return integrate(lambda x: (part_omega(x, n, w)**2 / p(x, n, w)), (-roi/2, roi/2))
    
#     def fi22(n, w):
#         return integrate(lambda x: (part_phi(x, n, w)**2 / p(x, n, w)), (-roi/2, roi/2))
    
#     def fi12(n, w):
#         return integrate(lambda x: (part_omega(x, n, w)*part_phi(x, n, w) / p(x, n, w)), (-roi/2, roi/2))

#     f11 = np.sum([fi11(n, w) for n in range(N)])
#     f22 = np.sum([fi22(n, w) for n in range(N)])
#     f12 = np.sum([fi12(n, w) for n in range(N)])

#     return np.array([[f11, f12],
#                      [f12, f22]])


# # The CFIM of SPADE is given by below. 
# def cfim_spade(A, w, omega, N=50):
#     A = A / 2 * dmd / 4.6 
#     sigma = 103 / 4.6

#     omega_ = omega / 22.17
#     phi_ = 0

#     epsilon = 1e-8
    
#     def p(x, n, w, omega=omega_, phi=phi_):
#         s = A * np.cos(omega * n + phi)
#         if x == '+':
#             return (1-w) * (s+2*sigma)**2 / (8*sigma**2) * np.exp(-s**2 / (4*sigma**2)) + w/2 
#         if x == '-':
#             return (1-w) * (s-2*sigma)**2 / (8*sigma**2) * np.exp(-s**2 / (4*sigma**2)) + w/2 

#     def part_omega(x, n, w):
#         return (p(x, n, w, omega=omega_+epsilon) - p(x, n, w)) / epsilon

#     def part_phi(x, n, w):
#         return (p(x, n, w, phi=phi_+epsilon) - p(x, n, w)) / epsilon

#     def fi11(n, w):
#         return sum([part_omega(x, n, w)**2 / p(x, n, w) for x in ['+', '-']])

#     def fi22(n, w):
#         return sum([part_phi(x, n, w)**2 / p(x, n, w) for x in ['+', '-']])

#     def fi12(n, w):
#         return sum([part_omega(x, n, w)*part_phi(x, n, w) / p(x, n, w) for x in ['+', '-']])
    
#     f11 = np.sum([fi11(n, w) for n in range(N)])
#     f22 = np.sum([fi22(n, w) for n in range(N)])
#     f12 = np.sum([fi12(n, w) for n in range(N)])

#     return np.array([[f11, f12],
#                      [f12, f22]])


# # QCRB in theory is given as follow. Note that the QCRB (and CRB) is in unit of frame rate.
# def qcrb_(A, N=50, sigma=103):
#     A = A * dmd / 2
#     return 12 / (N * (N**2-1)) * (2*sigma**2 / A**2)


# # Solve the inverse of CFIM then return the CRB of frequency. (ratio to QCRB)
# def crb_(A, w_range, omega, roi, measure: str, N=50):

#     if measure.lower() == 'spade':
#         return np.array([inv(cfim_spade(A, w, omega, N))[0, 0] for w in w_range]) / qcrb_(A)
    
#     if measure.lower() == 'di':
#         return np.array([inv(cfim_di(A, w, omega, roi, N))[0, 0] for w in w_range]) / qcrb_(A)


# # Because the DI's CRB calculation is slow, so cache the result into the cache folder.
# def crb_cache(A, w_range, omega, roi, measure: str, N=50):

#     if measure.lower() == 'spade':
#         return crb_(A, w_range, omega, roi, 'spade', N)
    
#     if measure.lower() == 'di':
#         if not os.path.exists(f'cache/di{roi}_n{N}.npz'):

#             dic = {
#                 'x': np.linspace(0, 0.99, 100),
#                 'y': np.array(crb_(1, np.linspace(0, 0.99, 100), tau, roi, 'di', N))
#             }
#             np.savez(**dic, file=f'cache/di{roi}_n{N}.npz')

#         return interp1d(**load_npz(f'cache/di{roi}_n{N}.npz'))(w_range)