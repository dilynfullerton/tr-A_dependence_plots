from __future__ import division, print_function, unicode_literals
from collections import namedtuple

from parse import half_int_float_to_str as to_str


# noinspection PyClassHasNoInit
class Shell(namedtuple('ShellLpt',
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
