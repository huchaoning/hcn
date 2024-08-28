import numpy as np
import scipy as sp
from math import *

from numpy.typing import ArrayLike

__all__ = [
    'integrate',
    'normalization',
    'max_min_normalization',
    'futils',
]


def integrate(target, int_range=(-inf, inf)):
    if isinstance(target, np.ndarray):
        print('warning: integrate target is an array, doing numerical integration')
        return target.sum()
    else:
        return sp.integrate.quad(target, *int_range)[0]


def normalization(target, int_range=(-inf, inf)):
    if isinstance(target, np.ndarray):
        print('warning: normalization target is an array, doing numerical integration')
        return target / target.sum()
    if callable(target):
        norm = integrate(target, int_range)
        def wrapper(*args, **kwargs):
            return target(*args, **kwargs) / norm
        return wrapper


def min_max_normalization(array: ArrayLike, min_=1, max_=0):
    if min_ > max_:
        raise ValueError('min_ must smaller than max_')
    scaled = (array - array.min()) / (array.max() - array.min())
    return scaled * (max_ - min_)  + min_


class Futils:
    def __init__(self, func):
        self.func = func

    def __repr__(self):
        return f'math_func({self.func})'

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def _operate(self, other, operation):
        if isinstance(other, Futils):
            def wrapper(*args, **kwargs):
                return operation(self.func(*args, **kwargs), other.func(*args, **kwargs))
            return Futils(wrapper)
        elif isinstance(other, (int, float)):
            def wrapper(*args, **kwargs):
                return operation(self.func(*args, **kwargs), other)
            return Futils(wrapper)
        else:
            return NotImplemented

    def __add__(self, other):
        return self._operate(other, lambda x, y: x + y)

    def __radd__(self, other):
        return self._operate(other, lambda x, y: y + x)

    def __sub__(self, other):
        return self._operate(other, lambda x, y: x - y)

    def __rsub__(self, other):
        return self._operate(other, lambda x, y: y - x)

    def __mul__(self, other):
        return self._operate(other, lambda x, y: x * y)

    def __rmul__(self, other):
        return self._operate(other, lambda x, y: y * x)

    def __truediv__(self, other):
        if isinstance(other, Futils):
            def wrapper(*args, **kwargs):
                other_result = other.func(*args, **kwargs)
                if other_result == 0:
                    raise ZeroDivisionError("division by zero")
                return self.func(*args, **kwargs) / other_result
            return Futils(wrapper)
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("division by zero")
            def wrapper(*args, **kwargs):
                return self.func(*args, **kwargs) / other
            return Futils(wrapper)
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        return self._operate(other, lambda x, y: x / y)
    
    def integrate(self, int_range=(-inf, inf)):
        return integrate(self.func, int_range)

    def __matmul__(self, other):
        if not isinstance(other, Futils):
            raise TypeError("Operand must be an instance of Futils")

        def product(x):
            return self.func(x) * other.func(x)
        def wrapper(a=-inf, b=inf):
            return integrate(product, (a, b))
        
        return Futils(wrapper)
    
    def __rmatmul__(self, other):
        if not isinstance(other, Futils):
            raise TypeError("Operand must be an instance of Futils")
        return other @ self


def futils(func):
    return Futils(func)