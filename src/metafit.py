"""Primary algorithms for fitting onto multiple single particle or
multiparticle plots simultaneously based on universal and specific parameters
for each plot
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from math import ceil

from matplotlib import cm
from matplotlib import colors
from matplotlib import pyplot as plt
from scipy.optimize import leastsq
from scipy.stats import linregress

from FitFunction import FitFunction
from ImsrgDataMap import ImsrgDataMap, Exp
from constants import *
from fit_transforms import *
from spfitting import map_to_arrays
from spfitting import print_io_key


def _set_const(k, identifier, io_map, me_map, mzbt_map, other_constants):
    e, hw, base, rp = identifier
    x, y = map_to_arrays(me_map)
    x0 = x[0]
    y0 = y[0]
    zbt_arr = map_to_arrays(mzbt_map)[1]
    zbt0 = zbt_arr[0]
    const_list = [None, e, hw, k, zbt_arr, y0, zbt0, rp, x0, base, identifier]
    const_dict = {'e': e,
                  'hw': hw,
                  'rp': rp,
                  'zbt_arr': zbt_arr,
                  'x0': x0,
                  'y0': y0,
                  'zbt0': zbt0,
                  'io_map': io_map,
                  'base': base,
                  'exp': identifier,
                  'others': other_constants}
    return x, y, const_list, const_dict


# noinspection PyUnusedLocal
def _single_particle_plot(k, identifier, io_map, me_map, mzbt_map, others,
                          *args):
    x, y, const_list, const_dict = _set_const(k, identifier, io_map, me_map,
                                              mzbt_map, others)
    qnums = io_map[k]
    const_list[0] = qnums
    const_dict['index'] = k
    const_dict['qnums'] = qnums
    # noinspection PyProtectedMember
    const_dict = dict(const_dict.items() + dict(qnums._asdict()).items())
    return x, y, const_list, const_dict


# noinspection PyUnusedLocal
def _multi_particle_plot(k, identifier, io_map, me_map, mzbt_map, others,
                         *args):
    x, y, const_list, const_dict = _set_const(k, identifier, io_map, me_map,
                                              mzbt_map, others)
    const_dict['interaction'] = k
    # noinspection PyProtectedMember
    const_dict = dict(const_dict.items() + dict(k._asdict()).items())
    return x, y, const_list, const_dict


def _printer_for_single_particle_metafit(metafit_results, linregress_results,
                                         print_mf_results=True,
                                         print_lr_results=True,
                                         full_output=False,
                                         header=''):
    if print_mf_results or print_lr_results:
        print('\n' + P_TITLE + header + '\n' + '=' * 80 + P_END)
    if print_mf_results:
        if full_output:
            params, cov, info, msg, ier = metafit_results
        else:
            params, cov = metafit_results[0:2]
        print('\n' + P_TITLE + 'META-FIT RESULTS:\n' +
              '-' * 80 + P_END)
        print(P_SUB + 'PARAMS =' + P_END)
        print('{}'.format(params))
        print(P_SUB + 'COV =' + P_END)
        print('{}'.format(cov))
        if full_output:
            print(P_SUB + 'INFO =' + P_END)
            for k in info.keys():
                print('{k}:'.format(k=k))
                print('{v}'.format(v=info[k]))
            print(P_SUB + 'MESSAGE =' + P_END)
            print('{}'.format(msg))
            print(P_SUB + 'IER =' + P_END)
            print('{}'.format(ier))

    if print_lr_results:
        print('\n' + P_TITLE + 'LINE REGRESSION RESULTS:\n' +
              '-' * 80 + P_END)
        for exp, qnums in sorted(linregress_results.keys()):
            slope, intercept, rvalue, pvalue, stderr = (
                linregress_results[(exp, qnums)])
        print(P_HEAD + '{exp}: {qn}'.format(exp=exp, qn=qnums) + P_END)
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


def _printer_for_multiparticle_metafit(metafit_results, linregress_results,
                                       print_mf_results=True,
                                       print_lr_results=True,
                                       full_output=False,
                                       header=''):
    return _printer_for_single_particle_metafit(metafit_results,
                                                linregress_results,
                                                print_mf_results,
                                                print_lr_results,
                                                full_output,
                                                header)


def single_particle_metafit(fitfn, e_hw_pairs, sourcedir, savedir,
                            transform=relative_y,
                            super_transform_pre=None,
                            super_transform_post=None,
                            imsrg_data_map=None,
                            std_io_map=STANDARD_IO_MAP,
                            print_key=False,
                            print_results=False,
                            print_mf_results=True,
                            print_lr_results=True,
                            show_plot=False,
                            show_fit=True,
                            show_legend=True,
                            full_output=False,
                            mf_name='single_particle_metafit',
                            code='',
                            title=('Metafit for single particle energy'
                                   ' {tr} data using {fn} for {ehw}'),
                            label='{e}, {hw}, {b}, {i}',
                            idx='qnums',
                            xlabel='A',
                            ylabel='Relative Energy (MeV)',
                            data_line_style='-',
                            fit_line_style='--',
                            cmap=PLOT_CMAP,
                            max_legend_cols=LEGEND_MAX_COLS,
                            max_legend_space=LEGEND_MAX_SPACE,
                            max_legend_fontsize=LEGEND_MAX_FONTSIZE,
                            legend_total_fontsize=LEGEND_TOTAL_FONTSIZE,
                            legend_rows_per_col=LEGEND_ROWS_PER_COL,
                            legend_space_scale=LEGEND_SPACE_SCALE,
                            savename='meta_{c}-{t}',
                            _plot_sort_key=lambda p: p[3]['qnums'],
                            _get_data=lambda dm: dm.index_mass_energy_map(),
                            _get_plot=_single_particle_plot,
                            _printer=_printer_for_single_particle_metafit):
    """A meta-fit for all the orbitals with a given e, hw, and rp, based on the
    given fit function

    :param print_lr_results:
    :param print_mf_results:
    :param fitfn: The FitFunction object to use for fitting. Alternatively,
    may be of the form in fitfns.py, although this is deprecated.
    :param e_hw_pairs: A list of tuples of (e, hw [, rp]), which fully specify
    the data set(s) to use. If rp is not included, it is assumed to be None.
    :param sourcedir: The main files directory to use for initializing the
    ImsrgDataMaps
    :param savedir: The directory in which to save plots
    :param transform: (Optional) A transformation to apply to the data before
    fitting,
        t(xarr, yarr, *args) -> (newxarr, newyarr, *args),
    where xarr, yarr, newxarr, and newyarr are arrays.
    :param super_transform_pre: (Optional) A transform to transform all of the
    plots together prior to the individual transform. Default is None.
    :param super_transform_post: (Optional) A transform to transform all of the
    plots together after the individual transform. Default is None.
    :param imsrg_data_map: (Optional) If included, will not retrieve data map
    from sourcedir and will instead take the given data map
    :param std_io_map: A standard index -> orbital mapping scheme to use for
    generating the data representations
    :param print_key: (Optional) Whether to print the index -> orbital key.
    Default is False.
    :param print_results: (Optional) Whether to print fit results. Default is
    False.
    :param show_plot: (Optional) Whether to show the data plot. Default False.
    :param show_fit: (Optional) Whether to show the fit plot when show_plot is
    True. Default True.
    :param show_legend: (Optional) Whether to show the legend when show_plot is
    True. Default True.
    :param full_output: (Optional) Whether the returned results should be the
    full output given by the leastsq function. Default False.
    :param code: (Optional) An identifier for the specific implementation of
    this function, to distinguish saved files.
    :param title: (Optional) The title by which to name the plot. Use the
    following keys to include information:
        {tr}: name of the transformation performed
        {fn}: name of the fit function applied
        {ehw}: (e, hw, rp) identifier of the data
    :param label: (Optional) The labeling scheme for the plot legend. Use the
    following keys to include information:
        {e}: emax
        {hw}: h-bar omega frequency
        {rp}: proton radius
        {i}: index
    :param idx: the key to use to get the index (for the label) from the
    constants dictionary for each plot
    :param xlabel: x label for plot
    :param ylabel: y label for plot
    :param data_line_style: (Optional) The style of line to use for plotting the
    data. Default is '-'
    :param fit_line_style: (Optional) The style of line to use for plotting the
    fit. Default is '--'
    :param savename: (Optional) The save name for the plot figure. Use the
    following keys to include information:
        {c}: code
        {t}: title
    :param cmap: (Optional) colormap string to use for plotting
    :param max_legend_cols: (Optional) The maximum number of columns to allow
    the legend to have
    :param max_legend_space: (Optional) The maximum proportion of horizonal
    space to allow for the legend
    :param max_legend_fontsize: (Optional) The maximum legend fontsize to allow
    :param legend_total_fontsize: (Optional) The "total fontsize" which
    represents the fontsize * the number of rows
    :param legend_rows_per_col: (Optional) The number of rows to warrant an
    additional column.
    :param legend_space_scale: (Optional) A scale-factor to append to
    calculation of legend space proportion
    :param mf_name: The name of the metafitter
    :param _plot_sort_key: (Optional) key for ordering plots, default is by
    Quantum numbers.
    :param _get_data: The function to be used to get data from the data map.
    Defult gets single particle data
    :param _get_plot: The function to be used to get a tuple that represents
    a particle plot from the available maps. Default gets the appropriate
    tuple for a single particle plot.
    :param _printer: The function to use to print results.
    :return: (mf_results, lr_results), A 2-tuple containing the meta-fit results
    and the regressional results for the fit.
    """
    # Get index->orbital and index->mass->energy maps
    exp_list = [Exp(*e_hw_pair) for e_hw_pair in e_hw_pairs]
    if imsrg_data_map is not None:
        all_data_map = imsrg_data_map
    else:
        all_data_map = ImsrgDataMap(parent_directory=sourcedir,
                                    exp_list=exp_list,
                                    standard_indices=std_io_map)

    plots = list()
    for exp in sorted(exp_list):
        data_maps = all_data_map.map[exp]
        io_map = data_maps.index_orbital_map
        ime_map = _get_data(data_maps)
        mzbt_map = data_maps.mass_zero_body_term_map
        other_constants = data_maps.other_constants

        # Print index orbital map for dataset, if not standard
        if print_key is True and std_io_map is None:
            print_io_key(io_map, heading='Index key for {}:'.format(exp))

        # Get list of plots
        for k in sorted(ime_map.keys()):
            plots.append(_get_plot(k, exp, io_map, ime_map[k], mzbt_map,
                                   other_constants))

    # Print index orbital map, if standard
    if print_key is True and std_io_map is not None:
        print_io_key(std_io_map, heading='Index key')

    # Transform plots
    if super_transform_pre is not None:
        plots = super_transform_pre(plots)
    if transform is not None:
        plots = [transform(*plot) for plot in plots]
    if super_transform_post is not None:
        plots = super_transform_post(plots)

    # Make an initial parameter guess based on the first plot
    if isinstance(fitfn, FitFunction):
        num_fit_params = fitfn.num_fit_params
    else:
        num_fit_params = fitfn.__code__.co_argcount - 1
    param_guess = _meta_fit([plots[0]], fitfn,
                            np.ones(num_fit_params))[0]

    # Do the meta-fit
    mf_results = _meta_fit(plots, fitfn, param_guess, full_output=full_output)
    params = mf_results[0]

    # Test goodness of fits
    lr_results = dict()
    for p in plots:
        x, y, const_list, const_dict = p
        if isinstance(fitfn, FitFunction):
            args = list([params, const_list, const_dict])
            ypred = np.array(list(map(lambda xi: fitfn.eval(xi, *args), x)))
        else:
            args = list(params)
            args.append(const_list)
            args.append(const_dict)
            ypred = np.array(list(map(lambda xi: fitfn(xi, *args), x)))
        yarr = np.array(y)
        lr_results[(exp, const_dict[idx])] = linregress(yarr, ypred)

    # Print results
    if print_results is True:
        _printer(mf_results, lr_results, print_mf_results, print_lr_results,
                 full_output,
                 header=title.format(tr=transform.__name__,
                                     fn=fitfn.__name__,
                                     ehw=exp))

    # Plot results
    if show_plot is True:
        # plt.style.use('dark_background')
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # Make color map
        cmap = plt.get_cmap(cmap)
        c_norm = colors.Normalize(vmin=0, vmax=len(plots) - 1)
        scalar_map = cm.ScalarMappable(norm=c_norm, cmap=cmap)
        # Do plots
        for p, i in zip(sorted(plots, key=_plot_sort_key),
                        range(len(plots))):
            x, y, const_list, const_dict = p

            qnums, e, hw, index = const_list[0:4]

            rp = const_dict['rp']
            b = const_dict['base']

            e_str = '' if e is None else e
            hw_str = '' if hw is None else hw
            rp_str = '' if rp is None else rp
            b_str = '' if b is None else b
            idxv = const_dict[idx]
            idxv_str = '' if idxv is None else idxv

            labelstr = label.format(e=e_str, hw=hw_str, b=b_str, rp=rp_str,
                                    i=idxv_str)

            cval = scalar_map.to_rgba(i)
            ax.plot(x, y, data_line_style, label=labelstr, color=cval)

            if show_fit is not False:
                xfit = np.linspace(x[0], x[-1])
                if isinstance(fitfn, FitFunction):
                    args = list([params, const_list, const_dict])
                    yfit = np.array(list(map(lambda xi: fitfn.eval(xi, *args),
                                         xfit)))
                else:
                    args = list(params)
                    args.append(const_list)
                    args.append(const_dict)
                    yfit = np.array(list(map(lambda xi: fitfn(xi, *args),
                                             xfit)))
                ax.plot(xfit, yfit, fit_line_style, color=cval)
                # label=labelstr + ' fit',

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        title = title.format(tr=transform.__name__,
                             fn=fitfn.__name__,
                             ehw=e_hw_pairs)
        plt.title(title)
        if show_legend is not False:
            l = len(plots)
            ncol = int(min(ceil(l/legend_rows_per_col), max_legend_cols))
            box = ax.get_position()
            fontsize = min(ncol*legend_total_fontsize/l, max_legend_fontsize)
            ax.set_position([box.x0, box.y0,
                             (box.width *
                              (1 - (max_legend_space*ncol/max_legend_cols) *
                               (fontsize / max_legend_fontsize) *
                               legend_space_scale)),
                             box.height])
            plt.legend(ncol=ncol, loc='upper left', bbox_to_anchor=(1.0, 1.0),
                       fontsize=fontsize)
        plt.savefig((savedir + '/' + savename + '.png').format(c=code, t=title))
    plt.show()

    # Make an info dict
    info = {
        'mf_code': code,
        'mf_name': mf_name,
        'ffn_name': fitfn.__name__,
        'ffn_code': fitfn.code if isinstance(fitfn, FitFunction) else ''}

    return mf_results, lr_results, plots, fitfn, info


def multi_particle_metafit(fitfn, e_hw_pairs, sourcedir, savedir,
                           transform=identity,
                           get_data=lambda dm:
                           dm.interaction_index_mass_energy_map(),
                           get_plot=_multi_particle_plot,
                           printer=_printer_for_multiparticle_metafit,
                           show_legend=False,
                           plot_sort_key=lambda p: p[3]['interaction'],
                           title=('Metafit for multiparticle matrix elements '
                                  '{tr} data using {fn} for {ehw}'),
                           idx='interaction',
                           ylabel='Energy (MeV)',
                           **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs, sourcedir, savedir,
                                   transform=transform,
                                   _get_data=get_data,
                                   _get_plot=get_plot,
                                   _printer=printer,
                                   show_legend=show_legend,
                                   _plot_sort_key=plot_sort_key,
                                   title=title,
                                   idx=idx,
                                   ylabel=ylabel,
                                   **kwargs)


def _meta_fit(plots, fitfn, params_guess, full_output=False, **lsqkwargs):
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
    if isinstance(fitfn, FitFunction):
        num_fit_params = fitfn.num_fit_params
    else:
        num_fit_params = fitfn.__code__.co_argcount - 1
    if len(params_guess) != num_fit_params:
        raise FunctionDoesNotMatchParameterGuessException
    combined_x = list()
    combined_y = list()
    constants_lists = list()
    constants_dicts = list()
    for p in plots:
        x, y, const_list, const_dict = p
        combined_x.append(x)
        combined_y.append(y)
        constants_lists.append(const_list)
        constants_dicts.append(const_dict)

    return leastsq(func=_mls, x0=params_guess,
                   args=(fitfn, combined_x, combined_y,
                         constants_lists, constants_dicts),
                   full_output=full_output,
                   **lsqkwargs)


def _mls(params, fitfn, lox, loy, const_lists, const_dicts):
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
    for x, cl, cd in zip(lox, const_lists, const_dicts):
        if isinstance(fitfn, FitFunction):
            args = list([params, cl, cd])
            yfit.extend(list(map(lambda xi: fitfn.eval(xi, *args), x)))
        else:
            args = list(params)
            args.append(cl)
            args.append(cd)
            yfit.extend(list(map(lambda xi: fitfn(xi, *args), x)))
    yflat = [item for y in loy for item in y]
    return np.array(yflat) - np.array(yfit)


class FunctionDoesNotMatchParameterGuessException(Exception):
    pass
