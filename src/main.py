from __future__ import division, print_function, unicode_literals
from matplotlib import pyplot as plt
from transforms import cubic_spline
from ncsm_out.plots import plot_ground_state_prescription_error_vs_exact as f

f(
    a_prescriptions=[
        # (4, 4, 4),
        # (4, 4, 5),
        # (4, 4, 6),
        # (4, 4, 7),
        # (4, 5, 5),
        (4, 5, 6),
        # (4, 5, 7),
        # (4, 6, 6),
        # (4, 6, 7),
        # (4, 7, 7),
        # (5, 5, 5),
        # (5, 5, 6),
        # (5, 5, 7),
        # (5, 6, 6),
        # (5, 6, 7),
        # (5, 7, 7),
        # (6, 6, 6),
        # (6, 6, 7),
        # (6, 7, 7),
        # (7, 7, 7),
    ],
    # transform=cubic_spline(500)
)
plt.show()
