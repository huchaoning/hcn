import numpy as np

zero_point = 0
pixel_size = 1

def photon_number(img):
    return img.sum()

def estimator(img, axis = 'y'):
    if axis == 'x':
        img = np.sum(img, axis=0)
        img = img / img.sum()
        index = np.arange(len(img))
        return (zero_point - index @ img) * pixel_size
    elif axis == 'y':
        img = np.sum(img, axis=1)
        img = img / img.sum()
        index = np.arange(len(img))
        return (zero_point - index @ img) * pixel_size

def estimator_1d(img):
    if len(np.shape(img)) != 1:
        raise ValueError('img must be 1d')
    else:
        img = img / img.sum()
        index = np.arange(len(img))
        return (zero_point - index @ img) * pixel_size
