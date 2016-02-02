from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from FitFunction import *
from metafitters_mp import *
from metafitters_sp import *

from generate_int import generate_int_file_from_fit_results

fz = None
fzfn = None
fk = None
fkfn = fk_to_y0

simple_asymps = [
    asymptote(1, force_zero=fz, force_zero_func=fzfn,
              force_k=fk, force_k_func=fkfn),
    asymptote(2, force_zero=fz, force_zero_func=fzfn,
              force_k=fk, force_k_func=fkfn),
    asymptote(3, force_zero=fz, force_zero_func=fzfn,
              force_k=fk, force_k_func=fkfn),
    asymptote_n(force_zero=fz, force_zero_func=fzfn,
                force_k=fk, force_k_func=fkfn),
]

dep1_asymps = [
    asymptote_with_linear_dependence(2, ['y0'],
                                     force_zero=fz, force_zero_func=fzfn,
                                     force_k=fk, force_k_func=fkfn),
    asymptote_with_linear_dependence(2, ['j'],
                                     force_zero=fz, force_zero_func=fzfn,
                                     force_k=fk, force_k_func=fkfn),
    asymptote_with_linear_dependence(2, [], [y0pzbt0],
                                     force_zero=fz, force_zero_func=fzfn,
                                     force_k=fk, force_k_func=fkfn),
    asymptote_with_linear_dependence(2, [], [joff2],
                                     force_zero=fz, force_zero_func=fzfn,
                                     force_k=fk, force_k_func=fkfn),
    asymptote_with_asymptotic_dependence(2, ['y0'],
                                         force_zero=fz, force_zero_func=fzfn,
                                         force_k=fk, force_k_func=fkfn),
    asymptote_with_asymptotic_dependence(2, ['j'],
                                         force_zero=fz, force_zero_func=fzfn,
                                         force_k=fk, force_k_func=fkfn),
    asymptote_with_asymptotic_dependence(2, [], [y0pzbt0],
                                         force_zero=fz, force_zero_func=fzfn,
                                         force_k=fk, force_k_func=fkfn),
    asymptote_with_asymptotic_dependence(2, [], [joff2],
                                         force_zero=fz, force_zero_func=fzfn,
                                         force_k=fk, force_k_func=fkfn),
]

dep2_asymps = [
    asymptote_with_linear_dependence(2, ['y0', 'zbt0'],
                                     force_zero=fz, force_zero_func=fzfn,
                                     force_k=fk, force_k_func=fkfn),
    asymptote_with_linear_dependence(2, ['j', 'tz'],
                                     force_zero=fz, force_zero_func=fzfn,
                                     force_k=fk, force_k_func=fkfn),
    asymptote_with_linear_dependence(2, ['tz'], [jjoff],
                                     force_zero=fz, force_zero_func=fzfn,
                                     force_k=fk, force_k_func=fkfn),
    asymptote_with_linear_dependence(1, ['tz'], [joff2],
                                     force_zero=fz, force_zero_func=fzfn,
                                     force_k=fk, force_k_func=fkfn),
    asymptote_with_linear_dependence(2, ['j', 'y0'],
                                     force_zero=fz, force_zero_func=fzfn,
                                     force_k=fk, force_k_func=fkfn),
    asymptote_with_linear_dependence(2, ['y0'], [joff2],
                                     force_zero=fz, force_zero_func=fzfn,
                                     force_k=fk, force_k_func=fkfn),
]

dep3_asymps = [
    asymptote_with_linear_dependence(2, ['j', 'tz', 'y0'],
                                     force_zero=fz, force_zero_func=fzfn,
                                     force_k=fk, force_k_func=fkfn),
]

multi_dep_asymps = [
    combine_ffns([asymptote(2),
                  asymptotic_dependence(2, ['y0']),
                  x1_dependence(['y0'])],
                 force_zero=fz, force_zero_func=fzfn,
                 force_k=fk, force_k_func=fkfn),
    combine_ffns([asymptote(2),
                  asymptotic_dependence(2, [], [y0pzbt0]),
                  x1_dependence([], [y0pzbt0])],
                 force_zero=fz, force_zero_func=fzfn,
                 force_k=fk, force_k_func=fkfn),
    combine_ffns([asymptote(2),
                  x2_dependence(['j']),
                  x1_dependence(['j', 'tz'])],
                 force_zero=fz, force_zero_func=fzfn,
                 force_k=fk, force_k_func=fkfn),
]

