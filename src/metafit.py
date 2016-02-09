"""Primary algorithms for fitting onto multiple single particle or
multiparticle plots simultaneously based on universal and specific parameters
for each plot
"""

from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

from matplotlib import pyplot as plt
from scipy.optimize import leastsq
from scipy.stats import linregress

from FitFunction import FitFunction
from ImsrgDataMap import ImsrgDataMapInt, ImsrgDataMapLpt
from fitting_sp import print_io_key
from plotting import plot_the_plots
from plotting import map_to_arrays

from constants import *
from fit_transforms import *


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
def _get_plot_single_particle(k, exp, me_map, mzbt_map, io_map, others, *args):
    x, y, const_list, const_dict = _set_const(k, exp, io_map, me_map,
                                              mzbt_map, others)
    qnums = io_map[k]
    const_list[0] = qnums
    const_dict['index'] = k
    const_dict['qnums'] = qnums
    # noinspection PyProtectedMember
    const_dict = dict(const_dict.items() + dict(qnums._asdict()).items())
    return x, y, const_list, const_dict


# noinspection PyUnusedLocal
def _get_plots_single_particle(exp_list, all_data_map, get_data,
                               get_plot=_get_plot_single_particle,
                               print_key=False, std_io_map=None, **kwargs):
    plots = list()
    for exp in sorted(exp_list):
        data_maps = all_data_map[exp]
        io_map = data_maps.index_orbital_map()
        ime_map = get_data(data_maps)
        mzbt_map = data_maps.mass_zero_body_term_map()
        other_constants = data_maps.other_constants()

        # Print index orbital map for dataset, if not standard
        if print_key is True and std_io_map is None:
            print_io_key(io_map, heading='Index key for {}:'.format(exp))

        # Get list of plots
        for k in sorted(ime_map.keys()):
            plots.append(get_plot(k=k, exp=exp, io_map=io_map,
                                  me_map=ime_map[k], mzbt_map=mzbt_map,
                                  others=other_constants))
    return plots


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


def _get_label_kwargs(plot, idx_key=None):
    x, y, const_list, const_dict = plot
    l = dict()
    for kw, key in zip(['e', 'hw', 'rp', 'b', 'i'],
                       ['e', 'hw', 'rp', 'base', idx_key]):
        if key in const_dict:
            v = const_dict[key]
            l[kw] = v if v is not None else ''
    return l


def _exp_list_to_string(exp_list):
    if exp_list is not None:
        return '[' + ', '.join([str(ei) for ei in exp_list]) + ']'
    else:
        return ''


