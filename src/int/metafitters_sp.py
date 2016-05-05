"""Specific wrappers for the single particle meta-fitter
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from transforms import *
from transforms_s import *
from constants import DPATH_FILES_INT, DPATH_PLOTS
from int.metafitter_abs import single_particle_metafit_int


# META-FITTERS
def single_particle_relative_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        code='spr', mf_name='single_particle_relative_metafit', **kwargs
    )


def single_particle_relative_per_nucleon_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=relative_y_div_x,
        code='sprpn', mf_name='single_particle_relative_per_nucleon_metafit',
        ylabel='Relative Energy per Nucleon (MeV)', **kwargs
    )


def single_particle_relative_log_log_per_nucleon_metafit(
        fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=relative_y_log_log_div_x,
        code='sprllpn',
        mf_name='single_particle_relative_log_log_per_nucleon_metafit',
        xlabel='log(A)', ylabel='relative log(Energy per Nucleon)',
        **kwargs
    )


def single_particle_relative_flip_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=relative_y_flip,
        code='sprf', mf_name='single_particle_relative_flip_metafit',
        xlabel='Relative Energy (MeV)', ylabel='A', **kwargs
    )


def single_particle_relative_flip_per_nucleon_metafit(
        fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=relative_y_flip_div_x,
        code='sprfpn',
        mf_name='single_particle_relative_flip_per_nucleon_metafit',
        xlabel='Energy per Nucleon (MeV)', ylabel='Relative A', **kwargs
    )


def single_particle_flip_relative_per_nucleon_metafit(
        fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=flip_relative_y_div_x,
        code='spfrpn',
        mf_name='single_particle_flip_relative_per_nucleon_metafit',
        xlabel='Relative Energy per Nucleon', ylabel='A', **kwargs
    )


def single_particle_relative_flip_relative_per_nuceon_metafit(
        fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=relative_y_flip_relative_y_div_x,
        mf_name='single_particle_relative_flip_relative_per_nuceon_metafit',
        code='sprfrpn',
        xlabel='Relative Energy per Nucleon', ylabel='Relative A', **kwargs
    )


def single_particle_relative_pzbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=relative_y_zbt,
        code='sprpz', mf_name='single_particle_relative_pzbt_metafit',
        xlabel='A',
        ylabel='Relative Single Particle Energy + Zero Body Term (MeV)',
        **kwargs
    )


def single_particle_pzbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS, transform=pzbt,
        code='sppz', mf_name='single_particle_pzbt_metafit',
        xlabel='A', ylabel='Single Particle Energy +Zero Body Term (MeV)',
        **kwargs
    )


def single_particle_relative_xy_pzbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=relative_xy_pzbt,
        code='sprrpz',
        mf_name='single_particle_relative_xy_pzbt_metafit',
        xlabel='Relative A',
        ylabel='Relative Single Particle Energy + Zero Body Term (MeV)',
        **kwargs
    )


def single_particle_identity_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=identity,
        code='spi', mf_name='single_particle_identity_metafit',
        xlabel='A', ylabel='Single Particle Energy (MeV)', **kwargs
    )


def single_particle_zbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs, sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=zbt, mf_name='single_particle_zbt_metafit', code='spz',
        xlabel='A', ylabel='Zero Body Term (MeV)', **kwargs
    )


def single_particle_firstp_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        super_transform=compose_super_transforms(
            list_of_st=[
                s_combine_like(keys=['qnums']),
                s_transform_to_super(transform=firstp)
            ]
        ),
        code='spf1p', mf_name='single_particle_firstp_metafit',
        xlabel='A', ylabel='Energy (MeV)',
        _data_line_style='-', _fit_line_style='--', **kwargs
    )


def single_particle_first2p_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        super_transform=compose_super_transforms(
            list_of_st=[
                s_combine_like(keys=['qnums']),
                s_transform_to_super(transform=first2p)
            ]
        ),
        code='spf2p', mf_name='single_particle_first2p_metafit',
        xlabel='A', ylabel='Energy (MeV)', **kwargs
    )


def single_particle_firstp_zbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        super_transform=compose_super_transforms(
            list_of_st=[
                s_combine_like(keys=[]),
                s_transform_to_super(
                    transform=compose_transforms(
                        list_of_transform=[firstp, zbt]))
            ]
        ),
        code='spf1pz', mf_name='single_particle_firstp_zbt_metafit',
        xlabel='A', ylabel='Zero Body Term (MeV)', **kwargs
    )


def single_particle_first2p_zbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return single_particle_metafit_int(
        fitfn, e_hw_pairs,
        sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        super_transform=compose_super_transforms(
            list_of_st=[
                s_combine_like(keys=[]),
                s_transform_to_super(
                    transform=compose_transforms(
                        list_of_transform=[first2p, zbt]))
            ]
        ),
        code='spf2pz', mf_name='single_particle_first2p_zbt_metafit',
        xlabel='A', ylabel='Zero Body Term (MeV)', **kwargs
    )


# META-FITTER GENERATORS
def single_particle_relative_to_y_pzbt_metafit(x0):
    name = b'single_particle_relative_to_y({})_pzbt_metafit'.format(x)

    def spryz(fitfn, e_hw_pairs, **kwargs):
        return single_particle_metafit_int(
            fitfn, e_hw_pairs,
            sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
            transform=compose_transforms([relative_to_y(x0), pzbt]),
            code='sprypz', mf_name=name,
            xlabel='A',
            ylabel='Relative Single Particle Energy'
                   ' + Zero Body Term with respect to A = {}'.format(x0),
            **kwargs
        )

    spryz.__name__ = name
    return spryz


def single_particle_ltrim_relative_pzbt_metafit(n):
    name = (b'single_particle_ltrim({})_relative_pzbt_metafit'
            b'').format(n)

    def spltrz(fitfn, e_hw_pairs, **kwargs):
        return single_particle_metafit_int(
            fitfn, e_hw_pairs,
            sourcedir=DPATH_FILES_INT,
            savedir=DPATH_PLOTS,
            transform=compose_transforms([ltrim(n), relative_y_zbt]),
            code='spltrz', mf_name=name,
            xlabel='A',
            ylabel='Relative Single Particle Energy + Zero Body Term',
            **kwargs
        )

    spltrz.__name__ = name
    return spltrz


def single_particle_first_np_zbt_metafit(n):
    name = b'single_particle_first_{}p_zbt_metafit'.format(n)

    def spfnpz(fitfn, e_hw_pairs, **kwargs):
        return single_particle_metafit_int(
            fitfn, e_hw_pairs,
            sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
            super_transform=compose_super_transforms(
                list_of_st=[
                    s_combine_like(keys=[]),
                    s_transform_to_super(
                        compose_transforms([first_np(n), zbt]))
                ]
            ),
            code='spf{}pz'.format(n), mf_name=name,
            xlabel='A', ylabel='Zero Body Term (MeV)', **kwargs
        )

    spfnpz.__name__ = name
    return spfnpz


def single_particle_first_np_metafit(n):
    name = b'single_particle_first_{}p_metafit'.format(n)

    def spfnp(fitfn, e_hw_pairs, **kwargs):
        return single_particle_metafit_int(
            fitfn, e_hw_pairs,
            sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
            super_transform=compose_super_transforms(
                list_of_st=[
                    s_combine_like(keys=['qnums']),
                    s_transform_to_super(first_np(n))
                ]
            ),
            code='spf{}p'.format(n), mf_name=name,
            xlabel='A', ylabel='Energy (MeV)', **kwargs
        )

    spfnp.__name__ = name
    return spfnp
