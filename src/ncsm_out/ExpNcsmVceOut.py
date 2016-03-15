from __future__ import print_function, division, unicode_literals

from collections import namedtuple


# noinspection PyClassHasNoInit
class ExpNcsmVceOut(namedtuple('ExpNcsmVceOut', ['Z', 'Nhw', 'n1', 'n2'])):
    """Identifier for a set of NCSD *.out files generated for the same
    element in the same model space
    """
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')

ExpNcsmVceOut.__new__.__defaults__ = (None,) * 3
