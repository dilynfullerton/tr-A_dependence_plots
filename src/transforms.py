"""Transforms to apply to plots before fitting

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
    x = np.array(xarr)[:-1]
    y = np.array(yarr)[:-1]
    for i in range(len(y)):
        y[i] = yarr[i+1] - yarr[i]
    return (x, y) + args


def log_log(xarr, yarr, *args):
    x = np.array(list(map(lambda xi: np.log(abs(xi)), xarr)))
    y = np.array(list(map(lambda yi: np.log(abs(yi)), yarr)))
    return (x, y) + args


def per_nucleon(xarr, yarr, *args):
    for i in range(len(yarr)):
        yarr[i] = yarr[i] / xarr[i]
    return (xarr, yarr) + args


def absval(xarr, yarr, *args):
    return (np.abs(xarr), np.abs(yarr)) + args


def relative_y(xarr, yarr, *args):
    return (xarr, yarr - yarr[0]) + args


def relative_x(xarr, yarr, *args):
    return (xarr - xarr[0], yarr) + args


def flip(xarr, yarr, *args):
    return (yarr, xarr) + args


def pzbt(xarr, yarr, *args):
    zbt_arr = args[1]['zbt_arr']
    return (xarr, yarr + zbt_arr) + args


# noinspection PyUnusedLocal
def zbt(xarr, yarr, *args):
    zbt_arr = args[1]['zbt_arr']
    return (xarr, zbt_arr) + args


def firstp(xarr, yarr, *args):
    return (xarr[0:1], yarr[0:1]) + args


def first2p(xarr, yarr, *args):
    return (xarr[0:2], yarr[0:2]) + args


# TRANSFORM COMPOSITIONS
def relative_per_nucleon(xarr, yarr, *args):
    return relative_y(*per_nucleon(xarr, yarr, *args))


def relative_log_log_per_nucleon(xarr, yarr, *args):
    return relative_y(*log_log(*per_nucleon(xarr, yarr, *args)))


def relative_flip(xarr, yarr, *args):
    return relative_y(*flip(xarr, yarr, *args))


def relative_flip_per_nucleon(xarr, yarr, *args):
    return relative_y(*flip(*per_nucleon(xarr, yarr, *args)))


def flip_relative_per_nucleon(xarr, yarr, *args):
    return flip(*relative_y(*per_nucleon(xarr, yarr, *args)))


def relative_flip_relative_per_nucleon(xarr, yarr, *args):
    return relative_y(*flip_relative_per_nucleon(xarr, yarr, *args))


def relative_zbt(xarr, yarr, *args):
    return relative_y(*pzbt(xarr, yarr, *args))


def relative_xy(xarr, yarr, *args):
    return relative_x(*relative_y(xarr, yarr, *args))


def relative_xy_zbt(xarr, yarr, *args):
    relative_xy(*pzbt(xarr, yarr, *args))


# TRANSFORM GENERATORS
def power(xpow, ypow):
    return lambda xarr, yarr, *args: (xarr ** xpow, yarr ** ypow) + args


def relative_to_y(x):
    def r(xarr, yarr, *args):
        return (xarr, yarr - yarr[np.where(xarr == x)[0][0]]) + args
    r.__name__ = b'relative_to_y({})'.format(x)
    return r


def relative_to_x(x):
    def r(xarr, yarr, *args):
        return (xarr - x, yarr) + args
    r.__name___ = b'relative_to_x={}'.format(x)
    return r


def ltrim(n):
    def t(xarr, yarr, *args):
        return (xarr[n:], yarr[n:]) + args
    t.__name__ = b'ltrim({})'.format(n)
    return t


def rtrim(n):
    def t(xarr, yarr, *args):
        return (xarr[:-n], yarr[:-n]) + args
    t.__name__ = b'rtrim({})'.format(n)
    return t


def first_np(n):
    def t(xarr, yarr, *args):
        return (xarr[:n], yarr[:n]) + args
    t.__name__ = b'first_{}p'.format(n)
    return t


def cubic_spline(num_pts):
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
