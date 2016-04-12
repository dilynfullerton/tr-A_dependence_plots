"""
Functions for making plots from NCSD data
"""
from __future__ import print_function, division, unicode_literals
import numpy as np
from os import path
from constants import DPATH_SHELL_RESULTS, DPATH_NCSM_RESULTS
from constants import DPATH_PLOTS_NCSMVCE
from plotting import map_to_arrays
from plotting import save_plot_figure, save_plot_data_file
from ncsm_out.DataMapNcsmVceOut import DataMapNcsmVceOut
from ncsm_vce_lpt.DataMapNcsmVceLpt import DataMapNcsmVceLpt


def plot_ground_state_prescription_error_vs_exact(
        a_prescriptions,
        z=2, nmax=4, n1=15, n2=15, nshell=1, ncomponent=2, scalefactor=None,
        abs_value=False,
        do_plot=True,
        transform=None,
        dm_exact=None, dm_vce=None,
        _dpath_shell=DPATH_SHELL_RESULTS, _dpath_ncsm=DPATH_NCSM_RESULTS,
        _savedir=DPATH_PLOTS_NCSMVCE,
):
    # exact
    if dm_exact is None:
        dm_exact = DataMapNcsmVceOut(
            parent_directory=_dpath_ncsm, exp_list=[(z, n1, n2, scalefactor)],)
    dat_exact = dm_exact.map.values()[0]
    ncsm_exact = dat_exact.aeff_exact_to_ground_state_energy_map(
        nmax=nmax, nshell=nshell, ncomponent=ncomponent,)
    x_ex, y_ex = [list(a) for a in map_to_arrays(ncsm_exact)]
    print('Exact NCSM')
    print('  x_ex = \n    {}'.format(x_ex))
    print('  y_ex = \n    {}'.format([round(yi, 2) for yi in y_ex]))
    # A = Aeff prescription
    if dm_vce is None:
        dm_vce = DataMapNcsmVceLpt(parent_directory=_dpath_shell)
    aeff_eq_a_map = dm_vce.aeff_eq_a_to_ground_energy_map(
        z=z, nmax=nmax, n1=n1, n2=n2,
        nshell=nshell, ncomponent=ncomponent, scalefactor=scalefactor
    )
    x_aaf, y_aaf = [list(a) for a in map_to_arrays(aeff_eq_a_map)]
    print('Prescription: Aeff = A')
    print('  x_aaf = \n    {}'.format(x_aaf))
    print('  y_aaf = \n    {}'.format([round(yi, 2) for yi in y_aaf]))
    x_del = sorted(list(set(x_ex) & set(x_aaf)))
    y_del = list()
    for x in x_del:
        y_del_i = (y_aaf[x_aaf.index(x)] - y_ex[x_ex.index(x)])
        if abs_value:
            y_del.append(abs(y_del_i))
        else:
            y_del.append(y_del_i)
    print('  x_del = \n    {}'.format(x_del))
    print('  y_del = \n    {}'.format([round(yi, 2) for yi in y_del]))
    plots = [(np.array(x_del), np.array(y_del), list(), {'name': 'Aeff = A'})]
    # prescriptions
    exp_list = [
        dm_vce.exp_type(z, ap, nmax, n1, n2, nshell, ncomponent, scalefactor)
        for ap in a_prescriptions
        ]
    d_vce_list = dm_vce.map.values()
    for d_vce in d_vce_list:
        if d_vce.exp not in exp_list:
            continue
        vce_ground_energy_map = d_vce.mass_ground_energy_map()
        x_vce, y_vce = [list(a) for a in map_to_arrays(vce_ground_energy_map)]
        print('Prescription: {}'.format(d_vce.exp.A_presc))
        print('  x_vce = \n    {}'.format(x_vce))
        print('  y_vce = \n    {}'.format([round(yi, 2) for yi in y_vce]))

        x_del = sorted(list(set(x_vce) & set(x_ex)))
        y_del = list()
        for x in x_del:
            y_del_i = (y_vce[x_vce.index(x)] - y_ex[x_ex.index(x)])
            if abs_value:
                y_del.append((abs(y_del_i)))
            else:
                y_del.append(y_del_i)

        print('  x_del = \n    {}'.format(x_del))
        print('  y_del = \n    {}'.format([round(yi, 2) for yi in y_del]))

        x_del = np.array(x_del)
        y_del = np.array(y_del)
        a_presc = d_vce.exp.A_presc
        plot_pr = (x_del, y_del, list(), {'name': '{}'.format(a_presc)})
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
    )
    if scalefactor is not None:
        title += (' with off-diagonal coupling terms scaled by '
                  '{}').format(scalefactor)
        savename += '_scale{:.2}'.format(scalefactor)

    if do_plot:
        save_plot_data_file(
            plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
            labels=labels, savepath=path.join(_savedir, savename + '.dat'),
        )
        return save_plot_figure(
            data_plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
            savepath=path.join(_savedir, savename + '.pdf'),
            data_labels=labels, cmap_name='jet',
        )
    else:
        return plots
