from .common import *

# SPADE's time domain estmator is extremely simple.
def estimator(data):
    data = read(data)
    time_domain = {}
    for k in data.keys():
        time_domain[k] = data[k][:, 1] - data[k][:, 0]
    return time_domain
