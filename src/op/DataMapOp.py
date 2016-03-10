from __future__ import print_function, division, unicode_literals

from os.path import sep

from DataMap import DataMap
from parse import matches_completely, get_files_r
from constants import FN_PARSE_OP_REGEX_EXT as _REGEX_FILENAME
from constants import FN_PARSE_OP_REGEX_HW as _REGEX_HW
from constants import F_PARSE_OP_ELT_SPLIT as _SPLIT_CHAR

from op.ExpOp import ExpOp
from op.DatumOp import DatumOp
from op.parse_op import exp


class DataMapOp(DataMap):
    # noinspection PyUnusedLocal
    def __init__(self, parent_directory, exp_list=None, exp_filter_fn=None,
                 _split_char=_SPLIT_CHAR,
                 _regex_hw=_REGEX_HW,
                 _regex_filename=_REGEX_FILENAME,
                 **kwargs):
        self._split_char = _split_char
        self._regex_hw = _regex_hw
        self._regex_filename = _regex_filename
        super(DataMapOp, self).__init__(
            parent_directory=parent_directory,
            exp_type=ExpOp, datum_type=DatumOp,
            exp_list=exp_list, exp_filter_fn=exp_filter_fn)

    def _exp_from_file_path(self, f):
        return exp(filepath=f,
                   split_char=self._split_char,
                   regex_hw=self._regex_hw)

    def _get_files(self):
        def op_file_filter(filepath):
            filename = filepath[filepath.rfind(sep) + 1:]
            return matches_completely(regex=self._regex_filename,
                                      string=filename)

        return get_files_r(directory=self.parent_dir, filterfn=op_file_filter)
