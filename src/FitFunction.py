from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np


class FitFunction:
    def __init__(self, function, num_fit_params, force_zero=None,
                 name=None,
                 code='',
                 force_zero_func=None,
                 force_k=None,
                 force_k_func=None):
        self.fn = function
        self.num_fit_params = num_fit_params
        self.fz = force_zero
        self.fzfn = force_zero_func
        self.fk = force_k
        self.fkfn = force_k_func
        self.name = name
        self.code = code

        self._set_name()
        self._set_code()
        self.__name__ = self.name

    def _set_name(self):
        if self.name is None:
            self.name = self.fn.__name__
        if self.fz is not None:
            self.name += b' force zero {}'.format(self.fz)
        elif self.fzfn is not None:
            self.name += b' force zero with {}'.format(self.fzfn.__name__)
        elif self.fk is not None:
            self.name += b' force point {}'.format(self.fk)
        elif self.fkfn is not None:
            self.name += b' force point with {}'.format(self.fkfn.__name__)

    def _set_code(self):
        if self.code is '':
            self.code = self.name if self.name is not None else self.fn.__name__
        if self.fz is not None:
            self.code += b'fz{}'.format(self.fz)
        elif self.fzfn is not None:
            self.code += b'fzfz'
        elif self.fk is not None:
            self.code += b'fk{}'.format(self.fk)
        elif self.fkfn is not None:
            self.code += b'fkfn'

    def eval(self, x, params, const_list, const_dict):
        if self.fz is not None:
            f = self.fn
            return (f(x, params, const_list, const_dict) -
                    f(self.fz, params, const_list, const_dict))
        elif self.fzfn is not None:
            f = self.fn
            x0 = self.fzfn(const_dict)
            return (f(x, params, const_list, const_dict) -
                    f(x0, params, const_list, const_dict))
        elif self.fk is not None:
            f = self.fn
            x0, k = self.fk
            return (f(x, params, const_list, const_dict) -
                    f(x0, params, const_list, const_dict) +
                    k)
        elif self.fkfn is not None:
            f = self.fn
            x0, k = self.fkfn(const_dict)
            return (f(x, params, const_list, const_dict) -
                    f(x0, params, const_list, const_dict) +
                    k)
        else:
            return self.fn(x, params, const_list, const_dict)


def combine_ffns(list_of_ffn, force_zero=None,
                 name_pref='[', name_sep=', ', name_suff=']',
                 code_pref='', code_sep='-', code_suff='',
                 **kwargs):
    """Combines multiple fit functions (and/or dependencies) into one fit
    function.

    :param code_suff:
    :param name_suff:
    :param code_sep:
    :param code_pref:
    :param list_of_ffn: A list of FitFunctions to combine into one
    :param force_zero: (optional) force the zero of the overall result to a
    specified point
    :param name_pref: prefix for the name of the combined fit function
    :param name_sep: separator to go between fit functions
    :return: A combined fit function object, which may be used to optimize with
    respect to all of the degrees of freedom of its sub-functions
    """
    params_lengths = [ffn.num_fit_params for ffn in list_of_ffn]
    params_breaks = [0]
    for pl, i in zip(params_lengths, range(len(params_lengths))):
        params_breaks.append(pl + params_breaks[i])
    total_params_length = params_breaks[-1]

    combined_name = name_pref
    combined_code = code_pref
    for ffn in list_of_ffn:
        combined_name += ffn.name + name_sep
        combined_code += ffn.code + code_sep
    combined_name = combined_name[:combined_name.rfind(name_sep)] + name_suff
    combined_code = combined_code[:combined_code.rfind(code_sep)] + code_suff

    def combined_ffns(x, params, const_list, const_dict):
        result = 0
        for fitfn, ii, jj in zip(list_of_ffn, params_breaks, params_breaks[1:]):
            result += fitfn.eval(x, params[ii:jj], const_list, const_dict)
        return result

    return FitFunction(combined_ffns, total_params_length,
                       force_zero=force_zero,
                       name=combined_name,
                       code=combined_code, **kwargs)


# INDEPENDENT
def scalar():
    # noinspection PyUnusedLocal
    def sf(x, params, const_list, const_dict):
        a = params[0]
        return a

    return FitFunction(sf, 1, name='scalar', code='s')


def x1(force_zero=None, **kwargs):
    # noinspection PyUnusedLocal
    def x1f(x, params, const_list, const_dict):
        a = params[0]
        return a * x

    return FitFunction(x1f, 1, force_zero, name='x^1', code='x1', **kwargs)


def linear(force_zero=None, **kwargs):
    if force_zero is None and len(kwargs) == 0:
        # noinspection PyUnusedLocal
        def lf(x, params, const_list, const_dict):
            a, b = params[0:2]
            return a * x + b

        return FitFunction(lf, 2, force_zero, name='linear', code='p1',
                           **kwargs)
    else:
        # noinspection PyUnusedLocal
        def lf(x, params, const_list, const_dict):
            a = params[0]
            return a * x

        return FitFunction(lf, 1, force_zero, name='linear', code='p1',
                           **kwargs)


