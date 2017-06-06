"""plotters.py
Various functions for plotting A-dependence data
"""
from __future__ import division, print_function, unicode_literals
from a_dependence_maps import *
from plotting_abs import map_to_arrays
from plotting_abs import save_plot_figure, save_plot_data_file
from LegendSize import LegendSize
from constants import LEGEND_SIZE
from parsers.parse_files import *
from parsers.LptEnergyLevel import LptEnergyLevel
from parsers.NcsdEnergyLevel import NcsdEnergyLevel


def _get_plots_a_to_energy_for_ncsd_states(parsed_ncsd_out_files):
    """Returns a list of plots in the form
            (xdata, ydata, const_list, const_dict),
    where A=Aeff is xdata, energy is ydata, and the const_dict constains
    the state list is generated from the data from the given NcsdOut objects
    :param parsed_ncsd_out_files: list of parsed NcsdOut objects from which
    to generate the map
    :return: [(a_array, energy_array, state)]
    """
    # make map state# -> A -> energy
    num_to_a_to_energy = dict()
    for ncsd_out_file in parsed_ncsd_out_files:
        assert isinstance(ncsd_out_file, NcsdOut)
        a = ncsd_out_file.n + ncsd_out_file.z
        aeff = ncsd_out_file.aeff
        if a != aeff:
            continue
        states = ncsd_out_file.energy_levels
        for state in states:
            # assert isinstance(state, NcsdEnergyLevel)
            num = state.N
            if num not in num_to_a_to_energy:
                num_to_a_to_energy[num] = dict()
            num_to_a_to_energy[num][a] = state.E
    # make plots
    list_of_plots = list()
    for num, a_to_energy in num_to_a_to_energy.items():
        list_of_plots.append(
            map_to_arrays(a_to_energy) + (list(), {'state': num}))
    return list_of_plots


def _get_ground_energy_plots(
        parsed_ncsd_out_files, parsed_int_files, parsed_lpt_files):
    z_a_aeff_to_ncsd_file = get_z_a_aeff_to_ncsd_out_map(parsed_ncsd_out_files)
    presc_a_to_int_and_lpt_files = get_presc_a_to_int_and_lpt_map(
        parsed_int_files, parsed_lpt_files)
    # make map (presc, a) to Nushell ground energy, assumed to be given
    # by the zero body term plus the lowest energy in the *.lpt file
    presc_a_to_ground_energy = dict()
    for presc_a, int_lpt in presc_a_to_int_and_lpt_files.items():
        int_file, lpt_file = int_lpt
        assert isinstance(int_file, NushellxInt)
        assert isinstance(lpt_file, NushellxLpt)
        zbt = int_file.zero_body_term
        ex0 = lpt_file.energy_levels[0].E
        presc_a_to_ground_energy[presc_a] = zbt + ex0
    # make map A -> listof(NcsdEnergyLevel)
    aeff_exact_to_ncsd_states = dict()
    for z_a_aeff, ncsd_file in z_a_aeff_to_ncsd_file.items():
        assert isinstance(ncsd_file, NcsdOut)
        z, a, aeff = z_a_aeff
        if a == aeff:
            aeff_exact_to_ncsd_states[a] = ncsd_file.energy_levels
    # make map A -> NCSD ground energy, assumed to be given by the lowest
    # NCSD state whose J and T agree with the corresponding Nushell ground
    # state for the (A, A, A) prescription
    a_to_ground_energy = dict()
    for a, ncsd_states in aeff_exact_to_ncsd_states.items():
        if ((a, a, a), a) in presc_a_to_int_and_lpt_files:
            int_file, lpt_file = presc_a_to_int_and_lpt_files[((a, a, a), a)]
            nushell_ground_state = lpt_file.energy_levels[0]
            assert isinstance(nushell_ground_state, LptEnergyLevel)
            j = nushell_ground_state.J
            t = nushell_ground_state.Tz
            for state in ncsd_states:
                assert isinstance(state, NcsdEnergyLevel)
                if state.J == j and state.T == t:
                    ground_energy = state.E
                    break
            else:
                continue
        else:
            continue
        a_to_ground_energy[a] = ground_energy
    return a_to_ground_energy, presc_a_to_ground_energy


