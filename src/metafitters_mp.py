from constants import FILES_DIR, PLOTS_DIR
from fittransforms import *
from metafit import multi_particle_metafit


def multi_particle_relative_zbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit(fitfn, e_hw_pairs,
                                  sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                  transform=relative_zbt,
                                  code='sprz',
                                  xlabel='A',
                                  ylabel='Relative Single Particle Energy + '
                                         'Zero Body Term (MeV)',
                                  **kwargs)
