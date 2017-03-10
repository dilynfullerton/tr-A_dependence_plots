"""DataMapOp.py
Implementation of DataMap (see DataMap.py) for *.op Trel files for calculation
of monopoles, etc.
"""
from __future__ import print_function, division, unicode_literals

from os.path import sep

from op.DatumOp import DatumOp
from op.ExpOp import ExpOp
from op.parser import exp

from constants import FN_PARSE_OP_RGX_EXT as _RGX_FILENAME
from constants import FN_PARSE_OP_RGX_HW as _RGX_HW
from constants import F_PARSE_OP_ELT_SPLIT as _SPLIT_CHAR
from deprecated.DataMap import DataMap
from parse import matches_completely, get_files_r


class DataMapOp(DataMap):
    """Stores a map containing data generated from *.op files
    """
    # noinspection PyUnusedLocal
    def __init__(
            self, parent_directory, exp_list=None, exp_filter_fn=None,
            _rgx_hw=_RGX_HW, _rgx_fname=_RGX_FILENAME,
            _split_char=_SPLIT_CHAR, **kwargs
    ):
        """Initializes the DataMap in the given parent directory
        :param parent_directory: main directory from which to recursively
        retrieve files
        :param exp_list: list of ExpOp (see ExpOp.py) for which to gather
        data
        :param exp_filter_fn: function with which to filter data to use based
        on ExpOp. (Another method to be used in combination with or as an
        alternative to exp_list)
        :param _rgx_hw: regular expression that matches the hw part of the
        filename
        :param _rgx_fname: regular expression that matches the full *.op
        filename
        :param _split_char: character that splits filename elements
        :param kwargs: other keyword arguments. These are not used here, so
        I guess this is just for duck-typing.
        """
        self._split_char = _split_char
        self._rgx_hw = _rgx_hw
        self._rgx_fname = _rgx_fname
        super(DataMapOp, self).__init__(
            parent_directory=parent_directory,
            exp_type=ExpOp, datum_type=DatumOp,
            exp_list=exp_list, exp_filter_fn=exp_filter_fn
        )

    def _exp_from_file_path(self, f):
        return exp(
            filepath=f, split_char=self._split_char, regex_hw=self._rgx_hw)

    def _get_files(self):
        def op_file_filter(filepath):
            filename = filepath[filepath.rfind(sep) + 1:]
            return matches_completely(regex=self._rgx_fname, string=filename)
        return get_files_r(directory=self.parent_dir, filterfn=op_file_filter)
