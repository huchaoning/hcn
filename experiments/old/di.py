import numpy as np
import os 
from ..macro import imread

zero_point = 161.8
old_zero_point = 110.3

pixel_size = 4.6
ax_1d = 81

use_1d_only = True
batch = True


def photon_number(img):
    if type(img) == str and os.path.exists(img):
        img = imread(img)
    if batch and (not use_1d_only):
        raise('if batch is True, use_1d_only must be True')
    if batch:
        img = img[:, :, ax_1d]
        return img.sum(axis=1)
    elif use_1d_only:
        img = img[:, ax_1d]
    return img.sum()


def estimator(img, axis = 'y'):
    if type(img) == str and os.path.exists(img):
        img = imread(img)
    if batch and (not use_1d_only):
        raise('if batch is True, use_1d_only must be True')
    if batch:
        img = img[:, :, ax_1d]
        img_shape = img.shape
        img_sum = img.sum(axis=1)
        index = np.arange(img_shape[1])
        normalized_img = img / img_sum.reshape(img_shape[0], 1)
        return (zero_point - normalized_img @ index) * pixel_size
    if use_1d_only:
        img = img[:, ax_1d]
        if len(np.shape(img)) != 1:
            raise ValueError('img must be 1d')
        else:
            img = img / img.sum()
            index = np.arange(len(img))
            return (zero_point - index @ img) * pixel_size
    else:
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


def run_all(img):
    if type(img) == str and os.path.exists(img):
        img = imread(img)
    return estimator(img), photon_number(img)


def log_likehood(data):
    def wapper(s):
        arr = (np.arange(318) - s)**2
        return (data * arr).sum()
    return wapper


def mle_estimator(img, eta, loops, init=0):
    from ..macro import gradient_descent
    sample = img[:, :, ax_1d].astype(float)
    s_list = []
    for i in range(sample.shape[0]):
        result = gradient_descent(log_likehood(sample[i]), eta, loops, init)
        s_list.append(result.argmin)
    return (zero_point - np.array(s_list)) * 4.6


# import numpy as np
# from ..plotter import imread

# zero_point = 0
# pixel_size = 1

# __all__ = ['photon_number', 'estimator']

# def photon_number(img):
#     return img.sum()

# def estimator_single(img, axis = 'y'):
#     if axis == 'x':
#         img = np.sum(img, axis=0)
#         img = img / img.sum()
#         index = np.arange(len(img))
#         return (zero_point - index @ img) * pixel_size
#     elif axis == 'y':
#         img = np.sum(img, axis=1)
#         img = img / img.sum()
#         index = np.arange(len(img))
#         return (zero_point - index @ img) * pixel_size

# def estimator_single_1d(img):
#     if len(np.shape(img)) != 1:
#         raise ValueError('img must be 1d')
#     else:
#         img = img / img.sum()
#         index = np.arange(len(img))
#         return (zero_point - index @ img) * pixel_size


# def estimator(data, axis='y', batch=True):
#     if type(data) is str:
#         data = imread(data)
#     elif type(data) is not np.ndarray:
#         raise ValueError('data is invalid, data must be image path or a numpy array')
#     elif data.ndim > 3:
#         raise ValueError('data is invalid, data must be a single tif or multi-tifs')

#     if batch and (data.ndim == 2):
#         _1d = True
#     elif (not batch) and (data.ndim == 1):
#         _1d = True
#     else:
#         _1d = False

#     if batch:
#         if _1d and len(data.shape) != 2:
#             samples, y = data.shape
#             index = np.arange(y)
#         elif not _1d:
#             samples, y, x = data.shape
#             if axis == 'x':
#                 data = data.sum(axis=1)
#                 index = np.arange(x)
#             if axis == 'y':
#                 data = data.sum(axis=2)
#                 index = np.arange(y)
#         data = data / data.sum(axis=1).reshape(samples, 1)
#         return (zero_point - data @ index) * pixel_size
    
#     elif _1d:
#         return estimator_single_1d(data)
    
#     elif not _1d:
#         return estimator_single(data)

