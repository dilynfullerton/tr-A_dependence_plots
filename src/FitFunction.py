"""FitFunction.py
Data definitions and examples of functional forms to be used in fitting.

Definitions:
    fit_function:
        Function that given an x value and a list of parameters and constants,
        returns a y value, which is the fit.
        A fit_function has the form:
            f(x, params, const_list, const_dict) -> y
        The FitFunction object defined below satisfies this definition
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np
from constants import FF_NAME_PREF, FF_NAME_SEP, FF_NAME_SUFF
from constants import FF_CODE_PREF, FF_CODE_SEP, FF_CODE_SUFF


class FitFunction:
    """A 'function' that is designed for use in fitting, particularly with
    the meta-fit algorithm.
    """
    def __init__(
            self, func, num_fit_params, name=None, code='',
            force_zero=None, force_zero_func=None,
            force_k=None, force_k_func=None
    ):
        """Initializes a FitFunction
        :param func: defines the functional form of the fit. This should
        satisfy the definition of a fit_function (see top of file)
        :param num_fit_params: number of fit parameters
        :param name: name of the fit func
        :param code: abbreviated name for use in file names
        :param force_zero: if not None, the fit will be forced to zero for
        this value of x.
        The functional form becomes
            f'(x) = f(x) - f(x0)
        :param force_zero_func: if not None (and force_zero is None), this
        func, f(const_dict) -> x0, is applied to the const_dict to
        determine x0, the x value for which the fit should be 0
        The functional form becomes
            f'(x) = f(x) - f(x0)
        :param force_k: if not None (and force_zero and force_zero_func are
        None), this 2-tuple (x0, k) defines a point that the fit should be
        forced through.
        The functional form becomes
            f'(x) = f(x) - f(x0) + k
        :param force_k_func: if not None (and force_zero and force_zero_func
        and force_k are None), this func, f(const_dict) -> (x0, k),
        defines a point that the fit should be forced through.
        The functional form becomes
            f'(x) = f(x) - f(x0) + k
        """
        self.fn = func
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

    def __call__(self, x, params, const_list, const_dict):
        if self.fz is not None:
            f = self.fn
            return (
                f(x, params, const_list, const_dict) -
                f(self.fz, params, const_list, const_dict)
            )
        elif self.fzfn is not None:
            f = self.fn
            x0 = self.fzfn(const_dict)
            return (
                f(x, params, const_list, const_dict) -
                f(x0, params, const_list, const_dict)
            )
        elif self.fk is not None:
            f = self.fn
            x0, k = self.fk
            return (
                f(x, params, const_list, const_dict) -
                f(x0, params, const_list, const_dict) +
                k
            )
        elif self.fkfn is not None:
            f = self.fn
            x0, k = self.fkfn(const_dict)
            return (
                f(x, params, const_list, const_dict) -
                f(x0, params, const_list, const_dict) +
                k
            )
        else:
            return self.fn(x, params, const_list, const_dict)

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
            self.code += b'fz:' + str(self.fzfn.__name__[6:])
        elif self.fk is not None:
            self.code += b'fk{}'.format(self.fk)
        elif self.fkfn is not None:
            self.code += b'fk:' + str(self.fkfn.__name__[6:])


def combine_ffns(
        list_of_ffn, force_zero=None,
        _name_pref=FF_NAME_PREF,
        _name_sep=FF_NAME_SEP,
        _name_suff=FF_NAME_SUFF,
        _code_pref=FF_CODE_PREF,
        _code_sep=FF_CODE_SEP,
        _code_suff=FF_CODE_SUFF,
        **kwargs
):
    """Linearly combines multiple fit functions (and/or dependencies)
    into one fit function.
    :param list_of_ffn: A list of FitFunctions to combine into one
    :param force_zero: (optional) force the zero of the overall result to a
    specified point
    :param _name_pref: prefix for the name of the combined fit function
    :param _name_sep: separator to go between fit functions
    :return: A combined fit function object, which may be used to optimize with
    respect to all of the degrees of freedom of its sub-functions
    :param _name_suff: suffix for the name of the combined fit function
    :param _code_pref: prefix for the code associated with the combined fit
    function
    :param _code_sep: separator to go between fit function codes
    :param _code_suff: suffix for the code of the combined fit function
    """
    params_lengths = [ffn.num_fit_params for ffn in list_of_ffn]
    params_breaks = [0]
    for pl, i in zip(params_lengths, range(len(params_lengths))):
        params_breaks.append(pl + params_breaks[i])
    total_params_length = params_breaks[-1]
    combined_name = _name_pref
    combined_code = _code_pref
    for ffn in list_of_ffn:
        combined_name += ffn.name + _name_sep
        combined_code += ffn.code + _code_sep
    combined_name = combined_name[:combined_name.rfind(_name_sep)] + _name_suff
    combined_code = combined_code[:combined_code.rfind(_code_sep)] + _code_suff

    def combined_ffns(x, params, const_list, const_dict):
        result = 0
        for fitfn, ii, jj in zip(list_of_ffn, params_breaks, params_breaks[1:]):
            result += fitfn(x, params[ii:jj], const_list, const_dict)
        return result

    return FitFunction(
        func=combined_ffns, num_fit_params=total_params_length,
        force_zero=force_zero, name=combined_name, code=combined_code, **kwargs
    )


# INDEPENDENT
def scalar():
    """Returns a scalar fit function
        y(x) = const
    """
    # noinspection PyUnusedLocal
    def sf(x, params, const_list, const_dict):
        a = params[0]
        return a
    return FitFunction(func=sf, num_fit_params=1, name='scalar', code='s')


def x1(force_zero=None, **kwargs):
    """Returns a fit function of the form
        y(x) = a0 * x,
    where a0 is the fit parameter
    """
    # noinspection PyUnusedLocal
    def x1f(x, params, const_list, const_dict):
        a = params[0]
        return a * x
    return FitFunction(func=x1f, num_fit_params=1, force_zero=force_zero,
                       name='x^1', code='x1', **kwargs)


def linear(force_zero=None, **kwargs):
    """Returns a fit function of the form
        y(x) = a0 + a1 * x,
    where a0 and a1 are fit parameters
    """
    if force_zero is None and len(kwargs) == 0:
        # noinspection PyUnusedLocal
        def lf(x, params, const_list, const_dict):
            a, b = params[0:2]
            return a * x + b
        return FitFunction(
            func=lf, num_fit_params=2, force_zero=force_zero,
            name='linear', code='p1', **kwargs
        )
    else:
        # noinspection PyUnusedLocal
        def lf(x, params, const_list, const_dict):
            a = params[0]
            return a * x
        return FitFunction(
            func=lf, num_fit_params=1, force_zero=force_zero,
            name='linear', code='p1', **kwargs
        )


def x2(force_zero=None, **kwargs):
    """Returns a fit function of the form
        y(x) = a0 * x^2
    """
    # noinspection PyUnusedLocal
    def x2f(x, params, const_list, const_dict):
        a = params[0]
        return a * x ** 2
    return FitFunction(func=x2f, num_fit_params=1, force_zero=force_zero,
                       name='x^2', code='x2', **kwargs)


def quadratic(force_zero=None, **kwargs):
    """Returns a fit function of the form
        y(x) = a0 + a1 * x + a2 * x^2
    """
    if force_zero is None and len(kwargs) == 0:
        # noinspection PyUnusedLocal
        def qf(x, params, const_list, const_dict):
            a, b, c = params[0:3]
            return np.polyval([a, b, c], x)
        return FitFunction(
            func=qf, num_fit_params=3, force_zero=force_zero,
            name='quadratic', code='p2', **kwargs
        )
    else:
        # noinspection PyUnusedLocal
        def qf(x, params, const_list, const_dict):
            a, b = params[0:2]
            return np.polyval([a, b, 0], x)
        return FitFunction(
            func=qf, num_fit_params=2, force_zero=force_zero,
            name='quadratic', code='p2', **kwargs
        )


def x_power(n, force_zero=None, **kwargs):
    """Returns a fit function of the form
        y(x) = x^n
    """
    # noinspection PyUnusedLocal
    def xnf(x, params, const_list, const_dict):
        a = params[0]
        return a * x ** n
    return FitFunction(
        func=xnf, num_fit_params=1, force_zero=force_zero,
        name='x^{}'.format(n), code='x{}'.format(n), **kwargs
    )


def poly(n, force_zero=None, **kwargs):
    """Returns a fit function that is a polynomial of degree n
        y(x) = a0 + a1 * x + a2 * x^2 + ... + an * x^n
    """
    if force_zero is None and len(kwargs) == 0:
        # noinspection PyUnusedLocal
        def pf(x, params, const_list, const_dict):
            return np.polyval(params, x)
        return FitFunction(
            func=pf, num_fit_params=n + 1, force_zero=force_zero,
            name='poly{}'.format(n), code='p{}'.format(n), **kwargs
        )
    else:
        # noinspection PyUnusedLocal
        def pf(x, params, const_list, const_dict):
            return np.polyval(np.concatenate((params, np.zeros(1))), x)
        return FitFunction(
            func=pf, num_fit_params=n, force_zero=force_zero,
            name='poly{}'.format(n), code='p{}'.format(n), **kwargs
        )


def asymptote(n, force_zero=None, **kwargs):
    """Returns a fit function of the form
        y(x) = - a0 / x^n
    I do not remember why I bothered putting the minus sign in the functional
    form, as that could have easily been absorbed into the constant, but
    whatevs broseph
    """
    # noinspection PyUnusedLocal
    def af(x, params, const_list, const_dict):
        a = params[0]
        return - a / x ** n
    return FitFunction(
        func=af, num_fit_params=1, force_zero=force_zero,
        name='asymptote{}'.format(n), code='a{}'.format(n), **kwargs
    )


def asymptote_n(force_zero=None, **kwargs):
    """Returns a fit function of the form
        y(x) = - a0 / x^(a1),
    where a0 and a1 are the fit parameters
    """
    # noinspection PyUnusedLocal
    def anf(x, params, const_list, const_dict):
        a, n = params[0:2]
        return - a / x ** n
    return FitFunction(
        func=anf, num_fit_params=2,
        force_zero=force_zero, name='asymptote_n', code='an', **kwargs
    )


# DEPENDENTS
# Allow a dependence on a particular constant in the const_dict, as identified
# by keys in dep_keys
def scalar_dependence(dep_keys, ctfs=list()):
    """Returns a fit function that allows scalar dependence on the constants
    associated with the given dep_keys
        y(x) = a0 * b0 + a1 * b1 + a2 * b2 + ...,
    where the a's are the fit parameters and the b's are the constants
    associated with the dep_keys in the const_dict or the constants
    constructed by the constant transform functions (ctfs)
    """
    return _dependence(
        f=lambda p, x: p[0], n_params=1, dep_keys=dep_keys,
        ctfs=ctfs, name='scalar dependence', code='s:{}'
    )


def x1_dependence(dep_keys, ctfs=list(), force_zero=None, **kwargs):
    """Returns a fit function that allows x depdendence on the constants
    associated with each of the dep_keys
        y(x) = (a0 * b0 + a1 * b1 + a2 * b2 + ...) * x,
    where each of the a's are fit parameters and each of the b's are either
    a constant associated with the keys in dep_keys or a constant constructed
    by a ctf (constant transform function) in ctfs
    """
    return _dependence(
        f=lambda p, x: p[0] * x, n_params=1,
        dep_keys=dep_keys, ctfs=ctfs,
        force_zero=force_zero, name='x dependence', code='x1:{}', **kwargs
    )


def linear_dependence(dep_keys, ctfs=list(), force_zero=None, **kwargs):
    """Returns a fit function that allows linear depdendence on the constants
    associated with each of the dep_keys
        y(x) = (a0,0 * b0,0 + a1,0 * b1,0 + ...) +
         (a0,1 * b0,1 + a1,1 * b1,1 + ...) * x,
    where each of the a's are fit parameters and each of the b's are either
    a constant associated with the keys in dep_keys or a constant constructed
    by a ctf (constant transform function) in ctfs
    """
    if force_zero is None and len(kwargs) == 0:
        return _dependence(
            f=np.polyval, n_params=2,
            dep_keys=dep_keys, ctfs=ctfs, force_zero=force_zero,
            name='linear dependence', code='p1:{}', **kwargs
        )
    else:
        return _dependence(
            f=lambda p, x: np.polyval(np.concatenate((p, np.zeros(1))), x),
            n_params=1, dep_keys=dep_keys, ctfs=ctfs, force_zero=force_zero,
            name='linear dependence', code='p1:{}', **kwargs
        )


def x2_dependence(dep_keys, ctfs=list(), force_zero=None, **kwargs):
    """Returns a fit function that allows x^2 depdendence on the constants
    associated with each of the dep_keys
        y(x) = (a0 * b0 + a1 * b1 + ...) * x^2,
    where each of the a's are fit parameters and each of the b's are either
    a constant associated with the keys in dep_keys or a constant constructed
    by a ctf (constant transform function) in ctfs
    """
    return _dependence(
        f=lambda p, x: p[0] * x ** 2, n_params=1,
        dep_keys=dep_keys, ctfs=ctfs, force_zero=force_zero,
        name='x^2 dependence', code='x2:{}', **kwargs
    )


def quadratic_dependence(dep_keys, ctfs=list(), force_zero=None, **kwargs):
    """Returns a fit function that allows quadratic depdendence on
    the constants associated with each of the dep_keys
        y(x) = (a0,0 * b0,0 + a1,0 * b1,0 + ...) +
         (a0,1 * b0,1 + a1,1 * b1,1 + ...) * x +
         (a0,2 * b0,2 + a1,2 * b1,2 + ...) * x^2,
    where each of the a's are fit parameters and each of the b's are either
    a constant associated with the keys in dep_keys or a constant constructed
    by a ctf (constant transform function) in ctfs
    """
    if force_zero is None and len(kwargs) == 0:
        return _dependence(
            f=np.polyval, n_params=3,
            dep_keys=dep_keys, ctfs=ctfs, force_zero=force_zero,
            name='quadratic dependence', code='p2:{}', **kwargs
        )
    else:
        return _dependence(
            f=lambda p, x: np.polyval(np.concatenate((p, np.zeros(1))), x),
            n_params=2, dep_keys=dep_keys, ctfs=ctfs, force_zero=force_zero,
            name='quadratic dependence', code='p2:{}', **kwargs
        )


def x_power_dependence(n, dep_keys, ctfs=list(), force_zero=None, **kwargs):
    """Returns a fit function that allows x^n depdendence on the constants
    associated with each of the dep_keys
        y(x) = (a0 * b0 + a1 * b1 + ...) * x^n
    where each of the a's are fit parameters and each of the b's are either
    a constant associated with the keys in dep_keys or a constant constructed
    by a ctf (constant transform function) in ctfs
    """
    return _dependence(
        f=lambda p, x: p[0] * x ** n, n_params=1,
        dep_keys=dep_keys, ctfs=ctfs, force_zero=force_zero,
        name='x^{} dependence'.format(n), code='x{}'.format(n)+':{}', **kwargs
    )


def poly_dependence(n, dep_keys, ctfs=list(), force_zero=None, **kwargs):
    """Returns a fit function that allows polynomial depdendence on the
    constants associated with each of the dep_keys
        y(x) = (a0,0 * b0,0 + a1,0 * b1,0 + ...) +
         (a0,1 * b0,1 + a1,1 * b1,1 + ...) * x +
         (a0,2 * b0,2 + a1,2 * b1,2 + ...) * x^2 +
         (a0,2 * b0,2 + a1,2 * b1,2 + ...) * x^3 +
         ... +
         (a0,2 * b0,2 + a1,2 * b1,2 + ...) * x^n,
    where each of the a's are fit parameters and each of the b's are either
    a constant associated with the keys in dep_keys or a constant constructed
    by a ctf (constant transform function) in ctfs
    """
    if force_zero is None and len(kwargs) == 0:
        return _dependence(
            f=np.polyval, n_params=n + 1, dep_keys=dep_keys, ctfs=ctfs,
            force_zero=force_zero, name='poly{n} dependence'.format(n=n),
            code='p{}'.format(n) + ':{}', **kwargs
        )
    else:
        return _dependence(
            f=lambda p, x: np.polyval(np.concatenate((p, np.zeros(1))), x),
            n_params=n, dep_keys=dep_keys, ctfs=ctfs, force_zero=force_zero,
            name='poly{n} dependence'.format(n=n),
            code='p{}'.format(n) + ':{}', **kwargs
        )


def asymptotic_dependence(n, dep_keys, ctfs=list(), force_zero=None, **kwargs):
    """Returns a fit function that allows asymptotic depdendence on the
    constants associated with each of the dep_keys
        y(x) = - (a0 * b0 + a1 * b1 + ...) / x^n,
    where each of the a's are fit parameters and each of the b's are either
    a constant associated with the keys in dep_keys or a constant constructed
    by a ctf (constant transform function) in ctfs
    """
    return _dependence(
        f=lambda p, x: - p[0] / x ** n, n_params=1,
        dep_keys=dep_keys, ctfs=ctfs, force_zero=force_zero,
        name='asymptotic{} dependence'.format(n), code='a{}'.format(n) + ':{}',
        **kwargs
    )


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
    return FitFunction(
        func=d, num_fit_params=(len(dep_keys) + len(ctfs)) * n_params,
        force_zero=force_zero,
        name=name + ' on {}'.format(dep_str), code=code.format(dep_str),
        **kwargs
    )


def _dep_str(dep_keys, ctfs):
    return (b'(' +
            b', '.join((dep_keys + list(map(lambda c: c.__name__, ctfs)))) +
            b')')


# FITTERS WITH DEPENDENCIES
# The following are examples of using combine_ffns() to combine regular fit
# functions with dependencies on constants
def linear_with_linear_dependence(
        dep_keys, ctfs=list(), force_zero=None, **kwargs):
    return combine_ffns(
        list_of_ffn=[linear(force_zero=force_zero),
                     linear_dependence(dep_keys, ctfs, force_zero=force_zero)],
        force_zero=force_zero, **kwargs
    )


def poly_with_linear_dependence(
        n, dep_keys, ctfs=list(), force_zero=None, **kwargs):
    return combine_ffns(
        list_of_ffn=[poly(n), linear_dependence(dep_keys, ctfs)],
        force_zero=force_zero, **kwargs
    )


def asymptote_with_linear_dependence(
        n, dep_keys, ctfs=list(), force_zero=None, **kwargs
):
    return combine_ffns(
        list_of_ffn=[asymptote(n), linear_dependence(dep_keys, ctfs)],
        force_zero=force_zero, **kwargs
    )


def asymptote_with_asymptotic_dependence(
        n, dep_keys, ctfs=list(), force_zero=None, **kwargs
):
    return combine_ffns(
            list_of_ffn=[asymptote(n),
                         asymptotic_dependence(n, dep_keys, ctfs)],
            force_zero=force_zero, **kwargs
    )


# CONSTANT TRANSFORMS
# I think these are self-explanatory
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
