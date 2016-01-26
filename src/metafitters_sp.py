from constants import FILES_DIR, PLOTS_DIR
from fit_transforms import *
from fit_transforms_s import *
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


def single_particle_relative_pzbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   transform=relative_zbt,
                                   code='sprpz',
                                   xlabel='A',
                                   ylabel='Relative Single Particle Energy + '
                                          'Zero Body Term (MeV)',
                                   **kwargs)


def single_particle_pzbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   transform=pzbt,
                                   code='sppz',
                                   xlabel='A',
                                   ylabel='Single Particle Energy + '
                                          'Zero Body Term (MeV)',
                                   **kwargs)


def single_particle_relative_xy_pzbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   transform=relative_xy_zbt,
                                   code='sprrpz',
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


def single_particle_zbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   transform=zbt,
                                   xlabel='A',
                                   ylabel='Zero Body Term (MeV)',
                                   **kwargs)


def single_particle_firstp_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   transform=firstp,
                                   super_transform_post=s_combine_like(qnums),
                                   xlabel='A',
                                   ylabel='Energy (MeV)',
                                   data_line_style='-',
                                   fit_line_style='--',
                                   **kwargs)


def single_particle_first2p_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit(fitfn, e_hw_pairs,
                                   sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                   transform=first2p,
                                   xlabel='A',
                                   ylabel='Energy (MeV)',
                                   **kwargs)


# META-FITTER GENERATORS
def single_particle_relative_to_y_pzbt_metafit(x):
    def spryz(fitfn, e_hw_pairs, **kwargs):
        return single_particle_metafit(fitfn, e_hw_pairs,
                                       sourcedir=FILES_DIR, savedir=PLOTS_DIR,
                                       transform=multi([relative_to_y(x),
                                                        pzbt]),
                                       code='sprypz',
                                       xlabel='A',
                                       ylabel='Relative Single Particle Energy'
                                              ' + Zero Body Term '
                                              'with respect to A = '
                                              '{}'.format(x),
                                       **kwargs)

    spryz.__name__ = 'single_particle_relative_to_y({})_pzbt_metafit'.format(x)
    return spryz


def single_particle_ltrim_relative_pzbt_metafit(n):
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

    spltrz.__name__ = ('single_particle_ltrim({})_relative_pzbt_metafit'
                       '').format(n)
    return spltrz
