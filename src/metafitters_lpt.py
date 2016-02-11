from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from transforms import *
from transforms_s import *
from metafit import metafit_lpt as mf


def lpt_pzbt_for_z_in_list_and_n_in_list_metafit(list_z, list_n):
    name = b'lpt_pzbt_for_Z_in_{}_and_N_in_{}_metafit'.format(list_z, list_n)

    def metafitter(fitfn, **kwargs):
        return mf(fitfn=fitfn,
                  transform=pzbt,
                  exp_list=None,
                  exp_filter_fn=lambda exp: exp.Z in list_z,
                  super_transform_pre=s_n_values(list_n),
                  code='pz',
                  mf_name=name,
                  xlabel='A',
                  ylabel='Energy + Zero Body Term (MeV)',
                  **kwargs)
    metafitter.__name__ = name
    return metafitter


def lpt_identity_for_z_in_list_and_n_in_list_metafit(list_z, list_n):
    name = b'lpt_identity_for_Z_in_{}_and_N_in_{}_metafit'.format(list_z,
                                                                  list_n)

    def metafitter(fitfn, **kwargs):
        return mf(fitfn=fitfn,
                  transform=identity,
                  exp_list=None,
                  exp_filter_fn=lambda exp: exp.Z in list_z,
                  super_transform_pre=s_n_values(list_n),
                  code='pz',
                  mf_name=name,
                  xlabel='A',
                  ylabel='Energy (MeV)',
                  **kwargs)
    metafitter.__name__ = name
    return metafitter
