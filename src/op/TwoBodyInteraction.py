from __future__ import print_function, division, unicode_literals

from collections import namedtuple


class TwoBodyInteraction(namedtuple('TwoBodyInteraction',
                                    ['a', 'b', 'c', 'd'])):
    __slots__ = ()

    def __str__(self):
        a = str(self.a)
        b = str(self.b)
        c = str(self.c)
        d = str(self.d)
        sep = unichr(9474).strip()
        left = unichr(12296).strip()
        right = unichr(12297).strip()
        # sep = '|'
        # left = '<'
        # right = '>'
        return ('({left}{a},{b}{s}'
                'V'
                '{s}{c},{d}{right})'
                '').format(a=a, b=b, c=c, d=d, left=left, right=right, s=sep)
