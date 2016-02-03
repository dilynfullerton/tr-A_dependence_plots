from __future__ import division
from __future__ import unicode_literals
from collections import namedtuple
from parse import half_int_float_to_str as to_str


# noinspection PyClassHasNoInit
class QuantumNumbers(namedtuple('QuantumNumbers', ['n', 'l', 'j', 'tz'])):
    """Stores descriptive quantum numbers for interaction (*.int) orbital
    """
    __slots__ = ()

    def __str__(self):
        n = str(int(self.n))
        l = str(int(self.l))
        j = str(int(2*self.j)) + '/2'
        tz = str(int(2*self.tz)) + '/2'
        tz = '+' + tz if self.tz > 0 else tz
        return '(n={n}, l={l}, j={j}, tz={tz})'.format(n=n, l=l, j=j, tz=tz)


# noinspection PyClassHasNoInit
class TwoBodyInteraction(namedtuple('TwoBodyInteraction',
                                    ['a', 'b', 'c', 'd', 'j', 'zzz'])):
    """Stores label for interaction (*.int) two-body matrix element label
    """
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
TwoBodyInteraction.__new__.__defaults__ = (None,)


# noinspection PyClassHasNoInit
class Shell(namedtuple('Shell',
                       ['NJ', 'E', 'Ex', 'J', 'T', 'p', 'lowest_Ex', 'name'])):
    """Holds the body data for *.lpt files
    """
    __slots__ = ()

    def __str__(self):
        s = '({}, {:.3}, {:.3}, {}, {}, {:+}, {:.3}, {})'
        j_str = to_str(self.J)
        t_str = to_str(self.T)
        v = self._asdict().values()
        v[3:5] = j_str, t_str
        v[6] = self.lowest_Ex if self.lowest_Ex is not None else ''
        return s.format(*v)
