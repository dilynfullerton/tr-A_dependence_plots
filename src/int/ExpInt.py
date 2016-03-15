from __future__ import division
from __future__ import unicode_literals

from collections import namedtuple


# noinspection PyClassHasNoInit
class ExpInt(namedtuple('ExpInt', ['e', 'hw', 'base', 'rp'])):
    """Descriptive key for *.int data.
    e: max e-level
    hw: hw frequency
    base: (default None) the base number of nucleons (e.g. in targeted)
    rp: (default None) the proton radius
    """
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')


ExpInt.__new__.__defaults__ = (None, None)
