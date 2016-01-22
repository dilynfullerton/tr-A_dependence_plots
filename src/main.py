from __future__ import division
from __future__ import print_function

from constants import *
from FitFunction import *
from fittransforms import *
from spmetafit import compare_params as compare
from spmetafit import max_r2_value as max_r2
from spmetafit import single_particle_relative_metafit as metaspr
from spmetafit import single_particle_relative_per_nucleon_metafit as metasprpn
from spmetafit import single_particle_relative_zbt_metafit as metasprz
from spmetafit import single_particle_relative_xy_zbt_metafit as metasprrz
from spmetafit import single_particle_zbt_metafit as metaspz

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


asymps = [asymptote(1, 17),
          asymptote(2, 17),
          asymptote_n(17),
          asymptote_with_linear_dependence(2, ['y0'], force_zero=17),
          asymptote_with_asymptotic_dependence(2, ['y0'], force_zero=17),
          asymptote_with_asymptotic_dependence(2, [], [y0pzbt0], 17),
          asymptote_with_asymptotic_dependence(2, [], [joff2], 17),
          combine([asymptote(2), asymptotic_dependence(2, ['y0']),
                   linear_dependence(['y0'])], force_zero=17),
          asymptote_with_linear_dependence(2, [], [y0pzbt0], 17),
          asymptote_with_linear_dependence(2, ['y0', 'zbt0'], force_zero=17),
          asymptote_with_linear_dependence(2, ['j', 'tz'], force_zero=17),
          asymptote_with_linear_dependence(2, ['tz'], [jjoff], 17),
          asymptote_with_linear_dependence(1, ['tz'], [joff2], 17),
          asymptote_with_linear_dependence(2, ['tz'], [joff2], 17),
          combine([asymptote(2), asymptote(1),
                   linear_dependence(['tz'], [joff2])], force_zero=17),
          asymptote_with_linear_dependence(2, ['j', 'y0'], force_zero=17),
          asymptote_with_linear_dependence(2, ['y0'], [joff2], 17),
          asymptote_with_linear_dependence(2, ['j', 'tz', 'y0'], force_zero=17),
          combine([asymptote(2), quadratic_dependence(['j']),
                   linear_dependence(['tz'])], force_zero=17),
          combine([asymptote(2), linear(), linear_dependence(['tz'], [joff2])],
                  force_zero=17),
          combine([asymptote(2), quadratic(),
                   linear_dependence(['tz'], [joff2])], force_zero=17)]

'''
max_r2(metasprz, asymps, [(12, 20), (12, 24), (12, 24, 2), (14, 20), (14, 24)],
       print_r2_results=False,
       print_results=False)
'''

ans = compare(metafitter=metasprz,
              fitfn=asymptote_with_linear_dependence(2, ['y0'],
                                                     force_zero_func=fz_to_x0),
              e_hw_pairs=[(12, 24), (12, 24, 2)],
              depth=2,
              print_compare_results=False,
              show_plot=True,
              show_fit=False,
              print_key=True,
              print_results=False)
