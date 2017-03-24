"""nushellx_lpt/metafitter_abs.py
Function definitions for an abstract *.lpt metafitter
"""
from __future__ import print_function, division, unicode_literals

import numpy as np
from deprecated.int.metafitter_abs import single_particle_metafit_int

from constants import DPATH_SHELL_RESULTS, DPATH_PLOTS
from deprecated.nushellx_lpt.DataMapNushellxLpt import DataMapNushellxLpt
from plotting import map_to_arrays
from transforms import pzbt


# noinspection PyUnusedLocal
# TODO: Use of zbt_array as a constant in this function is a hack.
# TODO: There should be well-defined methods for accessing zero-body term data
def _get_plot_lpt(n, exp, me_map, mzbt_map, *args):
    """Gets the energy vs. mass plot (x, y, const_list, const_dict) based
    on the given mass -> energy map, mass -> zero body map, etc
    :param n: state index (beginning at 1) from first column of *.lpt file
    :param exp: ExpNushellxLpt, which identifies the data being used for the
    plot
    :param me_map: mass number A -> enery map, where energy is that derived
    from the *.lpt file (without addition of zero body term)
    :param mzbt_map: mass number A -> zero body term map, derived from the
    interaction files
    :param args: allows extra args from compatibility (i.e. duck-typing).
    These are not used here
    :return: (x, y, const_list, const_dict), where const_list and const_dict
    contain exp, n, and zbt array
    """
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
def _get_plots_lpt(exp_list, data_map, get_data_fn, get_plot_fn=_get_plot_lpt,
                   **kwargs):
    """Gets a list of plot based on the given exp_list
    :param exp_list: list of exp values for which to get plots
    :param data_map: DataMapNushellxLpt object containing data for all
    of the exp in exp_list
    :param get_data_fn: function to retrieve n -> mass -> energy map from
    a value (DatumLpt) in data_map
    :param get_plot_fn: function to use to make plot from n, exp,
    mass -> energy map, and mass -> zero body term map
    :param kwargs: other arguments for compatibility (duck-typing). These
    are not used here.
    :return: list of plot, where a plot is (x, y, const_list, const_dict)
    """
    plots = list()
    if exp_list is not None:
        exps = exp_list
    else:
        exps = data_map.map.keys()
    for exp in sorted(exps):
        datum = data_map[exp]
        nme_map = get_data_fn(datum)
        mzbt_map = datum.mass_to_zbt_map()
        for n, me_map in nme_map.items():
            plots.append(get_plot_fn(n, exp, me_map, mzbt_map))
    return plots


# noinspection PyUnusedLocal
# TODO: Get rid of the need for this function. Top level functions should
# TODO: deal with labels, etc. The metafitters should be as minimalistic as
# TODO: possible.
def _get_label_kwargs_lpt(plot, idx_key=None):
    """Function to get a dictionary for the label keyword arguments for
    formatting
    :param plot: (x, y, const_list, const_dict)
    :param idx_key: I do not even remember what the point of this argument is.
    """
    return {'exp': plot[3]['exp'], 'N': plot[3]['N']}


def metafit_nushellx_lpt(
        fitfn, exp_list,
        transform=pzbt,
        exp_filter_fn=None,
        xlabel='A', ylabel='Energy + Zero Body Term (MeV)',
        show_fit=False,
        _sourcedir=DPATH_SHELL_RESULTS, _savedir=DPATH_PLOTS,
        _data_map=DataMapNushellxLpt,
        _get_data=lambda dm: dm.n_to_mass_to_ex_energy_map(),
        _get_plots=_get_plots_lpt, _get_plot=_get_plot_lpt,
        _plot_sort_key=lambda p: p[3]['exp'],
        _code_pref='LPT',
        _title='Metafit {mfn} for shell calculation {tr} data using {fn}',
        _label='{N}, {exp}', _get_label_fmt_kwargs=_get_label_kwargs_lpt,
        _print_results=False,
        _idx='N',
        **kwargs
):
    """See the documentation for single_particle_metafit_int
    (int/metafitter_abs.py)
    """
    return single_particle_metafit_int(
        fitfn=fitfn, exp_list=exp_list, exp_filter_fn=exp_filter_fn,
        dpath_sources=_sourcedir, dpath_plots=_savedir,
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