mixed = [
    combine_ffns([asymptote(2),
                  asymptote(1),
                  x1_dependence(['tz'], [joff2])],
                 force_zero=fz, force_zero_func=fzfn,
                 force_k=fk, force_k_func=fkfn),
    combine_ffns([asymptote(2),
                  x1(),
                  x1_dependence(['tz'], [joff2])],
                 force_zero=fz, force_zero_func=fzfn,
                 force_k=fk, force_k_func=fkfn),
    combine_ffns([asymptote(2),
                  x1(),
                  x1_dependence(['y0', 'zbt0'],
                                force_zero=fz, force_zero_func=fzfn,
                                force_k=fk, force_k_func=fkfn)],
                 force_zero=fz, force_zero_func=fzfn,
                 force_k=fk, force_k_func=fkfn),
    combine_ffns([asymptote(2),
                  quadratic(),
                  x1_dependence(['y0'], [])],
                 force_zero=fz, force_zero_func=fzfn,
                 force_k=fk, force_k_func=fkfn),
    combine_ffns([asymptote(2),
                  quadratic(),
                  x1_dependence([], [y0pzbt0])],
                 force_zero=fz, force_zero_func=fzfn,
                 force_k=fk, force_k_func=fkfn),
    combine_ffns([asymptote(2),
                  quadratic(),
                  x1_dependence(['j', 'tz'])],
                 force_zero=fz, force_zero_func=fzfn,
                 force_k=fk, force_k_func=fkfn),
    combine_ffns([asymptote(2),
                  quadratic(),
                  x1_dependence(['tz'], [joff2])],
                 force_zero=fz, force_zero_func=fzfn,
                 force_k=fk, force_k_func=fkfn),
    combine_ffns([asymptote(2),
                  quadratic(),
                  x1_dependence(['y0', 'zbt0'])],
                 force_zero=fz, force_zero_func=fzfn,
                 force_k=fk, force_k_func=fkfn),
]

asymps = (simple_asymps + dep1_asymps + dep2_asymps + dep3_asymps +
          multi_dep_asymps + mixed)

# max_r2(multi_particle_firstp_metafit,
#        asymps,
#        [(12, 20),
#         (12, 24, 22),
#         (12, 24, 24)],
#        print_r2_results=True,
#        print_results=False,
#        show_plot=False,
#        show_fit=False)


# f = combine_ffns([asymptote(2),
#                   linear_dependence(['y0'])], force_zero=17)

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

rz = single_particle_first_np_zbt_metafit(1)(
    fitfn=combine_ffns([linear()],
                       force_k_func=fk_to_zbt0),
    e_hw_pairs=[
        (12, 20),
        (12, 24, 22),
        (12, 24, 24)
    ],
    show_plot=True,
    show_fit=True,
    print_key=False,
    print_results=True,
    print_lr_results=False
)

rsp = single_particle_first_np_metafit(1)(
    fitfn=combine_ffns([linear(),
                        # scalar_dependence(['y0'])
                        ],
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
    print_results=True,
    print_lr_results=False
)

rmp = multi_particle_first_np_metafit(1)(
    fitfn=combine_ffns([linear(),
                        # scalar_dependence(['y0'])
                        ],
                       force_k_func=fk_to_y0
                       ),
    e_hw_pairs=[
        (12, 20),
        (12, 24, 22),
        (12, 24, 24)
    ],
    show_plot=True,
    show_fit=True,
    show_legend=True,
    print_key=False,
    print_results=True,
    print_lr_results=False)

generate_int_file_from_fit_results(
    results_zbt=rz, results_sp=rsp, results_mp=rmp,
    e_hw_pairs=[(12, 20), (12, 24, 22), (12, 24, 24)],
    mass_range=range(17, 29))


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
