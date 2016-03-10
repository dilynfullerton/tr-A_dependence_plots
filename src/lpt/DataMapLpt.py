from __future__ import print_function, division, unicode_literals

from os.path import sep

from DataMap import DataMap
from constants import FN_PARSE_LPT_REGEX_FILENAME as _REGEX_FILENAME
from constants import F_PARSE_LPT_CMNT_CHAR as _CMNT_CHAR
from constants import F_PARSE_LPT_ROW_AZ as _ROW_AZ
from parse import matches_completely, get_files_r
from lpt.ExpLpt import ExpLpt
from lpt.DatumLpt import DatumLpt
from lpt.parse_lpt import exp


class DataMapLpt(DataMap):
    """A mapping from ExpLpt to ImsrgDatumLpt
    """

    # noinspection PyUnusedLocal
    def __init__(self, parent_directory, exp_list=None, exp_filter_fn=None,
                 _comment_char=_CMNT_CHAR, _row_az=_ROW_AZ,
                 _regex_filename=_REGEX_FILENAME, **kwargs):
        self._comment_char = _comment_char
        self._row_az = _row_az
        self._regex_filename = _regex_filename
        super(DataMapLpt, self).__init__(
            parent_directory=parent_directory,
            exp_type=ExpLpt, datum_type=DatumLpt,
            exp_list=exp_list,
            exp_filter_fn=exp_filter_fn,
            _comment_char_lpt=self._comment_char,
            _row_az=self._row_az)

    def _exp_from_file_path(self, f):
        return exp(f, self._comment_char, self._row_az)

    def _get_files(self):
        def lpt_file_filter(filepath):
            filename = filepath[filepath.rfind(sep) + 1:]
            return matches_completely(regex=self._regex_filename,
                                      string=filename)

        return get_files_r(self.parent_dir, lpt_file_filter)
