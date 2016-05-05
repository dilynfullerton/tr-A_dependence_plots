"""metafitters_sp.py
Specific wrappers for the single particle meta-fitter
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from transforms import *
from transforms_s import *
from constants import DPATH_FILES_INT, DPATH_PLOTS
from int.metafitter_abs import single_particle_metafit_int


# META-FITTERS
def single_particle_relative_metafit(fitfn, exp_list, **kwargs):
    """Fit to single-particle energies, relative to the first point
    """
    return single_particle_metafit_int(
        fitfn, exp_list,
        dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
        code='spr', mf_name='single_particle_relative_metafit', **kwargs
    )


def single_particle_relative_per_nucleon_metafit(fitfn, exp_list, **kwargs):
    """Fit to single-particle energies per mass number, relative to the first
    point
    """
    return single_particle_metafit_int(
        fitfn, exp_list,
        dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
        transform=relative_y_div_x,
        code='sprpn', mf_name='single_particle_relative_per_nucleon_metafit',
        ylabel='Relative Energy per Nucleon (MeV)', **kwargs
    )


def single_particle_relative_log_log_per_nucleon_metafit(
        fitfn, exp_list, **kwargs):
    """Fit to log-log plots of single-particle energies, relative to the first
    point
    """
    return single_particle_metafit_int(
        fitfn, exp_list,
        dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
        transform=relative_y_log_log_div_x,
        code='sprllpn',
        mf_name='single_particle_relative_log_log_per_nucleon_metafit',
        xlabel='log(A)', ylabel='relative log(Energy per Nucleon)',
        **kwargs
    )


def single_particle_relative_flip_metafit(fitfn, exp_list, **kwargs):
    """Fit to single-particle energies with axes flipped, relative to the
    first point
    """
    return single_particle_metafit_int(
        fitfn, exp_list,
        dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
        transform=relative_y_flip,
        code='sprf', mf_name='single_particle_relative_flip_metafit',
        xlabel='Relative Energy (MeV)', ylabel='A', **kwargs
    )


def single_particle_relative_flip_per_nucleon_metafit(
        fitfn, exp_list, **kwargs):
    """Fit to single-particle energies per mass number with axes flipped,
    relative to the first point
    """
    return single_particle_metafit_int(
        fitfn, exp_list,
        dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
        transform=relative_y_flip_div_x,
        code='sprfpn',
        mf_name='single_particle_relative_flip_per_nucleon_metafit',
        xlabel='Energy per Nucleon (MeV)', ylabel='Relative A', **kwargs
    )


def single_particle_flip_relative_per_nucleon_metafit(
        fitfn, exp_list, **kwargs):
    """Fit to single-particle energies per mass number, relative to the first
    point, with axes flipped. This is similar to the previous function, but
    transformations are done in a different order.
    """
    return single_particle_metafit_int(
        fitfn, exp_list,
        dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
        transform=flip_relative_y_div_x,
        code='spfrpn',
        mf_name='single_particle_flip_relative_per_nucleon_metafit',
        xlabel='Relative Energy per Nucleon', ylabel='A', **kwargs
    )


def single_particle_relative_flip_relative_per_nuceon_metafit(
        fitfn, exp_list, **kwargs):
    """Fit to single-particle energies per mass number, relative to the first
    point, with axes flipped, relative to the first point.
    """
    return single_particle_metafit_int(
        fitfn, exp_list,
        dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
        transform=relative_y_flip_relative_y_div_x,
        mf_name='single_particle_relative_flip_relative_per_nuceon_metafit',
        code='sprfrpn',
        xlabel='Relative Energy per Nucleon', ylabel='Relative A', **kwargs
    )


def single_particle_relative_pzbt_metafit(fitfn, exp_list, **kwargs):
    """Fit to single-particle energies plus zero body term, relative to the
    first point
    """
    return single_particle_metafit_int(
        fitfn, exp_list,
        dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
        transform=relative_y_zbt,
        code='sprpz', mf_name='single_particle_relative_pzbt_metafit',
        xlabel='A',
        ylabel='Relative Single Particle Energy + Zero Body Term (MeV)',
        **kwargs
    )


def single_particle_pzbt_metafit(fitfn, exp_list, **kwargs):
    """Fit to single-particle energies plus zero body term
    """
    return single_particle_metafit_int(
        fitfn, exp_list,
        dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS, transform=pzbt,
        code='sppz', mf_name='single_particle_pzbt_metafit',
        xlabel='A', ylabel='Single Particle Energy +Zero Body Term (MeV)',
        **kwargs
    )


def single_particle_relative_xy_pzbt_metafit(fitfn, exp_list, **kwargs):
    """Fit to single-particle energies plus zero body term, relative to first
    x and first y
    """
    return single_particle_metafit_int(
        fitfn, exp_list,
        dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
        transform=relative_xy_pzbt,
        code='sprrpz',
        mf_name='single_particle_relative_xy_pzbt_metafit',
        xlabel='Relative A',
        ylabel='Relative Single Particle Energy + Zero Body Term (MeV)',
        **kwargs
    )


def single_particle_identity_metafit(fitfn, exp_list, **kwargs):
    """Fit to single-particle energies
    """
    return single_particle_metafit_int(
        fitfn, exp_list,
        dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
        transform=identity,
        code='spi', mf_name='single_particle_identity_metafit',
        xlabel='A', ylabel='Single Particle Energy (MeV)', **kwargs
    )


# todo: This is a hack. The method for fitting to zero body term should be
# todo: well defined
def single_particle_zbt_metafit(fitfn, exp_list, **kwargs):
    """Fit to zero-body terms
    """
    return single_particle_metafit_int(
        fitfn, exp_list, dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
        transform=zbt, mf_name='single_particle_zbt_metafit', code='spz',
        xlabel='A', ylabel='Zero Body Term (MeV)', **kwargs
    )


def single_particle_firstp_metafit(fitfn, exp_list, **kwargs):
    """Fit to single-particle energies for available normal-ordering
    schemes, taking only the first point from each
    """
    return single_particle_metafit_int(
        fitfn, exp_list,
        dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
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


def single_particle_first2p_metafit(fitfn, exp_list, **kwargs):
    """Fit to single-particle energies for all available normal-ordering
    schemes, taking only the first two points from each
    """
    return single_particle_metafit_int(
        fitfn, exp_list,
        dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
        super_transform=compose_super_transforms(
            list_of_st=[
                s_combine_like(keys=['qnums']),
                s_transform_to_super(transform=first2p)
            ]
        ),
        code='spf2p', mf_name='single_particle_first2p_metafit',
        xlabel='A', ylabel='Energy (MeV)', **kwargs
    )


# todo: Hack! Plots for zero body terms should be well-defined
def single_particle_firstp_zbt_metafit(fitfn, exp_list, **kwargs):
    """Fit to zero body terms for all available normal-ordering schemes,
    taking only the first point from each
    """
    return single_particle_metafit_int(
        fitfn, exp_list,
        dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
        super_transform=compose_super_transforms(
            list_of_st=[
                s_combine_like(keys=[]),
                s_transform_to_super(
                    transform=compose_transforms([firstp, zbt]))
            ]
        ),
        code='spf1pz', mf_name='single_particle_firstp_zbt_metafit',
        xlabel='A', ylabel='Zero Body Term (MeV)', **kwargs
    )


def single_particle_first2p_zbt_metafit(fitfn, exp_list, **kwargs):
    """Fit to zero body terms for all available normal-ordering schemes,
    taking only the first 2 points from each
    """
    return single_particle_metafit_int(
        fitfn, exp_list,
        dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
        super_transform=compose_super_transforms(
            list_of_st=[
                s_combine_like(keys=[]),
                s_transform_to_super(compose_transforms([first2p, zbt]))
            ]
        ),
        code='spf2pz', mf_name='single_particle_first2p_zbt_metafit',
        xlabel='A', ylabel='Zero Body Term (MeV)', **kwargs
    )


# META-FITTER GENERATORS
def single_particle_relative_to_y_pzbt_metafit(x0):
    """Returns a metafitter that fits to single-particle energies + zero body
    term relative to the value at x=x0
    """
    name = b'single_particle_relative_to_y({})_pzbt_metafit'.format(x)

    def spryz(fitfn, exp_list, **kwargs):
        return single_particle_metafit_int(
            fitfn, exp_list,
            dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
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
    """Returns a metafitter that fits to single-particle energies + zero body
    term, relative to the first point, with the first n point removed
    :param n: number of points to remove from the left
    """
    name = (b'single_particle_ltrim({})_relative_pzbt_metafit'
            b'').format(n)

    def spltrz(fitfn, exp_list, **kwargs):
        return single_particle_metafit_int(
            fitfn, exp_list,
            dpath_sources=DPATH_FILES_INT,
            dpath_plots=DPATH_PLOTS,
            transform=compose_transforms([ltrim(n), relative_y_zbt]),
            code='spltrz', mf_name=name,
            xlabel='A',
            ylabel='Relative Single Particle Energy + Zero Body Term',
            **kwargs
        )
    spltrz.__name__ = name
    return spltrz


def single_particle_first_np_zbt_metafit(n):
    """Returns a metafitter that fits to zero body term, keeping only the
    first n points
    :param n: number of points to include (starting from the leftmost point)
    """
    name = b'single_particle_first_{}p_zbt_metafit'.format(n)

    def spfnpz(fitfn, exp_list, **kwargs):
        return single_particle_metafit_int(
            fitfn, exp_list,
            dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
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
    """Returns a metafitter that fits to single-particle energies, keeping
    only the left-most n point
    :param n: number of points to include (starting from the left)
    """
    name = b'single_particle_first_{}p_metafit'.format(n)

    def spfnp(fitfn, exp_list, **kwargs):
        return single_particle_metafit_int(
            fitfn, exp_list,
            dpath_sources=DPATH_FILES_INT, dpath_plots=DPATH_PLOTS,
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
