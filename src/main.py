from __future__ import division, print_function, unicode_literals
from matplotlib import pyplot as plt
from transforms import cubic_spline
from ncsm_out.plots import plot_ground_state_prescription_error_vs_exact

plot_ground_state_prescription_error_vs_exact(
    a_prescriptions=[
        (4, 5, 6),
    ],
    nmax=6, n1=15, n2=15,
    nshell=1, ncomponent=2,
    abs_value=False,
    # transform=cubic_spline(500)
)
plt.show()
