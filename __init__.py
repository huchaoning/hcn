from math import *
import numpy as np
import matplotlib.pyplot as plt

import cv2 as cv
import pandas as pd

from scipy.special import hermite, laguerre

from matplotlib_inline import backend_inline
backend_inline.set_matplotlib_formats('svg')

import timeit

from . import di, spade, dmd, qcmos
from .laser import *


def abs_fft(array):
    return np.abs(np.fft(array))


def imread(img_path):
    return cv.imread(img_path, cv.IMREAD_GRAYSCALE | cv.IMREAD_ANYDEPTH)


def read_csv(path):
    return np.array(pd.read_csv(path, header=None))


def to_csv(array, filename):
    pd.DataFrame(array).to_csv(filename, header=None, index=None)



class matplotlib_font:
    def __init__(self) -> None:
        pass

    @classmethod
    def set(self, family=None, weight=None):
        plt.rc('font', family=family, weight=weight)

    @classmethod
    def default(self):
        from matplotlib.font_manager import fontManager
        fontManager.addfont('./font/SourceHanSans.otf')
        plt.rcParams['font.family'] = ['Source Han Sans SC']
        del fontManager

    @classmethod
    def show(self):
        from matplotlib.font_manager import get_font_names
        all_fonts = get_font_names()
        print('All font list get from matplotlib.font_manager:')
        for font in sorted(all_fonts):
            print('\t' + font)
        del get_font_names
    

def plot(x, y, fmts='-',
         title=None, label=None,
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         legend=True, grid=True, font=None, figsize=(5.6, 4),
         show=True, save=None):


    if isinstance(x, (list, tuple)) and len(x) == 2 :
        if callable(y):
            x = np.linspace(x[0], x[1], 300)
        else:
            x = np.linspace(x[0], x[1], len(y))

    if callable(y):
        y = y(x)

    if font is not None:
        if font == 'default':
            matplotlib_font.default()
        else:
            plt.rc('font', family=font)

    if figsize is not None:
        plt.rcParams['figure.figsize'] = figsize

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
         legend=True, grid=True, font=None, figsize=(5.6, 4),
         save=None):


    if font is not None:
        if font == 'default':
            plt.rcdefaults()
        else:
            plt.rc('font', family=font)


    if figsize is not None:
        plt.rcParams['figure.figsize'] = figsize

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


def imshow(x, cmap=None, via_opencv=False,
           title=None, colorbar=True, axis=False, font=None, 
           save=None):
    
    if via_opencv:
        if title is None:
            cv.imshow('Untitled', x)
            cv.waitKey(0)
            cv.destroyAllWindows()
        else:
            cv.imshow(title, x)
            cv.waitKey(0)
            cv.destroyAllWindows()

    elif not via_opencv:
        if font is not None:
            if font == 'default':
                plt.rcdefaults()
            else:
                plt.rc('font', family=font)

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

