from math import *
import numpy as np

from ...macro import read
from fractions import Fraction

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

