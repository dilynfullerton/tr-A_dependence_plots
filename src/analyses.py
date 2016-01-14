from __future__ import print_function
from __future__ import division
import numpy as np


def _is_increasing(a):
    """Determines whether a is an increasing array

    :param a: one dimensional array
    :return: True if increasing, false otherwise
    """
    return reduce(lambda x, y: x and y > 0, _deriv(a))


def _is_decreasing(a):
    """Determines whether a is a decreasing array

    :param a: one dimensional array
    :return: True if decreasing, false otherwise
    """
    return reduce(lambda x, y: x and y < 0, _deriv(a))


def _is_concave_up(a):
    """Determines whether the slope of a is always increasing

    :param a: one dimensional array
    :return: True if the slope of a is always increasing, false otherwise
    """
    return _is_increasing(_deriv(a))


def _is_concave_down(a):
    """Determines whether the slope of a is always decreasing

    :param a: one dimensional array
    :return: True if the slope of a is always decreasing, false otherwise
    """
    return _is_decreasing(_deriv(a))


def _local_maxima(x, y):
    """Given two arrays, x and y, determines the x values that produce a local
    maxima in y

    :param x: one-dim array
    :param y: one-dim array the same size as y
    :return: a list of the x values that produce a local max in y
    """
    return _local_extrema(x, y, lambda yi, yn: yi > yn)


def _local_minima(x, y):
    """Given two arrays, x and y, determines the x values that produce a local
    minimum in y

    :param x: one-dim array
    :param y: one-dim array the same size as x
    :return: a list of the x values that produce a local min in y
    """
    return _local_extrema(x, y, lambda yi, yn: yi < yn)


def _local_extrema(x, y, fn):
    """Given two arrays, x and y, determines the x values that produce a local
    extrema in y, where an extrema

    :param x: one-dim array
    :param y: one-dim array the same size as x
    :param fn: a function of two variables, the first of which describing
    the current point and the next operating on each of its neighbors
    :return: a list of the x values that produce a local extrema in y
    """
    extrema = list()
    for i in range(1, len(x) - 1):
        if fn(y[i], y[i-1]) and fn(y[i], y[i+1]):
            extrema.append(x[i])
    return extrema


def _mean_slope(a):
    """Returns the average slope in the array a

    :param a: one-dimensional array
    :return: the average slope in a
    """
    return (a[-1] - a[0]) / (len(a) - 1)


def _mean_concavity(a):
    """Returns the average concavity in the array a

    :param a: one-dimensional array
    :return: the average concavity in a
    """
    return _mean_slope(_deriv(a))


def _deriv(a):
    """Takes the first derivative of 1d array a"""
    return np.dot(_d_matrix(a.size), a)


def _d_matrix(n):
    """Construct the derivative finite differencing matrix of size (n-1) x n,
        where n is the size of the column vector whose derivative is to be
        determined
    """
    d = np.zeros([n-1, n])
    for i in range(n - 1):
        d[i, i] = -1
        d[i, i+1] = 1
    return d
