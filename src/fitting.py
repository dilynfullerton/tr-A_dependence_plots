from __future__ import division
from __future__ import print_function
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit as cf
import numpy as np
from constants import *
from ImsrgDataMap import ImsrgDataMap, Exp

E = 12
HW = 20

SHOW_INDIVIDUAL_FITS = True
COMPARE_RAW_DATA = True
COMPARE_FITS = True
COMPARE_DERIV = True
PRINT_FITTING_PARAMETERS = True


def _map_to_arrays(m):
    """Convert a map of dimensionality 2 into an x and y array"""
    length = len(m)
    x = np.empty(length)
    y = np.empty(length)
    for k, i in zip(sorted(m.keys()), range(length)):
        x[i] = k
        y[i] = m[k]
    return x, y


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


def single_particle_energy_curvefit(fitfn,
                                    show_fits=SHOW_INDIVIDUAL_FITS,
                                    show_data_compare=COMPARE_RAW_DATA,
                                    show_fit_compare=COMPARE_FITS,
                                    show_deriv_compare=COMPARE_DERIV,
                                    verbose=PRINT_FITTING_PARAMETERS):
    all_data_map = ImsrgDataMap(parent_directory=FILES_DIR)
    data_maps = all_data_map.map[Exp(E, HW)]
    index_orbital_map = data_maps.index_orbital_map
    ime_map = data_maps.index_mass_energy_map()

    data_plots = list()
    deriv_plots = list()
    fits_plots = list()
    orbital_fit_map = dict()
    for index in sorted(ime_map.keys(), key=lambda k: index_orbital_map[k].j):
        title = index_orbital_map[index]

        me_map = ime_map[index]
        xdata, ydata = _map_to_arrays(me_map)
        data_plots.append((xdata, ydata, title))

        xderiv = np.array(xdata)[:-1]
        yderiv = np.empty(shape=len(xderiv))
        for i in range(len(xderiv)):
            yderiv[i] = ydata[i+1] - ydata[i]
        deriv_plots.append((xderiv, yderiv, title))


        try:
            popt, pcov = cf(fitfn, xdata, ydata)
            orbital_fit_map[index_orbital_map[index]] = popt
        except RuntimeError:
            print('RuntimeError for orbital {o}'.format(o=title))
            continue

        if verbose:
            print(title)
            print(popt)
            print()

        curve_x = np.linspace(xdata[0], xdata[-1])
        curve_y = np.array(list(map(lambda x: fitfn(x, *popt), curve_x)))
        fits_plots.append((curve_x, curve_y, title))

        if show_fits:
            f = plt.figure()
            ax = f.add_subplot(111)
            ax.plot(xdata, ydata, '-b')
            ax.plot(curve_x, curve_y, '-r')
            plt.title(title)
            plt.show()

    if show_data_compare:
        for dat in data_plots:
            x, y, label = dat
            y = y - y[0]
            plt.plot(x, y, '-', label=tuple(label))
        plt.show()

    if show_fit_compare:
        for fit in fits_plots:
            x, y, label = fit
            y = y - y[0]
            plt.plot(x, y, '-', label=tuple(label))
        plt.show()

    if show_deriv_compare:
        for der in deriv_plots:
            x, y, label = der
            plt.plot(x, y, '-', label=tuple(label))
        plt.show()

    return orbital_fit_map

single_particle_energy_curvefit(fitfn=polyfit4)
