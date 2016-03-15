from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from matplotlib import pyplot as plt
from ncsm_out.plots import plot_ground_state_prescription_error_vs_exact as f

f(z=2, a_prescription=(4, 5, 6))
f(z=2, a_prescription=(4, 4, 4))
f(z=2, a_prescription=(5, 5, 5))
f(z=2, a_prescription=(6, 6, 6))
plt.show()
