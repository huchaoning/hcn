import numpy as np
from math import *
from tqdm import tqdm

from .common import *

# Use SciPy to do find the minimize function.
from scipy.optimize import minimize

# Using MLE as DI's time domain estimator.
# And using BFGS algorithm as optimizer to optimize the negative likelihood.
# Also accepts 'simple' to use the centroid position estimator.
def estimator(data, noise, method='mle'):
    data = read(data)
    noise = read(noise)

    time_domain = {k: [] for k in data.keys()}

    roi = np.array([data[k].shape[1] for k in data.keys()])
    if roi.var() != 0:
        raise ValueError('the shape of data must be same, check .npz file')
    roi = roi[0]

    if method.lower() == 'mle':
        def p(x, s, w):
            # The sigma (AKA characteristic width) of Airy disk is 103um.
            # And the camera pixel size is 4.6 um per pixel.
            sigma = 103 / 4.6
            return (1-w)/np.sqrt(2*pi*sigma**2)*np.exp(-(x-s)**2/(2*sigma**2)) + w/roi

        # negative log-likelihood
        def ll(sample, w):
            x = np.arange(roi)
            return lambda s: - sample.T @ np.log(p(x, s, w)) / sample.sum()

        for k in data.keys():
            print(f'{k}: ')
            for i in tqdm(range(data[k].shape[0])):
                if noise == 0:
                    w = 0
                else:
                    w = noise[k][i] / data[k][i].mean()

                # Use BFGS algorithm to minimize negative log-likelihood function.
                results = minimize(ll(data[k][i], w), x0=roi/2, method='BFGS')
                time_domain[k].append(results.x[0])

                if not results.success:
                    print(f"warning: data['di'][{i}] may not converged")
                    
            time_domain[k] = np.array(time_domain[k])
        return time_domain
    
    elif method.lower() == 'simple':
        for k in data.keys():
            index = np.arange(roi)
            normalized = data[k] / data[k].sum(axis=1).reshape(data[k].shape[0], 1)
            time_domain[k] = normalized @ index
        return time_domain
