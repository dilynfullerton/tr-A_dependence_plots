from os import sep
from re import match

from ImsrgDataMap import ImsrgDataMap
from ExpLpt import ExpLpt
from ImsrgDatumLpt import ImsrgDatumLpt
from parse import get_files_r
from parse_lpt import exp
from constants import F_PARSE_LPT_CMNT_CHAR as CMNT_CHAR
from constants import F_PARSE_LPT_ROW_AZ as ROW_AZ
from constants import FN_PARSE_LPT_REGEX_FILENAME as REGEX_FILENAME


class ImsrgDataMapLpt(ImsrgDataMap):
    def __init__(self, parent_directory, exp_list=None,
                 _comment_char=CMNT_CHAR,
                 _row_az=ROW_AZ,
                 _regex_filename=REGEX_FILENAME):
        self._comment_char = _comment_char
        self._row_az = _row_az
        self._regex_filename = _regex_filename
        super(ImsrgDataMapLpt, self).__init__(
            parent_directory=parent_directory,
            exp_type=ExpLpt, datum_type=ImsrgDatumLpt,
            exp_list=exp_list,
            _comment_char=_comment_char,
            _row_az=_row_az)

    def _exp_from_file_path(self, f):
        return exp(f, self._comment_char, self._row_az)

    def _get_files(self):
        def lpt_file_filter(filepath):
            filename = filepath[filepath.rfind(sep)+1:]
            m = match(self._regex_filename, filename)
            if m is not None and m.group(0) == filename:
                return True
            else:
                return False
        return get_files_r(self.parent_dir, lpt_file_filter)
