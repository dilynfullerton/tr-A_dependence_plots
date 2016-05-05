"""Specific wrappers for the multi-particle meta-fitter
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from transforms import *
from transforms_s import *
from int.metafitter_abs import multi_particle_metafit_int
from constants import DPATH_FILES_INT, DPATH_PLOTS


def multi_particle_relative_pzbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit_int(
            fitfn, e_hw_pairs,
            sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
            transform=relative_y_zbt,
            code='sprpz', mf_name='multi_particle_relative_pzbt_metafit',
            xlabel='A', ylabel='Relative Energy + Zero Body Term (MeV)',
            **kwargs
    )


def multi_particle_pzbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit_int(
        fitfn, e_hw_pairs, sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=pzbt,
        code='mppz', mf_name='multi_particle_pzbt_metafit',
        xlabel='A', ylabel='Energy + Zero Body Term (MeV)', **kwargs
    )


def multi_particle_identity_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit_int(
        fitfn, e_hw_pairs, sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=identity,
        code='mpi', mf_name='multi_particle_identity_metafit',
        xlabel='A', ylabel='Energy (MeV)', **kwargs
    )


def multi_particle_zbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit_int(
        fitfn, e_hw_pairs, sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=zbt, code='mpz', mf_name='multi_particle_zbt_metafit',
        xlabel='A', ylabel='Zero Body Term (MeV)', **kwargs
    )


def multi_particle_relative_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit_int(
        fitfn, e_hw_pairs, sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=relative_y,
        code='mpr', mf_name='multi_particle_relative_metafit',
        xlabel='A', ylabel='Relative Energy (MeV)', **kwargs
    )


def multi_particle_firstp_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit_int(
        fitfn, e_hw_pairs, sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=firstp, super_transform_post=s_combine_like(['interaction']),
        code='mpf1p', mf_name='multi_particle_firstp_metafit',
        xlabel='A', ylabel='Energy (MeV)', **kwargs
    )


def multi_particle_first_np_metafit(n):
    name = b'multi_particle_first_{}p_metafit'.format(n)

    def mpfnp(fitfn, e_hw_pairs, **kwargs):
        return multi_particle_metafit_int(
            fitfn, e_hw_pairs,
            sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
            transform=first_np(n),
            super_transform_post=s_combine_like(['interaction']),
            code='mpf{}p'.format(n), mf_name=name,
            xlabel='A', ylabel='Energy (MeV)', **kwargs
        )
    mpfnp.__name__ = name
    return mpfnp
