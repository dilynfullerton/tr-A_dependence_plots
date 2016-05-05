"""transforms.py
Transforms to apply to plots before fitting

Each transformation takes an 2+ arguments:
    xarr: ndarray
    yarr: ndarray
    *args: more arguments to be potentially involved in the transformations
Each transformation returns a tuple of the same length as the input containing:
    + transformed x array
    + transformed y array
    + *args unchanged, and in same order
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np


def identity(xarr, yarr, *args):
    return (xarr, yarr) + args


def derivative(xarr, yarr, *args):
    """Right-sided finite difference derivative.
        y'_i = (y_i+1 - y_i) / (x_i+1, x_i)
    The returned x and y arrays are one unit shorter than those given, as
    a consequence of the derivative.
    """
    x = np.array(xarr)[:-1]
    y = np.array(yarr)[:-1]
    for i in range(len(y)):
        y[i] = (yarr[i+1] - yarr[i])/(xarr[i+1] - xarr[i])
    return (x, y) + args


def log_log(xarr, yarr, *args):
    """Given x and y, returns log(x) and log(y) arrays.
    """
    x = np.array(list(map(lambda xi: np.log(abs(xi)), xarr)))
    y = np.array(list(map(lambda yi: np.log(abs(yi)), yarr)))
    return (x, y) + args


def div_x(xarr, yarr, *args):
    """y values are divided by their associated x values
    """
    for i in range(len(yarr)):
        yarr[i] = yarr[i] / xarr[i]
    return (xarr, yarr) + args


def abs_y(xarr, yarr, *args):
    """Absolute value of y
    """
    return (xarr, np.abs(yarr)) + args


def relative_y(xarr, yarr, *args):
    """First value in yarr is subtracted from each y
    """
    return (xarr, yarr - yarr[0]) + args


def relative_x(xarr, yarr, *args):
    """First value in xarr is subtracted from each x
    """
    return (xarr - xarr[0], yarr) + args


def flip(xarr, yarr, *args):
    """Flip the x and y axes
    """
    return (yarr, xarr) + args


# todo: This transform is kind of a hack. Adding the zero body term should be
# todo: built into DatumInt or wherever needed
def pzbt(xarr, yarr, *args):
    """Add zero body term to each y.
    """
    zbt_arr = args[1]['zbt_arr']
    return (xarr, yarr + zbt_arr) + args


# noinspection PyUnusedLocal
# todo: This transform is kind of a hack. The zero body term should be
# todo: built into DatumInt or wherever needed
def zbt(xarr, yarr, *args):
    """Plot the zero body term in place of y
    """
    zbt_arr = args[1]['zbt_arr']
    return (xarr, zbt_arr) + args


# TRANSFORM COMPOSITIONS
# The advantage of this "transform" definition is that transforms can be
# easily strung together. The following are examples of this.
def relative_y_div_x(xarr, yarr, *args):
    return relative_y(*div_x(xarr, yarr, *args))


def relative_y_log_log_div_x(xarr, yarr, *args):
    return relative_y(*log_log(*div_x(xarr, yarr, *args)))


def relative_y_flip(xarr, yarr, *args):
    return relative_y(*flip(xarr, yarr, *args))


def relative_y_flip_div_x(xarr, yarr, *args):
    return relative_y(*flip(*div_x(xarr, yarr, *args)))


def flip_relative_y_div_x(xarr, yarr, *args):
    return flip(*relative_y(*div_x(xarr, yarr, *args)))


def relative_y_flip_relative_y_div_x(xarr, yarr, *args):
    return relative_y(*flip_relative_y_div_x(xarr, yarr, *args))


def relative_y_zbt(xarr, yarr, *args):
    return relative_y(*pzbt(xarr, yarr, *args))


def relative_xy(xarr, yarr, *args):
    return relative_x(*relative_y(xarr, yarr, *args))


def relative_xy_pzbt(xarr, yarr, *args):
    relative_xy(*pzbt(xarr, yarr, *args))


# TRANSFORM GENERATORS
# The following are functions that return transforms based on the given
# arguments.
def power(xpow, ypow):
    """Returns a transform that raises x to xpow and y to ypow
    """
    return lambda xarr, yarr, *args: (xarr ** xpow, yarr ** ypow) + args


def relative_to_y(x0):
    """Returns a transform that subtracts y(x0) from each y
        T(x, y) = (x, y(x)-y(x0))
    """
    def r(xarr, yarr, *args):
        return (xarr, yarr - yarr[np.where(xarr == x0)[0][0]]) + args
    r.__name__ = b'relative_to_y({})'.format(x0)
    return r


def relative_to_x(x0):
    """Returns a transform that subtracts x0 from each x
        T(x, y) = (x-x0, y)
    """
    def r(xarr, yarr, *args):
        return (xarr - x0, yarr) + args
    r.__name___ = b'relative_to_x={}'.format(x0)
    return r


def ltrim(n):
    """Returns a transform that removes the leftmost n points.
    """
    def t(xarr, yarr, *args):
        return (xarr[n:], yarr[n:]) + args
    t.__name__ = b'ltrim({})'.format(n)
    return t


def rtrim(n):
    """Returns a transform that removes the rightmost n points
    """
    def t(xarr, yarr, *args):
        return (xarr[:-n], yarr[:-n]) + args
    t.__name__ = b'rtrim({})'.format(n)
    return t


def first_np(n):
    """Returns a transform that keeps only the leftmost n points
    """
    def t(xarr, yarr, *args):
        return (xarr[:n], yarr[:n]) + args
    t.__name__ = b'first_{}p'.format(n)
    return t

firstp = first_np(1)
first2p = first_np(2)


def cubic_spline(num_pts):
    """Returns a transform that performs a cubic spline through the given
    (x, y) points.
    :param num_pts: number of points (resolution) of the spline
    """
    def cs(xarr, yarr, *args):
        n = len(xarr)
        a = np.zeros(shape=(4*n-4, 4*n-4))
        y = np.zeros(shape=4*n-4)
        for relrow in range(n - 1):
            for p in reversed(range(4)):
                a[relrow][relrow*4+3-p] = (xarr[relrow])**p
                a[relrow+n-1][relrow*4+3-p] = (xarr[relrow+1])**p
            y[relrow] = yarr[relrow]
            y[relrow+n-1] = yarr[relrow+1]
        for relrow in range(n - 2):
            for p in reversed(range(3)):
                xp = (p+1)*(xarr[relrow+1])**p
                a[relrow+2*n-2][relrow*4+2-p] = xp
                a[relrow+2*n-2][(relrow+1)*4+2-p] = -xp
            for p in reversed(range(2)):
                xp = (p+2)*(p+1)*(xarr[relrow+1])**p
                a[relrow+3*n-4][relrow*4+1-p] = xp
                a[relrow+3*n-4][(relrow+1)*4+1-p] = -xp
        for relrow in range(2):
            for p in reversed(range(2)):
                xp = (p+2)*(p+1)*(xarr[p*(n-1)])**p
                a[relrow+4*n-6][relrow*4*(n-2)+1-p] = xp
        coeffs = np.linalg.solve(a, y)
        xnew = np.linspace(xarr[0], xarr[n-1], num=num_pts)
        ynew = np.empty(shape=num_pts)
        j = 0  # 1/4 index of coeffs to use
        cj = coeffs[4*j:4*j+4]
        for i in range(num_pts):
            xi = xnew[i]
            while xi > xarr[j+1]:
                j += 1
                cj = coeffs[4*j:4*j+4]
            ynew[i] = np.polyval(cj, xi)
        return (xnew, ynew) + args
    cs.__name__ = b'cubic_spline'
    return cs


def filter_x(func, name=None):
    """Returns a transform that keeps only (x, y) points for which func(x)
    returns true
    :param func: filter function f: float -> bool
    :param name: name to give the function
    """
    def t(xarr, yarr, *args):
        x_next = list()
        y_next = list()
        for xi, yi in zip(xarr, yarr):
            if func(xi):
                x_next.append(xi)
                y_next.append(yi)
        return (np.array(x_next), np.array(y_next)) + args
    t.__name__ = name if name else b'filter_x'
    return t

filter_evens = filter_x(func=lambda x: x % 2 == 0.0, name=b'filter_evens')
filter_odds = filter_x(func=lambda x: x % 2 == 1.0, name=b'filter_odds')


# TRANSFORM CHAIN GENERATION
def compose_transforms(list_of_transform, t_name_sep=b' '):
    """Returns a transform that applies all of the transforms in the
    given list_of_transform. These are applied in the reverse order that
    they are given, so as to be analogous with the standard way of expressing
    functional composition.
    Example:
        Suppose that list_of_transform is [U, T].
        Then, the composed transform is defined by (UT)(x) = U(T(x))
    :param list_of_transform: list of transform functions, in the order they
    are to be chained
    :param t_name_sep: string separator for the name of the composed transform
    :return: transform function whose behavior is equivalent to applying
    all of the transforms in the list_of_transform in the reversed order
    """
    def m(xarr, yarr, *args):
        a = (xarr, yarr) + args
        for tr in reversed(list_of_transform):
            a = tr(*a)
        return a
    names = [t.__name__ for t in list_of_transform]
    m.__name__ = t_name_sep.join(names)
    return m
