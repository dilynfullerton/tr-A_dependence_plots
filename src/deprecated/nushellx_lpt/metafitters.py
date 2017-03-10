"""nushellx_lpt/metafitters.py
Specific implementations of the abstract *.lpt metafitter in mettafitter_abs
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from transforms import *
from transforms_s import *
from nushellx_lpt.metafitter_abs import metafit_nushellx_lpt as mf


def lpt_pzbt_for_z_in_list_and_n_in_list_metafit(list_z, list_n):
    """Returns a metafitter that fits to Energy + Zero body term based
    on *.lpt data for the given allowed Z values and N values.
    NOTE: N here is not the neutron number; it is the state number, based
    on the convention used in the *.lpt files.
    :param list_z: list of proton numbers to use
    :param list_n: list of state levels to use
    """
    name = b'lpt_pzbt_for_Z_in_{}_and_N_in_{}_metafit'.format(list_z, list_n)

    def metafitter(fitfn, **kwargs):
        return mf(
            fitfn=fitfn, transform=pzbt,
            exp_list=None, exp_filter_fn=lambda exp: exp.Z in list_z,
            super_transform_pre=s_n_values(list_n),
            code='pz', mf_name=name,
            xlabel='A', ylabel='Energy + Zero Body Term (MeV)', **kwargs
        )
    metafitter.__name__ = name
    return metafitter


def lpt_identity_for_z_in_list_and_n_in_list_metafit(list_z, list_n):
    """Returns a metafitter that fits to Energy (without additional
    zero body term) based on *.lpt data for the given allowd Z values and
    N values.
    NOTE: N here is not the neutron nubmer; it is the state number,
    based on the convention used in the *.lpt files.
    :param list_z: list of proton numbers to use
    :param list_n: list of state levels to use
    """
    name = b'lpt_identity_for_Z_in_{}_and_N_in_{}_metafit'.format(
        list_z, list_n)

    def metafitter(fitfn, **kwargs):
        return mf(
            fitfn=fitfn, transform=identity,
            exp_list=None, exp_filter_fn=lambda exp: exp.Z in list_z,
            super_transform_pre=s_n_values(list_n),
            code='pz', mf_name=name, xlabel='A', ylabel='Energy (MeV)',
            **kwargs
        )
    metafitter.__name__ = name
    return metafitter
