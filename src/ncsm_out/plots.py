"""ncsm_out/plots.py
Functions for making plots from NCSD data
"""
from __future__ import print_function, division, unicode_literals

import numpy as np
from os import path
from constants import DPATH_SHELL_RESULTS, DPATH_NCSM_RESULTS
from constants import DPATH_PLOTS_NCSMVCE
from LegendSize import LegendSize
from constants import LEGEND_SIZE
from plotting import map_to_arrays
from plotting import save_plot_figure, save_plot_data_file
from transforms import relative_y
from ncsm_out.DataMapNcsmOut import DataMapNcsmOut
from ncsm_vce_lpt.DataMapNcsmVceLpt import DataMapNcsmVceLpt


# todo combine and abstract common parts of these functions

# todo: define A-prescription to be a function as opposed to a tuple, such
# todo: that exact can be treated as a prescription, for example
# todo: (see how this was done in vce_A_depdendence_toy


class DataNotFoundForExpException(Exception):
    pass


def plot_a_aeff_ground_energy_vs_nmax(
        a_aeff_pairs, nmax_range, scale=1.0,
        z=2, n1=15, n2=15, nshell=1, ncomponent=2,
        do_plot=True, transform=relative_y, dm_ncsm=None,
        _dpath_ncsm=DPATH_NCSM_RESULTS, _dpath_plots=DPATH_PLOTS_NCSMVCE
):
    """For the given A, Aeff pairs and Nmax range, plot ground state
    energy vs. Nmax
    :param a_aeff_pairs: sequence of (A, Aeff) pairs
    :param nmax_range: sequence of Nmax values
    :param scale: scale factor
    :param z: proton number (Z)
    :param n1: one-particle TBME interaction truncation
    :param n2: two-particle TBME interaction truncation
    :param nshell: (0=s, 1=p, 2=sd, ...)
    :param ncomponent: 1 -> neutrons, 2 -> protons and neutrons
    :param do_plot: if true, plots the plot to plt and saves the figure;
    otherwise the plots are simply returned
    :param transform: transform to apply to the plots (see transforms.py)
    :param dm_ncsm: existing DataMap to use. If None, one is created here
    :param _dpath_ncsm: path to ncsm results
    :param _dpath_plots: directory in which to save plots
    :return: plots list
    """
    if dm_ncsm is None:
        dm_ncsm = DataMapNcsmOut(
            parent_directory=_dpath_ncsm, exp_list=[(z, n1, n2, scale)])
    dat_ncsm = dm_ncsm[(z, n1, n2, scale)]
    a_aeff_to_x_to_y_map = dict()
    for nmax in nmax_range:
        a_aeff_to_ground_energy = dat_ncsm.a_aeff_to_ground_state_energy_map(
            nmax=nmax, nshell=nshell, ncomponent=ncomponent)
        for a, aeff in a_aeff_pairs:
            if (a, aeff) in a_aeff_to_ground_energy:
                if (a, aeff) not in a_aeff_to_x_to_y_map:
                    a_aeff_to_x_to_y_map[(a, aeff)] = dict()
                a_aeff_to_x_to_y_map[(a, aeff)].update(
                    {nmax: a_aeff_to_ground_energy[(a, aeff)]})
    plots = list()
    for a_aeff, x_to_y_map in sorted(a_aeff_to_x_to_y_map.items()):
        xarr, yarr = map_to_arrays(x_to_y_map)
        plots.append(
            (xarr, yarr, list(), {'name': 'A={}, Aeff={}'.format(*a_aeff)}))
    if transform is not None:
        next_plots = list()
        for plot in plots:
            next_plots.append(transform(*plot))
        plots = next_plots
    plots = sorted(plots, key=lambda p0: p0[3]['name'])
    title = 'NCSM ground state energy vs Nmax'
    labels = [p[3]['name'] for p in plots]
    xlabel, ylabel = 'Nmax', 'E_ncsm (MeV)'
    savename = 'ncsm_A,Aeff{}_Nmax{}_{}_{}_shell{}_dim{}_scale{}'.format(
        a_aeff_pairs, nmax_range, n1, n2, nshell, ncomponent, scale
    ).replace(' ', '')
    if do_plot:
        save_plot_data_file(
            plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
            labels=labels, savepath=path.join(_dpath_plots, savename + '.dat'),
        )
        return save_plot_figure(
            data_plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
            savepath=path.join(_dpath_plots, savename + '.pdf'),
            data_labels=labels, cmap_name='jet',
            data_line_style='-o',
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
    else:
        return plots


def plot_ncsm_exact_for_nmax_and_scale(
        z=2, nmax_range=list([4]), scale_range=list([1.0]),
        n1=15, n2=15, nshell=1, ncomponent=2,
        do_plot=True, transform=None, dm_exact=None,
        _dpath_ncsm=DPATH_NCSM_RESULTS, _dpath_plots=DPATH_PLOTS_NCSMVCE
):
    """Plots No-Core Shell Model exact (Aeff=A) results for the given
    sequences of nmax and scale factors
    :param z: proton number (Z)
    :param nmax_range: sequence of Nmax values to plot
    :param scale_range: sequence of scale factors to plot
    :param n1: one-particle TBME interaction truncation
    :param n2: two-particle TBME interaction truncation
    :param nshell: shell (0=s, 1=p, 2=sd, ...)
    :param ncomponent: 1 -> neutrons, 2 -> protons and neutrons
    :param do_plot: if true, make the plot figure and save it; else return
    the plots list
    :param transform: transform to apply to the plots (see transforms.py)
    :param dm_exact: existing DataMap to use; if None, one is created here
    :param _dpath_ncsm: path to the NCSM results directory
    :param _dpath_plots: directory in which to save the plot figure if do_plot
    is True
    :return: list of plots
    """
    # exact
    if dm_exact is None:
        dm_exact = DataMapNcsmOut(
            parent_directory=_dpath_ncsm,
            exp_list=[(z, n1, n2, sf) for sf in scale_range],)
    plots = list()
    for nmax in nmax_range:
        scale_aeff_gnd = dm_exact.scale_to_aeff_exact_to_ground_energy_map(
            z=z, n1=n1, n2=n2, nmax=nmax, nshell=nshell)
        for scale, aeff_to_ground in scale_aeff_gnd.items():
            x_ex, y_ex = [list(a) for a in map_to_arrays(aeff_to_ground)]
            plots.append(
                (np.array(x_ex), np.array(y_ex), list(),
                 {'name': 'NCSM exact, Nmax={}, scale={}'.format(nmax, scale)})
            )
    if transform is not None:
        next_plots = list()
        for plot in plots:
            next_plots.append(transform(*plot))
        plots = next_plots
    plots = sorted(plots, key=lambda p0: p0[3]['name'])
    title = 'NCSM exact ground state energies'
    labels = [p[3]['name'] for p in plots]
    xlabel, ylabel = 'A', 'E_ncsm (MeV)'
    savename = 'ncsm_exact_Nmax{}_scale{}_{}_{}_shell{}_dim{}'.format(
        nmax_range, list(scale_range), n1, n2, nshell, ncomponent,
    ).replace(' ', '')
    if do_plot:
        save_plot_data_file(
            plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
            labels=labels, savepath=path.join(_dpath_plots, savename + '.dat'),
        )
        return save_plot_figure(
            data_plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
            savepath=path.join(_dpath_plots, savename + '.pdf'),
            data_labels=labels, cmap_name='jet',
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
    else:
        return plots


def plot_ground_state_prescription_error_vs_ncsm_with_aeff(
        a_prescriptions, ncsm_aeff,
        z=2, nmax=4, n1=15, n2=15, nshell=1, ncomponent=2, scalefactor=1.0,
        incl_proton=True,
        do_plot=True,
        transform=None,
        dm_exact=None, dm_vce=None,
        _dpath_ncsm=DPATH_NCSM_RESULTS,
        _dpath_shell=DPATH_SHELL_RESULTS,
        _dpath_plots=DPATH_PLOTS_NCSMVCE,
):
    """Plots prescription error vs NCSM results with the given Aeff
    :param a_prescriptions: list of A-prescriptions to plot
    :param ncsm_aeff: constant Aeff value of the NCSM results to be used
    :param z: proton number (Z)
    :param nmax: major oscillator truncation level
    :param n1: one-particle TBME interaction truncation
    :param n2: two-particle TBME interaction truncation
    :param nshell: (0=s, 1=p, 2=sd,...)
    :param ncomponent: 1 -> neutrons, 2 -> protons and neutrons
    :param scalefactor: factor by which off-diagonal coupling terms were
    scaled
    :param incl_proton: whether the proton part of the interaction was included
    :param do_plot: if true, make and save the plot figure; else just return
    the plots
    :param transform: transform to apply to plots before making figure
    (see transforms.py)
    :param dm_exact: existing DataMap to use for exact NCSM results. If None,
    one is initialized here.
    :param dm_vce: existing DataMap to use for VCE results. If None, one is
    initialized here.
    :param _dpath_ncsm: directory for NCSM results
    :param _dpath_shell: directory for NuShellX results
    :param _dpath_plots: directory in which to save plot figure
    :return: plots list
    """
    # exact
    if dm_exact is None:
        dm_exact = DataMapNcsmOut(
            parent_directory=_dpath_ncsm,
            exp_list=[(z, n1, n2, scalefactor, incl_proton)],
        )
    dat_exact = dm_exact.map.values()[0]
    ncsm_exact_a_aeff = dat_exact.a_aeff_to_ground_state_energy_map(
        nshell=nshell, nmax=nmax, z=z).items()
    next_items = filter(lambda i: i[0][1] == ncsm_aeff, ncsm_exact_a_aeff)
    ncsm_exact = {k[0]: v for k, v in next_items}
    x_ex, y_ex = [list(a) for a in map_to_arrays(ncsm_exact)]
    print('Exact NCSM')
    print('  x_ex = \n    {}'.format(x_ex))
    print('  y_ex = \n    {}'.format([round(yi, 2) for yi in y_ex]))
    # prescriptions
    if dm_vce is None:
        dm_vce = DataMapNcsmVceLpt(parent_directory=_dpath_shell)
    exp_list = [
        dm_vce.exp_type(z, ap, nmax, n1, n2, nshell, ncomponent,
                        scalefactor, incl_proton)
        for ap in a_prescriptions
        ]
    d_vce_list = dm_vce.map.values()
    plots = list()
    for d_vce in d_vce_list:
        if d_vce.exp not in exp_list:
            continue
        vce_ground_energy_map = d_vce.mass_to_ground_energy_map(nshell=nshell)
        x_vce, y_vce = [list(a) for a in map_to_arrays(vce_ground_energy_map)]
        print('Prescription: {}'.format(d_vce.exp.A_presc))
        print('  x_vce = \n    {}'.format(x_vce))
        print('  y_vce = \n    {}'.format([round(yi, 2) for yi in y_vce]))
        x_del = sorted(list(set(x_vce) & set(x_ex)))
        y_del = list()
        for x in x_del:
            y_del.append(y_vce[x_vce.index(x)] - y_ex[x_ex.index(x)])
        print('  x_del = \n    {}'.format(x_del))
        print('  y_del = \n    {}'.format([round(yi, 2) for yi in y_del]))
        x_del = np.array(x_del)
        y_del = np.array(y_del)
        a_presc = d_vce.exp.A_presc
        plot_pr = (x_del, y_del, list(),
                   {'name': '{}, Nmax={}'.format(a_presc, nmax)})
        plots.append(plot_pr)
    if transform is not None:
        next_plots = list()
        for plot in plots:
            next_plots.append(transform(*plot))
        plots = next_plots
    plots = sorted(plots, key=lambda p0: p0[3]['name'])
    title = ('Ground state energy error due to various A-prescriptions with '
             'NCSM Aeff={}').format(ncsm_aeff)
    labels = [p[3]['name'] for p in plots]
    xlabel, ylabel = 'A', 'E_presc - E_ncsm (MeV)'
    savename = 'vce_presc{}_Nmax{}_{}_{}_shell{}_dim{}--aeff{}'.format(
        str(a_prescriptions).replace(' ', ''),
        nmax, n1, n2, nshell, ncomponent, ncsm_aeff
    ).replace(' ', '')
    if scalefactor != 1.0:
        title += (' with off-diagonal coupling terms scaled by '
                  '{}').format(scalefactor)
        savename += '_scale{:.2}'.format(scalefactor)
    if do_plot:
        save_plot_data_file(
            plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
            labels=labels, savepath=path.join(_dpath_plots, savename + '.dat'),
        )
        return save_plot_figure(
            data_plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
            savepath=path.join(_dpath_plots, savename + '.pdf'),
            data_labels=labels, cmap_name='jet',
        )
    else:
        return plots


def plot_ground_state_prescription_error_vs_exact(
        a_prescriptions,
        z=2, nmax=4, n1=15, n2=15, nshell=1, ncomponent=2, scalefactor=1.0,
        incl_proton=True,
        do_plot=True,
        transform=None,
        dm_exact=None, dm_vce=None,
        _dpath_shell=DPATH_SHELL_RESULTS, _dpath_ncsm=DPATH_NCSM_RESULTS,
        _dpath_plots=DPATH_PLOTS_NCSMVCE,
):
    """Plot the ground state energy error for each prescription
    :param a_prescriptions: list of 3-tuples representing A-prescriptions
    :param z: proton number (Z)
    :param nmax: major oscillator truncation
    :param n1: one-particle TBME interaction truncation
    :param n2: two-particle TBME interaction truncation
    :param nshell: (0=s, 1=p, 2=sd, ...)
    :param ncomponent: 1 -> neutrons, 2 -> protons and neutrons
    :param scalefactor: factor by which off-diagonal coupling terms in the
    TBME interaction were scaled
    :param incl_proton: whether or not proton part of the TBME interaction
    was included. 0 => Vpp and Vpn were set to 0.
    :param do_plot: if true, make and save the plot figure; else just return
    the plots
    :param transform: transform to apply to the plots (see transforms.py)
    :param dm_exact: existing DataMap to use for NCSM exact data. If None,
    one is created here.
    :param dm_vce: existing DataMap to use for VCE data. If None,
    one is created here.
    :param _dpath_shell: directory with shell results
    :param _dpath_ncsm: directory with NCSM results
    :param _dpath_plots: directory in which to save plot figure if do_plot is
    true
    :return: list of plots
    """
    # exact
    if dm_exact is None:
        dm_exact = DataMapNcsmOut(
            parent_directory=_dpath_ncsm,
            exp_list=[(z, n1, n2, scalefactor, incl_proton)],
        )
    dat_list = list(dm_exact.map.values())
    if len(dat_list) > 0:
        dat_exact = dat_list.pop()
    else:
        raise DataNotFoundForExpException(
            '\nNo data was found matching the given parameters')
    ncsm_exact = dat_exact.aeff_exact_to_ground_state_energy_map(
        nshell=nshell, nmax=nmax, z=z)
    x_ex, y_ex = [list(a) for a in map_to_arrays(ncsm_exact)]
    print('Exact NCSM')
    print('  x_ex = \n    {}'.format(x_ex))
    print('  y_ex = \n    {}'.format([round(yi, 2) for yi in y_ex]))
    # A = Aeff prescription
    if dm_vce is None:
        dm_vce = DataMapNcsmVceLpt(parent_directory=_dpath_shell)
    aeff_eq_a_map = dm_vce.aeff_eq_a_to_states_map(
        z=z, nmax=nmax, n1=n1, n2=n2,
        nshell=nshell, ncomponent=ncomponent, scalefactor=scalefactor,
        incl_proton=incl_proton,
    )
    x_aaf, y_aaf = [list(a) for a in map_to_arrays(aeff_eq_a_map)]
    print('Prescription: Aeff = A')
    print('  x_aaf = \n    {}'.format(x_aaf))
    print('  y_aaf = \n    {}'.format([round(yi, 2) for yi in y_aaf]))
    x_del = sorted(list(set(x_ex) & set(x_aaf)))
    y_del = list()
    for x in x_del:
        y_del.append(y_aaf[x_aaf.index(x)] - y_ex[x_ex.index(x)])
    print('  x_del = \n    {}'.format(x_del))
    print('  y_del = \n    {}'.format([round(yi, 2) for yi in y_del]))
    plots = [(np.array(x_del), np.array(y_del), list(),
              {'name': 'Aeff = A, Nmax={}'.format(nmax)})]
    # prescriptions
    exp_list = [
        dm_vce.exp_type(z, ap, nmax, n1, n2, nshell, ncomponent,
                        scalefactor, incl_proton)
        for ap in a_prescriptions
        ]
    d_vce_list = dm_vce.map.values()
    for d_vce in d_vce_list:
        if d_vce.exp not in exp_list:
            continue
        vce_ground_energy_map = d_vce.mass_to_ground_energy_map(nshell=nshell)
        x_vce, y_vce = [list(a) for a in map_to_arrays(vce_ground_energy_map)]
        print('Prescription: {}'.format(d_vce.exp.A_presc))
        print('  x_vce = \n    {}'.format(x_vce))
        print('  y_vce = \n    {}'.format([round(yi, 2) for yi in y_vce]))
        x_del = sorted(list(set(x_vce) & set(x_ex)))
        y_del = list()
        for x in x_del:
            y_del.append(y_vce[x_vce.index(x)] - y_ex[x_ex.index(x)])
        print('  x_del = \n    {}'.format(x_del))
        print('  y_del = \n    {}'.format([round(yi, 2) for yi in y_del]))
        x_del = np.array(x_del)
        y_del = np.array(y_del)
        a_presc = d_vce.exp.A_presc
        plot_pr = (x_del, y_del, list(),
                   {'name': '{}, Nmax={}'.format(a_presc, nmax)})
        plots.append(plot_pr)
    if transform is not None:
        next_plots = list()
        for plot in plots:
            next_plots.append(transform(*plot))
        plots = next_plots
    plots = sorted(plots, key=lambda p0: p0[3]['name'])
    title = 'Ground state energy error due to various A-prescriptions'
    labels = [p[3]['name'] for p in plots]
    xlabel, ylabel = 'A', 'E_presc - E_ncsm (MeV)'
    savename = 'vce_presc{}_Nmax{}_{}_{}_shell{}_dim{}'.format(
        str(a_prescriptions).replace(' ', ''),
        nmax, n1, n2, nshell, ncomponent,
    ).replace(' ', '')
    if scalefactor != 1.0:
        title += (' with off-diagonal coupling terms scaled by '
                  '{}').format(scalefactor)
        savename += '_scale{:.2}'.format(scalefactor)
    if do_plot:
        save_plot_data_file(
            plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
            labels=labels, savepath=path.join(_dpath_plots, savename + '.dat'),
        )
        return save_plot_figure(
            data_plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
            savepath=path.join(_dpath_plots, savename + '.pdf'),
            data_labels=labels, cmap_name='jet',
        )
    else:
        return plots
