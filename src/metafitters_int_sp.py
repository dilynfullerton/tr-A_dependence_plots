"""Specific wrappers for the single particle meta-fitter
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from constants import DIR_FILES, DIR_PLOTS
from fit_transforms import *
from fit_transforms_s import *
from metafit import single_particle_metafit_int


# META-FITTERS
def single_particle_relative_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DIR_FILES, savedir=DIR_PLOTS,
        code='spr',
        mf_name='single_particle_relative_metafit',
        **kwargs)


def single_particle_relative_per_nucleon_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DIR_FILES, savedir=DIR_PLOTS,
        transform=relative_per_nucleon,
        code='sprpn',
        mf_name='single_particle_relative_per_nucleon_metafit',
        ylabel='Relative Energy per Nucleon (MeV)',
        **kwargs)


def single_particle_relative_log_log_per_nucleon_metafit(fitfn, e_hw_pairs,
                                                         **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DIR_FILES, savedir=DIR_PLOTS,
        transform=relative_log_log_per_nucleon,
        code='sprllpn',
        mf_name='single_particle_relative_log_log_per_nucleon_metafit',
        xlabel='log(A)',
        ylabel='relative log(Energy per Nucleon)',
        **kwargs)


def single_particle_relative_flip_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DIR_FILES, savedir=DIR_PLOTS,
        transform=relative_flip,
        code='sprf',
        mf_name='single_particle_relative_flip_metafit',
        xlabel='Relative Energy (MeV)',
        ylabel='A',
        **kwargs)


def single_particle_relative_flip_per_nucleon_metafit(fitfn, e_hw_pairs,
                                                      **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DIR_FILES, savedir=DIR_PLOTS,
        transform=relative_flip_per_nucleon,
        code='sprfpn',
        mf_name='single_particle_relative_flip_per_nucleon_metafit',
        xlabel='Energy per Nucleon (MeV)',
        ylabel='Relative A',
        **kwargs)


def single_particle_flip_relative_per_nucleon_metafit(fitfn, e_hw_pairs,
                                                      **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DIR_FILES, savedir=DIR_PLOTS,
        transform=flip_relative_per_nucleon,
        code='spfrpn',
        mf_name='single_particle_flip_relative_per_nucleon_metafit',
        xlabel='Relative Energy per Nucleon',
        ylabel='A',
        **kwargs)


def single_particle_relative_flip_relative_per_nuceon_metafit(fitfn, e_hw_pairs,
                                                              **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DIR_FILES, savedir=DIR_PLOTS,
        transform=relative_flip_relative_per_nucleon,
        mf_name='single_particle_relative_flip_relative_per_nuceon_metafit',
        code='sprfrpn',
        xlabel='Relative Energy per Nucleon', ylabel='Relative A',
        **kwargs)


def single_particle_relative_pzbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DIR_FILES, savedir=DIR_PLOTS,
        transform=relative_zbt,
        code='sprpz',
        mf_name='single_particle_relative_pzbt_metafit',
        xlabel='A',
        ylabel='Relative Single Particle Energy + '
               'Zero Body Term (MeV)',
        **kwargs)


def single_particle_pzbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DIR_FILES, savedir=DIR_PLOTS,
        transform=pzbt,
        code='sppz',
        mf_name='single_particle_pzbt_metafit',
        xlabel='A',
        ylabel='Single Particle Energy +Zero Body Term (MeV)',
        **kwargs)


def single_particle_relative_xy_pzbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DIR_FILES, savedir=DIR_PLOTS,
        transform=relative_xy_zbt,
        code='sprrpz',
        mf_name='single_particle_relative_xy_pzbt_metafit',
        xlabel='Relative A',
        ylabel='Relative Single Particle Energy + '
               'Zero Body Term (MeV)',
        **kwargs)


def single_particle_identity_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DIR_FILES, savedir=DIR_PLOTS,
        transform=identity,
        code='spi',
        mf_name='single_particle_identity_metafit',
        xlabel='A',
        ylabel='Single Particle Energy (MeV)',
        **kwargs)


def single_particle_zbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(fitfn, e_hw_pairs,
                                       sourcedir=DIR_FILES, savedir=DIR_PLOTS,
                                       transform=zbt,
                                       mf_name='single_particle_zbt_metafit',
                                       code='spz',
                                       xlabel='A',
                                       ylabel='Zero Body Term (MeV)',
                                       **kwargs)


def single_particle_firstp_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DIR_FILES, savedir=DIR_PLOTS,
        transform=firstp,
        super_transform_post=s_combine_like(['qnums']),
        code='spf1p',
        mf_name='single_particle_firstp_metafit',
        xlabel='A',
        ylabel='Energy (MeV)',
        _data_line_style='-',
        _fit_line_style='--',
        **kwargs)


def single_particle_first2p_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DIR_FILES, savedir=DIR_PLOTS,
        transform=first2p,
        super_transform_post=s_combine_like(['qnums']),
        code='spf2p',
        mf_name='single_particle_first2p_metafit',
        xlabel='A',
        ylabel='Energy (MeV)',
        **kwargs)


def single_particle_firstp_zbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DIR_FILES, savedir=DIR_PLOTS,
        transform=compose_transforms([firstp, zbt]),
        super_transform_post=s_combine_like([]),
        code='spf1pz',
        mf_name='single_particle_firstp_zbt_metafit',
        xlabel='A',
        ylabel='Zero Body Term (MeV)',
        **kwargs
    )


def single_particle_first2p_zbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DIR_FILES, savedir=DIR_PLOTS,
        transform=compose_transforms([first2p, zbt]),
        super_transform_post=s_combine_like([]),
        code='spf2pz',
        mf_name='single_particle_first2p_zbt_metafit',
        xlabel='A',
        ylabel='Zero Body Term (MeV)',
        **kwargs
    )


# META-FITTER GENERATORS
def single_particle_relative_to_y_pzbt_metafit(x):
    name = b'single_particle_relative_to_y({})_pzbt_metafit'.format(x)

    def spryz(fitfn, e_hw_pairs, **kwargs):
        return single_particle_metafit_int(
            fitfn, e_hw_pairs,
            sourcedir=DIR_FILES, savedir=DIR_PLOTS,
            transform=compose_transforms([relative_to_y(x), pzbt]),
            code='sprypz',
            mf_name=name,
            xlabel='A',
            ylabel='Relative Single Particle Energy'
                   ' + Zero Body Term '
                   'with respect to A = '
                   '{}'.format(x),
            **kwargs)

    spryz.__name__ = name
    return spryz


def single_particle_ltrim_relative_pzbt_metafit(n):
    name = (b'single_particle_ltrim({})_relative_pzbt_metafit'
            b'').format(n)

    def spltrz(fitfn, e_hw_pairs, **kwargs):
        return single_particle_metafit_int(
            fitfn, e_hw_pairs,
            sourcedir=DIR_FILES,
            savedir=DIR_PLOTS,
            transform=compose_transforms([ltrim(n), relative_zbt]),
            code='spltrz',
            mf_name=name,
            xlabel='A',
            ylabel='Relative Single Particle Energy + Zero Body Term',
            **kwargs)

    spltrz.__name__ = name
    return spltrz


def single_particle_first_np_zbt_metafit(n):
    name = b'single_particle_first_{}p_zbt_metafit'.format(n)

    def spfnpz(fitfn, e_hw_pairs, **kwargs):
        return single_particle_metafit_int(
            fitfn, e_hw_pairs,
            sourcedir=DIR_FILES, savedir=DIR_PLOTS,
            transform=compose_transforms([first_np(n), zbt]),
            super_transform_post=s_combine_like([]),
            code='spf{}pz'.format(n),
            mf_name=name,
            xlabel='A',
            ylabel='Zero Body Term (MeV)',
            **kwargs)

    spfnpz.__name__ = name
    return spfnpz


def single_particle_first_np_metafit(n):
    name = b'single_particle_first_{}p_metafit'.format(n)

    def spfnp(fitfn, e_hw_pairs, **kwargs):
        return single_particle_metafit_int(
            fitfn, e_hw_pairs,
            sourcedir=DIR_FILES, savedir=DIR_PLOTS,
            transform=first_np(n),
            super_transform_post=s_combine_like(['qnums']),
            code='spf{}p'.format(n),
            mf_name=name,
            xlabel='A',
            ylabel='Energy (MeV)',
            **kwargs)

    spfnp.__name__ = name
    return spfnp
