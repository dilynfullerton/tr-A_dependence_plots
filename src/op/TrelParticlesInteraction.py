"""op/TrelParticlesIntearction.py
Definition of namedtuple representation of the 3-tuple
(particle1, particle2, interaction) specifying a 2 body term
"""
from __future__ import print_function, division, unicode_literals

from collections import namedtuple


# noinspection PyClassHasNoInit
class TrelParticlesInteraction(
    namedtuple('TrelParticlesInteraction',
               ['particle1', 'particle2', 'interaction'])):
    __slots__ = ()
