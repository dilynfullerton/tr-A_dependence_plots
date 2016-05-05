"""metafitter_abs.py
Abstract metafitter for interaction data
See definitions at top of metafit.py.
"""
from __future__ import print_function, division, unicode_literals

from metafit import metafitter_abs, print_io_key
from transforms import relative_y, identity
from transforms_s import s_transform_to_super
from plotting import map_to_arrays
from constants import P_TITLE, P_END, P_SUB, P_HEAD
from constants import STANDARD_IO_MAP, PLOT_CMAP, LEGEND_SIZE
from int.DataMapInt import DataMapInt


# todo: Re-evaluate method for doing all of this.
# todo: Currently, plotting zero body terms and such work because of little
# todo: hacks. Methods for doing these things should be well-defined


def _set_const(k, exp, io_map, me_map, mzbt_map, other_constants):
    """Set the const_dict
    :param k: I do not remember. This should probably be removed
    :param exp: exp
    :param io_map: index -> orbital map
    :param me_map: mass -> spe map
    :param mzbt_map: mass -> zbt map
    :param other_constants: values following SPE's on first line of *.int file
    :return: x, y, const_list, const_dict
    """
    e, hw, base, rp = exp
    x, y = map_to_arrays(me_map)
    x0, y0 = x[0], y[0]
    zbt_arr = map_to_arrays(mzbt_map)[1]
    zbt0 = zbt_arr[0]
    const_list = [None, e, hw, k, zbt_arr, y0, zbt0, rp, x0, base, exp]
    const_dict = {
        'e': e, 'hw': hw, 'rp': rp, 'zbt_arr': zbt_arr,
        'x0': x0, 'y0': y0, 'zbt0': zbt0,
        'io_map': io_map, 'base': base, 'exp': exp,
        'others': other_constants
    }
    return x, y, const_list, const_dict


# noinspection PyUnusedLocal
def _get_plot_single_particle(k, exp, me_map, mzbt_map, io_map, others, *args):
    x, y, const_list, const_dict = _set_const(
        k, exp, io_map, me_map, mzbt_map, others)
    qnums = io_map[k]
    const_list[0] = qnums
    const_dict['index'] = k
    const_dict['qnums'] = qnums
    # noinspection PyProtectedMember
    const_dict = dict(const_dict.items() + dict(qnums._asdict()).items())
    return x, y, const_list, const_dict


# noinspection PyUnusedLocal
def _get_plots_single_particle(
        exp_list, all_data_map, get_data, get_plot=_get_plot_single_particle,
        print_key=False, std_io_map=None, **kwargs
):
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
            plots.append(get_plot(
                k=k, exp=exp, io_map=io_map, me_map=ime_map[k],
                mzbt_map=mzbt_map, others=other_constants
            ))
    return plots


def _printer_for_single_particle_metafit(
        metafit_results, linregress_results, print_mf_results=True,
        print_lr_results=True, full_output=False, header=''
):
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
    for kw, key in zip(
            ['e', 'hw', 'rp', 'b', 'i'],
            ['e', 'hw', 'rp', 'base', idx_key]
    ):
        if key in const_dict:
            v = const_dict[key]
            l[kw] = v if v is not None else ''
    return l


