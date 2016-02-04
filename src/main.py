from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from FitFunction import *
from metafitters_int_mp import *
from metafitters_int_sp import *
from metafitters_lpt import *

from generate_int import generate_int_file_from_fit_results

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

# generate_int_file_from_fit_results(
#     results_zbt=rz, results_sp=rsp, results_mp=rmp,
#     e_hw_pairs=[(12, 20), (12, 24, 22), (12, 24, 24)],
#     mass_range=range(17, 29))

lpt_pzbt_for_z_in_list_and_n_in_list_metafit(list_z=[8],
                                             list_n=[1])(
    fitfn=linear(),
    show_plot=True
)

# lpt_identity_for_z_in_list_and_n_in_list_metafit(list_z=[8],
#                                                  list_n=[1])(
#     fitfn=linear(),
#     show_plot=True
# )

