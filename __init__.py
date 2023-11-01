from math import *
import numpy as np
import matplotlib.pyplot as plt

import cv2 as cv
import pandas as pd

from scipy.special import hermite, laguerre

import timeit

from . import di, spade, dmd, qcmos
from .laser import *


def abs_fft(array):
    return np.abs(np.fft.fft(array))


def imread(img_path):
    return cv.imread(img_path, cv.IMREAD_GRAYSCALE | cv.IMREAD_ANYDEPTH).astype(np.float64)


def read_csv(path):
    return np.array(pd.read_csv(path, header=None))


def to_csv(array, filename):
    pd.DataFrame(array).to_csv(filename, header=None, index=None)


class matplotlib_parameter:

    @classmethod
    def font_show(self):
        from matplotlib.font_manager import get_font_names
        all_fonts = get_font_names()
        print('All font list get from matplotlib.font_manager:')
        for font in sorted(all_fonts):
            print('\t' + font)
        del get_font_names

    @classmethod
    def font(self, family=None, weight=None):
        if family is None:
            from matplotlib.font_manager import fontManager
            from os import path
            fontManager.addfont(path.join(path.dirname(__file__), 'font/SourceHanSans.otf'))
            plt.rcParams['font.family'] = ['Source Han Sans SC']
            del fontManager, path
        else:
            plt.rc('font', family=family, weight=weight)

    @classmethod
    def figsize(self, figsize_x = 6, figsize_y = 4):
        plt.rcParams['figure.figsize'] = (figsize_x, figsize_y)

    @classmethod
    def default(self):
        from matplotlib_inline import backend_inline
        backend_inline.set_matplotlib_formats('svg')
        del backend_inline
        matplotlib_parameter.font()
        matplotlib_parameter.figsize()


def plot(x, y, fmts='-', num=300,
         title=None, label=None,
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         legend=True, grid=True,
         show=True, save=None):

    if isinstance(x, (list, tuple)) and len(x) == 2 :
        if callable(y):
            x = np.linspace(x[0], x[1], num)
        else:
            x = np.linspace(x[0], x[1], len(y))

    if callable(y):
        y = y(x)

    if title is not None:
        plt.title(title)

    if xlabel is not None:
        plt.xlabel(xlabel)

    if ylabel is not None:
        plt.ylabel(ylabel)

    if xlim is not None:
        plt.xlim(xlim)

    if ylim is not None:
        plt.ylim(ylim)

    if label is None:
        plt.plot(x, y, fmts)
    else:
        plt.plot(x, y, fmts, label=label)

    if legend and label is not None:
        plt.legend()

    if grid:
        plt.grid(True)
    else:
        plt.grid(False)

    if save is not None:
        plt.savefig(save)

    if show:
        plt.show()
    

def hist(x, bins=300, histtype='step', density=True,
         title=None, label=None,
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         legend=True, grid=True,
         save=None):

    if title is not None:
        plt.title(title)

    if xlabel is not None:
        plt.xlabel(xlabel)

    if ylabel is not None:
        plt.ylabel(ylabel)

    if xlim is not None:
        plt.xlim(xlim)

    if ylim is not None:
        plt.ylim(ylim)

    if label is None:
        plt.hist(x, bins=bins, histtype=histtype, density=density)
    else:
        plt.hist(x, bins=bins, histtype=histtype, density=density, label=label)

    if legend and label is not None:
        plt.legend()

    if grid:
        plt.grid(True)
    else:
        plt.grid(False)

    if save is not None:
        plt.savefig(save)

    plt.show()


def imshow(x, cmap=None,
           title=None, colorbar=True, axis=False, font=None, 
           save=None):

    if not axis:
        plt.xticks(())
        plt.yticks(())

    if title is not None:
        plt.title(title)

    if cmap is None:
        plt.imshow(x)
    else:
        plt.imshow(x, cmap=cmap)

    if colorbar:
        plt.colorbar()

    if save is not None:
        plt.savefig(save)

    plt.show()


matplotlib_parameter.default()

