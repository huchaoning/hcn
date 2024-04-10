import numpy as np
from matplotlib import pyplot as plt

import os
from time import time
from functools import wraps

from .macro import sha1


def plotter_decorator(**kwargs):
    default_params = {
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
             'show': True,
    }
    params = {**default_params, **kwargs}
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


def print_run_time(func):
    @wraps
    def wrapper(*args, **kargs):
        start = time()
        result = func(*args, **kargs)
        print(f'Function {func.__name__} took: {time() - start} seconds')
        return result
    return wrapper

# def npy_cache_mkdir(func):
#     @wraps
#     def wrapper(*args, **kwargs):
#         if kwargs['npy_cache']:
#             if not os.path.exists('./__npy_cache__'):
#                 os.mkdir('./__npy_cache__')
#         return func(*args, **kwargs)
#     return wrapper
