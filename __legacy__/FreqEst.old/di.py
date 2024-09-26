import numpy as np
from math import *
from tqdm import tqdm

from .common import *
from ..macro import read
from ..cache import cache
from ..futils import futils, integrate
from ..equipments import qcmos, dmd

# Use SciPy to do find the minimize function.
from scipy.optimize import minimize


# DI's hyperparameter
ax = 81
center = 110

def roi(pixels):
    s = pixels * dmd.pixel_size / qcmos.pixel_size
    sigma_ = sigma / qcmos.pixel_size
    return np.round([center - s - 3*sigma_, center + 3*sigma_]).astype(int)


def cropper(file, pixels):
    data = read(file)

    def _crop(data):
        temp = data[:, :-4, :]
        copped = temp[:, roi(pixels)[0]:roi(pixels)[1], ax]
        noise = (temp[:, :5, :5].mean((1,2)) + temp[:, -5:, :5].mean((1,2)) + 
                 temp[:, :5, -5:].mean((1,2)) + temp[:, -5:, -5:].mean((1,2))) / 4
        return copped, noise
    
    if isinstance(data, dict):
        copped, noise = {}, {}
        for k in data.keys():
            copped[k], noise[k] = _crop(data[k])
        return copped, noise
    
    else:
        return _crop(data)
    


def reshape(file, pixels):
    raw = read(file)

    for i, key in enumerate(freq_list):
        key = str(key)
        raw[key] = raw[key][:samples_length[i], :]
        raw[key] = raw[key].reshape(200, -1, -np.subtract(*roi(pixels)))
        raw[key] = raw[key][:, :50, :]

    return raw



# Use MLE as DI's time domain estimator.
# BFGS algorithm as optimizer to optimize the negative likelihood.
# Also accepts 'simple' to use the centroid position estimator.
@cache
def estimator(data_, noise_=0, method='mle'):
    from copy import deepcopy as cp 
    
    data_ = read(data_)
    noise_ = read(noise_)

    data = cp(data_)
    noise = cp(noise_)

    time_domain = {k: [] for k in data.keys()}

    roi = np.array([data[k].shape[-1] for k in data.keys()])
    if roi.var() != 0:
        raise ValueError('the shape of data must be same, check .npz file')
    roi = roi[0]

    if method.lower() == 'mle':
        def p(x, s, w):
            # The sigma (AKA characteristic width) of Airy disk is 103um.
            # And the camera pixel size is 4.6 um per pixel.
            sigma_ = sigma / qcmos.pixel_size
            return (1-w)/np.sqrt(tau*sigma_**2)*np.exp(-(x-s)**2/(2*sigma_**2)) + w/roi

        # negative log-likelihood
        def ll(sample, w):
            x = np.arange(roi)
            return lambda s: - sample.T @ np.log(p(x, s, w)) / sample.sum()

        for k in tqdm(data.keys()):
            origin_shape = data[k].shape
            data[k] = data[k].reshape(-1, roi)
            for i in range(data[k].shape[0]):
                if noise == 0:
                    w = 0
                else:
                    w = noise[k][i] / data[k][i].mean()

                # Use BFGS algorithm to minimize negative log-likelihood function.
                results = minimize(ll(data[k][i], w), x0=roi/2, method='BFGS')
                time_domain[k].append(results.x[0])

                if not results.success:
                    print(f"warning: data['di'][{i}] may not converged")
                    
            time_domain[k] = np.array(time_domain[k]).reshape(origin_shape[0], -1)
            # time_domain[k] = (time_domain[k] - roi/2) * qcmos.pixel_size
        return time_domain
    
    elif method.lower() == 'simple':
        for k in data.keys():
            origin_shape = data[k].shape
            data[k] = data[k].reshape(-1, roi)
            index = np.arange(roi)
            normalized = data[k] / data[k].sum(axis=1).reshape(data[k].shape[0], 1)
            time_domain[k] = (normalized @ index).reshape(origin_shape[0], -1)
            # time_domain[k] = (time_domain[k] - roi/2) * qcmos.pixel_size
        return time_domain
    

def gen(s_list, photons, dmd_pixels, noise=0):
    # Convert length units to camera pixel size to match experimental data.
    s_list_ = s_list / qcmos.pixel_size
    sigma_ = sigma / qcmos.pixel_size
    A_ = dmd_pixels * dmd.pixel_size / qcmos.pixel_size

    roi = int(A_ + 6*sigma_)
    
    data = [np.histogram(np.random.normal(s, sigma_, photons), 
                         bins=roi, range=(-roi/2, roi/2))[0] for s in s_list_]
    
    return (np.array(data) + np.random.poisson(noise, roi)).astype(float)


