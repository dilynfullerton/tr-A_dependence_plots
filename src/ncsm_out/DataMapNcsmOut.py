from __future__ import print_function, division
from os import sep
from DataMap import DataMap
from constants import FN_PARSE_NCSMVCE_OUT_RGX_FNAME as _RGX_FNAME
from parse import matches_completely, get_files_r
from ncsm_out.DatumNcsmOut import DatumNcsmOut
from ncsm_out.DatumNcsmOut import IncompleteArgumentsException
from ncsm_out.ExpNcsmOut import ExpNcsmOut
from ncsm_out.parser import exp


class DataMapNcsmOut(DataMap):
    """Stores map containing data retrieved from NCSD *.out files
    """
    # noinspection PyUnusedLocal
    def __init__(self, parent_directory, exp_list=None, exp_filter_fn=None,
                 **kwargs):
        self._rgx_fname = _RGX_FNAME
        super(DataMapNcsmOut, self).__init__(
            parent_directory=parent_directory,
            exp_type=ExpNcsmOut, datum_type=DatumNcsmOut,
            exp_list=exp_list, exp_filter_fn=exp_filter_fn
        )

    def _exp_from_file_path(self, f):
        return exp(filepath=f)

    def _get_files(self):
        def ncsmvce_out_file_filter(filepath):
            filename = filepath[filepath.rfind(sep)+1:]
            return matches_completely(regex=self._rgx_fname, string=filename)
        return get_files_r(directory=self.parent_dir,
                           filterfn=ncsmvce_out_file_filter)

    def scale_to_aeff_exact_to_ground_energy_map(
            self, z, n1, n2,
            nhw=None, nmax=None, a0=None, nshell=None, ncomponent=None
    ):
        m = dict()
        for k, v in self.map.items():
            if k.Z != z or k.n1 != n1 or k.n2 != n2:
                continue
            scale = k.scale if k.scale is not None else 1.0
            try:
                m[scale] = v.aeff_exact_to_ground_state_energy_map(
                    nhw=nhw, nmax=nmax, a0=a0,
                    nshell=nshell, ncomponent=ncomponent
                )
            except IncompleteArgumentsException:
                raise
        return m

    def aeff_exact_to_scale_to_ground_state_energy_map(
            self, z, n1, n2,
            nhw=None, nmax=None, a0=None, nshell=None, ncomponent=None
    ):
        try:
            scale_aeff_gnd = self.scale_to_aeff_exact_to_ground_energy_map(
                z=z, n1=n1, n2=n2, nhw=nhw, nmax=nmax, a0=a0,
                nshell=nshell, ncomponent=ncomponent,
            )
        except IncompleteArgumentsException:
            raise
        aeff_scale_gnd = dict()
        for scale, aeff_to_gnd in scale_aeff_gnd.items():
            for aeff, gnd in aeff_to_gnd.items():
                if aeff not in aeff_scale_gnd:
                    aeff_scale_gnd[aeff] = {scale: gnd}
                else:
                    aeff_scale_gnd[aeff].update({scale: gnd})
        return aeff_scale_gnd
