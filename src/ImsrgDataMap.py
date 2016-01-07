from __future__ import print_function
from __future__ import division
from collections import namedtuple

class ImsrgDataMap:
    """A data structure to hold a mapping from
    (e-level, hw) -> ImsrgDatum, which will consist of all available data
    """
    def __init__(self):
        self.map = dict()
