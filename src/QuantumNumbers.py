from __future__ import unicode_literals
from __future__ import division
from collections import namedtuple


# noinspection PyClassHasNoInit
class QuantumNumbers(namedtuple('QuantumNumbers', ['n', 'l', 'j', 'tz'])):
    __slots__ = ()

    def __str__(self):
        n = str(int(self.n))
        l = str(int(self.l))
        j = str(int(2*self.j)) + '/2'
        tz = str(int(2*self.tz)) + '/2'
        tz = '+' + tz if self.tz > 0 else tz
        return '(n={n}, l={l}, j={j}, tz={tz})'.format(n=n, l=l, j=j, tz=tz)
