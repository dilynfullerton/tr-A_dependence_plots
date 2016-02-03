"""Holds all of the *.int data for different data sets (specified by their Exp)
in a map
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ImsrgDataMap import ImsrgDataMap
from ImsrgDatumInt import ImsrgDatumInt
from ExpInt import ExpInt
from parse_int import exp_from_filename
from parse import get_files_r, has_extension
from constants import FN_PARSE_INT_EXT as EXT


class ImsrgDataMapInt(ImsrgDataMap):
    def __init__(self, parent_directory, exp_list=None, standard_indices=None):
        super(ImsrgDataMapInt, self).__init__(
            parent_directory=parent_directory,
            exp_type=ExpInt, datum_type=ImsrgDatumInt,
            exp_list=exp_list,
            std_io_map=standard_indices)

    def _exp_from_file_path(self, f):
        return exp_from_filename(f)

    def _get_files(self, ext=EXT):
        return get_files_r(self.parent_dir,
                           filterfn=lambda f: has_extension(f, ext))
