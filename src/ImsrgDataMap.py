from __future__ import print_function
from __future__ import division
from collections import namedtuple
from ImsrgDatum import ImsrgDatum
import parse


Exp = namedtuple('Exp', ['e', 'hw'])


class ImsrgDataMap:
    """A data structure to hold a mapping from
    (e-level, hw) -> ImsrgDatum, which will consist of all available data
    """
    def __init__(self, parent_directory):
        self.parent_dir = parent_directory
        self.map = dict()

        self._set_map()

    def _set_map(self):
        sub_directories = parse.files_with_ext_in_directory(self.parent_dir,
                                                            extension='')
        m = dict()
        for sd in sub_directories:
            files = parse.files_with_ext_in_directory(sd)
            f0 = files[0]
            
            e = parse.e_level_from_filename(f0)
            hw = parse.hw_from_filename(f0)
            key = Exp(e, hw)
            value = ImsrgDatum(sd, e, hw)

            m[key] = value
        
        self.map = m

idm = ImsrgDataMap('../files/')
print(idm.map)
            
