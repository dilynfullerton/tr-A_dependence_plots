from __future__ import division
from __future__ import print_function

import numpy as np
from time import time

TOTAL = 0


class FitFunction:
    def __init__(self, function, num_fit_params, force_zero=None, name=None):
        self.fn = function
        self.num_fit_params = num_fit_params
        self.fz = force_zero
        self.__name__ = name

        self._set_name()

    def _set_name(self):
        if self.__name__ is None:
            self.__name__ = self.fn.__name__

    def eval(self, x, params, const_list, const_dict):
        if self.fz is not None:
            f = self.fn
            return (f(x, params, const_list, const_dict) -
                    f(self.fz, params, const_list, const_dict))
        else:
            return self.fn(x, params, const_list, const_dict)


def combine(list_of_ffn, force_zero=None, name_pref='', name_sep=', '):
    """Combines multiple fit functions (and/or dependencies) into one fit
    function.

    :param list_of_ffn: A list of FitFunctions to combine into one
    :param force_zero: (optional) force the zero of the overall result to a
    specified point
    :param name_pref: prefix for the name of the combined fit function
    :param name_sep: separator to go between fit functions
    :return: A combined fit function object, which may be used to optimize with
    respect to all of the degrees of freedom of its sub-functions
    """
    params_lengths = list()
    params_lengths.extend(list(map(lambda ffn: ffn.num_fit_params,
                                   list_of_ffn)))
    total_params_length = reduce(lambda x, y: x + y, params_lengths)

    combined_name = name_pref
    for ffn in list_of_ffn:
        combined_name += ffn.__name__ + name_sep
    combined_name = combined_name[:combined_name.rfind(name_sep)]

    def combined_ffns(x, params, const_list, const_dict):
        params_lists = list()
        t = 0
        for pl in params_lengths:
            params_lists.append(params[t:t+pl])
            t += pl
        result = 0
        for ffn, params_list in zip(list_of_ffn, params_lists):
            result += ffn.eval(x, params_list, const_list, const_dict)
        return result

    return FitFunction(combined_ffns, total_params_length,
                       force_zero=force_zero, name=combined_name)


# INDEPENDENT
def scalar(force_zero=None):
    def sf(x, params, const_list, const_dict):
        a = params[0]
        return a
    return FitFunction(sf, 1, force_zero, name='scalar')


def x1(force_zero=None):
    def x1f(x, params, const_list, const_dict):
        a = params[0]
        return a * x
    return FitFunction(x1f, 1, force_zero, name='x^1')


def linear(force_zero=None):
    def lf(x, params, const_list, const_dict):
        a, b = params[0:2]
        return a * x + b
    return FitFunction(lf, 2, force_zero, name='linear')


def x2(force_zero=None):
    def x2f(x, params, const_list, const_dict):
        a = params[0]
        return a * x ** 2
    return FitFunction(x2f, 1, force_zero, name='x^2')


def quadratic(force_zero=None):
    def qf(x, params, const_list, const_dict):
        a, b, c = params[0:3]
        return np.polyval([a, b, c], x)
    return FitFunction(qf, 3, force_zero, name='quadratic')


def x_power(n, force_zero=None):
    def xnf(x, params, const_list, const_dict):
        a = params[0]
        return a * x ** n
    return FitFunction(xnf, 1, force_zero, name='x^{}'.format(n))


def poly(n, force_zero=None):
    def pf(x, params, const_list, const_dict):
        return np.polyval(params, x)
    return FitFunction(pf, n+1, force_zero, name='poly{}'.format(n))


def asymptote(n, force_zero=None):
    def af(x, params, const_list, const_dict):
        a = params[0]
        return - a / x**n
    return FitFunction(af, 1, force_zero, name='asymptote{}'.format(n))


def asymptote_n(force_zero=None):
    def anf(x, params, const_list, const_dict):
        a, n = params[0:2]
        return - a / x**n
    return FitFunction(anf, 2, force_zero, name='asymptote_n')


# DEPENDENTS
def scalar_dependence(dep_keys, ctfs=list(), force_zero=None):
    return _dependence(f=np.polyval,
                       n_params=1,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       force_zero=force_zero,
                       name='scalar dependence')


def x1_dependence(dep_keys, ctfs=list(), force_zero=None):
    if force_zero is not None:
        return _dependence(lambda p, x: p[0] * (x - force_zero),
                           n_params=1,
                           dep_keys=dep_keys,
                           ctfs=ctfs,
                           force_zero=None,
                           name='x dependence')
    else:
        return _dependence(lambda p, x: p[0] * x,
                           n_params=1,
                           dep_keys=dep_keys,
                           ctfs=ctfs,
                           force_zero=force_zero,
                           name='x dependence')


def linear_dependence(dep_keys, ctfs=list(), force_zero=None):
    return _dependence(np.polyval,
                       n_params=2,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       force_zero=force_zero,
                       name='linear dependence')