def _get_plot_aeff_exact_to_ground_energy(a_to_ground_state_energy):
    """Returns a list of plots in the form
            (xdata, ydata, const_list, const_dict),
    where A=Aeff is xdata, and ground energy is ydata
    """
    # a_aeff_to_ground_state_energy = get_a_aeff_to_ground_state_energy_map(
    #     parsed_ncsd_out_files=parsed_ncsd_out_files)
    # a_to_ground_state_energy = dict()
    # for a_aeff, e in a_aeff_to_ground_state_energy.items():
    #     if a_aeff[0] == a_aeff[1]:
    #         a_to_ground_state_energy[a_aeff[0]] = e
    return map_to_arrays(a_to_ground_state_energy) + (list(), dict())


def _get_plots_presc_a_to_ground_energy(presc_a_to_ground_energy):
    """Returns a list of plots in the form
            (xdata, ydata, const_list, const_dict),
    where A (mass) is xdata, ground energy is ydata, and const_dict contains
    an item 'presc' whose value is a 3-tuple representation of the 
    A-prescriptions
    """
    # presc_a_to_ground_energy = get_presc_a_to_ground_state_energy_map(
    #     parsed_int_files=parsed_int_files, parsed_lpt_files=parsed_lpt_files)
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


def make_plot_ncsd_exact(dpath_ncsd_files, dpath_plots, savename, subtitle='',
                         ground_state_plot=None, num_states_limit=None):
    plots = _get_plots_a_to_energy_for_ncsd_states(
        parsed_ncsd_out_files=parse_ncsd_out_files(dirpath=dpath_ncsd_files))
    title = 'NCSD exact energies: ' + subtitle
    labels = [str(p[3]['state']) for p in plots]
    if num_states_limit is not None and len(plots) > num_states_limit:
        plots = plots[:num_states_limit]
        labels = labels[:num_states_limit]
    if ground_state_plot is not None:
        plots.append(ground_state_plot)
        labels.append(str('Ground state'))
    xlabel, ylabel = 'A', 'E_ncsm (MeV)'
    savepath = path.join(dpath_plots, savename)
    save_plot_data_file(
        plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
        labels=labels, savepath=savepath+'.dat'
    )
    return save_plot_figure(
        data_plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
        savepath=savepath+'.pdf', data_labels=labels, cmap_name='jet',
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


def _make_plot_prescription_error_vs_exact_abstract(
        dpath_ncsd_files, dpath_nushell_files, dpath_plots, savename,
        title, subtitle='', a_prescriptions=None,
        get_ncsd_plots_fn=_get_plot_aeff_exact_to_ground_energy,
        get_vce_plots_fn=_get_plots_presc_a_to_ground_energy,
        filter_fn_ncsd=None, filter_fn_int=None, filter_fn_lpt=None,
):
    ncsd_files = parse_ncsd_out_files(dirpath=dpath_ncsd_files)
    int_files = parse_nushellx_int_files(dirpath=dpath_nushell_files)
    lpt_files = parse_nushellx_lpt_files(dirpath=dpath_nushell_files)
    if filter_fn_ncsd is not None:
        ncsd_files = filter(filter_fn_ncsd, ncsd_files)
    if filter_fn_int is not None:
        int_files = filter(filter_fn_int, int_files)
    if filter_fn_lpt is not None:
        lpt_files = filter(filter_fn_lpt, lpt_files)
    ground_energy_maps = _get_ground_energy_plots(
        parsed_ncsd_out_files=ncsd_files, parsed_int_files=int_files,
        parsed_lpt_files=lpt_files,
    )
    ncsd_plot = get_ncsd_plots_fn(
        a_to_ground_state_energy=ground_energy_maps[0])
    vce_plots = get_vce_plots_fn(
        presc_a_to_ground_energy=ground_energy_maps[1])

    # Ncsd exact arrays
    x_ex, y_ex = [list(i) for i in ncsd_plot[:2]]

    # Aeff = A prescription
    def is_exact_presc(plot0):
        p0 = plot0[3]['presc']
        return p0[0] == p0[1] and p0[1] == p0[2]

    x_aaf, y_aaf = list(), list()
    for vce_plot in sorted(filter(is_exact_presc, vce_plots),
                           key=lambda p0: p0[3]['presc']):
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
    fulltitle = title + ': ' + subtitle
    labels = [p[3]['name'] for p in plots]
    xlabel, ylabel = 'A', 'E_presc - E_ncsm (MeV)'
    savepath = path.join(dpath_plots, savename)

    # save ncsd ground state plot file
    ncsd_title = fulltitle+' - NCSD ground energy'
    ncsd_ylabel = 'E_ncsm (MeV)'
    ncsd_savepath = savepath+'_NCSD'
    save_plot_data_file(
        plots=[ncsd_plot], title=ncsd_title, xlabel=xlabel, ylabel=ncsd_ylabel,
        labels=['ground state'], savepath=ncsd_savepath+'.dat',
    )
    save_plot_figure(
        data_plots=[ncsd_plot], title=ncsd_title, xlabel=xlabel,
        ylabel=ncsd_ylabel, data_labels=['ground state'],
        savepath=ncsd_savepath+'.pdf', cmap_name='jet',
    )

    # save ncsd all states plot
    make_plot_ncsd_exact(
        dpath_ncsd_files=dpath_ncsd_files, dpath_plots=dpath_plots,
        savename=path.split(ncsd_savepath+'_all_states')[1], subtitle=subtitle,
        ground_state_plot=ncsd_plot, num_states_limit=15,
    )

    # save vce plots
    vce_title = fulltitle+' - VCE prescription ground energies'
    vce_ylabel = 'E_presc (MeV)'
    vce_labels = [str(p[3]['presc']) for p in vce_plots]
    vce_savepath = savepath+'_VCE'
    save_plot_data_file(
        plots=vce_plots, title=vce_title, xlabel=xlabel,
        ylabel=vce_ylabel, labels=vce_labels, savepath=vce_savepath+'.dat',
    )
    save_plot_figure(
        data_plots=vce_plots, title=vce_title, xlabel=xlabel, ylabel=vce_ylabel,
        data_labels=vce_labels, savepath=vce_savepath+'.pdf', cmap_name='jet',
    )

    # save error plot files
    save_plot_data_file(
        plots=plots, title=fulltitle, xlabel=xlabel, ylabel=ylabel,
        labels=labels, savepath=savepath + '.dat'
    )
    return save_plot_figure(
        data_plots=plots, title=fulltitle, xlabel=xlabel, ylabel=ylabel,
        savepath=savepath + '.pdf', data_labels=labels, cmap_name='jet',
    )


def make_plot_ground_state_prescription_error_vs_exact(
        dpath_ncsd_files, dpath_nushell_files, dpath_plots, savename,
        subtitle='', a_prescriptions=None,
        filter_fn_ncsd=None, filter_fn_int=None, filter_fn_lpt=None,
):
    return _make_plot_prescription_error_vs_exact_abstract(
        dpath_ncsd_files=dpath_ncsd_files,
        dpath_nushell_files=dpath_nushell_files,
        dpath_plots=dpath_plots, savename=savename, subtitle=subtitle,
        a_prescriptions=a_prescriptions,
        title='Ground state energy error for A-prescriptions',
        get_ncsd_plots_fn=_get_plot_aeff_exact_to_ground_energy,
        get_vce_plots_fn=_get_plots_presc_a_to_ground_energy,
        filter_fn_ncsd=filter_fn_ncsd,
        filter_fn_int=filter_fn_int,
        filter_fn_lpt=filter_fn_lpt,
    )

# test
# dpath = '~/workspace/triumf/tr-c-ncsm/old/results20170224/ncsd'
# all_ncsd_files = sorted(parse_ncsd_out_files(dirpath=dpath))
# he_ncsd_files = filter(lambda n: n.z == 2, all_ncsd_files)
# # plots = get_plots_aeff_exact_to_energy(he_ncsd_files)
# # for plot in sorted(plots, key=lambda p0: p0[3]['state']):
# #     xarr, yarr, const_list, const_dict = plot
# #     print('State = {}'.format(const_dict['state']))
# #     for p0, y in zip(xarr, yarr):
# #         print('  {:4} {:8.4}'.format(p0, y))
# xarr, yarr, cl, cd = get_plot_aeff_exact_to_ground_energy(he_ncsd_files)
# for p0, y in zip(xarr, yarr):
#     print('  {:4} {:8.4}'.format(p0, y))
