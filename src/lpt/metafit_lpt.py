from __future__ import print_function, division, unicode_literals

import numpy as np

from transforms import pzbt
from plotting import map_to_arrays
from constants import DIR_SHELL_RESULTS, DIR_PLOTS
from int.metafit_int import single_particle_metafit_int
from lpt.DataMapLpt import DataMapLpt


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
        xlabel='A', ylabel='Energy + Zero Body Term (MeV)',
        show_fit=False,
        _sourcedir=DIR_SHELL_RESULTS, _savedir=DIR_PLOTS,
        _data_map=DataMapLpt, _get_data=lambda dm: dm.n_mass_energy_map(),
        _get_plots=_get_plots_lpt, _get_plot=_get_plot_lpt,
        _plot_sort_key=lambda p: p[3]['exp'],
        _code_pref='LPT',
        _title='Metafit {mfn} for shell calculation {tr} data using {fn}',
        _label='{N}, {exp}', _get_label_fmt_kwargs=_get_label_kwargs_lpt,
        _print_results=False,
        _idx='N',
        **kwargs):
    return single_particle_metafit_int(
        fitfn=fitfn, exp_list=exp_list, exp_filter_fn=exp_filter_fn,
        sourcedir=_sourcedir, savedir=_savedir,
        transform=transform,
        xlabel=xlabel, ylabel=ylabel,
        show_fit=show_fit,
        _data_map=_data_map, _get_data=_get_data, _get_plots=_get_plots,
        _get_plot=_get_plot, _plot_sort_key=_plot_sort_key,
        _title=_title, _label=_label, _idx=_idx,
        print_results=_print_results,
        _get_label_fmt_kwargs=_get_label_fmt_kwargs,
        _code_pref=_code_pref,
        **kwargs)
