import numpy as np
import matplotlib.pyplot as plt

import os
import PIL

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


def figsize_fixed(x_figsize=None, y_figsize=None):
    if x_figsize is None or y_figsize is None:
        plt.rcParams['figure.figsize'] = (6, 4)
        print('warning: x_figsize or y_figsize is None, setting figsize to default.')
    else:
        plt.rcParams['figure.figsize'] = (x_figsize, y_figsize)


def imread(img_path):
    if os.path.exists(img_path):
        img = PIL.Image.open(img_path)
        array = []
        for i in range(img.n_frames):
            img.seek(i)
            array.append(np.array(img))
        array = np.array(array)
        if np.shape(array)[0] == 1:
            return array[0].astype(float)
        else:
            return array.astype(float)
    else:
        raise ValueError(f'{img_path} is not exists')


def imwrite(array=None, save=None):
    if array is not None:
        if array.dtype == np.uint8:
            PIL.Image.fromarray(array).save(save)
        else:
            raise TypeError('array.dtype must be np.uint8')
    else:
        raise TypeError('array is None')


def save_util(save=None, override=False):
    if type(save) is bool or type(save) is str:
        if save == True:
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


def plot(x, y, fmt='-', dots=300, figsize=None,
         alpha=None, xerr=None, yerr=None, capsize=3, 
         axis=True, title=None, label=None, legend=True, 
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         grid=True, show=True, save=None, override=False):

    if isinstance(x, tuple):
        if len(x) == 2:
            if callable(y):
                x = np.linspace(x[0], x[1], dots)
            else:
                x = np.linspace(x[0], x[1], len(y))
        else:
            raise TypeError('when x is a tuple, ' +
                            'it is treated as the domain of y, ' +
                            'so the len(x) must be 2')

    if callable(y):
        try: 
            y = y(x)
        except TypeError:
            y = [y(x_) for x_ in x]

    if figsize is not None:
        old_figsize = plt.rcParams['figure.figsize']
        plt.rcParams['figure.figsize'] = figsize
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

    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    if legend and label is not None:
        plt.legend()
    if save is not None:
        if (save == True) and (title is not None):
            save_util(save=title, override=override)
        else:
            save_util(save=save, override=override)
    if show:
        plt.show()
    if figsize is not None:
        plt.rcParams['figure.figsize'] = old_figsize
        del old_figsize


def hist(x, bins=300, histtype='step', density=True, figsize=None,
         axis=True, title=None, label=None, legend=True, 
         xlabel=None, ylabel=None, xlim=None, ylim=None,
         grid=True, show=True, save=None, override=False):

    if figsize is not None:
        old_figsize = plt.rcParams['figure.figsize']
        plt.rcParams['figure.figsize'] = figsize
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
        if (save == True) and (title is not None):
            save_util(save=title, override=override)
        else:
            save_util(save=save, override=override)
    if show:
        plt.show()
    if figsize is not None:
        plt.rcParams['figure.figsize'] = old_figsize
        del old_figsize


def scatter(x, y, s=None, c=None, marker=None, colorbar=False, figsize=None,
            alpha=None, xerr=None, yerr=None, capsize=3,
            axis=True, title=None, label=None, legend=True, 
            xlabel=None, ylabel=None, xlim=None, ylim=None,
            grid=True, show=True, save=None, override=False):

    if figsize is not None:
        old_figsize = plt.rcParams['figure.figsize']
        plt.rcParams['figure.figsize'] = figsize
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
        plt.scatter(x, y, s=s, c=c, alpha=alpha, label=label, marker=marker)
        if xerr is not None or yerr is not None:
            plt.errorbar(x, y, xerr=xerr, yerr=yerr, alpha=alpha, ecolor=c,
                         marker='none', linestyle='none', capsize=capsize)
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
        if (save == True) and (title is not None):
            save_util(save=title, override=override)
        else:
            save_util(save=save, override=override)
    if show:
        plt.show()
    if figsize is not None:
        plt.rcParams['figure.figsize'] = old_figsize
        del old_figsize


def imshow(x, cmap=None, pillow=False, figsize=None, 
           axis=False, title=None, colorbar=True,
           xlabel=None, ylabel=None, xlim=None, ylim=None,
           grid=True, show=True, save=None, override=False):


    if pillow:
        PIL.Image.fromarray(x).show()
    else:
        if figsize is not None:
            old_figsize = plt.rcParams['figure.figsize']
            plt.rcParams['figure.figsize'] = figsize
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
            if (save == True) and (title is not None):
                save_util(save=title, override=override)
            else:
                save_util(save=save, override=override)
        if show:
            plt.show()
        if figsize is not None:
            plt.rcParams['figure.figsize'] = old_figsize
            del old_figsize
