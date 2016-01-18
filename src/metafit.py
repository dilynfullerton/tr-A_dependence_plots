from __future__ import division
from __future__ import print_function

from itertools import combinations

import numpy as np

from scipy.optimize import leastsq
from scipy.optimize import curve_fit
from scipy.stats import linregress

from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib import cm

from constants import *
from fittransforms import *

from ImsrgDataMap import ImsrgDataMap, Exp
from fitting import print_key
from fitting import map_to_arrays


# STATISTICAL ANALYSIS TOOLS
def single_particle_max_r2_value(metafitter, fitfns, e_hw_pairs, **kwargs):
    """Returns the fit function (and its optimized results) that produces the
    largest total r^2 value

    :param metafitter: the metafitter method (e.g.
    single_particle_relative_metafigt)
    :param fitfns: the list of fitfns to test
    :param e_hw_pairs: the (e, hw) pairs to optimize
    :param kwargs: keyword arguments to pass to the metafitter
    :return: best fit function, results
    """
    fn_res_r2_map = dict()
    for fitfn in fitfns:
        res = metafitter(fitfn, e_hw_pairs, **kwargs)
        lg_res = res[1]
        r2 = 0
        length = 0
        for v in lg_res.values():
            r = v.rvalue
            r2 += r ** 2
            length += 1
        r2 = r2 / length
        fn_res_r2_map[fitfn] = (res, r2)
    rank_map = dict()
    result_map = dict()
    for fitfn, i in zip(sorted(fn_res_r2_map.keys(),
                               key=lambda f: -1 * fn_res_r2_map[f][1]),
                        range(len(fn_res_r2_map))):
        res, r2 = fn_res_r2_map[fitfn]
        rank_map[i+1] = (fitfn, r2)
        result_map[fitfn] = res
    return rank_map[1][0], rank_map[1][1], rank_map, result_map


def single_particle_compare_params(metafitter, fitfn, e_hw_pairs,
                                   depth, statfn=np.std,
                                   print_compare_results=False,
                                   **kwargs):
    """Compare parameter results for a given metafitter on a given fitfn using
    combinations of the given e_hw_pairs to the depth given by depth. The
    method of comparison is given by the statistical function statfn, whose
    default is the standard deviation.

    :param metafitter: the meta-fitting method to use (e.g.
    single_particle_relative_metafit)
    :param fitfn: the fit function to use
    :param e_hw_pairs: the set of (e, hw) pairs to look at
    :param depth: the depth of sub-combinations of e_hw_pairs to look at.
    For example, if e_hw_pairs = {(1, 1), (2, 2), (3, 3), (4, 4)} and depth is
    2, all of the length 4, length 3, and length 2 sub-combinations will be
    added to the analysis
    :param statfn: The comparison function to perform on the distribution of
    single-parameter results. Must take a single ndarray object as input and
    return a float output.
    :param print_compare_results: whether to print the results in a neat table
    :param kwargs: keyword arguments to be passed to the metafitter
    :return: a list of (param, result, relative result) 3-tuples
    """
    if depth > len(e_hw_pairs) - 1:
        depth = len(e_hw_pairs) - 1
    params = metafitter(fitfn, e_hw_pairs, **kwargs)[0][0]
    all_params_lists = list([params])
    for length in range(len(e_hw_pairs) - 1, len(e_hw_pairs) - depth - 1, -1):
        for sub_e_hw_pairs in combinations(e_hw_pairs, length):
            mod_params = metafitter(fitfn, sub_e_hw_pairs)[0][0]
            all_params_lists.append(mod_params)
    individual_params_lists = _distributions_from_lol(all_params_lists)
    param_result_list = list()
    for param, param_list in zip(params, individual_params_lists):
        param_array = np.array(param_list)
        result = statfn(param_array)
        rel_result = result / param
        param_result_list.append((param, result, rel_result))
    if print_compare_results is True:
        _printer_for_single_particle_compare_params(param_result_list,
                                                    depth, statfn,
                                                    e_hw_pairs, metafitter,
                                                    fitfn)
    return param_result_list


def _distributions_from_lol(lol):
    sublist_size = len(lol[0])
    distributions_list = list()
    for i in range(sublist_size):
        distributions_list.append(list(map(lambda sl: sl[i], lol)))
    return distributions_list


def _printer_for_single_particle_compare_params(params_result_list,
                                                depth, statfn,
                                                e_hw_pairs, metafitter,
                                                fitfn):
    title_str = ('Depth {d} comparison of {sfn} for {ehw} using meta-fitter '
                 '{mf} and fit function {ffn}'
                 '').format(d=depth,
                            sfn=statfn.__name__,
                            ehw=e_hw_pairs,
                            mf=metafitter.__name__,
                            ffn=fitfn.__name__)
    print(P_TITLE + title_str + '\n' + P_BREAK + P_END)
    temp_str = '{p:>20}\t{std:>20}\t{rel:>20}'
    print(P_HEAD +
          temp_str.format(p='Parameter val',
                          std='Compare result',
                          rel='Rel compare result') +
          P_END)
    for p, std, rel in params_result_list:
        print(temp_str.format(p=p, std=std, rel=rel))


