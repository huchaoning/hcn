import numpy as np
from .params import SPADEParams

point1 = SPADEParams.point1
point2 = SPADEParams.point2

def reader(arr, point1, point2):
    arr = np.array(arr)
    if len(arr.shape) == 3:
        return arr[:, point1[0], point1[1]], arr[:, point2[0], point2[1]]
    elif len(arr.shape) == 2:
        return arr[point1[0], point1[1]], arr[point2[0], point2[1]]
    else:
        raise ValueError('arr must be 2-d or 3-d')
    

def cropper(data):
    temp = data[:, :-4, :]
    copped = reader(temp, point1, point2)
    noise = (temp[:, :5, :5].mean((1,2)) + temp[:, -5:, :5].mean((1,2)) + 
             temp[:, :5, -5:].mean((1,2)) + temp[:, -5:, -5:].mean((1,2))) / 4
    return copped.T, noise



    
def reshape(data, length):
    temp = data[:length, :]
    temp = temp.reshape(200, -1, 2)[:, :50, :]
    return temp


# SPADE's time domain estmator is extremely simple.
def estimator(data):
    time_domain = {}
    for k in data.keys():
        time_domain[k] = data[k][:, :, 0] - data[k][:, :, 1]
    return time_domain
