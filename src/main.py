from __future__ import print_function
from __future__ import division
from matplotlib import pyplot as plt
from plotting import plot_energy_vs_mass_for_orbitals as oplot
from plotting import plot_energy_vs_mass_for_interactions as iplot
from fitting import single_particle_energy_curvefit as spec
from fitting import single_particle_deriv_curvefit as spdc
from fitting import single_particle_log_log_curvefit as spllc
from fitting import single_particle_identity_curvefit as spic
from fitting import single_particle_per_nucleon_curvefit as sppnc
from fitfns import *


DIR = '../files'
SAVE = '../plots'

# oplot(12, 20, filesdir=DIR, savedir=SAVE, show=True)
# oplot(14, 20, filesdir=DIR, savedir=SAVE, show=True)
# oplot(14, 24, filesdir=DIR, savedir=SAVE, show=True)

# iplot(12, 20, filesdir=DIR, savedir=SAVE, show=True)
# iplot(14, 20, filesdir=DIR, savedir=SAVE, show=True)
# iplot(14, 24, filesdir=DIR, savedir=SAVE, show=True)

'''
spic(polyfit4, e=12, hw=20,
     show_fits=True,
     show_data_compare=True,
     show_rel_data_compare=True)
'''
'''
spdc(polyfit4, e=14, hw=24,
     show_fits=True,
     show_data_compare=True,
     show_rel_data_compare=True)
'''
'''
spllc(polyfit4, e=14, hw=24,
      show_fits=True,
      show_data_compare=True,
      show_rel_data_compare=True)
'''

sppnc(polyfit2, e=12, hw=20,
      show_data_compare=True,
      show_rel_data_compare=True)
