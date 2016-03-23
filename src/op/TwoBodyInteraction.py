from __future__ import print_function, division, unicode_literals

from collections import namedtuple


# noinspection PyClassHasNoInit
class TwoBodyInteraction(namedtuple('TwoBodyInteraction',
                                    ['a', 'b', 'c', 'd'])):
    __slots__ = ()

    # noinspection PyCompatibility
    def __str__(self):
        sep = unichr(9474).strip()
        left = unichr(12296).strip()
        right = unichr(12297).strip()
        # sep = b'|'
        # left = b'('
        # right = b')'
        return ('{left}{a:2} {b:2}{s}'
                ' V '
                '{s}{c:2} {d:2}{right}'
                '').format(a=self.a, b=self.b, c=self.c, d=self.d,
                           left=left, right=right, s=sep)