def x2(force_zero=None, **kwargs):
    # noinspection PyUnusedLocal
    def x2f(x, params, const_list, const_dict):
        a = params[0]
        return a * x ** 2

    return FitFunction(x2f, 1, force_zero, name='x^2', code='x2', **kwargs)


def quadratic(force_zero=None, **kwargs):
    if force_zero is None and len(kwargs) == 0:
        # noinspection PyUnusedLocal
        def qf(x, params, const_list, const_dict):
            a, b, c = params[0:3]
            return np.polyval([a, b, c], x)

        return FitFunction(qf, 3, force_zero, name='quadratic', code='p2',
                           **kwargs)
    else:
        # noinspection PyUnusedLocal
        def qf(x, params, const_list, const_dict):
            a, b = params[0:2]
            return np.polyval([a, b, 0], x)

        return FitFunction(qf, 2, force_zero, name='quadratic', code='p2',
                           **kwargs)


def x_power(n, force_zero=None, **kwargs):
    # noinspection PyUnusedLocal
    def xnf(x, params, const_list, const_dict):
        a = params[0]
        return a * x ** n

    return FitFunction(xnf, 1, force_zero,
                       name='x^{}'.format(n),
                       code='x{}'.format(n), **kwargs)


def poly(n, force_zero=None, **kwargs):
    if force_zero is None and len(kwargs) == 0:
        # noinspection PyUnusedLocal
        def pf(x, params, const_list, const_dict):
            return np.polyval(params, x)

        return FitFunction(pf, n + 1, force_zero,
                           name='poly{}'.format(n),
                           code='p{}'.format(n), **kwargs)
    else:
        # noinspection PyUnusedLocal
        def pf(x, params, const_list, const_dict):
            return np.polyval(np.concatenate((params, np.zeros(1))), x)

        return FitFunction(pf, n, force_zero,
                           name='poly{}'.format(n),
                           code='p{}'.format(n), **kwargs)


def asymptote(n, force_zero=None, **kwargs):
    # noinspection PyUnusedLocal
    def af(x, params, const_list, const_dict):
        a = params[0]
        return - a / x ** n

    return FitFunction(af, 1, force_zero,
                       name='asymptote{}'.format(n),
                       code='a{}'.format(n),
                       **kwargs)


def asymptote_n(force_zero=None, **kwargs):
    # noinspection PyUnusedLocal
    def anf(x, params, const_list, const_dict):
        a, n = params[0:2]
        return - a / x ** n

    return FitFunction(anf, 2, force_zero,
                       name='asymptote_n',
                       code='an', **kwargs)


# DEPENDENTS
def scalar_dependence(dep_keys, ctfs=list()):
    return _dependence(f=lambda p, x: p[0],
                       n_params=1,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       name='scalar dependence',
                       code='s:{}')


def x1_dependence(dep_keys, ctfs=list(), force_zero=None, **kwargs):
    return _dependence(lambda p, x: p[0] * x,
                       n_params=1,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       force_zero=force_zero,
                       name='x dependence',
                       code='x1:{}',
                       **kwargs)


def linear_dependence(dep_keys, ctfs=list(), force_zero=None, **kwargs):
    if force_zero is None and len(kwargs) == 0:
        return _dependence(np.polyval,
                           n_params=2,
                           dep_keys=dep_keys,
                           ctfs=ctfs,
                           force_zero=force_zero,
                           name='linear dependence',
                           code='p1:{}',
                           **kwargs)
    else:
        return _dependence(lambda p, x:
                           np.polyval(np.concatenate((p, np.zeros(1))), x),
                           n_params=1,
                           dep_keys=dep_keys,
                           ctfs=ctfs,
                           force_zero=force_zero,
                           name='linear dependence',
                           code='p1:{}',
                           **kwargs)


def x2_dependence(dep_keys, ctfs=list(), force_zero=None, **kwargs):
    return _dependence(lambda p, x: p[0] * x ** 2,
                       n_params=1,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       force_zero=force_zero,
                       name='x^2 dependence',
                       code='x2:{}',
                       **kwargs)


def quadratic_dependence(dep_keys, ctfs=list(), force_zero=None, **kwargs):
    if force_zero is None and len(kwargs) == 0:
        return _dependence(np.polyval,
                           n_params=3,
                           dep_keys=dep_keys,
                           ctfs=ctfs,
                           force_zero=force_zero,
                           name='quadratic dependence',
                           code='p2:{}',
                           **kwargs)
    else:
        return _dependence(lambda p, x:
                           np.polyval(np.concatenate((p, np.zeros(1))), x),
                           n_params=2,
                           dep_keys=dep_keys,
                           ctfs=ctfs,
                           force_zero=force_zero,
                           name='quadratic dependence',
                           code='p2:{}',
                           **kwargs)


