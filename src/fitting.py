from __future__ import division
from __future__ import print_function

import numpy as np
from matplotlib import pyplot as plt
from openpyxl import Workbook, load_workbook
from scipy.optimize import curve_fit as cf

from ImsrgDataMap import ImsrgDataMap, Exp
from constants import *

E = 12
HW = 20

SHOW_INDIVIDUAL_FITS = True
COMPARE_RAW_DATA = True
COMPARE_FITS = True
COMPARE_PER_NUC_DATA = True
COMPARE_DERIV = True
COMPARE_LOG_LOG = True
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


def single_particle_energy_curvefit(fitfn, e=E, hw=HW,
                                    sourcedir=FILES_DIR,
                                    savedir=PLOTS_DIR,
                                    show_fits=SHOW_INDIVIDUAL_FITS,
                                    show_data_compare=COMPARE_RAW_DATA,
                                    show_fit_compare=COMPARE_FITS,
                                    show_data_compare2=COMPARE_PER_NUC_DATA,
                                    show_deriv_compare=COMPARE_DERIV,
                                    show_log_log_compare=COMPARE_LOG_LOG,
                                    verbose=PRINT_FITTING_PARAMETERS):
    """Perform a curve fit for each of the single particle orbitals, for
    the files in the given directory with the given e and hw values


    :param fitfn: Function to use for curve-fitting. Must be of the form
    f(x, a1, a2, a3, ... aN)
    :param e: the energy level
    :param hw: the hw frequency
    :param sourcedir: the parent directory containing related files
    :param show_fits: whether to show the individual orbital fits
    :param show_data_compare: whether to show a comparison between the
    single particle orbital energy dependencies on mass
    :param show_fit_compare: whether to show a comparison between the
    single particle fitted energy dependencies on mass
    :param show_deriv_compare: whether to show a comparison between the
    single particle first derivatives
    :param show_log_log_compare: whether to show a comparison between the log-log
    plots of the data
    :param verbose: whether to output the fitted data
    :return: a map from the QuantumNumbers of each orbital to its fit
    parameters
    """
    all_data_map = ImsrgDataMap(parent_directory=FILES_DIR)
    data_maps = all_data_map.map[Exp(E, HW)]
    index_orbital_map = data_maps.index_orbital_map
    ime_map = data_maps.index_mass_energy_map()

    data_plots = list()
    deriv_plots = list()
    fits_plots = list()
    orbital_fit_map = dict()
    for index in sorted(ime_map.keys(), key=lambda k: index_orbital_map[k].j):
        qnums = index_orbital_map[index]

        me_map = ime_map[index]
        xdata, ydata = _map_to_arrays(me_map)
        data_plots.append((xdata, ydata, qnums))

        xderiv = np.array(xdata)[:-1]
        yderiv = np.empty(shape=len(xderiv))
        for i in range(len(xderiv)):
            yderiv[i] = ydata[i+1] - ydata[i]
        deriv_plots.append((xderiv, yderiv, qnums))

        try:
            popt, pcov = cf(fitfn, xdata, ydata)
            orbital_fit_map[index_orbital_map[index]] = popt
        except RuntimeError:
            print('RuntimeError for orbital {o}'.format(o=qnums))
            continue

        if verbose:
            print(qnums)
            print(popt)
            print()

        curve_x = np.linspace(xdata[0], xdata[-1])
        curve_y = np.array(list(map(lambda x: fitfn(x, *popt), curve_x)))
        fits_plots.append((curve_x, curve_y, qnums))

        if show_fits:
            f = plt.figure()
            ax = f.add_subplot(111)
            ax.plot(xdata, ydata, '-b')
            ax.plot(curve_x, curve_y, '-r')
            title = ('Single particle energy fit using {fn} for '
                     'orbital {o} '
                     'with e={e} hw={hw}').format(fn=fitfn.__name__,
                                                  o=index,
                                                  e=e, hw=hw)
            plt.title(title)
            plt.xlabel('A')
            plt.ylabel('Energy (MeV)')
            plt.savefig(savedir + '/' + title + '.png')
            plt.show()

    if show_data_compare:
        for dat in data_plots:
            x, y, label = dat
            y = y - y[0]
            plt.plot(x, y, '-', label=tuple(label))
            title = ('Single particle energies: '
                     'Comparison of relative energy-mass dependence '
                     'with e={e} hw={hw}').format(e=e, hw=hw)
            plt.title(title)
            plt.xlabel('A')
            plt.ylabel('Relative energy (MeV)')
            plt.savefig(savedir + '/' + title + '.png')
        plt.show()

    if show_fit_compare:
        for fit in fits_plots:
            x, y, label = fit
            y = y - y[0]
            plt.plot(x, y, '-', label=tuple(label))
            title = ('Single particle energies: '
                     'Comparison of fits using {fit} with '
                     'e={e} hw={hw}').format(fit=fitfn.__name__,
                                             e=e, hw=hw)
            plt.title(title)
            plt.xlabel('A')
            plt.ylabel('Relative fit energy (MeV)')
            plt.savefig(savedir + '/' + title + '.png')
        plt.show()

    if show_data_compare2:
        for dat in data_plots:
            x, y, label = dat
            for i in range(len(y)):
                y[i] = y[i] / x[i]
            #y = y - y[0]
            plt.plot(x, y, label=tuple(label))
            title = ('Single particle energies: '
                     'Comparison of relative energy per nucleon '
                     'dependence on mass with '
                     'e={e} hw={hw}').format(e=e, hw=hw)
            plt.title(title)
            plt.xlabel('A')
            plt.ylabel('Energy per nucleon (MeV)')
            plt.savefig(savedir + '/' + title + '.png')
        plt.show()

    if show_log_log_compare:
        for dat in data_plots:
            x, y, label = dat
            plt.plot(np.log(abs(x)), np.log(abs(y)), label=tuple(label))
            title = ('Single particle energies: '
                     'Comparison of log-logs with '
                     'e={e} hw={hw}').format(e=e, hw=hw)
            plt.title(title)
            plt.xlabel('log(A)')
            plt.ylabel('log(energy)')
            plt.savefig(savedir + '/' + title + '.png')
        plt.show()

    if show_deriv_compare:
        for der in deriv_plots:
            x, y, label = der
            plt.plot(x, y, '-', label=tuple(label))
            title = ('Single particle energies: '
                     'Comparison of rate of change of mass-energy dependence '
                     'with e={e} hw={hw}').format(e=e, hw=hw)
            plt.title(title)
            plt.xlabel('A')
            plt.ylabel('dE/dA (MeV / nucleon)')
            plt.savefig(savedir + '/' + title + '.png')
        plt.show()

    return orbital_fit_map