def single_particle_metafit_int(
        fitfn, exp_list, sourcedir, savedir,
        transform=relative_y,
        super_transform_pre=None, super_transform_post=None,
        imsrg_data_map=None,
        exp_filter_fn=None,
        print_key=False, print_results=False,
        print_mf_results=True, print_lr_results=True,
        show_plot=False, show_fit=True, show_legend=True,
        full_output=False,
        mf_name='', code='',
        xlabel='A', ylabel='Relative Energy (MeV)',
        _code_pref='INT',
        _std_io_map=STANDARD_IO_MAP,
        _title=('Metafit {mfn} for single particle energy'
                ' {tr} data using {fn} for {ehw}'),
        _label='{e}, {hw}, {b}, {i}', _idx='qnums',
        _get_label_fmt_kwargs=_get_label_kwargs,
        _data_line_style='-', _fit_line_style='--',
        _cmap=PLOT_CMAP,
        _legend_size=LEGEND_SIZE,
        _savename='meta_{c}-{t}',
        _plot_sort_key=lambda p: p[3]['qnums'],
        _get_data=lambda dm: dm.index_mass_energy_map(),
        _data_map=ImsrgDataMapInt,
        _get_plots=_get_plots_single_particle,
        _get_plot=_get_plot_single_particle,
        _printer=_printer_for_single_particle_metafit):
    """A meta-fit for all the orbitals with a given e, hw, and rp,
     based on the given fit function

    :type _get_plots: (exp_list:list, all_data_map:_ImsrgDataMap,
    get_data:_ImsrgDatum -> dict, get_plot:Any->Tuple[Any, Any, list, dict])
    -> list
    :type _data_map: _ImsrgDataMap
    :param _get_plots:
    :param _data_map:
    :param _get_label_fmt_kwargs:
    :param _code_pref:
    :param exp_filter_fn:
    :param exp_list:
    :param _legend_size:
    :param print_lr_results:
    :param print_mf_results:
    :param fitfn: The FitFunction object to use for fitting. Alternatively,
    may be of the form in fitfns.py, although this is deprecated.
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
    :param _std_io_map: A standard index -> orbital mapping scheme to use for
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
    :param _title: (Optional) The title by which to name the plot. Use the
    following keys to include information:
        {tr}: name of the transformation performed
        {fn}: name of the fit function applied
        {ehw}: (e, hw, rp) identifier of the data
    :param _label: (Optional) The labeling scheme for the plot legend. Use the
    following keys to include information:
        {e}: emax
        {hw}: h-bar omega frequency
        {rp}: proton radius
        {i}: index
    :param _idx: the key to use to get the index (for the label) from the
    constants dictionary for each plot
    :param xlabel: x label for plot
    :param ylabel: y label for plot
    :param _data_line_style: (Optional) The style of line to use for plotting
    the data. Default is '-'
    :param _fit_line_style: (Optional) The style of line to use for plotting the
    fit. Default is '--'
    :param _savename: (Optional) The save name for the plot figure. Use the
    following keys to include information:
        {c}: code
        {t}: title
    :param _cmap: (Optional) colormap string to use for plotting
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
    code = _code_pref + code

    # Get index->orbital and index->mass->energy maps
    if imsrg_data_map is not None:
        all_data_map = imsrg_data_map
    else:
        all_data_map = _data_map(parent_directory=sourcedir,
                                 exp_list=exp_list,
                                 exp_filter_fn=exp_filter_fn,
                                 standard_indices=_std_io_map)

    exp_list = all_data_map.map.keys()

    plts = _get_plots(exp_list=exp_list, all_data_map=all_data_map,
                      get_data=_get_data, print_key=print_key,
                      std_io_map=_std_io_map, get_plot=_get_plot)

    # Print index orbital map, if standard
    if print_key is True and _std_io_map is not None:
        print_io_key(_std_io_map, heading='Index key')

    rr = _imsrg_meta_fit(plots=plts,
                         transform=transform,
                         super_transform_pre=super_transform_pre,
                         super_transform_post=super_transform_post,
                         fitfn=fitfn,
                         full_output=full_output, idx=_idx, )

    mf_results, lr_results, plots, fitfn = rr
    params = mf_results[0]

    formatted_title = _title.format(mfn=mf_name,
                                    tr=transform.__name__,
                                    fn=fitfn.__name__,
                                    ehw=_exp_list_to_string(exp_list))
    # Print results
    if print_results is True:
        _printer(mf_results, lr_results, print_mf_results, print_lr_results,
                 full_output, header=formatted_title)

    # Plot results
    if show_plot is True:
        plot_the_plots(
            plots,
            label=_label, get_label_kwargs=_get_label_fmt_kwargs, idx_key=_idx,
            title=formatted_title,
            xlabel=xlabel, ylabel=ylabel,
            data_line_style=_data_line_style, fit_line_style=_fit_line_style,
            sort_key=_plot_sort_key,
            cmap_name=_cmap,
            show_fit=show_fit, fit_params=params, fitfn=fitfn,
            include_legend=show_legend, legend_size=_legend_size,
            savedir=savedir, savename=_savename, code=code)
        plt.show()

    # Make an info dict
    info = {
        'mf_code': code,
        'mf_name': mf_name,
        'ffn_name': fitfn.__name__,
        'ffn_code': fitfn.code if isinstance(fitfn, FitFunction) else '',
        'exp_list': exp_list}

    return rr + (info,)


# noinspection PyUnusedLocal
def _get_multi_particle_plot(k, exp, io_map, me_map, mzbt_map, others,
                             *args):
    x, y, const_list, const_dict = _set_const(k, exp, io_map, me_map,
                                              mzbt_map, others)
    const_dict['interaction'] = k
    # noinspection PyProtectedMember
    const_dict = dict(const_dict.items() + dict(k._asdict()).items())
    return x, y, const_list, const_dict


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


def multi_particle_metafit_int(
        fitfn, e_hw_pairs, sourcedir, savedir,
        transform=identity,
        _get_data=lambda dm: dm.interaction_index_mass_energy_map(),
        _get_plot=_get_multi_particle_plot,
        _printer=_printer_for_multiparticle_metafit,
        show_legend=False,
        _plot_sort_key=lambda p: p[3]['interaction'],
        _title=('Metafit {mfn} for multiparticle matrix elements '
                '{tr} data using {fn} for {ehw}'),
        _idx='interaction',
        ylabel='Energy (MeV)',
        **kwargs):
    return single_particle_metafit_int(fitfn, e_hw_pairs, sourcedir, savedir,
                                       transform=transform,
                                       _get_data=_get_data,
                                       _get_plot=_get_plot,
                                       _printer=_printer,
                                       show_legend=show_legend,
                                       _plot_sort_key=_plot_sort_key,
                                       _title=_title,
                                       _idx=_idx,
                                       ylabel=ylabel,
                                       **kwargs)


# noinspection PyUnusedLocal
def _get_plot_lpt(n, exp, me_map, mzbt_map, *args):
    x, y = map_to_arrays(me_map)
    zbt_list = list()
    x_arr, zbt_arr = map_to_arrays(mzbt_map)
    for xa, zbta, i in zip(x_arr, zbt_arr, range(len(x_arr))):
        if xa in x:
            zbt_list.append(zbta)
    zbt_arr_fixed = np.array(zbt_list)
    const_list = [exp, n, np.array(zbt_arr_fixed)]
    const_dict = {'exp': exp, 'N': n, 'zbt_arr': zbt_arr_fixed}
    return x, y, const_list, const_dict


# noinspection PyUnusedLocal
def _get_plots_lpt(exp_list, all_data_map, get_data, get_plot=_get_plot_lpt,
                   **kwargs):
    plots = list()
    if exp_list is not None:
        exps = exp_list
    else:
        exps = all_data_map.map.keys()
    for exp in sorted(exps):
        data_map = all_data_map[exp]
        nme_map = get_data(data_map)
        mzbt_map = data_map.mass_zbt_map()

        for n, me_map in nme_map.iteritems():
            plots.append(get_plot(n, exp, me_map, mzbt_map))
    return plots


# noinspection PyUnusedLocal
def _get_label_kwargs_lpt(plot, idx_key=None):
    return {'exp': plot[3]['exp'], 'N': plot[3]['N']}


def metafit_lpt(
        fitfn, exp_list,
        transform=pzbt,
        exp_filter_fn=None,
        xlabel='A',
        ylabel='Energy + Zero Body Term (MeV)',
        show_fit=False,
        _sourcedir=DIR_SHELL_RESULTS, _savedir=DIR_PLOTS,
        _data_map=ImsrgDataMapLpt,
        _get_data=lambda dm: dm.n_mass_energy_map(),
        _get_plots=_get_plots_lpt,
        _get_plot=_get_plot_lpt,
        _plot_sort_key=lambda p: p[3]['exp'],
        _code_pref='LPT',
        _title='Metafit {mfn} for shell calculation {tr} data using {fn}',
        _label='{N}, {exp}',
        _get_label_fmt_kwargs=_get_label_kwargs_lpt,
        _print_results=False,
        _idx='N',
        **kwargs):
    return single_particle_metafit_int(
        fitfn=fitfn, exp_list=exp_list, exp_filter_fn=exp_filter_fn,
        sourcedir=_sourcedir, savedir=_savedir,
        transform=transform,
        xlabel=xlabel,
        ylabel=ylabel,
        show_fit=show_fit,
        _data_map=_data_map,
        _get_data=_get_data,
        _get_plots=_get_plots,
        _get_plot=_get_plot,
        _plot_sort_key=_plot_sort_key,
        _title=_title,
        _label=_label, _idx=_idx,
        print_results=_print_results,
        _get_label_fmt_kwargs=_get_label_fmt_kwargs,
        _code_pref=_code_pref,
        **kwargs)


def _imsrg_meta_fit(plots,
                    transform, super_transform_pre, super_transform_post,
                    fitfn,
                    full_output,
                    idx, ):
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
            args = list([params])
        else:
            args = list(params)
        args.extend([const_list, const_dict])
        ypred = np.array(list(map(lambda xi: fitfn(xi, *args), x)))
        yarr = np.array(y)
        exp = const_dict['exp']
        lr_results[(exp, const_dict[idx])] = linregress(yarr, ypred)

    return mf_results, lr_results, plots, fitfn


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
        raise FunctionDoesNotMatchParameterGuessException()
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
            args = list([params])
        else:
            args = list(params)
        args.extend([cl, cd])
        yfit.extend(list(map(lambda xi: fitfn(xi, *args), x)))
    yflat = [item for y in loy for item in y]
    return np.array(yflat) - np.array(yfit)


class FunctionDoesNotMatchParameterGuessException(Exception):
    pass
