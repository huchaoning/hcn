import numpy as np
import matplotlib.pyplot as plt

import os
import PIL
import cv2 as cv

from .macro import sha1

from matplotlib_inline import backend_inline
backend_inline.set_matplotlib_formats('svg')
del backend_inline

from matplotlib.font_manager import fontManager
fontManager.addfont(os.path.join(os.path.dirname(__file__), 'font/SourceHanSans.otf'))
del fontManager

plt.rcParams['font.family'] = ['Source Han Sans SC']
plt.rcParams['figure.figsize'] = (6, 4)
plt.rcParams['savefig.format'] = 'svg'


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


def set_figsize(figsize=None):
    if figsize is None:
        plt.rcParams['figure.figsize'] = (6, 4)
    else:
        plt.rcParams['figure.figsize'] = figsize


def imread(img_path, pillow=False):
    if os.path.exists(img_path):
        if pillow:
            return np.array(PIL.Image.open(img_path)).astype(float)
        else:
            return cv.imread(img_path, cv.IMREAD_GRAYSCALE | cv.IMREAD_ANYDEPTH).astype(float)
    else:
        raise ValueError(f'{img_path} is not exists')


def imreadmutli(img_path, pillow=True):
    if os.path.exists(img_path):
        if pillow:
            img = PIL.Image.open(img_path)
            mptiff = []
            for i in range(img.n_frames):
                img.seek(i)
                mptiff.append(np.array(img))
            return np.array(mptiff).astype(float)
        else:
            raise ValueError('cv2 is not available yet')
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


def save_util(save=None, override=False):
    if type(save) is bool or type(save) is str:
        if save:
            while True:
                temp_name = f'{np.random.randint(0, 1e8)}.svg'
                if not os.path.exists(temp_name):
                    break
            plt.savefig(temp_name)
            save = sha1(temp_name)
            os.rename(src=temp_name, dst=f'{save}.svg')
        elif type(save) is str:
            if os.path.exists(save) or os.path.exists(f'{save}.svg'):
                if override:
                    plt.savefig(save)
                else:
                    raise FileExistsError('file already exists')
            else:
                plt.savefig(save)
    else:
        raise TypeError('type(save) must be bool or str')


def plot(x, y, fmts='-', dots=300, 
         axis=True, title=None, label=None, legend=True, 
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         grid=True, show=True, save=None, override=False):

    if isinstance(x, (list, tuple)):
        if len(x) == 2:
            if callable(y):
                x = np.linspace(x[0], x[1], dots)
            else:
                x = np.linspace(x[0], x[1], len(y))
        else:
            raise TypeError('when x is a tuple or list, ' +
                            'it is treated as the domain of y, ' +
                            'len(x) must be 2')

    if callable(y):
        try: 
            y = y(x)
        except TypeError:
            y_ = []
            for x_ in x:
                y_.append(y(x_))
            y = np.array(y_)
            del x_, y_

    if not axis:
        plt.xticks([])
        plt.yticks([])
    if title is not None:
        plt.title(title)
    if grid is not None:    
        plt.grid(grid)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)

    if np.shape(x) == np.shape(y):
        plt.plot(x, y, fmts, label=label)
    else:
        raise ValueError( 'x and y must have same shape, ' +
                         f'but have shapes {np.shape(x)} and {np.shape(y)}')

    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    if legend and label is not None:
        plt.legend()
    if save is not None:
        save_util(save=save, override=override)
    if show:
        plt.show()


def hist(x, bins=300, histtype='step', density=True,
         axis=True, title=None, label=None, legend=True, 
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         grid=True, show=True, save=None, override=False):

    if not axis:
        plt.xticks([])
        plt.yticks([])
    if title is not None:
        plt.title(title)
    if grid is not None:    
        plt.grid(grid)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)

    plt.hist(x, bins=bins, histtype=histtype, density=density, label=label)

    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    if legend and label is not None:
        plt.legend()
    if save is not None:
        save_util(save=save, override=override)
    if show:
        plt.show()


def scatter(x, y, s=None, c=None, alpha=None, colorbar=False,
            axis=True, title=None, label=None, legend=True, 
            xlabel=None, ylabel=None, xlim=None, ylim=None,
            grid=True, show=True, save=None, override=False):

    if not axis:
        plt.xticks([])
        plt.yticks([])
    if title is not None:
        plt.title(title)
    if grid is not None:    
        plt.grid(grid)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)

    if np.shape(x) == np.shape(y):
        plt.scatter(x, y, s=s, c=c, alpha=alpha, label=label)
    else:
        raise ValueError( 'x and y must have same shape, ' +
                         f'but have shapes {np.shape(x)} and {np.shape(y)}')

    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    if legend and label is not None:
        plt.legend()
    if colorbar and (c is not None):
        plt.colorbar()
    if save is not None:
        save_util(save=save, override=override)
    if show:
        plt.show()

def imshow(x, cmap=None, pillow=False, colorbar=True, 
           axis=False, title=None,
           xlabel=None, ylabel=None, xlim=None, ylim=None,
           grid=True, show=True, save=None, override=False):

    if pillow:
        PIL.Image.fromarray(x).show()
    else:
        if not axis:
            plt.xticks([])
            plt.yticks([])
        if title is not None:
            plt.title(title)
        if grid is not None:    
            plt.grid(grid)
        if xlabel is not None:
            plt.xlabel(xlabel)
        if ylabel is not None:
            plt.ylabel(ylabel)

        plt.imshow(x, cmap=cmap)

        if xlim is not None:
            plt.xlim(xlim)
        if ylim is not None:
            plt.ylim(ylim)
        if colorbar:
            plt.colorbar()
        if save is not None:
            save_util(save=save, override=override)
        if show:
            plt.show()

