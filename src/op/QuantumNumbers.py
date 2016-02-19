from __future__ import print_function, division, unicode_literals

from collections import namedtuple


class QuantumNumbers(namedtuple('QuantumNumbers', ['j', 'p', 'tz'])):
    """j = angular momentum
       p = parity, 0 ==> +1, 1 ==> -1 (x ==> (-1)^x)
       tz = isospin projection
    """
    __slots__ = ()

    def __str__(self):
        s = super(QuantumNumbers, self).__str__()
        i = s.find('(')
        return s[i:]
