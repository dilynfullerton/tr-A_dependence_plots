"""TwoBodyInteraction.py
Defines namedtuple representation of a matrix element
"""
from __future__ import division, print_function, unicode_literals
from collections import namedtuple


# noinspection PyClassHasNoInit
class NushellTbme(namedtuple(
    'NushellTbme', ['a', 'b', 'c', 'd', 'j', 't']
)):
    """Stores label for interaction (*.int) two-body matrix element label
    """
    __slots__ = ()

    def __str__(self):
        a, b, c, d, j = [
            str(x) for x in [self.a, self.b, self.c, self.d, self.j]]
        sep, left, right = '|', '<', '>'
        return '({left}{a},{b}{s}V{s}{c},{d}{right}, j={j})'.format(
            a=a, b=b, c=c, d=d, j=j, left=left, right=right, s=sep)

    def __eq__(self, other):
        return self[0:5] == other[0:5]
NushellTbme.__new__.__defaults__ = (None,)
