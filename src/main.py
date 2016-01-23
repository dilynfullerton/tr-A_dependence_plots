from __future__ import division
from __future__ import print_function

from constants import *
from FitFunction import *
from fittransforms import *
from spmetafit import compare_params as compare
from spmetafit import max_r2_value as max_r2
from spmetafit import single_particle_identity_metafit as spi
from spmetafit import single_particle_relative_metafit as spr
from spmetafit import single_particle_relative_per_nucleon_metafit as sprpn
from spmetafit import single_particle_relative_zbt_metafit as sprz
from spmetafit import single_particle_relative_xy_zbt_metafit as sprrz
from spmetafit import single_particle_zbt_metafit as spz
from spmetafit import single_particle_relative_to_y_zbt_metafit as spryz
from spmetafit import single_particle_ltrim_relative_zbt_metafit as spltrz

from plotting import plot_energy_vs_mass_for_interactions as iplot
from plotting import plot_energy_vs_mass_for_orbitals as oplot

from time import time

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


simple_asymps = [
    asymptote(1, 17),
    asymptote(2, 17),
    asymptote(3, 17),
    asymptote_n(17)
]

dep1_asymps = [
    asymptote_with_linear_dependence(2, ['y0'], force_zero=17),
    asymptote_with_linear_dependence(2, ['j'], force_zero=17),
    asymptote_with_linear_dependence(2, [], [y0pzbt0], 17),
    asymptote_with_linear_dependence(2, [], [joff2], 17),
    asymptote_with_asymptotic_dependence(2, ['y0'], force_zero=17),
    asymptote_with_asymptotic_dependence(2, ['j'], force_zero=17),
    asymptote_with_asymptotic_dependence(2, [], [y0pzbt0], 17),
    asymptote_with_asymptotic_dependence(2, [], [joff2], 17),
]

dep2_asymps = [
    asymptote_with_linear_dependence(2, ['y0', 'zbt0'], force_zero=17),
    asymptote_with_linear_dependence(2, ['j', 'tz'], force_zero=17),
    asymptote_with_linear_dependence(2, ['tz'], [jjoff], 17),
    asymptote_with_linear_dependence(1, ['tz'], [joff2], 17),
    asymptote_with_linear_dependence(2, ['j', 'y0'], force_zero=17),
    asymptote_with_linear_dependence(2, ['y0'], [joff2], 17),
]

dep3_asymps = [
    asymptote_with_linear_dependence(2, ['j', 'tz', 'y0'], force_zero=17),
]

multi_dep_asymps = [
    combine([asymptote(2),
             asymptotic_dependence(2, ['y0']),
             x1_dependence(['y0'])], force_zero=17),
    combine([asymptote(2),
             asymptotic_dependence(2, [], [y0pzbt0]),
             x1_dependence([], [y0pzbt0])], force_zero=17),
    combine([asymptote(2),
             x2_dependence(['j']),
             x1_dependence(['j', 'tz'])], force_zero=17),
]

mixed = [
    combine([asymptote(2),
             asymptote(1),
             x1_dependence(['tz'], [joff2])], force_zero=17),
    combine([asymptote(2),
             x1(),
             x1_dependence(['tz'], [joff2])], force_zero=17),
    combine([asymptote(2),
             x1(),
             x1_dependence(['y0', 'zbt0'], force_zero=17)], force_zero=17),
    combine([asymptote(2),
             quadratic(),
             x1_dependence(['y0'], [])], force_zero=17),
    combine([asymptote(2),
             quadratic(),
             x1_dependence([], [y0pzbt0])], force_zero=17),
    combine([asymptote(2),
             quadratic(),
             x1_dependence(['j', 'tz'])], force_zero=17),
    combine([asymptote(2),
             quadratic(),
             x1_dependence(['tz'], [joff2])], force_zero=17),
    combine([asymptote(2),
             quadratic(),
             x1_dependence(['y0', 'zbt0'])], force_zero=17),
]

asymps = (simple_asymps + dep1_asymps + dep2_asymps + dep3_asymps +
          multi_dep_asymps + mixed)


max_r2(sprz, asymps, [(12, 20),
                      (14, 20), (14, 24)],
       print_r2_results=True,
       print_results=False)


f = asymptote_with_linear_dependence(2, ['y0'], [], force_zero=17)

ans = compare(metafitter=spltrz(0),
              fitfn=f,
              e_hw_pairs=[
                  (12, 20),
                  (14, 20), (14, 24),
                  # (12, 24)  # , (12, 24, 2)
              ],
              depth=2,
              print_compare_results=True,
              show_plot=True,
              show_fit=True,
              print_key=False,
              print_results=False)
