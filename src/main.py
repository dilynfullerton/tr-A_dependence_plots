from __future__ import division
from __future__ import print_function

from constants import *
from fitfns import *
from fittransforms import *
from spmetafit import compare_params as compare
from spmetafit import max_r2_value as max_r2
from spmetafit import single_particle_relative_metafit as metaspr
from spmetafit import single_particle_relative_per_nucleon_metafit as metasprpn
from spmetafit import single_particle_relative_zbt_metafit as metasprz


from plotting import plot_energy_vs_mass_for_interactions as iplot
from plotting import plot_energy_vs_mass_for_orbitals as oplot

'''
oplot(12, 20, filesdir=FILES_DIR, savedir=PLOTS_DIR, show=True,
      transform=relative)
oplot(14, 20, filesdir=FILES_DIR, savedir=PLOTS_DIR, show=True,
      transform=relative)
'''
'''
oplot(14, 24, filesdir=FILES_DIR, savedir=PLOTS_DIR, show=True,
      transform=relative)
'''
'''
iplot(12, 20, filesdir=FILES_DIR, savedir=PLOTS_DIR, show=True)
iplot(14, 20, filesdir=FILES_DIR, savedir=PLOTS_DIR, show=True)
iplot(14, 24, filesdir=FILES_DIR, savedir=PLOTS_DIR, show=True)
'''
'''
fitfns_to_test = \
    [poly4_fit_linear_j_tz_dependence_with_forced_zero(17),
     poly4_fit_linear_j_tz_jtz_dependence_with_forced_zero(17),
     poly4_fit_linear_n_j_tz_dependence_with_forced_zero(17),
     poly4_fit_linear_n_j_tz_e_hw_dependence_with_forced_zero(17),
     poly4_fit_quadratic_j_tz_dependence_with_forced_zero(17),
     poly4_fit_quadratic_j_tz_linear_n_dependence_with_forced_zero(17),
     poly4_fit_quadratic_j_tz_linear_n_ephw_dependence_with_forced_zero(17),
     poly4_fit_quadratic_j_tz_linear_n_e_hw_dependence_with_forced_zero(17),
     poly4_fit_quadratic_n_j_tz_linear_ephw_dependence_with_forced_zero(17),
     poly4_fit_quadratic_n_j_tz_linear_e_hw_dependence_with_forced_zero(17),
     poly4_fit_quadratic_n_j_tz_e_hw_dependence_with_forced_zero(17)]
'''

fitfns_to_test = [asymptote1_with_forced_zero(17),
                  asymptote2_with_forced_zero(17),
                  asymptote2_linear_j_tz_dependence_with_forced_zero(17),
                  asymptote2_linear_jjoff_tz_dependence_with_forced_zero(17),
                  asymptote1_linear_joff2_tz_dependence_with_forced_zero(17),
                  asymptote2_linear_joff2_tz_dependence_with_forced_zero(17),
                  asymptote12_linear_joff2_tz_dependence_with_forced_zero(17),
                  asymptote2_quadratic_j_linear_tz_dependence_with_forced_zero(17),
                  asymptote2_linear_with_linear_joff2_tz_dependence_with_forced_zero(17),
                  asymptote2_quadratic_with_linear_joff2_tz_dependence_with_forced_zero(17)]


fitfn, res, rank_map, result_map = max_r2(metasprz, fitfns_to_test,
                                          [(12, 20), (14, 20), (14, 24)],
                                          print_r2_results=True)


ans = compare(metafitter=metasprz,
              fitfn=asymptote2_quadratic_with_linear_joff2_tz_dependence_with_forced_zero(17),
              e_hw_pairs=[(12, 20), (14, 20), (14, 24)],
              depth=2,
              print_compare_results=True,
              show_plot=True,
              show_fit=True,
              print_key=True)

