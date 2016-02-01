from __future__ import unicode_literals
from collections import namedtuple


# noinspection PyClassHasNoInit
class Exp(namedtuple('Exp', ['e', 'hw', 'base', 'rp'])):
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')
Exp.__new__.__defaults__ = (None, None)
