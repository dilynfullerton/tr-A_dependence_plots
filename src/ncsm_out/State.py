from __future__ import print_function, division, unicode_literals
from collections import namedtuple


# noinspection PyClassHasNoInit
class State(namedtuple('State', ['E', 'Ex', 'J', 'T'])):
    """Stores the four data corresponding to a specific state
    """
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')
