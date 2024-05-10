import numpy as np
import matplotlib.pyplot as plt

import os
from PIL import Image as image

from .decorators import plotter_decorator

from matplotlib_inline import backend_inline
backend_inline.set_matplotlib_formats('svg')
del backend_inline

from matplotlib.font_manager import fontManager
fontManager.addfont(os.path.join(os.path.dirname(__file__), 'font/SourceHanSans.otf'))
del fontManager

plt.rcParams['font.family'] = ['Source Han Sans SC']
plt.rcParams['figure.figsize'] = (6, 4)
plt.rcParams['savefig.format'] = 'svg'

__all__ = ['show_all_fonts', 
           'set_font',
           'figsize_fixed',
           'plot',
           'hist',
           'scatter',
           'imshow']


def show_all_fonts():
    from matplotlib.font_manager import get_font_names
    all_fonts = get_font_names()
    print('font list got from matplotlib.font_manager:')
    for font in sorted(all_fonts):
        print('\t' + font)


def set_font(family=None, weight=None):
    if family is None:
        plt.rcParams['font.family'] = ['Source Han Sans SC']
    else:
        plt.rc('font', family=family, weight=weight)


def figsize_fixed(x_figsize=None, y_figsize=None):
    if isinstance(x_figsize, (tuple, list)) and (y_figsize is None):
        plt.rcParams['figure.figsize'] = x_figsize
    elif isinstance(y_figsize, (tuple, list)) and (x_figsize is None):
        plt.rcParams['figure.figsize'] = y_figsize
    elif x_figsize is None and y_figsize is None:
        plt.rcParams['figure.figsize'] = (6, 4)
        print('warning: x_figsize and y_figsize is None, setting figsize to default (6, 4)')
    elif isinstance(x_figsize, (int, float)) and isinstance(x_figsize, (int, float)):
        plt.rcParams['figure.figsize'] = (x_figsize, y_figsize)
    else:
        raise ValueError('invalid figsize parameters')


@plotter_decorator()
def plot(x=[], y=[], fmt='-', label=None, dots=300, alpha=None, xerr=None, yerr=None, capsize=3, *args, **kwargs):
    if len(x) == 0 and len(y) != 0:
        x = (0, 1)
        print('warning: x is a empty, x is treated as (0, 1)')
    if isinstance(x, tuple):
        if len(x) == 2:
            if callable(y):
                x = np.linspace(x[0], x[1], dots)
            else:
                x = np.linspace(x[0], x[1], len(y))
        else:
            raise TypeError('when x is a tuple, ' +
                            'it is treated as the domain of y, ' +
                            'so len(x) must be 2')
    if callable(y):
        try: 
            y = y(x)
        except (TypeError, ValueError):
            y = [y(x_) for x_ in x]
    if np.shape(x) == np.shape(y):
        if xerr is None and yerr is None:
            plt.plot(x, y, fmt, label=label, alpha=alpha)
        else:
            c = None if fmt=='-' or fmt=='' else fmt
            plt.errorbar(x, y, c=c, xerr=xerr, yerr=yerr, 
                         label=label, alpha=alpha, capsize=capsize,
                         marker='o', linestyle='--')
    else:
        raise ValueError( 'x and y must have same shape, ' +
                         f'but have shapes {np.shape(x)} and {np.shape(y)}')


@plotter_decorator()
def scatter(x, y, s=None, c=None, marker=None, alpha=None, xerr=None, yerr=None, capsize=3, label=None, *args, **kwargs):
    if np.shape(x) == np.shape(y):
        plt.scatter(x, y, s=s, c=c, alpha=alpha, label=label, marker=marker)
        if xerr is not None or yerr is not None:
            plt.errorbar(x, y, xerr=xerr, yerr=yerr, alpha=alpha, ecolor=c,
                         marker='none', linestyle='none', capsize=capsize)
    else:
        raise ValueError( 'x and y must have same shape, ' +
                         f'but have shapes {np.shape(x)} and {np.shape(y)}')


@plotter_decorator()
def hist(x, bins=300, histtype='step', density=True, label=None, *args, **kwargs):
    plt.hist(x, bins=bins, histtype=histtype, density=density, label=label)


@plotter_decorator(axis=False)
def imshow(x, cmap=None, pillow=False, colorbar=True, *args, **kwargs):
    if pillow:
        image.fromarray(x).show()
    else:
        plt.imshow(x, cmap=cmap)
    if colorbar:
        plt.colorbar()
