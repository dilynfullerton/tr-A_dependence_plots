"""metafit.py
Primary algorithms for fitting onto multiple single particle or
multiparticle plots simultaneously based on universal and specific parameters
for each plot

Definitions:
    exp:
        namedtuple that identifies a set of input files from which to retrieve
        data
    plot:
        4-tuple (xarray, yarray, const_list, const_dict)
    xarray:
        ndarray representing independent variable
    yarray:
        ndarray representing dependent variable
    const_list:
        ordered list of constants associated with a plot
    const_dict:
        dictionary of named constants associated with a plot
    transform:
        a transformation to apply to a single plot
        Form:
            T(*plot) = plot
    super_transform:
        a transformation to apply to a list of plots
        Form:
            T(list_of_plot) -> list_of_plot
    fitfn:
        function that when given and x value, a list of parameters, and
        constants, deterministically returns a y value (the fit)
        Form:
            f(x, params, const_list, const_dict) -> y

"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import leastsq
from scipy.stats import linregress
from FitFunction import FitFunction
from constants import P_TITLE, P_END
from plotting import plot_the_plots


class FunctionDoesNotMatchParameterGuessException(Exception):
    pass


def exp_list_to_string(exp_list):
    """Get a concise string representation of an exp.
    """
    if exp_list is not None:
        return '[' + ', '.join([str(ei) for ei in exp_list]) + ']'
    else:
        return ''


def print_io_key(iomap, sortkey=lambda k: k, heading='Index key:'):
    print('\n' + P_TITLE + heading + '\n' + '-' * 80 + P_END)
    for index in sorted(iomap.keys(), key=sortkey):
        print(str(index) + ': ' + str(iomap[index]))
    print()


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
    return leastsq(
        func=_mls, x0=params_guess,
        args=(fitfn, combined_x, combined_y, constants_lists, constants_dicts),
        full_output=full_output, **lsqkwargs
    )


# todo: combine transform, super_transform_pre, and super_transform_post into
# todo: single super_transform argument
def _meta_fit_with_transformation(
        plots, super_transform, fitfn, full_output, idx):
    """Perform a simultaneous fit on the given plots after transforming them
    with transform
    :param plots: list of plots. See definition of "plot" at top of file.
    :param super_transform: transform to apply to the list of plots
    :param fitfn: fit function. See definition at top of file.
    :param full_output: if true, return full output of fit
    :param idx: I do not actually know what this is. It should be removed.
    :return: mf_results, lr_results, plots, fitfn
    """
    # Transform plots
    if super_transform is not None:
        plots = super_transform(plots)
    # Make an initial parameter guess based on the first plot
    if isinstance(fitfn, FitFunction):
        num_fit_params = fitfn.num_fit_params
    else:
        num_fit_params = fitfn.__code__.co_argcount - 1
    param_guess = _meta_fit(
        [plots[0]], fitfn, np.ones(num_fit_params)
    )[0]
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


# todo: finish docstring
def metafitter_abs(
        fitfn, exp_list, exp_filter_fn, super_transform,
        sourcedir, data_map, mf_name, code,
        _get_data_from_map,
        _data_map_type,
        _get_plots,
        savedir_plots,
        title, xlabel, ylabel, label=None,
        _idx=None,  # todo: get rid of this parameter
        _get_label_fmt_kwargs=None,  # todo consider getting rid of this
        _data_line_style='-', _fit_line_style='--',
        _cmap=None,
        _legend_size=None,
        _savename=None,
        _plot_sort_key=lambda p: p,
        _get_plot=None,
        print_key=False, print_results=False,
        print_mf_results=True, print_lr_results=True,
        _printer=None,
        show_plot=False, show_fit=True, show_legend=True,
        full_output=False,
        _code_pref='',  # todo: get rid of this parameter
        _std_io_map=None,
):
    """An (abstract) function to be used by specific metafitters.
    Retrieves data from a given data map, transforms it, and fits to it
    based on both global and plot-specific parameters
    :param fitfn: The FitFunction object to use for fitting. Alternatively,
    may be of the form in fitfns.py, although this is deprecated.
    :param exp_list: List of exp values for which to gather data. An exp
    is simply a tuple that uniquely identifies a data file. I do not
    remember why I chose to call it an exp.
    :param exp_filter_fn: Function from exp to {True, False}. Used as an
    alternative to explicitly listing out exp tuples such that the set of
    data gathered are only those that satisfy the filter
    :param super_transform: transformation to apply to list of plots
    (see transforms_s.py)
    :param sourcedir: Main files directory to use for initializing the
    DataMaps
    :param data_map: (Optional) If included, will not retrieve data map
    from sourcedir and will instead take the given data map
    :param mf_name: Assigned name of the metafitter, for use in plot title,
    save name, etc
    :param code: (Optional) An identifier for the specific implementation of
    this function, to distinguish saved files.
    :param _get_data_from_map: (Must be specified by wrapper functions)
    Function to be used to get data from the data map.
    :param _data_map_type: (Must be specified by wrapper functions)
    Type of the data map (e.g. DataMapInt)
    :param _get_plots: (Must be specified by wrapper functions)
    Function that takes keyword arguments
        exp_list, all_data_map, get_data, print_key, std_io_map, get_plot
    and returns a list of plots, where a plot is defined to be a tuple
    containing (xarray, yarray, constants_list, constants_dict)
    :param savedir_plots: Directory in which to save plots
    :param title: (Optional) The title by which to name the plot. Use the
    following keys to include information:
        {tr}: name of the transformation performed
        {fn}: name of the fit function applied
        {ehw}: (e, hw, rp) identifier of the data
    :param xlabel: x label for plot
    :param ylabel: y label for plot
    :param label: (Optional) The labeling scheme for the plot legend. Use the
    following keys to include information:
        {e}: emax
        {hw}: h-bar omega frequency
        {rp}: proton radius
        {i}: index
    :param _idx: Key to use to get the index (for the label) from the
    constants dictionary for each plot
    :param _get_label_fmt_kwargs: Function that when given a plot and
    a _idx returns a dictionary containing the keywords arguments that
    the label string accepts and their respective values. If not specified,
    labels are assumed to not need formatting.
    :param _data_line_style: (Optional) The style of line to use for plotting
    the data. Default is '-'
    :param _fit_line_style: (Optional) The style of line to use for plotting the
    fit. Default is '--'
    :param _cmap: (Optional) colormap string to use for plotting
    :param _legend_size: Object that specifies the sizing of the legend. If
    not specified, the default matplotlib sizing is used
    :param _savename: (Optional) The save name for the plot figure. Use the
    following keys to include information:
        {c}: code
        {t}: title
    :param _plot_sort_key: (Optional) key for ordering plots, default is by
    Quantum numbers.
    :param _get_plot: The function to be used to get a tuple that represents
    a particle plot from the available maps. Default gets the appropriate
    tuple for a single particle plot.
    :param print_key: (Optional) Whether to print the index -> orbital key.
    Default is False.
    :param print_results: (Optional) Whether to print fit results. Default is
    False.
    :param print_mf_results: If True, prints out the metafit results
    :param print_lr_results: If True, prints out the linear regression
    results
    :param _printer: The function to use to print results.
    :param show_plot: (Optional) Whether to show the data plot. Default False.
    :param show_fit: (Optional) Whether to show the fit plot when show_plot is
    True. Default True.
    :param show_legend: (Optional) Whether to show the legend when show_plot is
    True. Default True.
    :param full_output: (Optional) Whether the returned results should be the
    full output given by the leastsq function. Default False.
    :param _code_pref: Prefix to append to the code string.
    :param _std_io_map: A standard index -> orbital mapping scheme to use for
    generating the data representations
    :return: mf_results, lr_results, plots, fitfn, info_dict
    """
    code = _code_pref + code
    # Get index->orbital and index->mass->energy maps
    if data_map is not None:
        all_data_map = data_map
    else:
        all_data_map = _data_map_type(
            parent_directory=sourcedir,
            exp_list=exp_list, exp_filter_fn=exp_filter_fn,
            standard_indices=_std_io_map
        )
    exp_list = all_data_map.map.keys()
    plts = _get_plots(
        exp_list=exp_list, all_data_map=all_data_map,
        get_data=_get_data_from_map, print_key=print_key,
        std_io_map=_std_io_map, get_plot=_get_plot
    )
    # Print index orbital map, if standard
    if print_key is True and _std_io_map is not None:
        print_io_key(_std_io_map, heading='Index key')
    rr = _meta_fit_with_transformation(
        plots=plts, super_transform=super_transform,
        fitfn=fitfn, full_output=full_output, idx=_idx,
    )
    mf_results, lr_results, plots, fitfn = rr
    params = mf_results[0]
    formatted_title = title.format(
        mfn=mf_name, tr=super_transform.__name__, fn=fitfn.__name__,
        ehw=exp_list_to_string(exp_list)
    )
    # Print results
    if print_results is True:
        _printer(mf_results, lr_results, print_mf_results, print_lr_results,
                 full_output, header=formatted_title)
    # Plot results
    if show_plot is True:
        plot_the_plots(
            plots,
            label=label, get_label_kwargs=_get_label_fmt_kwargs, idx_key=_idx,
            title=formatted_title,
            xlabel=xlabel, ylabel=ylabel,
            data_line_style=_data_line_style, fit_line_style=_fit_line_style,
            sort_key=_plot_sort_key,
            cmap_name=_cmap,
            show_fit=show_fit, fit_params=params, fitfn=fitfn,
            include_legend=show_legend, legend_size=_legend_size,
            dpath_fig=savedir_plots, fname=_savename, code=code
        )
        plt.show()
    # Make an info dict
    info = {
        'mf_code': code,
        'mf_name': mf_name,
        'ffn_name': fitfn.__name__,
        'ffn_code': fitfn.code if isinstance(fitfn, FitFunction) else '',
        'exp_list': exp_list
    }
    return rr + (info,)
