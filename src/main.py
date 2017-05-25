#!/bin/python
from __future__ import division, print_function, unicode_literals
from matplotlib import pyplot as plt
from plotters.plotters import *

if __name__ == '__main__':
    RESULTS_DIR = ('~/workspace/triumf/calculation_results/'
                   'lithium_nmax4_iter500_20170519')
    NCSD_DIR = RESULTS_DIR + '/ncsd'
    NUSHELL_DIR = RESULTS_DIR + '/vce'
    SAVENAME = 'li_nmax4_iter500_V2'
    SUBTITLE = 'Lithium exact, (4, 5, 6), (6, 7, 8); Nmax=4'

    make_plot_ncsd_exact(
        dpath_ncsd_files=NCSD_DIR,
        dpath_plots=RESULTS_DIR,
        savename='ncsd_all_states_'+SAVENAME,
        subtitle='Lithium; Nmax=4',
    )

    plt.show()

    make_plot_ground_state_prescription_error_vs_exact(
        dpath_ncsd_files=NCSD_DIR,
        dpath_nushell_files=NUSHELL_DIR,
        dpath_plots=RESULTS_DIR,
        savename='error_'+SAVENAME+'_ground_state',
        subtitle=SUBTITLE+' - Ground state',
        a_prescriptions=[(4, 5, 6), (6, 7, 8)],
    )

    plt.show()

    # make_plots_states_with_ground_j_prescription_error_vs_exact(
    #     dpath_ncsd_files=NCSD_DIR,
    #     dpath_nushell_files=NUSHELL_DIR,
    #     dpath_plots=RESULTS_DIR,
    #     savename=SAVENAME + 'states_with_ground_j',
    #     subtitle=SUBTITLE + ' - States with Ground J',
    #     a_prescriptions=[(4, 5, 6)]
    # )
    #
    # plt.show()
