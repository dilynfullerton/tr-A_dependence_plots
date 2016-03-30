from __future__ import print_function, division, unicode_literals

from os.path import sep

from DataMap import DataMap
from constants import FN_PARSE_LPT_RGX_FNAME as _RGX_FNAME
from constants import FN_PARSE_LPT_RGX_DNAME as _RGX_DNAME_GGP
from parse import matches_completely, get_files_r
from nushellx_lpt.ExpNushellxLpt import ExpNushellxLpt
from nushellx_lpt.DatumLpt import DatumLpt
from nushellx_lpt.parser import exp


class DataMapNushellxLpt(DataMap):
    """A mapping from ExpLpt to ImsrgDatumLpt
    """

    # noinspection PyUnusedLocal
    def __init__(
            self, parent_directory, exp_list=None, exp_filter_fn=None,
            _regex_filename=_RGX_FNAME, _regex_ggparent_dir=_RGX_DNAME_GGP,
            _exp_type=ExpNushellxLpt, _datum_type=DatumLpt, **kwargs
    ):
        self._regex_filename = _regex_filename
        self._regex_ggp_dirname = _regex_ggparent_dir
        super(DataMapNushellxLpt, self).__init__(
            parent_directory=parent_directory,
            exp_type=_exp_type, datum_type=_datum_type,
            exp_list=exp_list, exp_filter_fn=exp_filter_fn
        )

    def _exp_from_file_path(self, f):
        return exp(filepath=f)

    def _get_files(self):
        def lpt_file_filter(filepath):
            filename = filepath[filepath.rfind(sep) + 1:]
            ggp_dirname = filepath.split(sep)[-4]
            return (
                matches_completely(
                    regex=self._regex_filename, string=filename
                ) and matches_completely(
                    regex=self._regex_ggp_dirname, string=ggp_dirname
                )
            )
        return get_files_r(directory=self.parent_dir, filterfn=lpt_file_filter)
