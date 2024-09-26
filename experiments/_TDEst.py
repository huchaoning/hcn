
from math import *
import numpy as np

from .params import *
from ..cache import cache

from scipy.optimize import minimize


class TDEst:
    def __init__(self, measure):
        if measure.lower() in ('spade', 'di'):
            self.measure = measure.lower()
        else:
            raise ValueError('measure must be one of spade or di')


    def _normalize(self, data):
        data = np.array(data)
        temp = data - data.mean()
        scale = (temp[temp>0].mean() - temp[temp<0].mean()) / 2
        return temp / scale


    def estimator(self, dataset, noise=None, di_method='mle'):
        origin_shape = dataset.shape

        detectors = origin_shape[-1]
        works = np.prod(origin_shape[:-1])

        flatten_data = dataset.reshape(-1, detectors)

        if self.measure == 'di':
            if di_method.lower() == 'simple':
                temp = flatten_data / flatten_data.sum(axis=-1).reshape(-1, 1)
                x_axis = np.arange(detectors)
                time_domain = (temp @ x_axis)

            elif di_method.lower() == 'mle':
                def _p(x, s, w):
                    _sigma = Expt.sigma / qCMOS.pixel_size
                    return (1-w)/np.sqrt(tau*_sigma**2)*np.exp(-(x-s)**2/(2*_sigma**2)) + w/detectors
                
                def _negative_ll(data, w):
                    x_axis = np.arange(detectors)
                    return lambda s: - data.T @ np.log(_p(x_axis, s, w)) / data.sum()
                
                def _run_mle(data, w):
                    # Use BFGS algorithm to minimize negative log-likelihood function.
                    result = minimize(_negative_ll(data, w), x0=detectors/2, method='BFGS')
                    
                    if result.success:
                        return result.x[0]
                    else:
                        raise RuntimeError('not converged')
                
                if noise is None:
                    time_domain = [_run_mle(flatten_data[i], 0) for i in range(works)]
                else:
                    w_set = np.ravel(noise) / flatten_data.mean(-1)
                    time_domain = [_run_mle(flatten_data[i], w_set[i]) for i in range(works)]  

        if self.measure == 'spade':
            # SPADE's time domain estmator is extremely simple.
            time_domain = flatten_data[:, 0] - flatten_data[:, 1]

        return self._normalize(time_domain).reshape(*origin_shape[:-1])