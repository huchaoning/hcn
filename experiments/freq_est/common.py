from math import *
import numpy as np
from ...macro import read

sigma = 103

samples = 10000
N = 50

expo_time = 0.0451

sampling_rate = 1 / expo_time
timeline = np.arange(samples) * expo_time


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

