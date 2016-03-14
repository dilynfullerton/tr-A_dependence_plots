from __future__ import print_function, division, unicode_literals
from collections import namedtuple


class State(namedtuple('State', ['E', 'Ex', 'J', 'T'])):
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')
