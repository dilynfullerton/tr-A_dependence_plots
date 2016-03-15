from __future__ import print_function, division, unicode_literals
from matplotlib import pyplot as plt
from plotting import plot_the_plots, map_to_arrays
from ncsm_out.DataMapNcsmVceOut import DataMapNcsmVceOut
from ncsm_vce_lpt.DataMapNcsmVceLpt import DataMapNcsmVceLpt


def plot_ground_state_prescription_error_vs_exact(
        z, a_prescription,
        nhw=6, n1=15, n2=6
):

    data_maps_exact = DataMapNcsmVceOut(
        parent_directory='../../cougar-ncsm/results',
        exp_list=[(z, nhw, n1, n2)])
    data_maps_vce = DataMapNcsmVceLpt(
        parent_directory='../../cougar-nushellx/results',
        exp_list=[(z, a_prescription, nhw, n1, n2)])

    d_exact = data_maps_exact.map.values()[0]
    d_vce = data_maps_vce.map.values()[0]

    aeff_exact_vs_ground = d_exact.aeff_exact_to_ground_state_energy_map()
    vce_a_vs_zbt = d_vce.mass_zbt_map()
    vce_a_vs_gnd = d_vce.mass_lowest_energy_map()

    x_ex, y_ex = map_to_arrays(aeff_exact_vs_ground)
    x_vce_zbt, y_vce_zbt = map_to_arrays(vce_a_vs_zbt)
    x_vce_0, y_vce_0 = map_to_arrays(vce_a_vs_gnd)
    y_vce = y_vce_0 + y_vce_zbt

    plot_pr = (x_ex, y_vce - y_ex, list(),
               {'name': '{}'.format(a_prescription)})
    plot_ex = (x_ex, y_ex - y_ex, list(),
               {'name': 'Aeff = A'})
    plots = [plot_pr, plot_ex]

    plot_the_plots(
        plots=plots,
        title='Ground state energy error due to A-prescription '
              '{}'.format(a_prescription),
        label='{p}',
        xlabel='A',
        ylabel='E_presc - E_ex',
        get_label_kwargs=lambda p, i: {'p': p[3]['name']},
        sort_key=lambda p: p[3]['name'],
        include_legend=True,
    )
    plt.show()

