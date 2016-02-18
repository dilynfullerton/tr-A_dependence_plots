from __future__ import print_function, division, unicode_literals

from collections import namedtuple


class TrelOneBodyOp(namedtuple('TrelOneBodyOp', ['particle1', 'particle2'])):
    """Stores data lines for *.op one body relative kinetic energies
    """
    __slots__ = ()
