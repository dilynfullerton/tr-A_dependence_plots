import numpy as np


def polyfit4(x, a, b, c, d, e):
    return np.polyval([a, b, c, d, e], x)


def polyfit3(x, a, b, c, d):
    return np.polyval([a, b, c, d], x)


def polyfit2(x, a, b, c):
    return np.polyval([a, b, c], x)


def expfit1(x, a, b, c):
    return a*np.exp(b*x) + c


def logfit1(x, a, b, c):
    return a * np.log(b**2 * x + 1) + c


def logbasefit1(x, a, b, c):
    return a * np.log(x) / np.log(b**2 + 1) + c


def powerfit1(x, a, b, c):
    return a * np.power(x, b) + c


def sqrtfit1(x, a, b):
    return a * np.sqrt(x) + b


def invfit1(x, a, b):
    return a/(x+1) + b


def linvfit1(x, a, b):
    return a * x/(x+1) + b


def asymptote1(x, a, b, c):
    return a * (1 - b/x) + c


def rel1(x, a, b, c, d):
    return a * np.sqrt(b*x**2 + c) + d