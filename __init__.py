from math import *
import numpy as np
import matplotlib.pyplot as plt

import PIL
import cv2 as cv
import pandas as pd

import os, shutil, timeit
from glob import glob

from .equipments import *
from .laser import *
from . import spade, di, cgh


from matplotlib_inline import backend_inline
backend_inline.set_matplotlib_formats('svg')
del backend_inline


from .temp_code import run, run_all


def where_is_mypy():
    return os.path.dirname(__file__)


def square_abs(array):
    return np.square(np.abs(array))


def abs_fft(array):
    return np.abs(np.fft.fft(array))


def max_min_normalization(array):
    return (array - array.min()) / (array.max() - array.min())


def normalization(array):
    return array / array.sum()


def fast_meshgrid(h, v, scale = 1):
    return np.meshgrid(np.arange(-h/2, h/2) * scale, -np.arange(-v/2, v/2) * scale)


def read_csv(path):
    return np.array(pd.read_csv(path, header=None))


def to_csv(array=None, save=None):
    if array is not None:
        pd.DataFrame(array).to_csv(save, header=None, index=None)
    else:
        raise TypeError('array is None')


def imread(img_path, pillow=False):
    if pillow:
        return np.array(PIL.Image.open(img_path)).astype(float)
    else:
        return cv.imread(img_path, cv.IMREAD_GRAYSCALE | cv.IMREAD_ANYDEPTH).astype(float)


def imwrite(array=None, save=None, pillow=False):
    if array is not None:
        if array.dtype == np.uint8:
            if pillow:
                PIL.Image.fromarray(array).save(save)
            else:
                cv.imwrite(filename=save, img=array)
        else:
            raise TypeError('array.dtype must be np.uint8')
    else:
        raise TypeError('array is None')


def show_all_fonts():
    from matplotlib.font_manager import get_font_names
    all_fonts = get_font_names()
    print('All font list get from matplotlib.font_manager:')
    for font in sorted(all_fonts):
        print('\t' + font)
    del get_font_names


def set_font(family=None, weight=None, serif=False):
    if family is None:
        from matplotlib.font_manager import fontManager
        fontManager.addfont(os.path.join(os.path.dirname(__file__), 'font/SourceHanSerif.otf'))
        fontManager.addfont(os.path.join(os.path.dirname(__file__), 'font/SourceHanSans.otf'))
        if serif:
            plt.rcParams['font.family'] = ['Source Han Serif SC']
        else:
            plt.rcParams['font.family'] = ['Source Han Sans SC']
        del fontManager
    else:
        plt.rc('font', family=family, weight=weight)


def set_figsize(figsize=None):
    if figsize is None:
        plt.rcParams['figure.figsize'] = (6, 4)
    else:
        plt.rcParams['figure.figsize'] = figsize


def plot(x, y, fmts='-', num=300,
         title=None, label=None,
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         legend=True, grid=True, figsize=None, font=None,
         show=True, save=None):

    set_font(family=font)

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
         legend=True, grid=True, figsize=None, font=None,
         show=True, save=None):

    set_font(family=font)

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

    

def imshow(x, cmap=None, pillow=False,
           title=None, colorbar=True, axis=False, 
           figsize=None, font=None,
           show=True, save=None):

    set_font(family=font)

    if pillow:
        PIL.Image.fromarray(x).show()
    else:
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



def scatter(x, y, s=None, c=None, alpha=None, 
            title=None, label=None, colorbar=None,
            xlabel=None, ylabel=None, xlim=None, ylim=None,
            legend=True, grid=True, figsize=None, font=None,
            show=True, save=None):

    set_font(family=font)

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

