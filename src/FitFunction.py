from __future__ import division
from __future__ import print_function

import numpy as np


class FitFunction:
    def __init__(self, function, num_fit_params, force_zero=None, name=None):
        self.fn = function
        self.fit_params = num_fit_params
        self.fz = force_zero
        self.name = name

        self._set_name()

    def _set_name(self):
        if self.name is None:
            self.name = self.fn.__name__
        if self.fz is not None:
            self.name += 'with forced zero at x={}'.format(self.fz)

    def eval(self, x, params, constants):
        if self.fz is not None:
            f = self.fn
            return f(x, params, constants) - f(self.fz, params, constants)
        else:
            return self.fn(x, *params)


def combine(list_of_ffn, name_pref='', name_sep=' with '):
    params_lengths = list([len(list_of_ffn)])
    params_lengths.extend(list(map(lambda ffn: ffn.fit_params, list_of_ffn)))
    total_params_length = reduce(lambda x, y: x + y, params_lengths)

    combined_name = name_pref
    for ffn in list_of_ffn:
        combined_name += ffn.name + name_sep
    combined_name = combined_name[:combined_name.rfind(name_sep)]

    def combined_ffns(x, params, constants):
        params_lists = list()
        t = 0
        for pl in params_lengths:
            params_lists.append(params[t:t+pl])
            t += pl
        result = 0
        for ffn, p0, params_list in zip(list_of_ffn, params_lists[0],
                                        params_lists[1:]):
            result += p0 * ffn.eval(x, params_list, constants)
        return result

    return FitFunction(combined_ffns, total_params_length, name=combined_name)


# INDEPENDENT
def linear_fit(force_zero=None):
    def lf(x, params, constants):
        a, b = params[0:2]
        return a * x + b
    return FitFunction(lf, 2, force_zero, name='linear_fit')


def quadratic_fit(force_zero=None):
    def qf(x, params, constants):
        a, b, c = params[0:3]
        return np.polyval([a, b, c], x)
    return FitFunction(qf, 3, force_zero, name='quadratic_fit')


def poly_fit(n, force_zero=None):
    def pf(x, params, constants):
        return np.polyval(params, x)
    return FitFunction(pf, n+1, force_zero, name='poly_fit{}'.format(n))


def asymptote_fit(n, force_zero=None):
    def af(x, params, constants):
        a, b = params[0:2]
        return - a / x**n + b
    return FitFunction(af, 2, force_zero, name='asymptote{}_fit'.format(n))


# DEPENDENTS
def scalar_dependence(dep_keys, force_zero=None):
    def sd(x, params, constants):
        a = 0
        for k, a0 in zip(dep_keys, params):
            a += a0 * constants[k]
        return a
    return FitFunction(sd,
                       num_fit_params=len(dep_keys),
                       force_zero=force_zero,
                       name='scalar dependence on {}'.format(dep_keys))


def linear_dependence(dep_keys, force_zero=None):
    def ld(x, params, constants):
        a = 0
        b = 0
        for k, a0, b0 in zip(dep_keys, params[0::2], params[1::2]):
            a += a0 * constants[k]
            b += b0 * constants[k]
        return a * x + b
    return FitFunction(ld,
                       num_fit_params=2*len(dep_keys),
                       force_zero=force_zero,
                       name='linear dependence on {}'.format(dep_keys))


def quadratic_dependence(dep_keys, force_zero=None):
    def qd(x, params, constants):
        a = 0
        b = 0
        c = 0
        for k, a0, b0, c0 in zip(dep_keys,
                                 params[0::3], params[1::3], params[2::3]):
            v = constants[k]
            a += a0 * v
            b += b0 * v
            c += c0 * v
        return a * x**2 + b * x + c
    return FitFunction(qd,
                       num_fit_params=3 * len(dep_keys),
                       force_zero=force_zero,
                       name='quadratic dependence on {}'.format(dep_keys))


def poly_dependence(n, dep_keys, force_zero=None):
    def pd(x, params, constants):
        p = np.zeros(n+1)
        params_sublists = list()
        for i in range(n+1):
            params_sublists.append(params[i::n+1])
        for s in zip(dep_keys, *params_sublists):
            k = s[0]
            v = constants[k]
            p0 = s[1:]
            for j, p0j in zip(range(n+1), p0):
                p[i] = p[i] + p0j * v
        return np.polyval(p, x)
    return FitFunction(pd,
                       num_fit_params=(n+1)*len(dep_keys),
                       force_zero=force_zero,
                       name='poly{n} dependence on {d}'.format(n=n, d=dep_keys))


# FITTERS WITH DEPENDENCIES
def linear_fit_with_linear_dependence(dep_keys, force_zero=None):
    return combine([linear_fit(force_zero),
                    linear_dependence(dep_keys, force_zero)])


def poly_fit_with_linear_dependence(n, dep_keys, force_zero=None):
    return combine([poly_fit(n, force_zero),
                    linear_dependence(dep_keys, force_zero)])


def asymptote_fit_with_linear_dependence(n, dep_keys, force_zero=None):
    return combine([asymptote_fit(n, force_zero),
                    linear_dependence(dep_keys, force_zero)])

