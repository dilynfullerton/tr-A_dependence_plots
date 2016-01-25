from constants import FILES_DIR, PLOTS_DIR
from fittransforms import *
from metafit import single_particle_metafit


# META-FITTERS
def single_particle_relative_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   code='spr',
                                   **kwargs)


def single_particle_relative_per_nucleon_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   transform=relative_per_nucleon,
                                   code='sprpn',
                                   ylabel='Relative Energy per Nucleon (MeV)',
                                   **kwargs)


def single_particle_relative_log_log_per_nucleon_metafit(fitfn, e_hw_pairs,
                                                         **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   transform=relative_log_log_per_nucleon,
                                   code='sprllpn',
                                   xlabel='log(A)',
                                   ylabel='relative log(Energy per Nucleon)',
                                   **kwargs)


def single_particle_relative_flip_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   transform=relative_flip,
                                   code='sprf',
                                   xlabel='Relative Energy (MeV)',
                                   ylabel='A',
                                   **kwargs)


def single_particle_relative_flip_per_nucleon_metafit(fitfn, e_hw_pairs,
                                                      **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   transform=relative_flip_per_nucleon,
                                   code='sprfpn',
                                   xlabel='Energy per Nucleon (MeV)',
                                   ylabel='Relative A',
                                   **kwargs)


def single_particle_flip_relative_per_nucleon_metafit(fitfn, e_hw_pairs,
                                                      **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   transform=flip_relative_per_nucleon,
                                   code='spfrpn',
                                   xlabel='Relative Energy per Nucleon',
                                   ylabel='A',
                                   **kwargs)


def single_particle_relative_flip_relative_per_nuceon_metafit(fitfn, e_hw_pairs,
                                                              **kwargs):
    return single_particle_metafit(
            fitfn, e_hw_pairs,
            sourcedir=FILES_DIR, savedir=PLOTS_DIR,
            transform=relative_flip_relative_per_nucleon,
            code='sprfrpn',
            xlabel='Relative Energy per Nucleon', ylabel='Relative A',
            **kwargs)


def single_particle_relative_zbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   transform=relative_zbt,
                                   code='sprz',
                                   xlabel='A',
                                   ylabel='Relative Single Particle Energy + '
                                          'Zero Body Term (MeV)',
                                   **kwargs)


def single_particle_zbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   transform=zbt,
                                   code='spz',
                                   xlabel='A',
                                   ylabel='Single Particle Energy + '
                                          'Zero Body Term (MeV)',
                                   **kwargs)


def single_particle_relative_xy_zbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   transform=relative_xy_zbt,
                                   code='sprrz',
                                   xlabel='Relative A',
                                   ylabel='Relative Single Particle Energy + '
                                          'Zero Body Term (MeV)',
                                   **kwargs)


def single_particle_identity_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   transform=identity,
                                   code='spi',
                                   xlabel='A',
                                   ylabel='Single Particle Energy (MeV)',
                                   **kwargs)


# META-FITTER GENERATORS
def single_particle_relative_to_y_zbt_metafit(x):
    def spryz(fitfn, e_hw_pairs, **kwargs):
        return single_particle_metafit(fitfn, e_hw_pairs,
                                       sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                       transform=multi([relative_to_y(x),
                                                        zbt]),
                                       code='spryz',
                                       xlabel='A',
                                       ylabel='Relative Single Particle Energy'
                                              ' + Zero Body Term '
                                              'with respect to A = '
                                              '{}'.format(x),
                                       **kwargs)

    spryz.__name__ = 'single_particle_relative_to_y({})_zbt_metafit'.format(x)
    return spryz


def single_particle_ltrim_relative_zbt_metafit(n):
    def spltrz(fitfn, e_hw_pairs, **kwargs):
        return single_particle_metafit(fitfn, e_hw_pairs,
                                       sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                       transform=multi([
                                           ltrim(n), relative_zbt
                                       ]),
                                       code='spltrz',
                                       xlabel='A',
                                       ylabel='Relative Single Particle Energy'
                                              ' + Zero Body Term',
                                       **kwargs)

    spltrz.__name__ = 'single_particle_ltrim({})_relative_zbt_metafit'.format(n)
    return spltrz
