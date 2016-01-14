from __future__ import print_function
from __future__ import division
from matplotlib import pyplot as plt
from plotting import plot_energy_vs_mass_for_orbitals as oplot
from plotting import plot_energy_vs_mass_for_interactions as iplot
from fitting import single_particle_energy_curvefit as spec
from fitfns import *


DIR = '../files'
SAVE = '../plots'

# oplot(12, 20, filesdir=DIR, savedir=SAVE, show=True)
# oplot(14, 20, filesdir=DIR, savedir=SAVE, show=True)
# oplot(14, 24, filesdir=DIR, savedir=SAVE, show=True)

# iplot(12, 20, filesdir=DIR, savedir=SAVE, show=True)
# iplot(14, 20, filesdir=DIR, savedir=SAVE, show=True)
# iplot(14, 24, filesdir=DIR, savedir=SAVE, show=True)

spec(polyfit4, e=14, hw=24)
