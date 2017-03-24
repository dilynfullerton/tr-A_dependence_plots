"""DataMapInt.py
Implementation of DataMap (see DataMap.py) for NuShellX interaction data
"""
from __future__ import print_function, division, unicode_literals

from deprecated.int.DatumInt import DatumInt
from deprecated.int.ExpInt import ExpInt

from constants import FN_PARSE_INT_STR_EXT as _INT_EXT
from deprecated.DataMap import DataMap
from deprecated.int.parser import exp
from parse import get_files_r, has_extension


class DataMapInt(DataMap):
    """A mapping from ExpInt to ImsrgDatumInt
    """

    # noinspection PyUnusedLocal
    def __init__(self, parent_directory, exp_list=None, exp_filter_fn=None,
                 standard_indices=None, _extension=_INT_EXT, **kwargs):
        """Initialize DataMap
        :param parent_directory: directory from which to recursively
        retrieve files
        :param exp_list: list of exp for which to take data
        :param exp_filter_fn: alternate (additional) method of restricting
        data. This function will be used to keep only files whose exp returns
        True.
        :param standard_indices: standard index -> orbital map
        :param _extension: extension for int files
        :param kwargs: other arguments to pass to DatumInt
        """
        self.extension = _extension
        super(DataMapInt, self).__init__(
            parent_directory=parent_directory,
            exp_type=ExpInt, datum_type=DatumInt,
            exp_list=exp_list,
            exp_filter_fn=exp_filter_fn,
            std_io_map=standard_indices
        )

    def _exp_from_file_path(self, f):
        return exp(f)

    def _get_files(self):
        return get_files_r(self.parent_dir,
                           filterfn=lambda f: has_extension(f, self.extension))