def single_particle_metafit_int(
        fitfn, exp_list, dpath_sources, dpath_plots,
        transform=relative_y,
        super_transform=None,
        imsrg_data_map=None,
        exp_filter_fn=None,
        print_key=False, print_results=False,
        print_mf_results=True, print_lr_results=True,
        show_plot=False, show_fit=True, show_legend=True,
        full_output=False,
        mf_name='', code='',
        xlabel='A', ylabel='Relative Energy (MeV)',
        _code_pref='INT',  # todo: get rid of this
        _std_io_map=STANDARD_IO_MAP,
        _title=('Metafit {mfn} for single particle energy'
                ' {tr} data using {fn} for {ehw}'),
        _label='{e}, {hw}, {b}, {i}', _idx='qnums',
        _get_label_fmt_kwargs=_get_label_kwargs,  # todo: get rid of this
        _data_line_style='-', _fit_line_style='--',
        _cmap=PLOT_CMAP,
        _legend_size=LEGEND_SIZE,
        _savename='meta_{c}-{t}',
        _plot_sort_key=lambda p: p[3]['qnums'],
        _get_data=lambda dm: dm.index_mass_energy_map(),
        _data_map=DataMapInt,
        _get_plots=_get_plots_single_particle,
        _get_plot=_get_plot_single_particle,
        _printer=_printer_for_single_particle_metafit
):
    """A meta-fit for all the orbitals with a given e, hw, and rp,
     based on the given fit function
    :type _get_plots: (exp_list:list, all_data_map:_ImsrgDataMap,
    get_data:_ImsrgDatum -> dict, get_plot:Any->Tuple[Any, Any, list, dict])
    -> list
    :type _data_map: _ImsrgDataMap
    :param fitfn: FitFunction object to use for fitting. Alternatively,
    may be of the form in fitfns.py, although this is deprecated.
    the data set(s) to use. If rp is not included, it is assumed to be None.
    :param exp_list: list of exp for which to gather data
    :param dpath_sources: main files directory to use for initializing the
    ImsrgDataMaps
    :param dpath_plots: directory in which to save plots
    :param transform: transform to apply to all plots
    :param super_transform: (optional) if not None, this is applied to
    the list of plots as a whole, instead of applying transform to each
    individually.
    :param imsrg_data_map: (optional) if included, will not retrieve data map
    from sourcedir and will instead take the given data map
    :param exp_filter_fn: (optional) this may be supplied as an alternative
    method to listing all desired exp's in exp_list. This filter function
    will be applied in determining what files/data to include in the plot
    :param _std_io_map: (optional) standard (index -> orbital) mapping
    scheme to use for generating the data representations
    :param print_key: (optional) if true, prints the index -> orbital key.
    Default is False.
    :param print_results: (optional) if true, prints fit results. Default is
    False.
    :param print_mf_results: (optional) if true, prints metafit results to
    stdout. Default is False.
    :param print_lr_results: (optional) if true, prints line regression
    results to stdout. Default is False.
    :param show_plot: (optional) if true, shows the data plot. Default False.
    :param show_fit: (optional) if true, shows the fit plot when show_plot is
    True. Default True.
    :param show_legend: (optional) if true, shows the legend when show_plot is
    True. Default True.
    :param full_output: (optional) if true, returned results include the
    full output given by the leastsq function. Default False.
    :param code: (optional) abbreviated name/identifier for the specific
    implementation of this function, to distinguish saved files.
    :param _title: (optional) title to include above the plot.
    Use the following keys to include information:
        {tr}: name of the transformation performed
        {fn}: name of the fit function applied
        {ehw}: (e, hw, rp) identifier of the data
    :param _label: (optional) labeling scheme for the plot legend.
    :param _get_label_fmt_kwargs: function that given a plot and _idx,
    returns a dictionary specifying how to format _label
    :param _idx: key to use to get the index (for the label) from the
    constants dictionary for each plot
    :param xlabel: x axis label for plot
    :param ylabel: y axis label for plot
    :param _code_pref: prefix for code
    :param _data_line_style: (optional) style of line to use for plotting
    the data. Default is '-'
    :param _fit_line_style: (optional) style of line to use for plotting
    the fit. Default is '--'
    :param _savename: (optional) save name for the plot figure.
    Use the following keys to include information:
        {c}: code
        {t}: title
    :param _cmap: (optional) colormap name (string) to use for coloring lines
    :param _legend_size: (optional) LegendSize object that specifies how to
    size the legend. See LegendSize.py
    :param mf_name: name of the metafitter (for filename)
    :param _plot_sort_key: (optional) key for ordering plots. Default is by
    Quantum numbers.
    :param _get_data: function to be used to get data from the data map.
    Defult gets single particle data
    :param _get_plot: function to be used to get a tuple that represents
    a particle plot from the available maps. Default gets the appropriate
    tuple for a single particle plot.
    :param _printer: The function to use to print results.
    :return: mf_results, lr_results, plots, fitfn, info_dict
    """
    if super_transform is None:
        super_transform = s_transform_to_super(transform=transform)
    return metafitter_abs(
        fitfn=fitfn, exp_list=exp_list, sourcedir=dpath_sources,
        savedir_plots=dpath_plots, super_transform=super_transform,
        data_map=imsrg_data_map, exp_filter_fn=exp_filter_fn,
        print_key=print_key, print_results=print_results,
        print_mf_results=print_mf_results, print_lr_results=print_lr_results,
        show_plot=show_plot, show_fit=show_fit, show_legend=show_legend,
        full_output=full_output, mf_name=mf_name, code=code,
        xlabel=xlabel, ylabel=ylabel, _code_pref=_code_pref,
        _std_io_map=_std_io_map,
        title=_title, label=_label, _idx=_idx,
        _get_label_fmt_kwargs=_get_label_fmt_kwargs,
        _data_line_style=_data_line_style, _fit_line_style=_fit_line_style,
        _cmap=_cmap, _legend_size=_legend_size, _savename=_savename,
        _plot_sort_key=_plot_sort_key, _get_data_from_map=_get_data,
        _data_map_type=_data_map, _get_plot=_get_plot, _get_plots=_get_plots,
        _printer=_printer
    )


# noinspection PyUnusedLocal
def _get_multi_particle_plot(k, exp, io_map, me_map, mzbt_map, others, *args):
    x, y, const_list, const_dict = _set_const(
        k, exp, io_map, me_map, mzbt_map, others)
    const_dict['interaction'] = k
    # noinspection PyProtectedMember
    const_dict = dict(const_dict.items() + dict(k._asdict()).items())
    return x, y, const_list, const_dict


def _printer_for_multiparticle_metafit(
        metafit_results, linregress_results,
        print_mf_results=True, print_lr_results=True, full_output=False,
        header=''
):
    return _printer_for_single_particle_metafit(
        metafit_results, linregress_results,
        print_mf_results, print_lr_results, full_output, header
    )


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
        _idx='interaction',  # todo get rid of this
        ylabel='Energy (MeV)',
        **kwargs
):
    """Wrapper of single_particle_metafit_int for use with two-body matrix
    elements
    """
    return single_particle_metafit_int(
        fitfn, e_hw_pairs, sourcedir, savedir,
        super_transform=s_transform_to_super(transform=transform),
        _get_data=_get_data, _get_plot=_get_plot,
        _printer=_printer, show_legend=show_legend,
        _plot_sort_key=_plot_sort_key, _title=_title, _idx=_idx, ylabel=ylabel,
        **kwargs
    )
