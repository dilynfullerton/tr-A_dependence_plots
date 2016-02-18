from __future__ import print_function, division, unicode_literals

from collections import namedtuple


class ExpOp(namedtuple('ExpOp', ['hw'])):
    """Exp definition for *.op files
            hw: hw frequency number
    """
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')