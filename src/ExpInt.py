from __future__ import unicode_literals
from collections import namedtuple


# noinspection PyClassHasNoInit
class ExpInt(namedtuple('ExpInt', ['e', 'hw', 'base', 'rp'])):
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')
ExpInt.__new__.__defaults__ = (None, None)
