from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np


def s_identity(plots):
    return plots


def s_combine_like(f):
    def scl(plots):
        m = dict()
        for plot in plots:
            const = f(plot)
            if const in m:
                m[const] = _combine_plots(m[const], plot)
            else:
                m[const] = plot
        return m.values()
    scl.__name__ = b's_combine_like {}'.format(f.__name__)
    return scl


def _combine_plots(p1, p2):
    x1, y1 = p1[0:2]
    x2, y2 = list(), list()
    for x2i, y2i in zip(*p2[0:2]):
        if x2i not in x1:
            x2.append(x2i)
            y2.append(y2i)
    x = np.concatenate((x1, np.array(x2)))
    y = np.concatenate((y1, np.array(y2)))
    const_list = list()
    for c1, c2 in zip(p1[2], p2[2]):
        if c1 is not None and c2 is not None and c1 == c2:
            const_list.append(c1)
        else:
            const_list.append(None)
    const_dict = dict()
    d1, d2 = p1[3], p2[3]
    for k in set(d1.keys() + d2.keys()):
        if k in d1 and k in d2:
            v1, v2 = d1[k], d2[k]
            if v1 is not None and v2 is not None and v1 == v2:
                const_dict[k] = d1[k]
            else:
                const_dict[k] = None
        else:
            const_dict[k] = None
    return x, y, const_list, const_dict


def qnums(plot):
    return plot[3]['qnums']
