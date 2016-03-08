from __future__ import print_function, division, unicode_literals

from collections import namedtuple


# noinspection PyClassHasNoInit
class TrelParticles(namedtuple('TrelParticles', ['particle1', 'particle2'])):
    """Stores data lines for *.op one body relative kinetic energies
    """
    __slots__ = ()
