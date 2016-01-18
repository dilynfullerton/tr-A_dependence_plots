from __future__ import division
from __future__ import print_function

from fitfns import *
from fittransforms import *
from metafit import single_particle_compare_params as compare
from metafit import single_particle_relative_metafit as metaspr
from metafit import single_particle_max_r2_value as max_r2

from plotting import plot_energy_vs_mass_for_interactions as iplot

DIR = '../files'
SAVE = '../plots'

# oplot(12, 20, filesdir=DIR, savedir=SAVE, show=True)
# oplot(14, 20, filesdir=DIR, savedir=SAVE, show=True)
# oplot(14, 24, filesdir=DIR, savedir=SAVE, show=True)

# iplot(12, 20, filesdir=DIR, savedir=SAVE, show=True)
# iplot(14, 20, filesdir=DIR, savedir=SAVE, show=True)
# iplot(14, 24, filesdir=DIR, savedir=SAVE, show=True)


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
fitfn, res, rank_map, result_map = max_r2(metaspr, fitfns_to_test,
                                          [(14, 20), (14, 24)],
                                          print_r2_results=True)
'''
'''
ans = compare(metafitter=metaspr,
              fitfn=poly4_fit_linear_n_j_tz_e_hw_dependence_with_forced_zero(
                  17),
              e_hw_pairs=[(12, 20), (14, 20), (14, 24)],
              depth=2,
              print_compare_results=True,
              showplot=True)
'''