def x2_dependence(dep_keys, ctfs=list(), force_zero=None):
    return _dependence(lambda p, x: p[0] * x ** 2,
                       n_params=1,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       force_zero=force_zero,
                       name='x^2 dependence')


def quadratic_dependence(dep_keys, ctfs=list(), force_zero=None):
    return _dependence(np.polyval,
                       n_params=3,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       force_zero=force_zero,
                       name='quadratic dependence')


def x_power_dependence(n, dep_keys, ctfs=list(), force_zero=None):
    return _dependence(lambda p, x: p[0] * x ** n,
                       n_params=1,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       force_zero=force_zero,
                       name='x^{} dependence'.format(n))


def poly_dependence(n, dep_keys, ctfs=list(), force_zero=None):
    return _dependence(np.polyval,
                       n_params=n + 1,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       force_zero=force_zero,
                       name='poly{n} dependence'.format(n=n))


def asymptotic_dependence(n, dep_keys, ctfs=list(), force_zero=None):
    return _dependence(lambda p, x: - p[0] / x**n,
                       n_params=1,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       force_zero=force_zero,
                       name='asymptotic{} dependence'.format(n))


def _dependence(f, n_params, dep_keys, name, ctfs=list(), force_zero=None):
    """An abstract function to determine f-dependence on constants given by
    dep_keys and ctfs

    :param f: f(p, x) -> y, a function that maps an array of parameters and an
    x value to a y value. Example: If one wants linear dependence on x,
    f(p, x) = p[0] * x + p[1], would be the correct function to use
    :param n_params: the number of parameters that f requires
    :param dep_keys: the keys to use with a constants dictionary to determine
    constants values. Example: If one wants dependence on the values of n and
    j, dep_keys=['n', 'j']
    :param name: the name of the dependence function
    :param ctfs: (Optional) constants transform functions are functions of the
    constants dictionary that return special combinations of the constants.
    Example: If one wants dependence on j^2, one would add the following
    function to ctfs: lambda cd: cd['j]^2
    :param force_zero: (Optional) an x value at which to force the dependence
    function to be 0
    :return: The dependence fit function
    """
    l1 = len(dep_keys) * n_params
    l2 = len(ctfs) * n_params

    def d(x, params, const_list, const_dict):
        more_constants = _do_transforms(ctfs, const_dict)
        p = np.zeros(n_params)
        dep_psubs = [params[i:i + n_params] for i in range(0, l1, n_params)]
        ctf_psubs = [params[i:i + n_params] for i in range(l1, l1+l2, n_params)]
        for dep in zip(dep_keys, *dep_psubs):
            k, p0 = dep[0], dep[1:]
            v = const_dict[k]
            for j, p0j in zip(range(n_params), p0):
                p[j] = p[j] + p0j * v
        for ctf in zip(more_constants, *ctf_psubs):
            c, p0 = ctf[0], ctf[1:]
            for j, p0j in zip(range(n_params), p0):
                p[j] = p[j] + p0j * c
        return f(p, x)
    return FitFunction(d,
                       num_fit_params=(len(dep_keys)+len(ctfs)) * n_params,
                       force_zero=force_zero,
                       name=name + ' on {}'.format(_dep_str(dep_keys, ctfs)))


def _dep_str(dep_keys, ctfs):
    return ('(' +
            ', '.join((dep_keys + list(map(lambda c: c.__name__, ctfs)))) +
            ')')


# FITTERS WITH DEPENDENCIES
def linear_with_linear_dependence(dep_keys, ctfs=list(), force_zero=None):
    return combine([linear(), linear_dependence(dep_keys, ctfs)],
                   force_zero=force_zero)


def poly_with_linear_dependence(n, dep_keys, ctfs=list(), force_zero=None):
    return combine([poly(n), linear_dependence(dep_keys, ctfs)],
                   force_zero=force_zero)


def asymptote_with_linear_dependence(n, dep_keys, ctfs=list(),
                                     force_zero=None):
    return combine([asymptote(n), linear_dependence(dep_keys, ctfs)],
                   force_zero=force_zero)


def asymptote_with_asymptotic_dependence(n, dep_keys, ctfs=list(),
                                         force_zero=None):
    return combine([asymptote(n), asymptotic_dependence(n, dep_keys, ctfs)],
                   force_zero=force_zero)


# CONSTANT TRANSFORMS
def _do_transforms(ctfs, const_dict):
    r = list()
    for ctf in ctfs:
        r.append(ctf(const_dict))
    return r


def joff2(const_dict):
    j = const_dict['j']
    return (j-1) * abs(j-1)


def jjoff(const_dict):
    j = const_dict['j']
    return j * (j - 1)


def ephw(const_dict):
    e = const_dict['e']
    hw = const_dict['hw']
    return e + hw


def y0pzbt0(const_dict):
    y0 = const_dict['y0']
    zbt0 = const_dict['zbt0']
    return y0 + zbt0
