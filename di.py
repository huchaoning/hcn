import numpy as np

zero_point = 0
pixel_size = 1
axis = 'y'

def estimator(img, axis = axis):

    if axis == 'x':
        img = np.sum(img, axis=0)
        img = img / img.sum()
        index = np.arange(len(img))
        return (index @ img - zero_point) * pixel_size
    
    elif axis == 'y':
        img = np.sum(img, axis=1)
        img = img / img.sum()
        index = np.arange(len(img))
        return (index @ img - zero_point) * pixel_size

