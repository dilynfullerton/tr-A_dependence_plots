from __future__ import unicode_literals
from collections import namedtuple


# noinspection PyClassHasNoInit
class ExpLpt(namedtuple('ExpLpt', ['Z', 'A', 'int'])):
    """Z: proton number
       A: nucleon number
       int: interaction type (e.g. 'usdb')
    """
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')
