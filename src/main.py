from __future__ import division, print_function, unicode_literals
from matplotlib import pyplot as plt
from transforms import cubic_spline, filter_evens
from ncsm_out.plots import plot_ground_state_prescription_error_vs_exact
from ncsm_out.plots import (
    plot_ground_state_prescription_error_vs_ncsm_with_aeff)
from ncsm_out.plots import plot_ncsm_exact_for_nmax_and_scale
from ncsm_out.plots import plot_a_aeff_ground_energy_vs_nmax

# plot_ground_state_prescription_error_vs_exact(
#     a_prescriptions=[
#         (4, 5, 6),
#     ],
#     nmax=0, n1=15, n2=15,
#     nshell=1, ncomponent=2, scalefactor=1.00, incl_proton=False, z=2,
#     abs_value=False,
#     # transform=filter_evens,
# )

plot_ground_state_prescription_error_vs_exact(
    a_prescriptions=[
        (16, 17, 18),
    ],
    nmax=2, n1=15, n2=15,
    nshell=2, ncomponent=2, scalefactor=1.00, z=8,
    abs_value=False,
    # transform=filter_evens,
)

# plot_ground_state_prescription_error_vs_ncsm_with_aeff(
#     a_prescriptions=[
#         (500, 500, 500),
#     ],
#     ncsm_aeff=500, z=8, nmax=0, nshell=2,
# )

# plot_ncsm_exact_for_nmax_and_scale(
#     # nmax_range=range(0, 7, 2), scale_range=[0.00]
#     nmax_range=[0], scale_range=[x/10 for x in range(11)]
# )

# plot_a_aeff_ground_energy_vs_nmax(
#     a_aeff_pairs=[(a, 500) for a in range(16, 24)],
#     nmax_range=[0],
#     scale=1.0,
#     # transform=None,
# )

plt.show()
