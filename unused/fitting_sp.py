"""Simple curve-fitter. I don't know if this really has much use now that the
meta-fitter is developed
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from matplotlib import pyplot as plt
from scipy.optimize import curve_fit as cf
from scipy.stats import linregress as lg

from deprecated.int import ExpInt
from metafit import print_io_key
from plotting import map_to_arrays
from transforms import *

E = 12
HW = 20

SHOW_INDIVIDUAL_FITS = True
COMPARE_RAW_DATA = True
COMPARE_FITS = True
COMPARE_PER_NUC_DATA = True
COMPARE_DERIV = True
COMPARE_LOG_LOG = True
PRINT_FITTING_PARAMETERS = True


def single_particle_deriv_curvefit(fitfn, e=E, hw=HW, **kwargs):
    return _single_particle_curvefit(fitfn, e, hw,
                                     code='spd', transform=derivative,
                                     ylabel='dE/dA',
                                     **kwargs)


def single_particle_log_log_curvefit(fitfn, e=E, hw=HW, **kwargs):
    return _single_particle_curvefit(fitfn, e, hw,
                                     code='spll', transform=log_log,
                                     xlabel='log(A)',
                                     ylabel='log(Energy)',
                                     **kwargs)


def single_particle_identity_curvefit(fitfn, e=E, hw=HW, **kwargs):
    return _single_particle_curvefit(fitfn, e, hw,
                                     code='spi', transform=identity,
                                     **kwargs)


# def single_particle_per_nucleon_curvefit(fitfn, e=E, hw=HW, **kwargs):
#     return _single_particle_curvefit(fitfn, e, hw,
#                                      code='sppn', transform=per_nucleon,
#                                      ylabel='Energy per nucleon (MeV)',
#                                      **kwargs)


# def single_particle_per_nucleon_power_curvefit(fitfn, e=E, hw=HW,
#                                                xpow=1, ypow=1,
#                                                **kwargs):
#     if xpow != 1:
#         xlabel = '[A]^{xp}'.format(xp=xpow)
#     else:
#         xlabel = 'A'
#     if ypow != 1:
#         ylabel = '[Energy per nucleon]^{yp} (MeV)^{yp}'.format(yp=ypow)
#     else:
#         ylabel = 'Energy per nucleon (MeV)'
#     return _single_particle_curvefit(
#             fitfn, e, hw, code='sppnp',
#             transform=lambda x, y: power(xpow, ypow)(*per_nucleon(x, y)),
#             xlabel=xlabel, ylabel=ylabel,
#             **kwargs)


def single_particle_power_curvefit(fitfn, e=E, hw=HW, xpow=1, ypow=1, **kwargs):
    if xpow != 1:
        xlabel = '[A]^{xp}'.format(xp=xpow)
    else:
        xlabel = 'A'
    if ypow != 1:
        ylabel = '[Energy per nucleon]^{yp} (MeV)^{yp}'.format(yp=ypow)
    else:
        ylabel = 'Energy per nucleon (MeV)'
    return _single_particle_curvefit(fitfn, e, hw,
                                     code='spp', transform=power(xpow, ypow),
                                     xlabel=xlabel, ylabel=ylabel,
                                     **kwargs)


# def _single_particle_curvefit(fitfn, e=E, hw=HW,
#                               sourcedir=DIR_FILES,
#                               savedir=DIR_PLOTS,
#                               show_fits=False,
#                               show_data_compare=False,
#                               show_rel_data_compare=False,
#                               legend_data_compare=True,
#                               show_fit_compare=False,
#                               show_rel_fit_compare=False,
#                               legend_rel_data_compare=True,
#                               transform=identity,
#                               printkey=False,
#                               printresults=False,
#                               code='',
#                               xlabel='A',
#                               ylabel='Energy (MeV)',
#                               sortkey=lambda k: k):
#     """Create curvefits for each of the single-particle orbits individually
#
#     :param fitfn: The function of the form f(x, *params) to fit to, where the
#     params are definite in number (as they are being optimized)
#     :param e: the e value
#     :param hw: the hw value
#     :param sourcedir: the main files directory used for initializing an
#     ImsrgDataMaps object
#     :param savedir: the directory in which to save plots
#     :param show_fits: whether or not to show individual fits
#     :param show_data_compare: whether or not to show a data comparison plot
#     :param show_rel_data_compare: whether or not to show a relative data
#     comparison plot
#     :param legend_data_compare: whether or not to show a legend on the data
#      comparison plots
#     :param show_fit_compare: whether or not to show a fits comparison plots
#     :param show_rel_fit_compare: whether to show a relative fits comparison plot
#     :param legend_rel_data_compare: whether to show a legend on the fits
#     comparison plots
#     :param transform: the transform to be applied to the data before fitting
#     :param printkey: whether to print a key (index -> quantum numbers)
#     :param printresults: whether to print fitting parameters and statistical
#     results
#     :param code: a code to be prepended to the file names of the plots
#     :param xlabel: the x label for the plots
#     :param ylabel: the y label for the plots
#     :param sortkey: the key by which to sort indices (order the fits are
#     performed)
#     :return: a map from (quantum numbers) --> (fit parameters, covariance array,
#     slope, intercept, rvalue, pvalue, stderr)
#     """
#     all_data_map = ImsrgDataMapInt(parent_directory=sourcedir)
#     data_maps = all_data_map.map[ExpInt(e, hw)]
#     io_map = data_maps.index_orbital_map
#     ime_map = data_maps.index_mass_energy_map()
#
#     individual_plots = dict()
#     compare_data_plots = list()
#     compare_fit_plots = list()
#     orbital_fit_map = dict()
#
#     if printkey:
#         print_io_key(io_map, sortkey)
#
#     for index in sorted(ime_map.keys(), key=sortkey):
#         qnums = io_map[index]
#         me_map = ime_map[index]
#
#         xdata, ydata = map_to_arrays(me_map)
#         x, y = transform(xdata, ydata, qnums)[0:2]
#         compare_data_plots.append((x, y, index))
#
#         popt, pcov = cf(fitfn, x, y)
#         ypred = np.array(list(map(lambda xi: fitfn(xi, *popt), x)))
#         slope, intercept, rvalue, pvalue, stderr = lg(y, ypred)
#         orbital_fit_map[qnums] = (popt, pcov, slope, intercept, rvalue, pvalue,
#                                   stderr)
#
#         if printresults:
#             print(str(index) + ': ' + str(qnums))
#             print('Fitting parameters:')
#             print(str(popt))
#             print('Covariance:')
#             print(str(pcov))
#             print('Correlation:')
#             # print('  slope =     ' + str(slope))
#             # print('  intercept = ' + str(intercept))
#             print('  r-sqr =     ' + str(rvalue ** 2))
#             print('  p-val =     ' + str(pvalue))
#             print('  stderr =    ' + str(stderr))
#             print()
#
#         fitx = np.linspace(x[0], x[-1])
#         fity = np.array(list(map(lambda xi: fitfn(xi, *popt), fitx)))
#         compare_fit_plots.append((fitx, fity, index))
#
#         individual_plots[index] = (x, y, fitx, fity)
#
#     # INDIVIDUAL FIT PLOT
#     if show_fits:
#         for index in sorted(individual_plots.keys(), key=sortkey):
#             f = plt.figure()
#             ax = f.add_subplot(111)
#             ax.plot(xdata, ydata, '-b')
#             ax.plot(fitx, fity, '-r')
#             plt.plot(xdata, ydata, '-b')
#             plt.plot(fitx, fity, '-r')
#             title = ('{c}-Single particle energy {tr} fit using {fn} for '
#                      'orbital {o} with e={e} '
#                      'hw={hw}').format(c=code,
#                                        tr=transform.__name__,
#                                        fn=fitfn.__name__,
#                                        o=index,
#                                        e=e, hw=hw)
#             plt.title(title)
#             plt.xlabel(xlabel)
#             plt.ylabel(ylabel)
#             plt.savefig(savedir + '/' + title + '.png')
#
#     # DATA COMPARISON PLOTS
#     title_temp = ('{c}-Comparison of {rel}{sp1}single particle energy {tr} '
#                   '{dof}{sp2}{us}{sp2}{fn} with e={e} hw={hw}'
#                   '').format(c=code,
#                              tr=transform.__name__,
#                              e=e, hw=hw,
#                              rel='{rel}',
#                              sp1='{sp1}',
#                              fn='{fn}',
#                              sp2='{sp2}',
#                              dof='{dof}',
#                              us='{us}')
#
#     if show_data_compare:
#         fdat = plt.figure()
#         axdat = fdat.add_subplot(111)
#         for dat in compare_data_plots:
#             x, y, label = dat
#             axdat.plot(x, y, '-', label=label)
#             # plt.plot(x, y, '-', label=label)
#         title = title_temp.format(rel='', sp1='', fn='', sp2='', dof='data',
#                                   us='')
#         _do_plot(title, xlabel, ylabel,
#                  saveloc=savedir + '/' + title + '.png',
#                  showlegend=legend_data_compare)
#
#     if show_rel_data_compare:
#         frdat = plt.figure()
#         axrdat = frdat.add_subplot(111)
#         for rdat in compare_data_plots:
#             x, y, label = rdat
#             y = y - y[0]
#             axrdat.plot(x, y, '-', label=label)
#             # plt.plot(x, y, '-', label=label)
#         title = title_temp.format(rel='relative', sp1=' ', fn='',
#                                   sp2='', dof='data', us='')
#         _do_plot(title, xlabel, 'relative ' + ylabel,
#                  saveloc=savedir + '/' + title + '.png',
#                  showlegend=legend_rel_data_compare)
#
#     if show_fit_compare:
#         ffit = plt.figure()
#         axfit = ffit.add_subplot(111)
#         for fit in compare_fit_plots:
#             x, y, label = fit
#             axfit.plot(x, y, '-', label=label)
#             # plt.plot(x, y, '-', label=label)
#         title = title_temp.format(rel='', sp1='', fn=fitfn.__name__,
#                                   sp2=' ', dof='fit', us='using')
#         _do_plot(title, xlabel, ylabel + ' fit',
#                  saveloc=savedir + '/' + title + '.png',
#                  showlegend=legend_data_compare)
#
#     if show_rel_fit_compare:
#         frfit = plt.figure()
#         axrfit = frfit.add_subplot(111)
#         for rfit in compare_fit_plots:
#             x, y, label = rfit
#             y = y - y[0]
#             axrfit.plot(x, y, '-', label=label)
#             # plt.plot(x, y, '-', label=label)
#         title = title_temp.format(rel='relative', sp1=' ', fn=fitfn.__name__,
#                                   sp2=' ', dof='fit', us='using')
#         _do_plot(title, xlabel, 'relative ' + ylabel + ' fit',
#                  saveloc=savedir + '/' + title + '.png',
#                  showlegend=legend_rel_data_compare)
#
#     plt.show()
#
#     return orbital_fit_map
#

def _do_plot(title, xlabel, ylabel, saveloc, showlegend):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if showlegend:
        plt.legend()
    plt.savefig(saveloc)
