from __future__ import division
from __future__ import print_function

import numpy as np


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


def combine(list_of_ffn, name_pref='', name_sep=' '):
    #params_lengths = list([len(list_of_ffn)])
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
        # for ffn, p0, params_list in zip(list_of_ffn, params_lists[0],
        #                                 params_lists[1:]):
        #     result += p0 * ffn.eval(x, params_list, constants)
        for ffn, params_list in zip(list_of_ffn, params_lists):
            result += ffn.eval(x, params_list, const_list, const_dict)
        return result

    return FitFunction(combined_ffns, total_params_length, name=combined_name)


# INDEPENDENT
def linear(force_zero=None):
    def lf(x, params, const_list, const_dict):
        a, b = params[0:2]
        return a * x + b
    return FitFunction(lf, 2, force_zero, name='linear')


def quadratic(force_zero=None):
    def qf(x, params, const_list, const_dict):
        a, b, c = params[0:3]
        return np.polyval([a, b, c], x)
    return FitFunction(qf, 3, force_zero, name='quadratic')


def poly(n, force_zero=None):
    def pf(x, params, const_list, const_dict):
        return np.polyval(params, x)
    return FitFunction(pf, n+1, force_zero, name='poly{}'.format(n))


def asymptote(n, force_zero=None):
    def af(x, params, const_list, const_dict):
        a, b = params[0:2]
        return - a / x**n + b
    return FitFunction(af, 2, force_zero, name='asymptote{}'.format(n))


def asymptote_n(force_zero=None):
    def anf(x, params, const_list, const_dict):
        a, b, n = params[0:3]
        return - a / x**n + b
    return FitFunction(anf, 3, force_zero, name='asymptote_n')


# DEPENDENTS
def scalar_dependence(dep_keys, ctfs=list(), force_zero=None):
    return _dependence(f=np.polyval,
                       num_params=1,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       force_zero=force_zero,
                       name='scalar dependence')


def linear_dependence(dep_keys, ctfs=list(), force_zero=None):
    return _dependence(np.polyval,
                       num_params=2,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       force_zero=force_zero,
                       name='linear dependence')


def quadratic_dependence(dep_keys, ctfs=list(), force_zero=None):
    return _dependence(np.polyval,
                       num_params=3,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       force_zero=force_zero,
                       name='quadratic dependence')


def poly_dependence(n, dep_keys, ctfs=list(), force_zero=None):
    return _dependence(np.polyval,
                       num_params=n+1,
                       dep_keys=dep_keys,
                       ctfs=ctfs,
                       force_zero=force_zero,
                       name='poly{n} dependence'.format(n=n))


def _dependence(f, num_params, dep_keys, name, ctfs=list(), force_zero=None):
    def d(x, params, const_list, const_dict):
        more_constants = _do_transforms(ctfs, const_dict)
        p = np.zeros(num_params)
        dep_params_sublists = list()
        ctf_params_sublists = list()
        for i in range(num_params):
            ii = len(dep_keys) * num_params
            dep_params_sublists.append(params[i:ii:num_params])
            ctf_params_sublists.append(params[ii+i::num_params])
        for dep in zip(dep_keys, *dep_params_sublists):
            k, p0 = dep[0], dep[1:]
            v = const_dict[k]
            for j, p0j in zip(range(num_params), p0):
                p[j] = p[j] + p0j * v
        for ctf in zip(more_constants, *ctf_params_sublists):
            c, p0 = ctf[0], ctf[1:]
            for j, p0j in zip(range(num_params), p0):
                p[j] = p[j] + p0j * c
        return f(p, x)
    return FitFunction(d,
                       num_fit_params=(len(dep_keys)+len(ctfs))*num_params,
                       force_zero=force_zero,
                       name=name + ' on {}'.format(_dep_str(dep_keys, ctfs)))


def _dep_str(dep_keys, ctfs):
    return str(dep_keys + list(map(lambda c: c.__name__, ctfs)))


# FITTERS WITH DEPENDENCIES
def linear_with_linear_dependence(dep_keys, ctfs=list(), force_zero=None):
    return combine([linear(force_zero),
                    linear_dependence(dep_keys, ctfs, force_zero)])


def poly_with_linear_dependence(n, dep_keys, ctfs=list(), force_zero=None):
    return combine([poly(n, force_zero),
                    linear_dependence(dep_keys, ctfs, force_zero)])


def asymptote_with_linear_dependence(n, dep_keys, ctfs=list(),
                                     force_zero=None):
    return combine([asymptote(n, force_zero),
                    linear_dependence(dep_keys, ctfs, force_zero)])


# CONSTANT TRANSFORMS
def _do_transforms(ctfs, constants):
    r = list()
    for ctf in ctfs:
        r.append(ctf(constants))
    return r


def joff2(constants):
    j = constants['j']
    return (j-1) * abs(j-1)
