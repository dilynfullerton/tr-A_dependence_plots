"""int/QuantumNumbers.py
Defines namedtuple representation of single particle orbital quantum numbers
"""
from __future__ import division, print_function, unicode_literals
from collections import namedtuple


# noinspection PyClassHasNoInit
class NushellOrbital(namedtuple('NushellOrbital', ['n', 'l', 'j', 'tz'])):
    """Stores descriptive quantum numbers for interaction (*.int) orbital
    """
    __slots__ = ()

    def __str__(self):
        n = str(int(self.n))
        l = str(int(self.l))
        if self.j != int(self.j):
            j = str(int(2*self.j)) + '/2'
        else:
            j = str(int(self.j))
        if self.tz != int(self.tz):
            tz = str(int(2*self.tz)) + '/2'
        else:
            tz = str(int(self.tz))
        tz = '+' + tz if self.tz > 0 else tz
        return '(n={n}, l={l}, j={j}, tz={tz})'.format(n=n, l=l, j=j, tz=tz)
