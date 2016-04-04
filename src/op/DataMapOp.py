from __future__ import print_function, division, unicode_literals

from os.path import sep

from DataMap import DataMap
from parse import matches_completely, get_files_r
from constants import FN_PARSE_OP_RGX_EXT as _REGEX_FILENAME
from constants import FN_PARSE_OP_RGX_HW as _REGEX_HW
from constants import F_PARSE_OP_ELT_SPLIT as _SPLIT_CHAR

from op.ExpOp import ExpOp
from op.DatumOp import DatumOp
from op.parser import exp


class DataMapOp(DataMap):
    """Stores a map containing data generated from *.op files
    """
    # noinspection PyUnusedLocal
    def __init__(
            self, parent_directory, exp_list=None, exp_filter_fn=None,
            _rgx_hw=_REGEX_HW, _rgx_fname=_REGEX_FILENAME,
            _split_char=_SPLIT_CHAR, **kwargs
    ):
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
