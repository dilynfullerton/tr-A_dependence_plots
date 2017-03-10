"""metafitters_mp.py
Specific wrappers for the multi-particle (TBME) meta-fitter
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from transforms import *
from transforms_s import *
from int.metafitter_abs import multi_particle_metafit_int
from constants import DPATH_FILES_INT, DPATH_PLOTS


def multi_particle_relative_pzbt_metafit(fitfn, exp_list, **kwargs):
    """Fit to plots of two-body matrix elements plus the zero body term,
    relative to the first point
    """
    return multi_particle_metafit_int(
            fitfn, exp_list,
            sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
            transform=relative_y_zbt,
            code='sprpz', mf_name='multi_particle_relative_pzbt_metafit',
            xlabel='A', ylabel='Relative Energy + Zero Body Term (MeV)',
            **kwargs
    )


def multi_particle_pzbt_metafit(fitfn, exp_list, **kwargs):
    """Fit to plots of two-body matrix elements plus the zero body term
    """
    return multi_particle_metafit_int(
        fitfn, exp_list, sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=pzbt,
        code='mppz', mf_name='multi_particle_pzbt_metafit',
        xlabel='A', ylabel='Energy + Zero Body Term (MeV)', **kwargs
    )


def multi_particle_identity_metafit(fitfn, exp_list, **kwargs):
    """Fit to plots of two-body matrix elements
    """
    return multi_particle_metafit_int(
        fitfn, exp_list, sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=identity,
        code='mpi', mf_name='multi_particle_identity_metafit',
        xlabel='A', ylabel='Energy (MeV)', **kwargs
    )


# Again, this method of doing zero-body terms is kind of a hack.
# A more well-defined method should be developed
def multi_particle_zbt_metafit(fitfn, exp_list, **kwargs):
    """Fit to zero body terms
    """
    return multi_particle_metafit_int(
        fitfn, exp_list, sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=zbt, code='mpz', mf_name='multi_particle_zbt_metafit',
        xlabel='A', ylabel='Zero Body Term (MeV)', **kwargs
    )


def multi_particle_relative_metafit(fitfn, exp_list, **kwargs):
    """Fit to plots of two-body matrix elements relative to the first point
    """
    return multi_particle_metafit_int(
        fitfn, exp_list, sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=relative_y,
        code='mpr', mf_name='multi_particle_relative_metafit',
        xlabel='A', ylabel='Relative Energy (MeV)', **kwargs
    )


def multi_particle_firstp_metafit(fitfn, exp_list, **kwargs):
    """Fit to plots of two-body matrix elements from various normal-ordering
    schemes, where only the first point is taken from each scheme
    """
    return multi_particle_metafit_int(
        fitfn, exp_list, sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
        transform=firstp, super_transform_post=s_combine_like(['interaction']),
        code='mpf1p', mf_name='multi_particle_firstp_metafit',
        xlabel='A', ylabel='Energy (MeV)', **kwargs
    )


def multi_particle_first_np_metafit(n):
    """Fit to plots of two-body matrix elements from various normal-ordering
    schemes, where only the first n points are taken from each scheme
    """
    name = b'multi_particle_first_{}p_metafit'.format(n)

    def mpfnp(fitfn, exp_list, **kwargs):
        return multi_particle_metafit_int(
            fitfn, exp_list,
            sourcedir=DPATH_FILES_INT, savedir=DPATH_PLOTS,
            transform=first_np(n),
            super_transform_post=s_combine_like(['interaction']),
            code='mpf{}p'.format(n), mf_name=name,
            xlabel='A', ylabel='Energy (MeV)', **kwargs
        )
    mpfnp.__name__ = name
    return mpfnp
