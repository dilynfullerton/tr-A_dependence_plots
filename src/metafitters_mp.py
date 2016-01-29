from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from constants import DIR_FILES, DIR_PLOTS
from fit_transforms import *
from fit_transforms_s import *
from metafit import multi_particle_metafit


def multi_particle_relative_pzbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit(
            fitfn, e_hw_pairs,
            sourcedir=DIR_FILES, savedir=DIR_PLOTS,
            transform=relative_zbt,
            code='sprpz',
            mf_name='multi_particle_relative_pzbt_metafit',
            xlabel='A',
            ylabel='Relative Energy + '
                   'Zero Body Term (MeV)',
            **kwargs)


def multi_particle_pzbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit(fitfn, e_hw_pairs,
                                  sourcedir=DIR_FILES, savedir=DIR_PLOTS,
                                  transform=pzbt,
                                  code='mppz',
                                  mf_name='multi_particle_pzbt_metafit',
                                  xlabel='A',
                                  ylabel='Energy + Zero Body Term (MeV)',
                                  **kwargs)


def multi_particle_identity_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit(fitfn, e_hw_pairs,
                                  sourcedir=DIR_FILES, savedir=DIR_PLOTS,
                                  transform=identity,
                                  code='mpi',
                                  mf_name='multi_particle_identity_metafit',
                                  xlabel='A',
                                  ylabel='Energy (MeV)',
                                  **kwargs)


def multi_particle_zbt_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit(fitfn, e_hw_pairs,
                                  sourcedir=DIR_FILES, savedir=DIR_PLOTS,
                                  transform=zbt,
                                  code='mpz',
                                  mf_name='multi_particle_zbt_metafit',
                                  xlabel='A',
                                  ylabel='Zero Body Term (MeV)',
                                  **kwargs)


def multi_particle_relative_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit(fitfn, e_hw_pairs,
                                  sourcedir=DIR_FILES, savedir=DIR_PLOTS,
                                  transform=relative_y,
                                  code='mpr',
                                  mf_name='multi_particle_relative_metafit',
                                  xlabel='A',
                                  ylabel='Relative Energy (MeV)',
                                  **kwargs)


def multi_particle_firstp_metafit(fitfn, e_hw_pairs, **kwargs):
    return multi_particle_metafit(
            fitfn, e_hw_pairs,
            sourcedir=DIR_FILES, savedir=DIR_PLOTS,
            transform=firstp,
            super_transform_post=s_combine_like(['interaction']),
            code='mpf1p',
            mf_name='multi_particle_firstp_metafit',
            xlabel='A',
            ylabel='Energy (MeV)',
            **kwargs)
