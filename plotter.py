import numpy as np
import matplotlib.pyplot as plt

import os
from PIL import Image as image

from .decorators import plotter_decorator

from matplotlib.font_manager import fontManager
assets_dir = os.path.join(os.path.dirname(__file__), 'assets/')
fontManager.addfont(os.path.join(assets_dir, 'fonts/SourceHanSans.otf'))
fontManager.addfont(os.path.join(assets_dir, 'fonts/lmroman10.otf'))
plt.style.use(os.path.join(assets_dir, 'mplstyle/draft.mplstyle'))
del fontManager


__all__ = ['show_all_fonts', 
           'set_font',
           'style_use',
           'inline_format',
           'figsize_fixed',
           'axline',
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


def style_use(style='draft'):
    plt.rcdefaults()
    plt.style.use(os.path.join(assets_dir, f'mplstyle/{style}.mplstyle'))


def inline_format(fmt='bitmap'):
    from matplotlib_inline import backend_inline
    if fmt.lower() == 'svg':
        backend_inline.set_matplotlib_formats('svg')
    elif fmt.lower() == 'bitmap':
        backend_inline.set_matplotlib_formats('retina')


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


def axline(h=None, v=None, c='k', w=0.5, s='--', *args, **kwargs):
    if h is not None:
        plt.axhline(h, color=c, lw=w, ls=s, *args, **kwargs)

    if v is not None:
        plt.axvline(v, color=c, lw=w, ls=s, *args, **kwargs)


@plotter_decorator()
def plot(x=[], y=None, fmt=None, label=None, dots=300, alpha=None, xerr=None, yerr=None, capsize=3, *args, **kwargs):
    if y is None:
        y = np.copy(x)
        x = np.arange(len(y))

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
    
    y == [] if y is None else y
    if np.shape(x) == np.shape(y):
        if xerr is None and yerr is None:
            _param = [x, y] if fmt is None else [x, y, fmt]
            plt.plot(*_param, label=label, alpha=alpha, *args, **kwargs)
        else:
            c = None if fmt=='-' or fmt=='' else fmt
            plt.errorbar(x, y, c=c, xerr=xerr, yerr=yerr, 
                         label=label, alpha=alpha, capsize=capsize,
                         marker='o', linestyle='--', *args, **kwargs)
    else:
        raise ValueError( 'x and y must have same shape, ' +
                         f'but have shapes {np.shape(x)} and {np.shape(y)}')


@plotter_decorator()
def scatter(x, y, s=None, c=None, marker=None, alpha=None, xerr=None, yerr=None, capsize=3, label=None, *args, **kwargs):
    if np.shape(x) == np.shape(y):
        plt.scatter(x, y, s=s, c=c, alpha=alpha, label=label, marker=marker, *args, **kwargs)
        if xerr is not None or yerr is not None:
            plt.errorbar(x, y, xerr=xerr, yerr=yerr, alpha=alpha, ecolor=c,
                         marker='none', linestyle='none', capsize=capsize, *args, **kwargs)
    else:
        raise ValueError( 'x and y must have same shape, ' +
                         f'but have shapes {np.shape(x)} and {np.shape(y)}')


@plotter_decorator()
def hist(x, bins=300, histtype='step', density=True, label=None, *args, **kwargs):
    plt.hist(x, bins=bins, histtype=histtype, density=density, label=label, *args, **kwargs)


@plotter_decorator(axis=False)
def imshow(x, cmap=None, pillow=False, colorbar=True, *args, **kwargs):
    if pillow:
        image.fromarray(x).show()
    else:
        plt.imshow(x, cmap=cmap, *args, **kwargs)
    if colorbar:
        plt.colorbar()
