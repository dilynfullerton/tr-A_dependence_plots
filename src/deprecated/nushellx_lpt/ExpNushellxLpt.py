"""ExpNushellxLpt.py
Definition for namedtuple representation of a set of *.lpt file data
from running NuShellX on Magnus, Heiko, or normal-ordered interactions
"""
from __future__ import print_function, division, unicode_literals

from collections import namedtuple


# noinspection PyClassHasNoInit
class ExpNushellxLpt(namedtuple('ExpNushellxLpt', ['Z', 'int'])):
    """Exp definition for *.nushellx_lpt files
           Z: proton number
           int: interaction type (e.g. 'usdb', 'sd-shell...', 'fit-gen...')
    """
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')
