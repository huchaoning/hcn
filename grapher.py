from math import *
import numpy as np
import matplotlib.pyplot as plt

import PIL
import cv2 as cv

from matplotlib_inline import backend_inline
backend_inline.set_matplotlib_formats('svg')

import os
from matplotlib.font_manager import fontManager
fontManager.addfont(os.path.join(os.path.dirname(__file__), 'font/SourceHanSans.otf'))
plt.rcParams['font.family'] = ['Source Han Sans SC']

plt.rcParams['figure.figsize'] = (6, 4)


def show_all_fonts():
    from matplotlib.font_manager import get_font_names
    all_fonts = get_font_names()
    print('font list got from matplotlib.font_manager:')
    for font in sorted(all_fonts):
        print('\t' + font)


def set_font(family=None, weight=None, lock=False):
    if family is None:
        plt.rcParams['font.family'] = ['Source Han Sans SC']
    else:
        plt.rc('font', family=family, weight=weight)


def set_figsize(figsize=None, lock=False):
    if figsize is None:
        plt.rcParams['figure.figsize'] = (6, 4)
    else:
        plt.rcParams['figure.figsize'] = figsize


def plot(x, y, fmts='-', dots=300, 
         figsize=None, title=None, label=None, legend=True, 
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         grid=True, show=True, save=None):

    if isinstance(x, (list, tuple)):
        if len(x) == 2:
            if callable(y):
                x = np.linspace(x[0], x[1], dots)
            else:
                x = np.linspace(x[0], x[1], len(y))
        else:
            raise TypeError('when x is a tuple or list, it is treated as the domain of y')

    if callable(y):
        try: 
            y = y(x)
        except TypeError:
            y_ = []
            for x_ in x:
                y_.append(y(x_))
            y = np.array(y_)
            del x_, y_
    
    plt.figure(figsize=figsize)
    plt.title(title)
    plt.grid(grid)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.plot(x, y, fmts, label=label)

    plt.xlim(xlim)
    plt.ylim(ylim)

    if legend and label is not None:
        plt.legend()
    if save is not None:
        plt.savefig(save)
    if show:
        plt.show()


def hist(x, bins=300, histtype='step', density=True,
         figsize=None, title=None, label=None, legend=True, 
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         grid=True, show=True, save=None):

    plt.figure(figsize=figsize)
    plt.title(title)
    plt.grid(grid)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.hist(x, bins=bins, histtype=histtype, density=density, label=label)

    plt.xlim(xlim)
    plt.ylim(ylim)

    if legend and label is not None:
        plt.legend()
    if save is not None:
        plt.savefig(save)
    if show:
        plt.show()


def scatter(x, y, s=None, c=None, alpha=None, colorbar=None,
            figsize=None, title=None, label=None, legend=True, 
            xlabel=None, ylabel=None, xlim=None, ylim=None,
            grid=True, show=True, save=None):

    plt.figure(figsize=figsize)
    plt.title(title)
    plt.grid(grid)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.scatter(x, y, s=s, c=c, alpha=alpha, label=label)

    plt.xlim(xlim)
    plt.ylim(ylim)

    if colorbar:
        plt.colorbar()
    elif (colorbar is not False) and (c is not None):
        plt.colorbar()
    if legend and label is not None:
        plt.legend()
    if save is not None:
        plt.savefig(save)
    if show:
        plt.show()


def imshow(x, cmap=None, pillow=False, colorbar=True, axis=False, 
         figsize=None, title=None,
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         grid=True, show=True, save=None):

    if pillow:
        PIL.Image.fromarray(x).show()
    else:
        plt.figure(figsize=figsize)
        plt.title(title)
        plt.grid(grid)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        if not axis:
            plt.xticks([])
            plt.yticks([])

        plt.imshow(x, cmap=cmap)

        plt.xlim(xlim)
        plt.ylim(ylim)

        if colorbar:
            plt.colorbar()
        if save is not None:
            plt.savefig(save)
        if show:
            plt.show()


def imread(img_path, pillow=False):
    if os.path.exists(img_path):
        if pillow:
            return np.array(PIL.Image.open(img_path)).astype(float)
        else:
            return cv.imread(img_path, cv.IMREAD_GRAYSCALE | cv.IMREAD_ANYDEPTH).astype(float)
    else:
        raise ValueError(f'{img_path} is not exists')


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

