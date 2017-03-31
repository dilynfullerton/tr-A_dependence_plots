"""plotters.py
Various functions for plotting A-dependence data
"""
from __future__ import division, print_function, unicode_literals
from data_maps import *
from plotting import map_to_arrays
from plotting import save_plot_figure, save_plot_data_file
from LegendSize import LegendSize
from constants import LEGEND_SIZE
from parsers.parse_files import *


def _get_plots_aeff_exact_to_energy(parsed_ncsd_out_files):
    """Returns a list of plots in the form
            (xdata, ydata, const_list, const_dict),
    where A=Aeff is xdata, energy is ydata, and the const_dict constains
    the state list is generated from the data from the given NcsdOut objects
    :param parsed_ncsd_out_files: list of parsed NcsdOut objects from which
    to generate the map
    :return: [(a_array, energy_array, state)]
    """
    state_to_a_aeff_to_energy = get_state_to_a_aeff_to_energy_map(
        parsed_ncsd_out_files=parsed_ncsd_out_files)
    state_to_a_exact_to_energy = dict()
    for state, a_aeff_to_energy in state_to_a_aeff_to_energy.items():
        for a_aeff, energy in a_aeff_to_energy.items():
            if a_aeff[0] == a_aeff[1]:
                if state not in state_to_a_exact_to_energy:
                    state_to_a_exact_to_energy[state] = dict()
                state_to_a_exact_to_energy[state][a_aeff[0]] = energy
    list_of_plots = list()
    for state, a_to_energy in state_to_a_exact_to_energy.items():
        if len(a_to_energy) < 2:
            continue
        list_of_plots.append(
            map_to_arrays(a_to_energy) + (list(), {'state': state}))
    return list_of_plots


def _get_plot_aeff_exact_to_ground_energy(parsed_ncsd_out_files):
    """Returns a list of plots in the form
            (xdata, ydata, const_list, const_dict),
    where A=Aeff is xdata, and ground energy is ydata
    """
    a_aeff_to_ground_state_energy = get_a_aeff_to_ground_state_energy_map(
        parsed_ncsd_out_files=parsed_ncsd_out_files)
    a_to_ground_state_energy = dict()
    for a_aeff, e in a_aeff_to_ground_state_energy.items():
        if a_aeff[0] == a_aeff[1]:
            a_to_ground_state_energy[a_aeff[0]] = e
    return map_to_arrays(a_to_ground_state_energy) + (list(), dict())


def _get_plots_presc_a_to_ground_energy(parsed_int_files, parsed_lpt_files):
    """Returns a list of plots in the form
            (xdata, ydata, const_list, const_dict),
    where A (mass) is xdata, ground energy is ydata, and const_dict contains
    an item 'presc' whose value is a 3-tuple representation of the 
    A-prescriptions
    """
    presc_a_to_ground_energy = get_presc_a_to_ground_state_energy_map(
        parsed_int_files=parsed_int_files, parsed_lpt_files=parsed_lpt_files)
    presc_to_a_to_ground_energy = dict()
    for presc_a, energy in presc_a_to_ground_energy.items():
        presc, a = presc_a
        if presc not in presc_to_a_to_ground_energy:
            presc_to_a_to_ground_energy[presc] = dict()
        presc_to_a_to_ground_energy[presc][a] = energy
    list_of_plots = list()
    for presc, a_to_ground in presc_to_a_to_ground_energy.items():
        list_of_plots.append(
            map_to_arrays(a_to_ground) + (list(), {'presc': presc}))
    return list_of_plots


def make_plot_ncsd_exact(dpath_ncsd_files, dpath_plots, savename, subtitle=''):
    plots = _get_plots_aeff_exact_to_energy(
        parsed_ncsd_out_files=parse_ncsd_out_files(dirpath=dpath_ncsd_files))
    title = 'NCSD exact energies: ' + subtitle
    labels = [str(p[3]['state']) for p in plots]
    xlabel, ylabel = 'A', 'E_ncsm (MeV)'
    savepath = path.join(dpath_plots, savename + '.pdf')
    save_plot_data_file(
        plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
        labels=labels, savepath=savepath
    )
    return save_plot_figure(
        data_plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
        savepath=savepath, data_labels=labels, cmap_name='jet',
        legendsize=LegendSize(
            max_cols=LEGEND_SIZE.max_cols,
            max_h_space=LEGEND_SIZE.max_h_space,
            max_fontsize=LEGEND_SIZE.max_fontsize,
            min_fontsize=LEGEND_SIZE.min_fontsize,
            total_fontsize=LEGEND_SIZE.total_fontsize,
            rows_per_col=LEGEND_SIZE.rows_per_col,
            space_scale=6,
        )
    )


