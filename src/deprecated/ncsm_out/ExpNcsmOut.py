"""ExpNcsmOut.py
Definition for namedtuple to specify a set of NcsmOut data
"""
from __future__ import print_function, division, unicode_literals

from collections import namedtuple


# noinspection PyClassHasNoInit
class ExpNcsmOut(namedtuple('ExpNcsmVceOut',
                            ['Z', 'n1', 'n2', 'scale', 'incl_proton'])):
    """Identifier for a set of NCSD *.out files generated for the same
    element in the same model space
        Z:
            proton number
        n1:
            one-particle TBME truncation
        n2:
            two-particle TBME truncation
        scale:
            factor by which off-diagonal coupling terms of the TBME were
            scaled
        incl_proton:
            if false, proton parts of the interaction (Vpp and Vpn) were
            set to 0
    """
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')

ExpNcsmOut.__new__.__defaults__ = (None,) * 4
