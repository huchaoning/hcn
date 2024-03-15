import numpy as np
import os 
from ..plotter import imread
from ..equipments import qcmos, dmd
from .__init__ import sigma

zero_point = 110.3
pixel_size = 4.6
axis_of_interest = 81
bad_points = -2


def photon_number(img):
    if type(img) == str and os.path.exists(img):
        img = imread(img)
    img = img[:, :bad_points, axis_of_interest]
    return img.sum(axis=1)


def estimator(img, output_photon_number=True):
    if type(img) == str and os.path.exists(img):
        img = imread(img)
    img = img[:, :bad_points, axis_of_interest]
    normalized_img = img / img.sum()
    index = np.arange(len(normalized_img))
    if output_photon_number:
        return (zero_point - index @ normalized_img) * pixel_size, photon_number(img)
    else:
        return (zero_point - index @ normalized_img) * pixel_size


def gen_signal(s, resource, roi=218):
    s_pixels = zero_point - s / qcmos.pixel_size
    sigma_pixels = sigma / qcmos.pixel_size
    random_data = np.random.normal(s_pixels, sigma_pixels, size=resource)
    return np.histogram(random_data, bins=np.arange(roi+1))[0]