def make_plot_ground_state_prescription_error_vs_exact(
        dpath_ncsd_files, dpath_nushell_files, dpath_plots, savename,
        subtitle='', a_prescriptions=None
):
    ncsd_plot = _get_plot_aeff_exact_to_ground_energy(
        parsed_ncsd_out_files=parse_ncsd_out_files(dirpath=dpath_ncsd_files))
    vce_plots = _get_plots_presc_a_to_ground_energy(
        parsed_int_files=parse_nushellx_int_files(dirpath=dpath_nushell_files),
        parsed_lpt_files=parse_nushellx_lpt_files(dirpath=dpath_nushell_files))

    # Ncsd exact arrays
    x_ex, y_ex = [list(i) for i in ncsd_plot[:2]]

    # Aeff = A prescription
    def is_exact_presc(plot):
        p = plot[3]['presc']
        return p[0] == p[1] and p[1] == p[2]
    x_aaf, y_aaf = list(), list()
    for vce_plot in sorted(filter(is_exact_presc, vce_plots),
                           key=lambda p: p[3]['presc']):
        x_arr, y_arr, const_list, const_dict = vce_plot
        a = const_dict['presc'][0]
        if a not in x_arr:
            continue
        x_aaf.append(a)
        y_aaf.append(y_arr[list(x_arr).index(a)])
    x_del = sorted(list(set(x_ex) & set(x_aaf)))
    y_del = list()
    for x in x_del:
        y_del.append(y_aaf[x_aaf.index(x)] - y_ex[x_ex.index(x)])
    plots = [(x_del, y_del, list(), {'name': 'Aeff = A'})]

    # other prescriptions
    for vce_plot in vce_plots:
        if a_prescriptions is None or vce_plot[3]['presc'] in a_prescriptions:
            x_p, y_p = [list(i) for i in vce_plot[:2]]
            presc = vce_plot[3]['presc']
            x_del = sorted(list(set(x_ex) & set(x_p)))
            y_del = list()
            for x in x_del:
                y_del.append(y_p[x_p.index(x)] - y_ex[x_ex.index(x)])
            plot = (x_del, y_del, list(), {'name': 'Aeff = {}'.format(presc)})
            plots.append(plot)

    # make plot
    title = 'Ground state energy error for A-prescriptions: ' + subtitle
    labels = [p[3]['name'] for p in  plots]
    xlabel, ylabel = 'A', 'E_presc - E_ncsm (MeV)'
    savepath = path.join(dpath_plots, savename + '.pdf')
    save_plot_data_file(
        plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
        labels=labels, savepath=savepath
    )
    return save_plot_figure(
        data_plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
        savepath=savepath, data_labels=labels, cmap_name='jet',
    )





# test
# dpath = '/Users/Alpha/workspace/triumf/tr-c-ncsm/old/results20170224/ncsd'
# all_ncsd_files = sorted(parse_ncsd_out_files(dirpath=dpath))
# he_ncsd_files = filter(lambda n: n.z == 2, all_ncsd_files)
# # plots = get_plots_aeff_exact_to_energy(he_ncsd_files)
# # for plot in sorted(plots, key=lambda p: p[3]['state']):
# #     xarr, yarr, const_list, const_dict = plot
# #     print('State = {}'.format(const_dict['state']))
# #     for x, y in zip(xarr, yarr):
# #         print('  {:4} {:8.4}'.format(x, y))
# xarr, yarr, cl, cd = get_plot_aeff_exact_to_ground_energy(he_ncsd_files)
# for x, y in zip(xarr, yarr):
#     print('  {:4} {:8.4}'.format(x, y))
