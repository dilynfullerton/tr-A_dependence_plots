"""State.py
Definition for namedtuple representation of a State
"""
from __future__ import print_function, division, unicode_literals
from collections import namedtuple


# noinspection PyClassHasNoInit
class NcsdEnergyLevel(namedtuple('NcsdEnergyLevel', ['N', 'J', 'T', 'E'])):
    """Stores the data corresponding to a specific state
        N:
            state number
        J:
            angular momentum
        T:
            isospin
    """
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')
