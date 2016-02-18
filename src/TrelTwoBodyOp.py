from __future__ import print_function, division, unicode_literals

from collections import namedtuple


class TrelTwoBodyOp(namedtuple('TrelTwoBodyOp',
                               ['particle1', 'particle2', 'interaction'])):
    __slots__ = ()

    def __getitem__(self, item):
        if item in ['a', 'b', 'c', 'd']:
            return self['interaction'][item]
        else:
            return super(TrelTwoBodyOp, self)[item]
