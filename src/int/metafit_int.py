from __future__ import print_function, division, unicode_literals

from metafit import imsrg_metafitter, print_io_key
from transforms import relative_y, identity
from plotting import map_to_arrays
from constants import P_TITLE, P_END, P_SUB, P_HEAD
from constants import STANDARD_IO_MAP, PLOT_CMAP, LEGEND_SIZE
from int.ImsrgDataMapInt import ImsrgDataMapInt


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
    return imsrg_metafitter(fitfn=fitfn, exp_list=exp_list,
                            sourcedir=sourcedir, savedir=savedir,
                            transform=transform,
                            super_transform_pre=super_transform_pre,
                            super_transform_post=super_transform_post,
                            imsrg_data_map=imsrg_data_map,
                            exp_filter_fn=exp_filter_fn,
                            print_key=print_key, print_results=print_results,
                            print_mf_results=print_mf_results,
                            print_lr_results=print_lr_results,
                            show_plot=show_plot, show_fit=show_fit,
                            show_legend=show_legend,
                            full_output=full_output,
                            mf_name=mf_name, code=code,
                            xlabel=xlabel, ylabel=ylabel,
                            _code_pref=_code_pref,
                            _std_io_map=_std_io_map,
                            _title=_title, _label=_label, _idx=_idx,
                            _get_label_fmt_kwargs=_get_label_fmt_kwargs,
                            _data_line_style=_data_line_style,
                            _fit_line_style=_fit_line_style,
                            _cmap=_cmap,
                            _legend_size=_legend_size,
                            _savename=_savename,
                            _plot_sort_key=_plot_sort_key,
                            _get_data=_get_data, _data_map=_data_map,
                            _get_plot=_get_plot, _get_plots=_get_plots,
                            _printer=_printer)


# noinspection PyUnusedLocal
def _get_multi_particle_plot(k, exp, io_map, me_map, mzbt_map, others, *args):
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
