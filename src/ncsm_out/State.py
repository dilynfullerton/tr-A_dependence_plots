"""State.py
Definition for namedtuple representation of a State
"""
from __future__ import print_function, division, unicode_literals
from collections import namedtuple


# noinspection PyClassHasNoInit
class State(namedtuple('State', ['E', 'Ex', 'J', 'T'])):
    """Stores the four data corresponding to a specific state
        E:
            energy
        Ex:
            excitation
        J:
            angular momentum
        T:
            isospin
    """
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')
