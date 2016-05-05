"""ExpInt.py
Definition of the namedtuple that identifies a set of interaction files from
which to derive data
"""
from __future__ import division
from __future__ import unicode_literals

from collections import namedtuple


# noinspection PyClassHasNoInit
class ExpInt(namedtuple('ExpInt', ['e', 'hw', 'base', 'rp'])):
    """Descriptive key for *.int data.
    e: max e-level
    hw: hw frequency
    base: (default None) the mass number that normal ordering was done WRT
    rp: (default None) the proton radius? I do not really know what this is
    """
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')


ExpInt.__new__.__defaults__ = (None, None)
