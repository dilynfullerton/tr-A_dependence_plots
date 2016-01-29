from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import namedtuple

import parse
from ImsrgDatum import ImsrgDatum


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
        sub_directories = parse.files_with_ext_in_directory(self.parent_dir,
                                                            extension='')
        for sd in sub_directories:
            files = parse.files_with_ext_in_directory(sd)
            if len(files) == 0:
                continue

            for f in files:
                key = Exp(*parse.exp_from_filename(f))

                if self.exp_list is not None and key not in self.exp_list:
                    continue

                if key not in self.map:
                    value = ImsrgDatum(sd, *key, std_io_map=self.std_io_map)
                    self.map[key] = value

    def all_e_hw_pairs(self):
        return set(self.map.keys())


class DataAlreadyPresentForKeyException(Exception):
    pass
