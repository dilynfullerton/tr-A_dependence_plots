from __future__ import division
from __future__ import print_function

import numpy as np
from scipy.optimize import leastsq
from scipy.optimize import curve_fit
from scipy.stats import linregress
from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib import cm

from constants import *
from fittransforms import relative
from ImsrgDataMap import ImsrgDataMap, Exp
from fitting import print_key
from fitting import map_to_arrays


def single_particle_relative_metafit(fitfn, e, hw, **kwargs):
    return _single_particle_metafit(fitfn, e, hw,
                                    sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                    code='spr',
                                    **kwargs)


def _single_particle_metafit(fitfn, e, hw, sourcedir, savedir,
                             transform=relative,
                             printkey=False,
                             printresults=False,
                             showplot=False,
                             sortkey=lambda k: k,
                             code='',
                             xlabel='A',
                             ylabel='Relative Energy (MeV)',
                             cmap='brg'):
    """A meta-fit for all the orbitals with a given e and hw, based on the
    given fit function

    :param fitfn: The fit function to use for fitting of the form
    f(x, a0, a1, ..., aN, *constants) -> y, where x, y, and a0...aN are floats
    :param e: e value
    :param hw: hw frequency value
    :param sourcedir: main files directory to use for initializing the
    ImsrgDataMaps
    :param savedir: the directory in which to save plots
    :param transform: A transformation to apply to the data before fitting,
    t(xarr, yarr, *args) -> (newxarr, newyarr, *args), where xarr, yarr,
    newxarr, and newyarr are arrays
    :param printkey: whether to print the index -> orbital key
    :param printresults: whether to print fit results
    :param showplot: whether to show the fit plot
    :param sortkey: key for ordering items
    :param code: code name to precede file name in saving of plot
    :param xlabel: x label for plot
    :param ylabel: y label for plot
    :param cmap: colormap string to use for plotting
    :return:
    """
    # Get index->orbital and index->mass->energy maps
    all_data_map = ImsrgDataMap(parent_directory=sourcedir)
    data_maps = all_data_map.map[Exp(e, hw)]
    io_map = data_maps.index_orbital_map
    ime_map = data_maps.index_mass_energy_map()

    if printkey is True:
        print_key(io_map, sortkey)

    # Get list of plots
    plots = list()
    for index in sorted(io_map.keys()):
        qnums = io_map[index]
        me_map = ime_map[index]

        x, y = map_to_arrays(me_map)
        plots.append(transform(x, y, [qnums, index]))

    # Make an initial parameter guess based on the first plot
    x0, y0, c0 = plots[0]
    param_guess = curve_fit(fitfn, x0, y0)[0]

    # Do the meta-fit
    mf_results = _meta_fit(plots, fitfn, param_guess)
    params = mf_results[0]

    # Test goodness of fits
    lr_results = dict()
    for p in plots:
        x_p, y_p, qn_p, i_p = p[0], p[1], p[2][0], p[2][1]
        args = list(params)
        args.append(qn_p)
        yarr = np.array(y_p)
        ypred = np.array(list(map(lambda xi: fitfn(xi, *args), x_p)))
        lr_results[qn_p] = linregress(yarr, ypred)

    # Print results
    if printresults is True:
        _print_results(mf_results, lr_results)

    # Plot results
    if showplot is True:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # Make color map
        cmap = plt.get_cmap(cmap)
        cNorm = colors.Normalize(vmin=0, vmax=len(plots) - 1)
        scalarMap = cm.ScalarMappable(norm=cNorm, cmap=cmap)
        # Do plots
        for p, i in zip(plots, range(len(plots))):
            x, y, qn, index = p[0], p[1], p[2][0], p[2][1]
            args = list(params)
            args.append(qn)
            xfit = np.linspace(x[0], x[-1])
            yfit = np.array(list(map(lambda xi: fitfn(xi, *args), xfit)))

            cval = scalarMap.to_rgba(i)
            ax.plot(x, y, label=index, color=cval)
            ax.plot(xfit, yfit, '--', label=str(index)+' fit', color=cval)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            title = ('Metafit for single particle energy {tr} data '
                     'using {fn} with e={e} hw={hw}'
                     '').format(tr=transform.__name__,
                                fn=fitfn.__name__, e=e, hw=hw)
            plt.title(title)
            plt.legend()
            plt.savefig(savedir + '/meta_{c}-{t}.png'.format(c=code, t=title))
    plt.show()


