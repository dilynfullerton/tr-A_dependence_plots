"""op/ExpOp.py
Definition for the namedtuples representation fo a set of *.op files from
which to construct a Datum
"""
from __future__ import print_function, division, unicode_literals

from collections import namedtuple


# noinspection PyClassHasNoInit
class ExpOp(namedtuple('ExpOp', ['hw'])):
    """Exp definition for *.op files
    hw: hw frequency number
    """
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')
