from __future__ import division, print_function, unicode_literals
import numpy as np
from matplotlib import pyplot as plt
from transforms import cubic_spline
from ncsm_out.plots import plot_ground_state_prescription_error_vs_exact
from ncsm_out.plots import plot_ncsm_exact_for_nmax_and_scale
from ncsm_out.plots import plot_a_aeff_ground_energy_vs_nmax

# plot_ground_state_prescription_error_vs_exact(
#     a_prescriptions=[
#         (4, 5, 6),
#         # (5, 5, 5),
#         # (6, 6, 6),
#         # (7, 7, 7),
#         # (8, 8, 8),
#         # (9, 9, 9),
#         # (10, 10, 10),
#     ],
#     nmax=6, n1=15, n2=15,
#     nshell=1, ncomponent=2, scalefactor=0.00,
#     abs_value=False,
#     # transform=cubic_spline(500)
# )

# plot_ncsm_exact_for_nmax_and_scale(
#     # nmax_range=range(0, 7, 2), scale_range=[0.00]
#     nmax_range=[2], scale_range=[x/10 for x in range(11)]
# )

plot_a_aeff_ground_energy_vs_nmax(
    a_aeff_pairs=[(a, aeff) for a in [6] for aeff in [7, 8, 9, 10]],
    nmax_range=range(0, 9, 2),
    scale=0.0, transform=None
)

plt.show()
