from __future__ import print_function, division, unicode_literals

from collections import namedtuple


class ExpLpt(namedtuple('ExpLpt', ['Z', 'int'])):
    """Exp definition for *.lpt files
           Z: proton number
           int: interaction type (e.g. 'usdb', 'sd-shell...', 'fit-gen...')
    """
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')
