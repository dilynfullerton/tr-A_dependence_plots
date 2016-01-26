from constants import FILES_DIR, PLOTS_DIR
from fittransforms import *
from metafit import multi_particle_metafit


def multi_particle_relative_pzbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit(fitfn, e_hw_pairs,
                                  sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                  transform=relative_zbt,
                                  code='sprpz',
                                  xlabel='A',
                                  ylabel='Relative Energy + '
                                         'Zero Body Term (MeV)',
                                  **kwargs)


def multi_particle_pzbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit(fitfn, e_hw_pairs,
                                  sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                  transform=pzbt,
                                  code='mppz',
                                  xlabel='A',
                                  ylabel='Energy + Zero Body Term (MeV)',
                                  **kwargs)


def multi_particle_identity_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit(fitfn, e_hw_pairs,
                                  sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                  transform=identity,
                                  code='mpi',
                                  xlabel='A',
                                  ylabel='Energy (MeV)',
                                  **kwargs)


def multi_particle_zbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit(fitfn, e_hw_pairs,
                                  sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                  transform=zbt,
                                  code='mpz',
                                  xlabel='A',
                                  ylabel='Zero Body Term (MeV)',
                                  **kwargs)
