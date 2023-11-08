from math import *
import numpy as np
import matplotlib.pyplot as plt

import cv2 as cv
import pandas as pd

from scipy.special import hermite, laguerre

import timeit

from .equipments import *

from .laser import *


def where_is_mypy():
    from os.path import dirname
    dir =  dirname(__file__)
    del dirname
    return dir


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
    def show_font(self):
        from matplotlib.font_manager import get_font_names
        all_fonts = get_font_names()
        print('All font list get from matplotlib.font_manager:')
        for font in sorted(all_fonts):
            print('\t' + font)
        del get_font_names

    @classmethod
    def set_font(self, family=None, weight=None):
        if family is None:
            from matplotlib.font_manager import fontManager
            from os import path
            fontManager.addfont(path.join(path.dirname(__file__), 'font/SourceHanSans.otf'))
            plt.rcParams['font.family'] = ['Source Han Sans SC']
            del fontManager, path
        else:
            plt.rc('font', family=family, weight=weight)

    @classmethod
    def set_figsize(self, figsize_x = 6, figsize_y = 4):
        plt.rcParams['figure.figsize'] = (figsize_x, figsize_y)

    @classmethod
    def set_default(self):
        from matplotlib_inline import backend_inline
        backend_inline.set_matplotlib_formats('svg')
        del backend_inline
        matplotlib_parameter.set_font()
        matplotlib_parameter.set_figsize()


def plot(x, y, fmts='-', num=300,
         title=None, label=None,
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         legend=True, grid=True, figsize=None, font=None,
         show=True, save=None):

    default = True

    if isinstance(x, (list, tuple)) and len(x) == 2 :
        if callable(y):
            x = np.linspace(x[0], x[1], num)
        else:
            x = np.linspace(x[0], x[1], len(y))

    if callable(y):
        try: 
            y = y(x)
        except TypeError:
            y_ = []
            for x_ in x:
                y_.append(y(x_))
            y = np.array(y_)
            del x_, y_

    if figsize is not None:
        matplotlib_parameter.set_figsize(figsize[0], figsize[1])
        default = False

    if font is not None:
        matplotlib_parameter.set_font(family=font)
        default = False

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

    if not default:
        matplotlib_parameter.set_default()
        default = True
    

def hist(x, bins=300, histtype='step', density=True,
         title=None, label=None,
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         legend=True, grid=True, figsize=None, font=None,
         show=True, save=None):

    default = True

    if figsize is not None:
        matplotlib_parameter.set_figsize(figsize[0], figsize[1])
        default = False

    if font is not None:
        matplotlib_parameter.set_font(family=font)
        default = False

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

    if show:
        plt.show()

    if not default:
        matplotlib_parameter.set_default()
        default = True
    

def imshow(x, cmap=None,
           title=None, colorbar=True, axis=False, 
           figsize=None, font=None,
           show=True, save=None):

    default = True

    if figsize is not None:
        matplotlib_parameter.set_figsize(figsize[0], figsize[1])
        default = False

    if font is not None:
        matplotlib_parameter.set_font(family=font)
        default = False

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

    if show:
        plt.show()

    if not default:
        matplotlib_parameter.set_default()
        default = True
    

def scatter(x, y, s=None, c=None, alpha=None, 
            title=None, label=None, colorbar=None,
            xlabel=None, ylabel=None, xlim=None, ylim=None,
            legend=True, grid=True, figsize=None, font=None,
            show=True, save=None):

    default = True

    if figsize is not None:
        matplotlib_parameter.set_figsize(figsize[0], figsize[1])
        default = False

    if font is not None:
        matplotlib_parameter.set_font(family=font)
        default = False

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
        plt.scatter(x, y, s=s, c=c, alpha=alpha)
    else:
        plt.scatter(x, y, s=s, c=c, alpha=alpha, label=label)

    if legend and label is not None:
        plt.legend()

    if grid:
        plt.grid(True)
    else:
        plt.grid(False)

    if colorbar:
        plt.colorbar()
    elif (colorbar is not False) and (c is not None):
        plt.colorbar()

    if save is not None:
        plt.savefig(save)

    if show:
        plt.show()

    if not default:
        matplotlib_parameter.set_default()
        default = True
    

matplotlib_parameter.set_default()

