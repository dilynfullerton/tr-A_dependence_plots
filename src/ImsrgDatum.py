from __future__ import print_function
from __future__ import division
from collections import namedtuple

class ImsrgDatum:
    def __init__(self, directory, e, hw, name=None):
        self.e = e
        self.hw = hw
        self.name = name

        self.interaction_index_engery_map = dict()  # empty
        self.single_index_engery_map = dict()       # empty
        self.index_orbital_map = dict()             # empty
