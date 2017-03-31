from __future__ import division, print_function, unicode_literals
from matplotlib import pyplot as plt
from transforms import cubic_spline, filter_evens, filter_odds
from transforms import compose_transforms
from deprecated.ncsm_out.plots import plot_ground_state_prescription_error_vs_exact
from deprecated.ncsm_out.plots import plot_prescription_error_vs_exact_with_ground_state_j
from deprecated.ncsm_out.plots import plot_ground_state_prescription_error_vs_ncsm_with_aeff
from deprecated.ncsm_out.plots import plot_ncsm_exact_for_nmax_and_scale
from deprecated.ncsm_out.plots import plot_a_aeff_ground_energy_vs_nmax
from plotters.plotters import *

TRDIR = '~/workspace/triumf'

# make_plot_ncsd_exact(
#     dpath_ncsd_files='/Users/Alpha/workspace/triumf/tr-c-ncsm/old/results20170224/ncsd/helium',
#     dpath_plots='/Users/Alpha/workspace/triumf/tr-c-ncsm/old/results20170224/ncsd',
#     savename='plot_attempt'
# )

make_plot_ground_state_prescription_error_vs_exact(
    dpath_ncsd_files=TRDIR + '/tr-c-ncsm/results/helium20170330',
    dpath_nushell_files=TRDIR + '/tr-c-nushellx/results/helium20170330',
    dpath_plots=TRDIR + '/tr-c-ncsm/results/helium20170330',
    savename='error_helium_nmax2',
    subtitle='Helium, Nmax=2',
    a_prescriptions=[(4, 5, 6)]
)


# plot_ground_state_prescription_error_vs_exact(
#     a_prescriptions=[
#         (4, 5, 6),
#     ],
#     nmax=4, n1=15, n2=15,
#     nshell=1, ncomponent=2, scalefactor=1.00, z=2,
#     # transform=compose_transforms([cubic_spline(500), filter_evens]),
#     # transform=cubic_spline(500),
#     # transform=filter_evens,
#     # transform=filter_odds,
# )

# plot_ground_state_prescription_error_vs_exact(
#     a_prescriptions=[
#         (16, 17, 18),
#     ],
#     nmax=2, n1=15, n2=15,
#     nshell=2, ncomponent=2, scalefactor=1.00, z=8,
#     # transform=compose_transforms([cubic_spline(500), filter_evens]),
#     # transform=cubic_spline(500),
#     # transform=filter_evens,
#     # transform=filter_odds,
# )

# plot_prescription_error_vs_exact_with_ground_state_j(
#     a_prescriptions=[
#         (4, 5, 6),
#     ],
#     nmax=2, n1=15, n2=15,
#     nshell=1, ncomponent=2, scalefactor=1.00, incl_proton=True, z=2,
#     # transform=compose_transforms([cubic_spline(500), filter_evens]),
#     # transform=cubic_spline(500),
#     # transform=filter_evens,
#     # transform=filter_odds,
# )

# plot_prescription_error_vs_exact_with_ground_state_j(
#     a_prescriptions=[
#         (16, 17, 18),
#     ],
#     nmax=2, n1=15, n2=15,
#     nshell=2, ncomponent=2, scalefactor=1.00, z=8,
#     # transform=compose_transforms([cubic_spline(500), filter_evens]),
#     # transform=cubic_spline(500),
#     # transform=filter_evens,
#     # transform=filter_odds,
# )

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
