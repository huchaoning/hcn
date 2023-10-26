import numpy as np
import pandas as pd

import cv2 as cv

import matplotlib.pyplot as plt
from matplotlib_inline import backend_inline

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


def show_all_fonts():
    from matplotlib.font_manager import FontManager
    all_fonts = set(f.name for f in FontManager().ttflist)
    print('All font list get from matplotlib.font_manager:')
    for f in sorted(all_fonts):
        print('\t' + f)


def plot(X, Y, fmts='-',
         title=None, label=None,
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         legend=True, grid=True, font=None, figsize=(5.6, 4),
         show=True, save=None):

    backend_inline.set_matplotlib_formats('svg')

    if font is None:
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
        plt.plot(X, Y, fmts)
    else:
        plt.plot(X, Y, fmts, label=label)

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
    

def hist(X, bins=300, histtype='step', density=True,
         title=None, label=None,
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         legend=True, grid=True, font=None, figsize=(5.6, 4),
         save=None):

    backend_inline.set_matplotlib_formats('svg')

    if font is None:
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
        plt.hist(X, bins=bins, histtype=histtype, density=density)
    else:
        plt.hist(X, bins=bins, histtype=histtype, density=density, label=label)

    if legend and label is not None:
        plt.legend()

    if grid:
        plt.grid(True)
    else:
        plt.grid(False)

    if save is not None:
        plt.savefig(save)

    plt.show()


def imshow(X, cmap=None, title=None, colorbar=True, axis=False, font=None, save=None):
    backend_inline.set_matplotlib_formats('svg')
    if font is None:
        plt.rcdefaults()
    else:
        plt.rc('font', family=font)

    if not axis:
        plt.xticks(())
        plt.yticks(())

    if title is not None:
        plt.title(title)

    if cmap is None:
        plt.imshow(X)
    else:
        plt.imshow(X, cmap=cmap)

    if colorbar:
        plt.colorbar()

    if save is not None:
        plt.savefig(save)

    plt.show()


if __name__ == "__main__":
    main()
