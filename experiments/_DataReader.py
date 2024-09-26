import numpy as np

from .params import *
from ..macro import aviread


__all__ = ['DataReader']

class DataReader:
    def __init__(self, measure):
        if measure.lower() in ('spade', 'di'):
            self.measure = measure.lower()
        else:
            raise ValueError('measure must be one of spade or di')


    def _spade_reader(self, data):
        return data[:, SPADE.point1[0], SPADE.point1[1]], data[:, SPADE.point2[0], SPADE.point2[1]]


    def _di_roi(self, mirrors):
        if mirrors is None:
            raise ValueError('type(mirrors) must be int, ' + 
                             'mirrors stands for how many DMD pixels')
        
        s = mirrors * DMD.pixel_size / qCMOS.pixel_size
        _sigma = Expt.sigma / qCMOS.pixel_size
        
        return np.ceil([DI.center - s - 3*_sigma, DI.center + 3*_sigma]).astype(int)


    def _cropping(self, data, mirrors=None):
        temp = data[:, :-4, :]
        noise = (temp[:, :5,   :5].mean((1, 2)) + temp[:, -5:,   :5].mean((1, 2))  + 
                 temp[:, :5, -5: ].mean((1, 2)) + temp[:, -5:, -5: ].mean((1, 2))) / 4
        
        if self.measure == 'spade':
            cropped = np.array(self._spade_reader(temp)).T
        if self.measure == 'di':
            cropped = temp[:, self._di_roi(mirrors)[0]:self._di_roi(mirrors)[1], DI.ax]
        
        return cropped, noise


    def _reshaping(self, data, noise, length, mirrors=None):
        detectors = 2 if self.measure == 'spade' else - np.subtract(*self._di_roi(mirrors))
        reshaped_data = data[:length, :].reshape(200, -1, detectors)[:, :50, :]
        reshaped_noise = noise[:length].reshape(200, -1)[:, :50]
        return reshaped_data, reshaped_noise


    def _processing(self, avi, length, mirrors=None):
        avi = aviread(avi)
        cropped, noise = self._cropping(avi, mirrors)
        return self._reshaping(cropped, noise, length, mirrors)
    

    def load(self, files, lengths, mirrors=None):
        if len(files) != len(lengths):
            raise ValueError('len(files) and len(lengths) must be the same')
        else:
            l = len(files)

        processed, noise = zip(*[
            self._processing(files[i], lengths[i], mirrors) for i in range(l)])
        
        return np.array(processed), np.array(noise)







