from __future__ import division
from __future__ import print_function

from fitfns import *
from fitting import single_particle_deriv_curvefit as spd
from fitting import single_particle_identity_curvefit as spi
from fitting import single_particle_log_log_curvefit as spll
from fitting import single_particle_per_nucleon_curvefit as sppn
from fitting import single_particle_per_nucleon_power_curvefit as sppnp
from fitting import single_particle_power_curvefit as spp
from metafit import single_particle_relative_metafit as metaspr
from plotting import plot_energy_vs_mass_for_interactions as iplot
from plotting import plot_energy_vs_mass_for_orbitals as oplot

DIR = '../files'
SAVE = '../plots'

# oplot(12, 20, filesdir=DIR, savedir=SAVE, show=True)
# oplot(14, 20, filesdir=DIR, savedir=SAVE, show=True)
# oplot(14, 24, filesdir=DIR, savedir=SAVE, show=True)

# iplot(12, 20, filesdir=DIR, savedir=SAVE, show=True)
# iplot(14, 20, filesdir=DIR, savedir=SAVE, show=True)
# iplot(14, 24, filesdir=DIR, savedir=SAVE, show=True)

metaspr(poly4_fit_quadratic_n_l_j_tz_dependence_with_forced_zero(17),
        e=12, hw=20,
        showplot=True,
        printresults=True)

'''
metaspr(quadratic_fit_linear_j_tz_dependence_with_forced_zero(17), e=12, hw=20,
        showplot=True,
        printresults=True)
'''
'''
spi(polyfit4, e=12, hw=20,
    show_data_compare=True,
    show_fit_compare=True,
    printkey=True,
    printresults=True)
'''
'''
spi(polyfit4, e=14, hw=24,
    # show_fits=True,
    show_data_compare=True,
    show_fit_compare=True,
    printresults=True)
'''
'''
spd(polyfit4, e=12, hw=20,
    # show_fits=True,
    show_rel_data_compare=True,
    show_rel_fit_compare=True,
    printkey=True,
    printresults=True)
'''
'''
sppn(polyfit2, e=14, hw=24,
     # show_fits=True,
     # show_data_compare=True,
     # show_fit_compare=True,
     printresults=True)
'''
'''
spp(polyfit1, e=12, hw=20,
    xpow=1, ypow=1,
    show_rel_fit_compare=True,
    show_rel_data_compare=True,
    printresults=True)
'''
'''
spll(polyfit1, e=12, hw=20,
     show_rel_data_compare=True,
     show_rel_fit_compare=True,
     printkey=True,
     printresults=True)
'''
