"""These definitions hold key-value maps to store data of different types.

For example, ImsrgDataMapInt stores a mapping from ExpInt to ImsrgDatumInt,
the data-type that stores data retrieved from *.int files.
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from os.path import sep

from Exp import ExpInt, ExpLpt, ExpOp
from ImsrgDatum import ImsrgDatumInt, ImsrgDatumLpt, ImsrgDatumOp

from constants import FN_PARSE_INT_EXT as _INT_EXT

from constants import F_PARSE_LPT_CMNT_CHAR as _LPT_CMNT_CHAR
from constants import F_PARSE_LPT_ROW_AZ as _LPT_ROW_AZ
from constants import FN_PARSE_LPT_REGEX_FILENAME as _LPT_REGEX_FILENAME

from constants import F_PARSE_OP_ELT_SPLIT as _OP_SPLIT_CHAR
from constants import FN_PARSE_OP_REGEX_HW as _OP_REGEX_HW
from constants import FN_PARSE_OP_REGEX_EXT as _OP_REGEX_FILENAME

from parse import get_files_r, has_extension, matches_completely
from parse_int import exp as exp_int
from parse_lpt import exp as exp_lpt
from parse_op import exp as exp_op


class _ImsrgDataMap(object):
    def __init__(self, parent_directory, exp_type, datum_type,
                 exp_list=None, exp_filter_fn=None, **kwargs):
        self.parent_dir = parent_directory
        self.map = dict()
        if exp_list is not None:
            self.exp_list = [exp_type(*exp_item) for exp_item in exp_list]
        else:
            self.exp_list = None
        self.exp_filter_fn = exp_filter_fn
        self.exp_type = exp_type
        self.datum_type = datum_type
        self.kwargs = kwargs
        self._set_maps()

    def __getitem__(self, item):
        return self.map[item]

    def _set_maps(self):
        files = self._get_files()
        for f in files:
            key = self.exp_type(*self._exp_from_file_path(f))
            if self.exp_list is not None and key not in self.exp_list:
                continue
            elif self.exp_filter_fn is not None and not self.exp_filter_fn(key):
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
        raise NotImplemented()

    def _get_files(self):
        raise NotImplemented()


class ImsrgDataMapInt(_ImsrgDataMap):
    """A mapping from ExpInt to ImsrgDatumInt
    """

    # noinspection PyUnusedLocal
    def __init__(self, parent_directory, exp_list=None, exp_filter_fn=None,
                 standard_indices=None, _extension=_INT_EXT, **kwargs):
        self.extension = _extension
        super(ImsrgDataMapInt, self).__init__(
            parent_directory=parent_directory,
            exp_type=ExpInt, datum_type=ImsrgDatumInt,
            exp_list=exp_list,
            exp_filter_fn=exp_filter_fn,
            std_io_map=standard_indices)

    def _exp_from_file_path(self, f):
        return exp_int(f)

    def _get_files(self):
        return get_files_r(self.parent_dir,
                           filterfn=lambda f: has_extension(f, self.extension))


class ImsrgDataMapLpt(_ImsrgDataMap):
    """A mapping from ExpLpt to ImsrgDatumLpt
    """

    # noinspection PyUnusedLocal
    def __init__(self, parent_directory, exp_list=None, exp_filter_fn=None,
                 _comment_char=_LPT_CMNT_CHAR,
                 _row_az=_LPT_ROW_AZ,
                 _regex_filename=_LPT_REGEX_FILENAME, **kwargs):
        self._comment_char = _comment_char
        self._row_az = _row_az
        self._regex_filename = _regex_filename
        super(ImsrgDataMapLpt, self).__init__(
            parent_directory=parent_directory,
            exp_type=ExpLpt, datum_type=ImsrgDatumLpt,
            exp_list=exp_list,
            exp_filter_fn=exp_filter_fn,
            _comment_char_lpt=self._comment_char,
            _row_az=self._row_az)

    def _exp_from_file_path(self, f):
        return exp_lpt(f, self._comment_char, self._row_az)

    def _get_files(self):
        def lpt_file_filter(filepath):
            filename = filepath[filepath.rfind(sep) + 1:]
            return matches_completely(regex=self._regex_filename,
                                      string=filename)

        return get_files_r(self.parent_dir, lpt_file_filter)


class ImsrgDataMapOp(_ImsrgDataMap):
    def __init__(self, parent_directory, exp_list, exp_filter_fn,
                 _split_char=_OP_SPLIT_CHAR,
                 _regex_hw=_OP_REGEX_HW,
                 _regex_filename=_OP_REGEX_FILENAME,
                 **kwargs):
        self._split_char = _split_char
        self._regex_hw = _regex_hw
        self._regex_filename = _regex_filename
        super(ImsrgDataMapOp, self).__init__(
            parent_directory=parent_directory,
            exp_type=ExpOp, datum_type=ImsrgDatumOp,
            exp_list=exp_list, exp_filter_fn=exp_filter_fn)

    def _exp_from_file_path(self, f):
        return exp_op(filepath=f,
                      split_char=self._split_char,
                      regex_hw=self._regex_hw)

    def _get_files(self):
        def op_file_filter(filepath):
            filename = filepath[filepath.rfind(sep) + 1:]
            return matches_completely(regex=self._regex_filename,
                                      string=filename)

        return get_files_r(directory=self.parent_dir, filterfn=op_file_filter)
