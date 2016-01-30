"""Holds all of the data for different data sets (specified by their Exp) in
a map
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import namedtuple

from parse import sub_directories
from parse import files_with_ext_in_directory
from parse import exp_from_filename
from ImsrgDatum import ImsrgDatum


# noinspection PyClassHasNoInit
class Exp(namedtuple('Exp', ['e', 'hw', 'base', 'rp'])):
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')
Exp.__new__.__defaults__ = (None, None)


class ImsrgDataMap:
    """A data structure to hold a mapping from
    (e-level, hw) -> ImsrgDatum, which will consist of all available data
    """
    def __init__(self, parent_directory, exp_list=None, standard_indices=None):
        self.parent_dir = parent_directory
        self.map = dict()
        self.exp_list = [Exp(*exp_item) for exp_item in exp_list]
        self.std_io_map = standard_indices

        self._set_maps()

    def _set_maps(self):
        sub_dirs = sub_directories(self.parent_dir)

        for sd in sub_dirs:
            files = files_with_ext_in_directory(sd)
            if len(files) == 0:
                continue

            for f in files:
                key = Exp(*exp_from_filename(f))

                if self.exp_list is not None and key not in self.exp_list:
                    continue

                if key not in self.map:
                    value = ImsrgDatum(sd, *tuple(key),
                                       std_io_map=self.std_io_map)
                    self.map[key] = value

    def all_e_hw_pairs(self):
        return set(self.map.keys())


class DataAlreadyPresentForKeyException(Exception):
    pass
