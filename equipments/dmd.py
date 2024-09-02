import numpy as np

pixel_size = 19.374725804511403

def picture_time(f, round=True, expo_time=45100):
    if round:
        t = (picture_time(f, False) // expo_time) * expo_time
        return t, 1e6/(2*t)
    return np.round(1000000 / (2*f)).astype(int)
