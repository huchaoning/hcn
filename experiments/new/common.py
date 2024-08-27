from math import *
import numpy as np
from ...macro import read


def photons(data):
    data = read(data)
    n = {}
    for k in data.keys():
        n[k] = data[k].sum(axis=1)
    return n


# Normalize the data into (-1, 1).
def normalize(data):
    temp = data - data.mean()
    scale = (temp[temp>0].mean() - temp[temp<0].mean()) / 2
    return temp / scale

