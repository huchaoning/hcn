import numpy as np

pixel_size = 19.374725804511403

def picture_time(f):
    return np.round(1000000 / (2*f)).astype(int)

