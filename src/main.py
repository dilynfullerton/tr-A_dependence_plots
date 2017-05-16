#!/bin/python
from __future__ import division, print_function, unicode_literals
from matplotlib import pyplot as plt
from transforms import cubic_spline, filter_evens, filter_odds
from transforms import compose_transforms
from deprecated.ncsm_out.plots import plot_ground_state_prescription_error_vs_exact
from deprecated.ncsm_out.plots import plot_prescription_error_vs_exact_with_ground_state_j
from deprecated.ncsm_out.plots import plot_ground_state_prescription_error_vs_ncsm_with_aeff
from deprecated.ncsm_out.plots import plot_ncsm_exact_for_nmax_and_scale
from deprecated.ncsm_out.plots import plot_a_aeff_ground_energy_vs_nmax
from plotters.plotters import *

if __name__ == '__main__':
    RESULTS_DIR = ('~/workspace/triumf/calculation_results/'
                   'helium_nmax2_scale0_beta0_20170516')
    NCSD_DIR = RESULTS_DIR + '/ncsd'
    NUSHELL_DIR = RESULTS_DIR + '/vce'
    SAVENAME = 'error_he_nmax2_scale0_beta0'
    SUBTITLE = 'Helium (scaled interaction) exact and (4, 5, 6), Nmax=2'

    # make_plot_ncsd_exact(
    #     dpath_ncsd_files=TRDIR+'/tr-c-ncsm/old/results20170224/ncsd/helium',
    #     dpath_plots=TRDIR+'/triumf/tr-c-ncsm/old/results20170224/ncsd',
    #     savename='plot_attempt'
    # )

    make_plot_ground_state_prescription_error_vs_exact(
        dpath_ncsd_files=NCSD_DIR,
        dpath_nushell_files=NUSHELL_DIR,
        dpath_plots=RESULTS_DIR,
        savename=SAVENAME + 'ground_state',
        subtitle=SUBTITLE + ' - Ground state',
        a_prescriptions=[(4, 5, 6)],
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
