from __future__ import division
from __future__ import print_function

from collections import namedtuple

import parse
from ImsrgDatum import ImsrgDatum

Exp = namedtuple('Exp', ['e', 'hw', 'rp'])
Exp.__new__.__defaults__ = (None,)


class ImsrgDataMap:
    """A data structure to hold a mapping from
    (e-level, hw) -> ImsrgDatum, which will consist of all available data
    """
    def __init__(self, parent_directory):
        self.parent_dir = parent_directory
        self.map = dict()
        # self.sub_dir_tuple_map = dict()

        self._set_maps()

    def _set_maps(self):
        sub_directories = parse.files_with_ext_in_directory(self.parent_dir,
                                                            extension='')
        for sd in sub_directories:
            files = parse.files_with_ext_in_directory(sd)
            try:
                f0 = files[0]
            except IndexError:
                continue

            for f in files:
                e = parse.e_level_from_filename(f)
                hw = parse.hw_from_filename(f)
                rp = parse.rp_from_filename(f)

                key = Exp(e, hw, rp)
                value = ImsrgDatum(sd, e, hw, rp)

                if key not in self.map:
                    # self.sub_dir_tuple_map[sd] = key
                    self.map[key] = value

    def all_e_hw_pairs(self):
        return set(self.map.keys())


class DataAlreadyPresentForKeyException(Exception):
    pass
