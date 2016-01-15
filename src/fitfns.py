import numpy as np


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
