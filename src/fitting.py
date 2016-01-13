from __future__ import division
from __future__ import print_function
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit as cf
import numpy as np
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

all_data_map = ImsrgDataMap(parent_directory=FILES_DIR)
data_maps = all_data_map.map[Exp(E, HW)]

index_orbital_map = data_maps.index_orbital_map
ime_map = data_maps.index_mass_energy_map()

fitfn = _polyfit4

fits = list()
for index in sorted(ime_map.keys(), key=lambda k: index_orbital_map[k].j):
    me_map = ime_map[index]
    xdata, ydata = _map_to_arrays(me_map)

    popt, pcov = cf(fitfn, xdata, ydata)

    title = index_orbital_map[index]

    print(title)
    print(popt)
    print()

    curve_x = np.linspace(xdata[0], xdata[-1])
    curve_y = np.array(list(map(lambda x: fitfn(x, *popt), curve_x)))
    fits.append((curve_x, curve_y-ydata[0], title))

    f = plt.figure()
    ax = f.add_subplot(111)

    ax.plot(xdata, ydata, '-b')
    ax.plot(curve_x, curve_y, '-r')
    plt.title(title)
    plt.show()

for fit in fits:
    x, y, label = fit
    plt.plot(x, y, label=[q for q in label])
    plt.legend()
plt.show()
