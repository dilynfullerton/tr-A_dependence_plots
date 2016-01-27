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


def multi(list_of_transform, t_name_sep=b' '):
    def m(xarr, yarr, *args):
        a = (xarr, yarr) + args
        for tr in reversed(list_of_transform):
            a = tr(*a)
        return a
    names = [t.__name__ for t in list_of_transform]
    m.__name__ = t_name_sep.join(names)
    return m