# META-FITTERS
def single_particle_relative_metafit(fitfn, e_hw_pairs, **kwargs):
    return _single_particle_metafit(fitfn, e_hw_pairs,
                                    sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                    code='spr',
                                    **kwargs)


def single_particle_relative_per_nucleon_metafit(fitfn, e_hw_pairs, **kwargs):
    return _single_particle_metafit(fitfn, e_hw_pairs,
                                    sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                    transform=relative_per_nucleon,
                                    code='sprpn',
                                    ylabel='Relative Energy per Nucleon (MeV)',
                                    **kwargs)


def single_particle_relative_log_log_per_nucleon_metafit(fitfn, e_hw_pairs,
                                                         **kwargs):
    return _single_particle_metafit(fitfn, e_hw_pairs,
                                    sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                    transform=relative_log_log_per_nucleon,
                                    code='sprllpn',
                                    xlabel='log(A)',
                                    ylabel='relative log(Energy per Nucleon)',
                                    **kwargs)


def single_particle_relative_flip_metafit(fitfn, e_hw_pairs, **kwargs):
    return _single_particle_metafit(fitfn, e_hw_pairs,
                                    sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                    transform=relative_flip,
                                    code='sprf',
                                    xlabel='Relative Energy (MeV)',
                                    ylabel='A',
                                    **kwargs)


def single_particle_relative_flip_per_nucleon_metafit(fitfn, e_hw_pairs,
                                                      **kwargs):
    return _single_particle_metafit(fitfn, e_hw_pairs,
                                    sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                    transform=relative_flip_per_nucleon,
                                    code='sprfpn',
                                    xlabel='Energy per Nucleon (MeV)',
                                    ylabel='Relative A',
                                    **kwargs)


def single_particle_flip_relative_per_nucleon_metafit(fitfn, e_hw_pairs,
                                                      **kwargs):
    return _single_particle_metafit(fitfn, e_hw_pairs,
                                    sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                    transform=flip_relative_per_nucleon,
                                    code='spfrpn',
                                    xlabel='Relative Energy per Nucleon',
                                    ylabel='A',
                                    **kwargs)


def single_particle_relative_flip_relative_per_nuceon_metafit(fitfn, e_hw_pairs,
                                                              **kwargs):
    return _single_particle_metafit(fitfn, e_hw_pairs,
                                    sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                    transform=relative_flip_relative_per_nucleon,
                                    code='sprfrpn',
                                    xlabel='Relative Energy per Nucleon',
                                    ylabel='Relative A',
                                    **kwargs)


# HELPER FUNCTIONS
def _single_particle_metafit(fitfn, e_hw_pairs, sourcedir, savedir,
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

    plots = list()
    for e, hw in sorted(e_hw_pairs):
        data_maps = all_data_map.map[Exp(e, hw)]
        io_map = data_maps.index_orbital_map
        ime_map = data_maps.index_mass_energy_map()

        if printkey is True:
            print_key(io_map, sortkey,
                      'Index key for e={e} hw={hw}:'.format(e=e, hw=hw))

        # Get list of plots
        for index in sorted(io_map.keys()):
            qnums = io_map[index]
            me_map = ime_map[index]

            x, y = map_to_arrays(me_map)
            plots.append(transform(x, y, [qnums, e, hw, index]))

    # Make an initial parameter guess based on the first plot
    x0, y0, c0 = plots[0]
    param_guess = curve_fit(fitfn, x0, y0)[0]

    # Do the meta-fit
    mf_results = _meta_fit(plots, fitfn, param_guess)
    params = mf_results[0]

    # Test goodness of fits
    lr_results = dict()
    for p in plots:
        x, y, constants = p
        qnums, e, hw, index = constants
        args = list(params)
        args.extend(constants)
        yarr = np.array(y)
        ypred = np.array(list(map(lambda xi: fitfn(xi, *args), x)))
        lr_results[(e, hw, qnums)] = linregress(yarr, ypred)

    # Print results
    if printresults is True:
        print_results(mf_results, lr_results)

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
            x, y, constants = p
            qnums, e, hw, index = constants
            args = list(params)
            args.extend(constants)
            xfit = np.linspace(x[0], x[-1])
            yfit = np.array(list(map(lambda xi: fitfn(xi, *args), xfit)))

            cval = scalarMap.to_rgba(i)
            labelstr = '{e}, {hw}, {i}'.format(e=e, hw=hw, i=index)
            ax.plot(x, y, label=labelstr, color=cval)
            ax.plot(xfit, yfit, '--', label=labelstr+' fit', color=cval)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        title = ('Metafit for single particle energy {tr} data '
                 'using {fn} for (e, hw) = {ehw}'
                 '').format(tr=transform.__name__, fn=fitfn.__name__,
                            ehw=e_hw_pairs)
        plt.title(title)
        plt.legend()
        plt.savefig(savedir + '/meta_{c}-{t}.png'.format(c=code, t=title))
    plt.show()

    return mf_results, lr_results


def print_results(metafit_results, linregress_results):
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
    for e, hw, qnums in sorted(linregress_results.keys()):
        slope, intercept, rvalue, pvalue, stderr = linregress_results[(e, hw,
                                                                       qnums)]
        print(P_HEAD + 'e={e} hw={hw}: {qn}'.format(e=e, hw=hw, qn=qnums) +
              P_END)
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