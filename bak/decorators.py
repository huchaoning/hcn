import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

import os
from functools import wraps

from .macro import hashsum, format_time


__all__ = [
    'stopwatch',
    'parallelize'
]


def plotter_decorator(**kwargs):
    default_params = {
          'figsize': None, 
             'axis': True, 
             'grid': None, 
           'xlabel': None, 
           'ylabel': None, 
            'title': None,
             'xlim': None, 
             'ylim': None, 
           'legend': True, 
            'label': None, 
             'save': None, 
         'override': False, 
             'show': False,
    }
    default_params = {**default_params, **kwargs}
    def decorator(plotter_function):
        from functools import wraps
        @wraps(plotter_function)
        def wrapper(*args, **kwargs): 
            params = {**default_params, **kwargs}
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

            # plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
            # plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
            # plt.ticklabel_format(style='sci', axis='both')
            
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
                        save = hashsum(temp_name, algorithm='sha1')
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


def stopwatch(func):
    from time import time
    @wraps(func)
    def wrapper(*args, **kargs):
        start = time()
        result = func(*args, **kargs)
        print(f'Function {func.__name__} took: {format_time(time() - start)}')
        return result
    return wrapper



def parallelize(cores: int = 0):
    from dask import delayed, compute
    from dask.distributed import Client

    if cores <= 0:
        import psutil
        cores = psutil.cpu_count(logical=False)

    def decorator(func):
        @wraps(func)
        def wrapper(tasks, *args, **kwargs):

            @delayed
            def _delayed_func(*args, **kwargs):
                return func(*args, **kwargs)
            
            all_tasks = [_delayed_func(task, *args, **kwargs) for task in tasks]
            with Client(n_workers=cores, threads_per_worker=1):
                results = compute(*all_tasks)

            return results
        return wrapper
    return decorator
