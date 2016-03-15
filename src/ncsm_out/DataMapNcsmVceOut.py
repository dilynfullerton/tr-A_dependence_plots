from __future__ import print_function, division, unicode_literals
from os import sep
from DataMap import DataMap
from constants import FN_PARSE_NCSMVCE_OUT_RGX_FNAME as _RGX_FNAME
from parse import matches_completely, get_files_r
from ncsm_out.DatumNcsmVceOut import DatumNcsmVceOut
from ncsm_out.ExpNcsmVceOut import ExpNcsmVceOut
from ncsm_out.parser import exp


class DataMapNcsmVceOut(DataMap):
    """Stores map containing data retrieved from NCSD *.out files
    """
    # noinspection PyUnusedLocal
    def __init__(self, parent_directory, exp_list=None, exp_filter_fn=None,
                 _rgx_fname=_RGX_FNAME, **kwargs):
        self._rgx_fname = _rgx_fname
        super(DataMapNcsmVceOut, self).__init__(
            parent_directory=parent_directory,
            exp_type=ExpNcsmVceOut, datum_type=DatumNcsmVceOut,
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
