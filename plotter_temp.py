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

__all__ = [
    'show_all_fonts', 
    'set_font',
    'figsize_fixed',
    'imread',
    'imwrite',
    'plot',
    'hist',
    'scatter',
    'imshow'
]


shared_params = {
    'figsize': None, 
    'axis': True, 
    'grid': True, 
    'xlabel': None, 
    'ylabel': None, 
    'title': None,
    'xlim': None, 
    'ylim': None, 
    'legend': True, 
    'label': None, 
    'save': None, 
    'override': False, 
    'show': True
}


def plotter_decorator(**kwargs):
    params = {**shared_params, **kwargs}
    def decorator(plotter_function):
        from functools import wraps
        @wraps(plotter_function)
        def wrapper(*args, **kwargs):    
            if params['figsize'] is not None:
                old_figsize = plt.rcParams['figure.figsize']
                plt.rcParams['figure.figsize'] = params['figsize']
            if not params['axis']:
                plt.xticks([])
                plt.yticks([])
            if params['grid'] is not None:    
                plt.grid(params['grid'])
            if params['xlabel'] is not None:
                plt.xlabel(params['xlabel'])
            if params['ylabel'] is not None:
                plt.ylabel(params['ylabel'])
            if params['title'] is not None:
                plt.title(params['title'])

            plotter_function(*args, **kwargs)
            
            if params['xlim'] is not None:
                plt.xlim(params['xlim'])
            if params['ylim'] is not None:
                plt.ylim(params['ylim'])
            if params['legend'] and params['label'] is not None:
                plt.legend()
            save = params['save']
            if save is not None:
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
                            if params['override']:
                                plt.savefig(save)
                            else:
                                raise FileExistsError('file already exists')
                        else:
                            plt.savefig(save)
                else:
                    raise TypeError('type(save) must be bool or str')
            if params['show']:
                plt.show()
            if params['figsize'] is not None:
                plt.rcParams['figure.figsize'] = old_figsize
        return wrapper
    return decorator


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
        print('warning: x_figsize and y_figsize is None, setting figsize to default.')
    elif isinstance(x_figsize, (int, float)) and isinstance(x_figsize, (int, float)):
        plt.rcParams['figure.figsize'] = (x_figsize, y_figsize)
    else:
        raise ValueError('invalid figsize parameters')


def imread(img_path):
    if os.path.exists(img_path):
        img = PIL.Image.open(img_path)
        array = []
        for i in range(img.n_frames):
            img.seek(i)
            array.append(np.array(img))
        array = np.array(array, dtype=float)
        if np.shape(array)[0] == 1:
            return array[0]
        else:
            return array
    else:
        raise FileNotFoundError(f'{img_path} is not exists')


def imwrite(array=None, save=None):
    if array is not None:
        if array.dtype == np.uint8:
            PIL.Image.fromarray(array).save(save)
        else:
            raise TypeError('array.dtype must be np.uint8')
    else:
        raise TypeError('array is None')


@plotter_decorator()
def plot(
    x: np.ndarray or tuple = [], 
    y: np.ndarray or function = [], 
    fmt: str = '-', 
    dots: int = 300, 
    alpha: float = None, 
    xerr: np.ndarray = None, 
    yerr: np.ndarray = None, 
    capsize: float = 3,

    figsize: tuple = shared_params['figsize'], 
    axis: bool = shared_params['axis'], 
    grid: bool = shared_params['grid'], 
    xlabel: str = shared_params['xlabel'], 
    ylabel: str = shared_params['ylabel'], 
    title: str = shared_params['title'],
    xlim: tuple = shared_params['xlim'], 
    ylim: tuple = shared_params['ylim'], 
    legend: bool = shared_params['legend'], 
    label: str = shared_params['label'], 
    save: bool or str = shared_params['save'], 
    override: bool = shared_params['override'], 
    show: bool = shared_params['show']
):
    if len(x) == 0:
        x = (0, 1)
        if len(y) != 0:
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
        except TypeError:
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
def scatter(
    x: np.ndarray = [], 
    y: np.ndarray = [], 
    s: np.ndarray = None, 
    c: str = None, 
    marker: str = None, 
    alpha: float = None, 
    xerr: np.ndarray = None, 
    yerr: np.ndarray = None, 
    capsize: float = 3,

    figsize: tuple = shared_params['figsize'], 
    axis: bool = shared_params['axis'], 
    grid: bool = shared_params['grid'], 
    xlabel: str = shared_params['xlabel'], 
    ylabel: str = shared_params['ylabel'], 
    title: str = shared_params['title'],
    xlim: tuple = shared_params['xlim'], 
    ylim: tuple = shared_params['ylim'], 
    legend: bool = shared_params['legend'], 
    label: str = shared_params['label'], 
    save: bool or str = shared_params['save'], 
    override: bool = shared_params['override'], 
    show: bool = shared_params['show']
):
    if np.shape(x) == np.shape(y):
        plt.scatter(x, y, s=s, c=c, alpha=alpha, label=label, marker=marker)
        if xerr is not None or yerr is not None:
            plt.errorbar(x, y, xerr=xerr, yerr=yerr, alpha=alpha, ecolor=c,
                         marker='none', linestyle='none', capsize=capsize)
    else:
        raise ValueError( 'x and y must have same shape, ' +
                         f'but have shapes {np.shape(x)} and {np.shape(y)}')


@plotter_decorator()
def hist(
    x: np.ndarray = [], 
    bins: int = 300, 
    histtype: str = 'step', 
    density: bool = True,

    figsize: tuple = shared_params['figsize'], 
    axis: bool = shared_params['axis'], 
    grid: bool = shared_params['grid'], 
    xlabel: str = shared_params['xlabel'], 
    ylabel: str = shared_params['ylabel'], 
    title: str = shared_params['title'],
    xlim: tuple = shared_params['xlim'], 
    ylim: tuple = shared_params['ylim'], 
    legend: bool = shared_params['legend'], 
    label: str = shared_params['label'], 
    save: bool or str = shared_params['save'], 
    override: bool = shared_params['override'], 
    show: bool = shared_params['show']
):
    plt.hist(x, bins=bins, histtype=histtype, density=density, label=label)


@plotter_decorator(axis=False)
def imshow(
    x: np.ndarray = [], 
    cmap: str = None, 
    pillow: bool = False, 
    colorbar:bool = True,
           
    figsize: tuple = shared_params['figsize'], 
    axis: bool = shared_params['axis'], 
    grid: bool = shared_params['grid'], 
    xlabel: str = shared_params['xlabel'], 
    ylabel: str = shared_params['ylabel'], 
    title: str = shared_params['title'],
    xlim: tuple = shared_params['xlim'], 
    ylim: tuple = shared_params['ylim'], 
    legend: bool = shared_params['legend'], 
    label: str = shared_params['label'], 
    save: bool or str = shared_params['save'], 
    override: bool = shared_params['override'], 
    show: bool = shared_params['show']
):
    if pillow:
        PIL.Image.fromarray(x).show()
    else:
        plt.imshow(x, cmap=cmap)
    if colorbar:
        plt.colorbar()