def print_single_particle_energy_data_to_excel(e, hw, datadir, savepath,
                                               startrow=2):
    all_data_map = ImsrgDataMap(parent_directory=FILES_DIR)
    data_maps = all_data_map.map[Exp(E, HW)]
    index_orbital_map = data_maps.index_orbital_map
    ime_map = data_maps.index_mass_energy_map()

    try:
        wb = load_workbook(savepath)
    except IOError:
        wb = Workbook()

    ws = wb.active
    ws.title = 'e={e} hw={hw}'.format(e=e, hw=hw)

    row = startrow
    col = 1

    ws.cell(row=row, column=col).value = 'KEY'
    row += 1

    for i, s in zip(range(5), ['Index', 'n', 'l', 'j', 'tz']):
        ws.cell(row=row, column=col+i).value = s
    row += 1

    for oindex in sorted(index_orbital_map.keys()):
        ws.cell(row=row, column=col).value = int(oindex)
        qnums = index_orbital_map[oindex]
        for i, qn in zip(range(1, 5), qnums):
            ws.cell(row=row, column=col+i).value = qn
        row += 1
    row += 1

    ws.cell(row=row, column=col).value = 'DATA'
    row += 1

    ws.cell(row=row, column=col).value = 'Index'
    ws.cell(row=row, column=col+1).value = 'A'
    ws.cell(row=row, column=col+2).value = 'energy (MeV)'
    row += 1

    for oindex in sorted(ime_map.keys()):
        me_map = ime_map[oindex]

        for m in me_map.keys():
            ws.cell(row=row, column=col).value = int(oindex)
            ws.cell(row=row, column=col+1).value = int(m)
            ws.cell(row=row, column=col+2).value = me_map[m]
            row += 1

    wb.save(savepath)

# single_particle_energy_curvefit(fitfn=polyfit4)
'''
print_single_particle_energy_data_to_excel(
        12, 20,
        datadir=FILES_DIR,
        savepath='../fitting/e12_hw20.xlsx')
'''
