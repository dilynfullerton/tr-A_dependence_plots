from __future__ import division
from __future__ import print_function

from fitfns import *
from metafit import single_particle_compare_params as compare
from metafit import single_particle_relative_metafit as metaspr
from metafit import single_particle_max_r2_value as max_r2

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
fitfn, res, rank_map, result_map = max_r2(metaspr, fitfns_to_test,
                                          [(14, 20), (14, 24)],
                                          print_r2_results=True)

'''
ans = metasprpn(
        quadratic_fit_quadratic_j_tz_linear_n_l_e_hw_dependence_with_forced_zero(17),
        [(12, 20), (14, 20), (14, 24)],
        showplot=True,
        printkey=True,
        printresults=True)
'''

ans = compare(metafitter=metaspr,
              fitfn=poly4_fit_linear_n_j_tz_e_hw_dependence_with_forced_zero(
                  17),
              e_hw_pairs=[(12, 20), (14, 20), (14, 24)],
              depth=2,
              print_compare_results=True,
              showplot=True)

'''
metaspr(quadratic_fit_linear_j_tz_dependence_with_forced_zero(17), e=12, hw=20,
        showplot=True,
        printresults=True)
'''
'''
spi(polyfit4, e=12, hw=20,
    show_data_compare=True,
    show_fit_compare=True,
    printkey=True,
    printresults=True)
'''
'''
spi(polyfit4, e=14, hw=24,
    # show_fits=True,
    show_data_compare=True,
    show_fit_compare=True,
    printresults=True)
'''
'''
spd(polyfit4, e=12, hw=20,
    # show_fits=True,
    show_rel_data_compare=True,
    show_rel_fit_compare=True,
    printkey=True,
    printresults=True)
'''
'''
sppn(polyfit2, e=14, hw=24,
     # show_fits=True,
     # show_data_compare=True,
     # show_fit_compare=True,
     printresults=True)
'''
'''
spp(polyfit1, e=12, hw=20,
    xpow=1, ypow=1,
    show_rel_fit_compare=True,
    show_rel_data_compare=True,
    printresults=True)
'''
'''
spll(polyfit1, e=12, hw=20,
     show_rel_data_compare=True,
     show_rel_fit_compare=True,
     printkey=True,
     printresults=True)
'''
