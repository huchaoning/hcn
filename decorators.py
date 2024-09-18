import numpy as np
from matplotlib import pyplot as plt

import os
from functools import wraps
import inspect

from .macro import hashsum, format_time


__all__ = [
    'stopwatch',
    # 'save'
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


# 有一些问题暂时搁置:
# 1. 保存进去的函数不一定是可以运行的, 比如保存的函数:
# @save
# def f():
#     np.random.randn(1)
# 这个函数必须要 import numpy as np 才可以, 但是这个函数不会自动检查并添加这一段
# 2. 如果有错误的函数一旦保存进去后续 import 就会不通过, 从而导致整个 saved 都不会被 import. 所以要加一个 clear 函数
# 3. 还是得去看看李沐的 d2l 怎么写的

# def save(func):
#     module_path = os.path.join(whereis_myutils(), 'saved.py')
#     func_code = inspect.getsource(func)
    
#     if not os.path.exists(module_path):
#         with open(module_path, 'w') as f:
#             f.write('# Automatically generated locally. Will not be synchronized by git.\n')
    
#     with open(module_path, 'a') as f:
#         f.write(func_code[5:])

#     return func
