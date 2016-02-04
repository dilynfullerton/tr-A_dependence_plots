from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from FitFunction import *
from metafitters_mp import *
from metafitters_sp import *
#
# from generate_int import generate_int_file_from_fit_results
from plotting import lpt_plot_energy_vs_mass_for_n
from fit_transforms import *


lpt_plot_energy_vs_mass_for_n(1, proton_num=8, transform=pzbt)

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

# rz = single_particle_first_np_zbt_metafit(1)(
#     fitfn=combine_ffns([linear()],
#                        force_k_func=fk_to_zbt0),
#     e_hw_pairs=[
#         (12, 20),
#         (12, 24, 22),
#         (12, 24, 24)
#     ],
#     show_plot=True,
#     show_fit=True,
#     print_key=False,
#     print_results=True,
#     print_lr_results=False
# )
#
# rsp = single_particle_first_np_metafit(1)(
#     fitfn=combine_ffns([linear(),
#                         # scalar_dependence(['y0'])
#                         ],
#                        force_k_func=fk_to_y0
#                        ),
#     e_hw_pairs=[
#         (12, 20),
#         (12, 24, 22),
#         (12, 24, 24)
#     ],
#     show_plot=True,
#     show_fit=True,
#     print_key=False,
#     print_results=True,
#     print_lr_results=False
# )
#
# rmp = multi_particle_first_np_metafit(1)(
#     fitfn=combine_ffns([linear(),
#                         # scalar_dependence(['y0'])
#                         ],
#                        force_k_func=fk_to_y0
#                        ),
#     e_hw_pairs=[
#         (12, 20),
#         (12, 24, 22),
#         (12, 24, 24)
#     ],
#     show_plot=True,
#     show_fit=True,
#     show_legend=True,
#     print_key=False,
#     print_results=True,
#     print_lr_results=False)
#
# generate_int_file_from_fit_results(
#     results_zbt=rz, results_sp=rsp, results_mp=rmp,
#     e_hw_pairs=[(12, 20), (12, 24, 22), (12, 24, 24)],
#     mass_range=range(17, 29))


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
