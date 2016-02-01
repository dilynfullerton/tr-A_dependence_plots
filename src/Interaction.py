from __future__ import unicode_literals
from collections import namedtuple


# noinspection PyClassHasNoInit
class Interaction(namedtuple('InteractionTuple',
                             ['a', 'b', 'c', 'd', 'j', 'zzz'])):
    __slots__ = ()

    def __str__(self):
        a = str(self.a)
        b = str(self.b)
        c = str(self.c)
        d = str(self.d)
        j = str(self.j)
        sep = unichr(9474).strip()
        left = unichr(12296).strip()
        right = unichr(12297).strip()
        # sep = '|'
        # left = '<'
        # right = '>'
        return ('({left}{a},{b}{s}'
                'V'
                '{s}{c},{d}{right}, j={j})'
                '').format(a=a, b=b, c=c, d=d, j=j,
                           left=left, right=right,
                           s=sep)

    def __eq__(self, other):
        return self[0:5] == other[0:5]

Interaction.__new__.__defaults__ = (None,)
