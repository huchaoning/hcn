import numpy as np
import scipy as sp
from math import *

from numpy.typing import ArrayLike

__all__ = [
    'integrate',
    'normalize',
    'min_max_normalize',
    'futils',
]


def integrate(target, int_range=(-inf, inf)):
    if isinstance(target, np.ndarray):
        print('warning: integrate target is an array, doing numerical integration')
        return target.sum()
    else:
        return sp.integrate.quad(target, *int_range)[0]


def normalize(target, int_range=(-inf, inf)):
    if isinstance(target, np.ndarray):
        print('warning: normalization target is an array, doing numerical integration')
        return target / target.sum()
    if callable(target):
        norm = integrate(target, int_range)
        def wrapper(*args, **kwargs):
            return target(*args, **kwargs) / norm
        return wrapper


def min_max_normalize(array: ArrayLike, min_=0, max_=1):
    if min_ > max_:
        raise ValueError('min_ must smaller than max_')
    scaled = (array - array.min()) / (array.max() - array.min())
    return scaled * (max_ - min_)  + min_


class Futils:
    def __init__(self, func):
        self.func = func

    def __repr__(self):
        return f'Futils({self.func})'

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
    
    def integrate(self, a=-inf, b=inf):
        return integrate(self.func, (a, b))

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
    
    def normalize(self, a=-inf, b=inf):
        return Futils(normalize(self.func, (a, b)))
    
    def as_pdf(self, a=-inf, b=inf):
        if (a and b) is not False:
            func_ = self.normalize(a, b).func
        else:
            func_ = self.func
        class distribution(sp.stats.rv_continuous):
            def _pdf(self, x):
                return func_(x)
            def _cdf(self, x):
                return integrate(func_, (a, x))
        return distribution()


def futils(func) -> Futils:
    return Futils(func)