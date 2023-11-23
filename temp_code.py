import numpy as np
from glob import glob
from math import sqrt

from .plotter import imread
from .experiments import spade, di

def run(_, method):

    s, n1, n2= [], [], []
    estimator = eval(f'{method}.estimator')
    photon_number = eval(f'{method}.photon_number')
    for img in glob(f'./{method}/s{_}_*.tif'):
        temp = imread(img)
        s.append(estimator(temp))
        if method == 'spade':
            n1.append(photon_number(temp)[0])
            n2.append(photon_number(temp)[1])
        elif method == 'di':
            n1.append(photon_number(temp))
            n2 = 0
        else:
            raise TypeError
    return np.array(s), np.array(n1), np.array(n2)


def run_all(_, method):
    if method != 'di' and method != 'spade':
        raise TypeError
    mean, var, nvar = [], [], []
    for i in _:
        s, n1, n2 = run(i, method)
        mean.append(s.mean())
        var.append(s.var())
        nvar.append(sqrt((n1+n2).mean() * s.var()))
    return np.array(mean), np.array(var), np.array(nvar)

