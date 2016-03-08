from __future__ import print_function, division, unicode_literals

from collections import namedtuple


# noinspection PyClassHasNoInit
class TrelParticlesInteraction(
    namedtuple('TrelParticlesInteraction',
               ['particle1', 'particle2', 'interaction'])):
    __slots__ = ()
