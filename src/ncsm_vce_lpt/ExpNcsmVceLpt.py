from __future__ import print_function, division, unicode_literals

from collections import namedtuple


# noinspection PyClassHasNoInit
class ExpNcsmVceLpt(namedtuple('ExpNcsmVceLpt',
                               ['Z', 'A_presc', 'Nhw', 'n1', 'n2'])):
    """Identifier for a group of *.lpt results from performing NuShellX
    calculations on *.int files from a VCE
    """
    __slots__ = ()

    def __str__(self):
        return str(tuple(self._asdict().values())).replace(', None', '')

ExpNcsmVceLpt.__new__.__defaults__ = (None, None, None)
