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
from spmetafit import single_particle_zbt_metafit as metaspz


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


asymps = [asymptote1_with_forced_zero(17),
          asymptote2_with_forced_zero(17),
          asymptote_n_with_forced_zero(17),
          asymptote2_asymptotic_y0_dependence_with_forced_zero(17),
          asymptote2_asymptotic_y0pzbt0_dependence_with_forced_zero(17),
          asymptote2_asymptotic_joff2_dependence_with_forced_zero(17),
          asymptote2_asymptotic_and_linear_y0_dependence_with_forced_zero(17),
          asymptote2_linear_y0_dependence_with_forced_zero(17),
          asymptote2_linear_y0pzbt0_dependence_with_forced_zero(17),
          asymptote2_linear_y0_zbt0_dependence_with_forced_zero(17),
          asymptote2_linear_j_tz_dependence_with_forced_zero(17),
          asymptote2_linear_jjoff_tz_dependence_with_forced_zero(17),
          asymptote1_linear_joff2_tz_dependence_with_forced_zero(17),
          asymptote2_linear_joff2_tz_dependence_with_forced_zero(17),
          asymptote12_linear_joff2_tz_dependence_with_forced_zero(17),
          asymptote2_linear_j_y0_dependence_with_forced_zero(17),
          asymptote2_linear_joff2_y0_dependence_with_forced_zero(17),
          asymptote2_linear_j_tz_y0_dependence_with_forced_zero(17),
          asymptote2_quadratic_j_linear_tz_dependence_with_forced_zero(17),
          asymptote2_linear_with_linear_joff2_tz_dependence_with_forced_zero(17),
          asymptote2_quadratic_with_linear_joff2_tz_dependence_with_forced_zero(17)]


fitfn, res, rank_map, result_map = max_r2(metasprz, asymps,
                                          [(12, 20), (14, 20), (14, 24)],
                                          print_r2_results=True)


ans = compare(metafitter=metasprz,
              fitfn=asymptote2_with_forced_zero(17),
              e_hw_pairs=[(12, 20), (14, 20), (14, 24)],
              depth=2,
              print_compare_results=True,
              show_plot=True,
              show_fit=True,
              print_key=False,
              print_results=False)

