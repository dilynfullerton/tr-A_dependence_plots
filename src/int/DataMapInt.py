from __future__ import print_function, division, unicode_literals

from DataMap import DataMap
from parse import get_files_r, has_extension
from constants import FN_PARSE_INT_EXT as _INT_EXT
from int.ExpInt import ExpInt
from int.DatumInt import DatumInt
from int.parse_int import exp


class DataMapInt(DataMap):
    """A mapping from ExpInt to ImsrgDatumInt
    """

    # noinspection PyUnusedLocal
    def __init__(self, parent_directory, exp_list=None, exp_filter_fn=None,
                 standard_indices=None, _extension=_INT_EXT, **kwargs):
        self.extension = _extension
        super(DataMapInt, self).__init__(
            parent_directory=parent_directory,
            exp_type=ExpInt, datum_type=DatumInt,
            exp_list=exp_list,
            exp_filter_fn=exp_filter_fn,
            std_io_map=standard_indices)

    def _exp_from_file_path(self, f):
        return exp(f)

    def _get_files(self):
        return get_files_r(self.parent_dir,
                           filterfn=lambda f: has_extension(f, self.extension))
