from __future__ import division
from __future__ import print_function

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


def relative(xarr, yarr, *args):
    return (xarr, yarr - yarr[0]) + args


def flip(xarr, yarr, *args):
    return (yarr, xarr) + args


def zbt(xarr, yarr, *args):
    zbt_arr = args[0][4]
    return (xarr, yarr + zbt_arr) + args


# TRANSFORM COMPOSITIONS
def relative_per_nucleon(xarr, yarr, *args):
    return relative(*per_nucleon(xarr, yarr, *args))


def relative_log_log_per_nucleon(xarr, yarr, *args):
    return relative(*log_log(*per_nucleon(xarr, yarr, *args)))


def relative_flip(xarr, yarr, *args):
    return relative(*flip(xarr, yarr, *args))


def relative_flip_per_nucleon(xarr, yarr, *args):
    return relative(*flip(*per_nucleon(xarr, yarr, *args)))


def flip_relative_per_nucleon(xarr, yarr, *args):
    return flip(*relative(*per_nucleon(xarr, yarr, *args)))


def relative_flip_relative_per_nucleon(xarr, yarr, *args):
    return relative(*flip_relative_per_nucleon(xarr, yarr, *args))


def relative_zbt(xarr, yarr, *args):
    return relative(*zbt(xarr, yarr, *args))


# TRANSFORM GENERATORS
def power(xpow, ypow):
    return lambda xarr, yarr, *args: (xarr ** xpow, yarr ** ypow) + args