def x_power_dependence(n, dep_keys, ctfs=list(), force_zero=None, **kwargs):
    return _dependence(lambda p, x: p[0] * x ** n,
                       n_params=1,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       force_zero=force_zero,
                       name='x^{} dependence'.format(n),
                       code='x{}'.format(n)+':{}',
                       **kwargs)


def poly_dependence(n, dep_keys, ctfs=list(), force_zero=None, **kwargs):
    if force_zero is None and len(kwargs) == 0:
        return _dependence(np.polyval,
                           n_params=n + 1,
                           dep_keys=dep_keys,
                           ctfs=ctfs,
                           force_zero=force_zero,
                           name='poly{n} dependence'.format(n=n),
                           code='p{}'.format(n) + ':{}',
                           **kwargs)
    else:
        return _dependence(lambda p, x:
                           np.polyval(np.concatenate((p, np.zeros(1))), x),
                           n_params=n,
                           dep_keys=dep_keys,
                           ctfs=ctfs,
                           force_zero=force_zero,
                           name='poly{n} dependence'.format(n=n),
                           code='p{}'.format(n) + ':{}',
                           **kwargs)


def asymptotic_dependence(n, dep_keys, ctfs=list(), force_zero=None, **kwargs):
    return _dependence(lambda p, x: - p[0] / x ** n,
                       n_params=1,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       force_zero=force_zero,
                       name='asymptotic{} dependence'.format(n),
                       code='a{}'.format(n) + ':{}',
                       **kwargs)


def _dependence(f, n_params, dep_keys, name, ctfs=list(), force_zero=None,
                code='', **kwargs):
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

    # noinspection PyUnusedLocal
    def d(x, params, const_list, const_dict):
        more_constants = _do_transforms(ctfs, const_dict)
        p = np.zeros(n_params)
        dep_psubs = [params[i:i + n_params] for i in range(0, l1, n_params)]
        ctf_psubs = [params[i:i + n_params] for i in
                     range(l1, l1 + l2, n_params)]
        for dep in zip(dep_keys, *dep_psubs):
            k, p0 = dep[0], dep[1:]
            if k not in const_dict:
                continue
            else:
                v = const_dict[k]
            for j, p0j in zip(range(n_params), p0):
                p[j] = p[j] + p0j * v
        for ctf in zip(more_constants, *ctf_psubs):
            c, p0 = ctf[0], ctf[1:]
            for j, p0j in zip(range(n_params), p0):
                p[j] = p[j] + p0j * c
        return f(p, x)

    dep_str = _dep_str(dep_keys, ctfs)
    return FitFunction(d,
                       num_fit_params=(len(dep_keys) + len(ctfs)) * n_params,
                       force_zero=force_zero,
                       name=name + ' on {}'.format(dep_str),
                       code=code.format(dep_str),
                       **kwargs)


def _dep_str(dep_keys, ctfs):
    return ('(' +
            ', '.join((dep_keys + list(map(lambda c: c.__name__, ctfs)))) +
            ')')


# FITTERS WITH DEPENDENCIES
def linear_with_linear_dependence(dep_keys, ctfs=list(), force_zero=None,
                                  **kwargs):
    return combine_ffns([linear(force_zero=force_zero),
                         linear_dependence(dep_keys, ctfs,
                                           force_zero=force_zero)],
                        force_zero=force_zero,
                        **kwargs)


def poly_with_linear_dependence(n, dep_keys, ctfs=list(), force_zero=None,
                                **kwargs):
    return combine_ffns([poly(n), linear_dependence(dep_keys, ctfs)],
                        force_zero=force_zero,
                        **kwargs)


def asymptote_with_linear_dependence(n, dep_keys, ctfs=list(),
                                     force_zero=None,
                                     **kwargs):
    return combine_ffns([asymptote(n), linear_dependence(dep_keys, ctfs)],
                        force_zero=force_zero,
                        **kwargs)


def asymptote_with_asymptotic_dependence(n, dep_keys, ctfs=list(),
                                         force_zero=None, **kwargs):
    return combine_ffns(
            [asymptote(n), asymptotic_dependence(n, dep_keys, ctfs)],
            force_zero=force_zero, **kwargs)


# CONSTANT TRANSFORMS
def _do_transforms(ctfs, const_dict):
    r = list()
    for ctf in ctfs:
        r.append(ctf(const_dict))
    return r


def joff2(const_dict):
    j = const_dict['j']
    return (j - 1) * abs(j - 1)


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


# FORCE ZERO FUNCTIONS
def fz_to_x0(const_dict):
    return const_dict['x0']


# FORCE K FUNCTIONS
def fk_to_y0(const_dict):
    return const_dict['x0'], const_dict['y0']


def fk_to_zbt0(const_dict):
    return const_dict['x0'], const_dict['zbt0']
