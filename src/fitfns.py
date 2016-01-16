from __future__ import print_function
from __future__ import division

import numpy as np

from constants import *


def polyfit4(x, a, b, c, d, e, *constants):
    return _polyfitn(x, a, b, c, d, e)


def polyfit3(x, a, b, c, d, *constants):
    return _polyfitn(x, a, b, c, d)


def polyfit2(x, a, b, c, *constants):
    return _polyfitn(x, a, b, c)


def polyfit1(x, a, b, *constants):
    return _polyfitn(x, a, b)


def _polyfitn(x, *params):
    return np.polyval(params, x)


def expfit1(x, a, b, c, *constants):
    return a * np.exp(b * x) + c


def logfit1(x, a, b, c, *constants):
    return a * np.log(b ** 2 * x + 1) + c


def logbasefit1(x, a, b, c, *constants):
    return a * np.log(x) / np.log(b ** 2 + 1) + c


def powerfit1(x, a, b, c, *constants):
    return a * np.power(x, b) + c


def sqrtfit1(x, a, b, *constants):
    return a * np.sqrt(x) + b


def invfit1(x, a, b, *constants):
    return a / (x + 1) + b


def linvfit1(x, a, b, *constants):
    return a * x / (x + 1) + b


def asymptote1(x, a, b, c, *constants):
    return a * (1 - b / x) + c


def rel1(x, a, b, c, d, *constants):
    return a * np.sqrt(b * x ** 2 + c) + d


# Involving quantum numbers
def linear_j_and_tz_dependence(x, a, b, c, d, *constants):
    if len(constants) == 0:
        return a * x + c
    else:
        quantum_numbers = constants[0]
        j = quantum_numbers.j
        tz = quantum_numbers.tz
        return a * x + b * j * x + c * j * x + d


def quadratic_j_and_tz_dependence(x, a, b, c, d, e, f, g, *constants):
    if len(constants) == 0:
        return np.polyval([a, d, g], x)
    else:
        qnums = constants[0]
        j = qnums.j
        tz = qnums.tz
        return np.polyval([a + b*j + c*tz, d + e*j + f*tz, g], x)


# Fit function generators
def quadratic_j_and_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, d, e, f, *constants):
        if len(constants) == 0:
            return a*(x - zero)**2 + d*(x - zero)
        else:
            qnums = constants[0]
            j = qnums.j
            tz = qnums.tz
            return (a + b*j + c*tz)*(x-zero)**2 + (d + e*j + f*tz)*(x-zero)
    fn.__name__ = ('quadratic_j_and_tz_dependence_with_force_zero_at_'
                   '{z}'.format(z=zero))
    return fn


def quadratic_fit_linear_j_tz_dependence_with_forced_zero(zero):
    def fn(x, a, d, e, f, *constants):
        if len(constants) == 0:
            return a*(x - zero)**2 + d*(x - zero)
        else:
            qnums = constants[0]
            j = qnums.j
            tz = qnums.tz
            return a*(x-zero)**2 + (d + e*j + f*tz)*(x-zero)
    fn.__name__ = ('quadratic_fit_linear_j_tz_dependence_with_forced_zero_at_'
                   '{z}'.format(z=zero))
    return fn


def cubic_fit_linear_j_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, d, e, f, *constants):
        if len(constants) == 0:
            return a*(x - zero)**3 + b*(x-zero)**2 + d*(x - zero)
        else:
            qnums = constants[0]
            j = qnums.j
            tz = qnums.tz
            xp = x - zero
            return np.polyval([a, b, d + e*j + f*tz, 0], xp)
    fn.__name__ = ('cubic_fit_linear_j_tz_dependence_with_forced_zero_at_'
                   '{z}'.format(z=zero))
    return fn


def poly4_fit_linear_j_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, d, e, f, *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            qnums = constants[0]
            j = qnums.j
            tz = qnums.tz
            return np.polyval([a, b, c, d + e*j + f*tz, 0], xp)
    fn.__name__ = ('poly4_fit_linear_j_tz_dependence_with_forced_zero_at_'
                   '{z}'.format(z=zero))
    return fn


def poly4_fit_linear_j_tz_jtz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, d, d1, d2, d12, *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            qnums = constants[0]
            j = qnums.j
            tz = qnums.tz
            return np.polyval([a, b, c, d + d1*j + d2*tz + d12*j*tz, 0], xp)
    fn.__name__ = ('poly4_fit_linear_j_tz_jtz_dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn


def poly4_fit_linear_n_l_j_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, d, d1, d2, d3, d4, *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            qnums = constants[0]
            n, l, j, tz = qnums
            return np.polyval([a, b, c, d+d1*n+d2*l+d3*j+d4*tz, 0], xp)
    fn.__name__ = ('poly4_fit_linear_n_l_j_tz_dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn


def poly4_fit_quadratic_j_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, c1, c2, d, d1, d2, *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            qnums = constants[0]
            j = qnums.j
            tz = qnums.tz
            return np.polyval([a, b, c+c1*j+c2*tz, d+d1*j+d2*tz, 0], xp)
    fn.__name__ = ('poly4_fit_quadratic_j_tz_dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn


def poly4_fit_quadratic_n_l_j_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, c1, c2, c3, c4, d, d1, d2, d3, d4, *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            qnums = constants[0]
            n, l, j, tz = qnums
            return np.polyval([a, b, c+c1*n+c2*l+c3*j+c4*tz,
                               d+d1*n+d2*l+d3*j+d4*tz, 0], xp)
    fn.__name__ = ('poly4_fit_quadratic_n_l_j_tz_dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn
