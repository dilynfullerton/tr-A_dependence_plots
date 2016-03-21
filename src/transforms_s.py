"""SUPER-transforms to apply to lists of plots before fitting

These are transforms that operate on a list of multiple plots as a whole.
For example, combine_like will combine multiple plots that share a common set
of properties into a single plot
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np


def s_identity(plots):
    return plots


def s_n_values(n_values_list):
    """(For *.lpt) Returns a function that filters the given list of plots to
    only include those with N values in the n_values_list
    :param n_values_list: a list of N values
    """
    def snv(plots):
        return list(filter(lambda p: p[3]['N'] in n_values_list, plots))
    snv.__name__ = b's_n_values {}'.format(n_values_list)
    return snv


# COMBINE RULES FOR s_combine_like
def keep_lesser_x0_y0_zbt0_pair_in_dict(p, p1, p2):
    const_dict = p[3]
    cd1, cd2 = p1[3], p2[3]
    if 'x0' in cd1 and 'x0' in cd2:
        if cd2['x0'] < cd1['x0']:
            const_dict['x0'] = cd2['x0']
            const_dict['y0'] = cd2['y0'] if 'y0' in cd2 else None
            const_dict['zbt0'] = cd2['zbt0'] if 'zbt0' in cd2 else None
        else:
            const_dict['x0'] = cd1['x0']
            const_dict['y0'] = cd1['y0'] if 'y0' in cd1 else None
            const_dict['zbt0'] = cd1['zbt0'] if 'zbt0' in cd1 else None
    p = p[0:3] + (const_dict,)
    return p


def s_combine_like(keys=None, f=None,
                   combine_rules=list([keep_lesser_x0_y0_zbt0_pair_in_dict]),
                   sort_plot=False, sort_key=lambda x_y: x_y[0]):
    """Returns a super-fit-transform that combines all plots that share the
    same value returned by the given f, which acts on a single plot

    :param keys: keys for the const_dict by which to specify the set of values,
    by ALL of which plots are to be compared
    :param f: a function which acts on a single plot and returns a comparable
    item
    :param combine_rules: function of the form f(plot, plot, plot) -> plot
    that define ways that the constants lists and dicts should be merged
    :param sort_plot: if true, (x, y) pairs are sorted based on sort_key
    :param sort_key: key by which (x, y) pairs are sorted;
    (e.g. lambda x_y: x_y[0] sorts by x)
    """
    if keys is not None:
        f = _keys(keys)
    elif f is None:
        return lambda p: p

    def scl(plots):
        m = dict()
        for plot in plots:
            const = f(plot)
            if const in m:
                m[const] = _combine_plots(
                    p1=m[const], p2=plot, combine_rules=combine_rules,
                    sort_plot=sort_plot, sort_key=sort_key
                )
            else:
                m[const] = plot
        return m.values()
    scl.__name__ = b's_combine_like {}'.format(f.__name__)
    return scl


def _combine_plots(p1, p2, combine_rules=None,
                   sort_plot=False, sort_key=lambda x_y: x_y[0]):
    # Combine x arrays with each other and y arrays with each other
    x1, y1 = p1[0:2]
    x2, y2 = list(), list()
    for x2i, y2i in zip(*p2[0:2]):
        if x2i not in x1:
            x2.append(x2i)
            y2.append(y2i)
    x = np.concatenate((x1, np.array(x2)))
    y = np.concatenate((y1, np.array(y2)))
    # Sort plot
    if sort_plot:
        next_x, next_y = list(), list()
        for xi, yi in sorted(zip(x, y), key=sort_key):
            next_x.append(xi)
            next_y.append(yi)
        x = np.array(next_x)
        y = np.array(next_y)
    # Combine constant lists
    const_list = list()
    for c1, c2 in zip(p1[2], p2[2]):
        if c1 is not None and c2 is not None and _const_equals(c1, c2):
            const_list.append(c1)
        else:
            const_list.append(None)
    const_dict = dict()
    # Combine constant dicts
    d1, d2 = p1[3], p2[3]
    for k in set(d1.keys() + d2.keys()):
        if k in d1 and k in d2:
            v1, v2 = d1[k], d2[k]
            if v1 is not None and v2 is not None and _const_equals(v1, v2):
                const_dict[k] = d1[k]
            else:
                const_dict[k] = None
        else:
            const_dict[k] = None
    # Other combine rules
    p = x, y, const_list, const_dict
    if combine_rules is not None:
        for rule in combine_rules:
            p = rule(p, p1, p2)
    return p


def _const_equals(c1, c2):
    if isinstance(c1, np.ndarray) and isinstance(c2, np.ndarray):
        return c1.all() == c2.all()
    else:
        return c1 == c2


# FUNCTIONS FOR s_combine_like
def qnums(plot):
    return plot[3]['qnums']


def _keys(list_of_key):
    def const_vals(plot):
        const_dict = plot[3]
        vals = tuple(map(lambda k: const_dict[k] if k in const_dict else None,
                         list_of_key))
        return vals
    const_vals.__name__ = str(list_of_key)
    return const_vals
