from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from FitFunction import *
from metafit import compare_params as compare
from metafit import max_r2_value as max_r2

from metafitters_sp import *
from metafitters_mp import *


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
    combine_ffns([asymptote(2),
                  asymptotic_dependence(2, ['y0']),
                  x1_dependence(['y0'])], force_zero=17),
    combine_ffns([asymptote(2),
                  asymptotic_dependence(2, [], [y0pzbt0]),
                  x1_dependence([], [y0pzbt0])], force_zero=17),
    combine_ffns([asymptote(2),
                  x2_dependence(['j']),
                  x1_dependence(['j', 'tz'])], force_zero=17),
]

mixed = [
    combine_ffns([asymptote(2),
                  asymptote(1),
                  x1_dependence(['tz'], [joff2])], force_zero=17),
    combine_ffns([asymptote(2),
                  x1(),
                  x1_dependence(['tz'], [joff2])], force_zero=17),
    combine_ffns([asymptote(2),
                  x1(),
                  x1_dependence(['y0', 'zbt0'], force_zero=17)], force_zero=17),
    combine_ffns([asymptote(2),
                  quadratic(),
                  x1_dependence(['y0'], [])], force_zero=17),
    combine_ffns([asymptote(2),
                  quadratic(),
                  x1_dependence([], [y0pzbt0])], force_zero=17),
    combine_ffns([asymptote(2),
                  quadratic(),
                  x1_dependence(['j', 'tz'])], force_zero=17),
    combine_ffns([asymptote(2),
                  quadratic(),
                  x1_dependence(['tz'], [joff2])], force_zero=17),
    combine_ffns([asymptote(2),
                  quadratic(),
                  x1_dependence(['y0', 'zbt0'])], force_zero=17),
]

asymps = (simple_asymps + dep1_asymps + dep2_asymps + dep3_asymps +
          multi_dep_asymps + mixed)

'''
max_r2(single_particle_relative_pzbt_metafit,
       asymps, [(12, 20), (14, 20), (14, 24)],
       print_r2_results=True,
       print_results=False)
'''

f = combine_ffns([asymptote(2),
                  linear_dependence(['y0'])], force_zero=17)

# ans = compare(metafitter=single_particle_identity_metafit,
#               fitfn=f,
#               e_hw_pairs=[
#                   (12, 20),
#                   (14, 20),
#                   (14, 24),
#                   (12, 24, 22),
#                   (12, 24, 24)
#               ],
#               depth=2,
#               print_compare_results=True,
#               show_plot=True,
#               show_fit=False,
#               show_legend=True,
#               print_key=False,
#               print_results=False)

single_particle_firstp_metafit(
    fitfn=combine_ffns([linear()],
                       force_k_func=fk_to_y0
                       ),
    e_hw_pairs=[
        (12, 20),
        (12, 24, 22),
        (12, 24, 24)
    ],
    show_plot=True,
    show_fit=True,
    print_key=False,
    print_results=False

)

single_particle_firstp_zbt_metafit(
    fitfn=combine_ffns([asymptote(1)],
                       force_k_func=fk_to_zbt0
                       ),
    e_hw_pairs=[
        (12, 20),
        (12, 24, 22, None),
        (12, 24, 24, None)
    ],
    show_plot=True,
    show_fit=True,
    print_key=False,
    print_results=False
)

multi_particle_identity_metafit(
        fitfn=asymptote(2,
                        #force_zero=17,
                        force_k_func=fk_to_y0),
        e_hw_pairs=[
            (12, 20),
            (12, 24, 22),
            (12, 24, 24)
        ],
        show_plot=True,
        show_fit=True,
        show_legend=True,
        print_key=False,
        print_results=False)

# multi_particle_relative_pzbt_metafit(
#     fitfn=combine_ffns([asymptote(2)], force_zero_func=fz_to_x0),
#     e_hw_pairs=[
#         (12, 20),
#         #(12, 24, 22),
#         #(12, 24, 24)
#     ],
#     show_plot=True,
#     show_fit=True,
#     show_legend=True
# )
