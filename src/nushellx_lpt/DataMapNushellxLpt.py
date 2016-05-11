"""DataMapNushellxLpt.py
Implementation of DataMap (see DataMap.py) for NuShellX *.lpt files
based on Magnus, Heiko, and targeted normal-ordering interaction files
"""
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
            _rgx_fname_lpt=_RGX_FNAME, _rgx_dname_ggparent_dir=_RGX_DNAME_GGP,
            _exp_type=ExpNushellxLpt, _datum_type=DatumLpt, **kwargs
    ):
        """Initialize the DataMap in the given parent_directory
        :param parent_directory: directory in which to recursively retrieve
        files
        :param exp_list: list of exp for which to gather data
        :param exp_filter_fn: function with which to filter files by their exp
        :param _rgx_fname_lpt: regular expression that fully matches a
        *.lpt file name
        :param _rgx_dname_ggparent_dir: regular expression that fully matches the
        great-grandparent directory to the *.lpt file. Note: This is
        inconsistent with calling the parent_directory the "parent" directory,
        as the parent directory is actually the main directory from which
        all files are gathered, whereas the "great-grandparent" directory, as
        used here is the great-grandparent to a given *.lpt file.
        :param _exp_type: type for the Exp.
        :param _datum_type: type for the Datum.
        :param kwargs: other arguments to pass to DatumLpt
        """
        self._regex_filename = _rgx_fname_lpt
        self._regex_ggp_dirname = _rgx_dname_ggparent_dir
        super(DataMapNushellxLpt, self).__init__(
            parent_directory=parent_directory,
            exp_type=_exp_type, datum_type=_datum_type,
            exp_list=exp_list, exp_filter_fn=exp_filter_fn
        )

    def _exp_from_file_path(self, f):
        return exp(filepath=f)

    def _get_files(self):
        def lpt_file_filter(filepath):
            lpt_fname = filepath[filepath.rfind(sep) + 1:]
            ggp_dname = filepath.split(sep)[-4]
            return (
                matches_completely(
                    regex=self._regex_filename, string=lpt_fname
                ) and matches_completely(
                    regex=self._regex_ggp_dirname, string=ggp_dname
                )
            )
        return get_files_r(directory=self.parent_dir, filterfn=lpt_file_filter)