def _print_results(metafit_results, linregress_results):
    params, cov, info, msg, ier = metafit_results
    print('\n' + P_TITLE + 'Meta-fit results:\n' + '-' * 80 + P_END)
    print(P_SUB + 'PARAMS =' + P_END)
    print('{}'.format(params))
    print(P_SUB + 'COV =' + P_END)
    print('{}'.format(cov))
    print(P_SUB + 'INFO =' + P_END)
    for k in info.keys():
        print('{k}:'.format(k=k))
        print('{v}'.format(v=info[k]))
    print(P_SUB + 'MESSAGE =' + P_END)
    print('{}'.format(msg))
    print(P_SUB + 'IER =' + P_END)
    print('{}'.format(ier))

    print('\n' + P_TITLE + 'Line regression results:\n' + '-' * 80 + P_END)
    for qnums in linregress_results.keys():
        slope, intercept, rvalue, pvalue, stderr = linregress_results[qnums]
        print(P_HEAD + str(qnums) + P_END)
        print(P_SUB + 'SLOPE = ' + P_END)
        print('  ' + str(slope))
        print(P_SUB + 'INTERCEPT = ' + P_END)
        print('  ' + str(intercept))
        print(P_SUB + 'R = ' + P_END)
        print('  ' + str(rvalue))
        print(P_SUB + 'P = ' + P_END)
        print('  ' + str(pvalue))
        print(P_SUB + 'STDERR = ' + P_END)
        print('  ' + str(stderr))
        print()


    # slope, intercept, rvalue, pvalue, stderr = linregress_results


def _meta_fit(plots, fitfn, params_guess, **lsqkwargs):
    """Perform a least squares fit using fitfn for multiple plots

    :param plots: A list of the 3-tuples each with (x, y, const), where x is an
    array of length L, y is an array of length L, and const is a list of
    constants that are unique to the plot.
    :param fitfn: A function of the form f(x, a, b, ...n, *const) -> y, where
    x is float, const is list, a to n are float parameters, and y is
    a float.
    :param params_guess: An initial guess of the fit parameters. The length of
    this list should be the same size as the number of arguments in fitfn - 1
    :return: output of the leastsq function, i.e. (final_params, covariance_arr,
    infodict, message, integer_flag)
    """
    if len(params_guess) != fitfn.__code__.co_argcount - 1:
        raise FunctionDoesNotMatchParameterGuessException
    combined_x = list()
    combined_y = list()
    constants_lists = list()
    for p in plots:
        x, y, constants = p
        combined_x.append(x)
        combined_y.append(y)
        constants_lists.append(constants)
    return leastsq(func=_mls, x0=params_guess,
                   args=(fitfn, combined_x, combined_y, constants_lists),
                   full_output=True,
                   **lsqkwargs)


def _mls(params, fitfn, lox, loy, const_lists):
    """Meta least squares function to be minimized.

    :param params: the parameters to give to the fit function
    :param fitfn: the fit function, which is of the form
    f(x, a, b, ..., n, *const) -> y, where x is a float, a...n are parameters
    to vary, const is a list of constants, and y is a float.
    :param lox: x array of values
    :param loy: y array of values
    :param const_lists: list of constants associated with each
    :return: The difference between the flattened loy array and the flattened
    yfit array
    """
    yfit = list()
    for x, cl in zip(lox, const_lists):
        args = list(params)
        args.extend(cl)
        yfit.extend(list(map(lambda xi: fitfn(xi, *args), x)))
    yflat = [item for y in loy for item in y]
    return np.array(yflat) - np.array(yfit)


class FunctionDoesNotMatchParameterGuessException(Exception):
    pass
'''
from fitfns import polyfit1
_single_particle_metafit(polyfit1, 12, 20, '../files', '../plots',
                         printresults=True,
                         showplot=True)
'''
'''
from fitfns import polyfit1 as f
from matplotlib import pyplot as plt
x1 = [1.0, 2.0, 3.0]
y1 = [2.0, 3.0, 4.0]
x2 = [1.0, 2.0, 3.0, 4.0]
y2 = [1.0, 4.0, 9.0, 16.0]
x3 = [1.0, 2.0, 3.0, 4.0, 5.0]
y3 = [2.0, 4.0, 8.0, 16.0, 32.0]
plots = [(x1, y1, []), (x2, y2, []), (x3, y3, [])]
pg = [1.0, 1.0]

A = _meta_fit(plots, f, pg)[0]

x = np.linspace(1, 5)
y = np.array(list(map(lambda xi: f(xi, *A), x)))

#plt.plot(x, y)
print(A)
'''