"""
Functions for making plots from NCSD data
"""
from __future__ import print_function, division, unicode_literals
import numpy as np
from plotting import plot_the_plots, map_to_arrays
from ncsm_out.DataMapNcsmVceOut import DataMapNcsmVceOut
from ncsm_vce_lpt.DataMapNcsmVceLpt import DataMapNcsmVceLpt


def plot_ground_state_prescription_error_vs_exact(
        a_prescriptions, z=2,
        nhw=6, n1=15, n2=6,
        transform=None,
        **kwargs
):
    # exact
    data_maps_exact = DataMapNcsmVceOut(
        parent_directory='../../cougar-ncsm/results',
        exp_list=[(z, nhw, n1, n2)])
    d_exact = data_maps_exact.map.values()[0]
    aeff_exact_vs_ground = d_exact.aeff_exact_to_ground_state_energy_map()
    x_ex, y_ex = [list(a) for a in map_to_arrays(aeff_exact_vs_ground)]
    plots = [(np.array(x_ex), np.array([0*yi for yi in y_ex]),
              list(), {'name': 'Aeff = A'})]
    # prescriptions
    data_maps_vce = DataMapNcsmVceLpt(
        parent_directory='../../cougar-nushellx/results',
        exp_list=[(z, ap, nhw, n1, n2) for ap in a_prescriptions])
    d_vce_list = data_maps_vce.map.values()
    for d_vce in d_vce_list:
        vce_a_vs_zbt = d_vce.mass_zbt_map()
        vce_a_vs_gnd = d_vce.mass_lowest_energy_map()

        x_vce_zbt, y_vce_zbt = [list(a) for a in map_to_arrays(vce_a_vs_zbt)]
        x_vce_0, y_vce_0 = [list(a) for a in map_to_arrays(vce_a_vs_gnd)]

        x_del = list(set(x_vce_0) & set(x_vce_zbt) & set(x_ex))
        y_del = list()
        for x in sorted(x_del):
            y_del.append(y_vce_0[x_vce_0.index(x)] +
                         y_vce_zbt[x_vce_zbt.index(x)] -
                         y_ex[x_ex.index(x)])
        x_del = np.array(x_del)
        y_del = np.array(y_del)
        print(x_del.shape)
        print(y_del.shape)
        a_presc = d_vce.exp.A_presc
        plot_pr = (x_del, y_del, list(), {'name': '{}'.format(a_presc)})
        if transform is not None:
            plot_pr = transform(*plot_pr)
        plots.append(plot_pr)

    # do plots
    return plot_the_plots(
        plots=plots,
        title='Ground state energy error due to various A-prescriptions',
        label='{p}',
        xlabel='A',
        ylabel='E_presc - E_ex',
        get_label_kwargs=lambda p, i: {'p': p[3]['name']},
        sort_key=lambda p: p[3]['name'],
        include_legend=True,
        **kwargs
    )
