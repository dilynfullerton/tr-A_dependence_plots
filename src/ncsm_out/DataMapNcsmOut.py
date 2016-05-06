"""DataMapNcsmOut
Imlementation of DataMap (see DataMap.py) for *.out files produced by
running NCSD
"""
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
        """Initialize the DataMap in the given parent_directory
        :param parent_directory: directory in which to recursively retrieve
        files
        :param exp_list: list of exp for which to gather data
        :param exp_filter_fn: function with which to filter files by their exp
        :param kwargs: other arguments to pass to DatumNcsmOut
        """
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
            self, z, n1, n2, nshell, nhw=None, nmax=None):
        """Returns a map
            scale -> A=Aeff -> Ground energy
        from the interaction scale factor to the mass number to the ground
        state energy associated with the case in which Aeff=A.
        One of nhw or nmax must be provided.
        :param z: proton number (Z)
        :param n1: one-particle truncation level
        :param n2: two-particle truncation level
        :param nshell: major oscillator shell (0=s, 1=p, 2=sd, ...)
        :param nhw: major oscillator shell truncation
        :param nmax: major oscillator shell truncation - minimum needed
        orbitals
        """
        m = dict()
        for k, v in self.map.items():
            if k.Z != z or k.n1 != n1 or k.n2 != n2:
                continue
            scale = k.scale if k.scale is not None else 1.0
            try:
                m[scale] = v.aeff_exact_to_ground_state_energy_map(
                    nhw=nhw, nmax=nmax, z=z, nshell=nshell)
            except IncompleteArgumentsException:
                raise
        return m

