from __future__ import division
from __future__ import print_function
import numpy as np


def identity(xarr, yarr, *args):
    return xarr, yarr


def derivative(xarr, yarr, *args):
    x = np.array(xarr)[:-1]
    y = np.array(yarr)[:-1]
    for i in range(len(y)):
        y[i] = yarr[i+1] - yarr[i]
    return x, y


def log_log(xarr, yarr, *args):
    x = np.array(list(map(lambda xi: np.log(abs(xi)), xarr)))
    y = np.array(list(map(lambda yi: np.log(abs(yi)), yarr)))
    return x, y


def per_nucleon(xarr, yarr, *args):
    for i in range(len(yarr)):
        yarr[i] = yarr[i] / xarr[i]
    return xarr, yarr


def absval(xarr, yarr, *args):
    return np.abs(xarr), np.abs(yarr)


def power(xpow, ypow, *args):
    return lambda xarr, yarr: (xarr ** xpow, yarr ** ypow)
