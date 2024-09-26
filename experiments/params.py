import numpy as np
from fractions import Fraction
from dataclasses import dataclass 

__all__ = [
    'Expt',

    'DI',
    'SPADE',

    'DMD',
    'qCMOS',
]


@dataclass
class Expt:
    def validate(params):
        params = np.array(params)
        if (params % 1 == 0).all():
            return (params).astype(int)
        else:
            raise ValueError('invalid params')
        
    # The sigma (AKA characteristic width) of Airy disk is 103um.
    sigma = 103 #um
    expo_time = 0.0451 #s
    # freq_list = np.array([0.1, 0.125, 0.15625, 0.2, 0.22, 0.25, 0.275, 0.3125, 0.34375, 0.4])
    freq_list = np.array([0.1, 0.125, 0.15625, 0.2, 0.22, 0.25, 0.3125, 0.34375, 0.4])

    sampling_rate = 1 / expo_time

    pic_time = validate(1e6 / (2 * freq_list * sampling_rate))

    samples_pre_cycle = validate([Fraction(str(f)).denominator for f in freq_list])
    samples_length = validate((np.ceil(50 / samples_pre_cycle) * samples_pre_cycle) * 200)

    cut_point = validate(np.ceil(50 / samples_pre_cycle) * samples_pre_cycle)

    spade_avis = [f'spade{i}.avi' for i in range(len(freq_list))]
    di_avis = [f'di{i}.avi' for i in range(len(freq_list))]


@dataclass
class DI:
    ax = 81
    center = 110


@dataclass
class SPADE:
    point1 = (119, 91)
    point2 = (407, 91)


@dataclass
class qCMOS:
    # The camera pixel size is 4.6 um per pixel.
    pixel_size = 4.6 #um


@dataclass
class DMD:
    pixel_size = 19.374725804511403 #um


