from __future__ import division
from __future__ import print_function
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit as cf
import numpy as np
import math
from constants import *
from ImsrgDataMap import ImsrgDataMap, Exp
from ImsrgDatum import ImsrgDatum, QuantumNumbers

E = 12
HW = 20


def _map_to_arrays(m):
    """Convert a map of dimensionality 2 into an x and y array"""
    length = len(m)
    x = np.empty(length)
    y = np.empty(length)
    for k, i in zip(m.keys(), range(length)):
        x[i] = k
        y[i] = m[k]
    return x, y


def _polyfit4(x, a, b, c, d, e):
    return np.polyval([a, b, c, d, e], x)


def _polyfit3(x, a, b, c, d):
    return np.polyval([a, b, c, d], x)


def _polyfit2(x, a, b, c):
    return np.polyval([a, b, c], x)


def _expfit1(x, a, b, c):
    return a*np.exp(b*x) + c


def _logfit1(x, a, b, c):
    return a * np.log(b*x) + c


def _powerfit1(x, a, b, c):
    return a * np.power(x, b) + c


def _sqrtfit1(x, a, b):
    return a * np.sqrt(x) + b


def _invfit1(x, a, b):
    return a/(x+1) + b


def _linvfit1(x, a, b):
    return a * x/(x+1) + b


def _asymptote1(x, a, b, c):
    return a * (1 - b/x) + c


def _rel1(x, a, b, c, d):
    return a * np.sqrt(b*x**2 + c) + d


all_data_map = ImsrgDataMap(parent_directory=FILES_DIR)
data_maps = all_data_map.map[Exp(E, HW)]

index_orbital_map = data_maps.index_orbital_map
ime_map = data_maps.index_mass_energy_map()

fitfn = _polyfit4

data = list()
fits = list()
for index in sorted(ime_map.keys(), key=lambda k: index_orbital_map[k].j):
    title = index_orbital_map[index]

    me_map = ime_map[index]
    xdata, ydata = _map_to_arrays(me_map)
    data.append((xdata, ydata, title))

    try:
        popt, pcov = cf(fitfn, xdata, ydata)
    except RuntimeError:
        print('RuntimeError for orbital {o}'.format(o=title))
        continue

    print(title)
    print(popt)
    print()

    curve_x = np.linspace(xdata[0], xdata[-1])
    curve_y = np.array(list(map(lambda x: fitfn(x, *popt), curve_x)))
    fits.append((curve_x, curve_y, title))

    f = plt.figure()
    ax = f.add_subplot(111)

    ax.plot(xdata, ydata, '-b')
    ax.plot(curve_x, curve_y, '-r')
    plt.title(title)
    plt.show()

for dat in data:
    x, y, label = dat
    y = y - y[0]
    plt.plot(x, y, label=tuple(label))
    plt.title('Data')
plt.show()

for fit in fits:
    x, y, label = fit
    y = y - y[0]
    plt.plot(x, y, label=tuple(label))
    plt.title('Fits')
plt.show()
