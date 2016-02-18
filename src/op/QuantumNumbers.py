from __future__ import print_function, division, unicode_literals

from collections import namedtuple


class QuantumNumbers(namedtuple('QuantumNumbers', ['n', 'p', 'tz'])):
    """n = energy level
       p = parity, 0 ==> +1, 1 ==> -1 (x ==> (-1)^x)
       tz = isospin projection
    """
    __slots__ = ()

    def __str__(self):
        return str(self._asdict().values())
