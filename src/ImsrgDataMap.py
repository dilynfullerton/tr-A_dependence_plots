from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from os.path import sep
from re import match

from Exp import ExpInt, ExpLpt
from ImsrgDatum import ImsrgDatumInt, ImsrgDatumLpt
from constants import FN_PARSE_INT_EXT as EXT
from constants import F_PARSE_LPT_CMNT_CHAR as CMNT_CHAR
from constants import F_PARSE_LPT_ROW_AZ as ROW_AZ
from constants import FN_PARSE_LPT_REGEX_FILENAME as REGEX_FILENAME
from parse import get_files_r, has_extension
from parse_int import exp_from_filename
from parse_lpt import exp


class _ImsrgDataMap(object):
    def __init__(self, parent_directory, exp_type, datum_type,
                 exp_list=None, **kwargs):
        self.parent_dir = parent_directory
        self.map = dict()
        if exp_list is not None:
            self.exp_list = [exp_type(*exp_item) for exp_item in exp_list]
        else:
            self.exp_list = None
        self.exp_type = exp_type
        self.datum_type = datum_type
        self.kwargs = kwargs
        self._set_maps()

    def _set_maps(self):
        files = self._get_files()
        for f in files:
            key = self.exp_type(*self._exp_from_file_path(f))
            if self.exp_list is not None and key not in self.exp_list:
                continue
            elif key not in self.map:
                key_files = list(
                    filter(lambda ff: key == self._exp_from_file_path(ff),
                           files))
                value = self.datum_type(directory=self.parent_dir, exp=key,
                                        files=key_files,
                                        **self.kwargs)
                self.map[key] = value

    def _exp_from_file_path(self, f):
        raise NotImplemented

    def _get_files(self):
        raise NotImplemented


class ImsrgDataMapInt(_ImsrgDataMap):
    def __init__(self, parent_directory, exp_list=None, standard_indices=None,
                 extension=EXT):
        self.extension = extension
        super(ImsrgDataMapInt, self).__init__(
            parent_directory=parent_directory,
            exp_type=ExpInt, datum_type=ImsrgDatumInt,
            exp_list=exp_list,
            std_io_map=standard_indices)

    def _exp_from_file_path(self, f):
        return exp_from_filename(f)

    def _get_files(self):
        return get_files_r(self.parent_dir,
                           filterfn=lambda f: has_extension(f, self.extension))


class ImsrgDataMapLpt(_ImsrgDataMap):
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
            _comment_char_lpt=_comment_char,
            _row_az=_row_az)

    def _exp_from_file_path(self, f):
        return exp(f, self._comment_char, self._row_az)

    def _get_files(self):
        def lpt_file_filter(filepath):
            filename = filepath[filepath.rfind(sep) + 1:]
            m = match(self._regex_filename, filename)
            if m is not None and m.group(0) == filename:
                return True
            else:
                return False

        return get_files_r(self.parent_dir, lpt_file_filter)
