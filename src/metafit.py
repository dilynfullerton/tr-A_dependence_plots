from __future__ import division
from __future__ import print_function
from fittransforms import identity
import numpy as np
from scipy.optimize import leastsq


def _meta_fit(plots, fitfn, params_guess, transform=identity, **lsqkwargs):
    """Perform a least squares fit using fitfn for multiple plots

    :param plots: A list of the 3-tuples each with (x, y, const), where x is an
    array of length L, y is an array of length L, and const is a list of
    constants that are unique to the plot.
    :param fitfn: A function of the form f(x, a, b, ...n, *const) -> y, where
    x is float, const is list, a to n are float parameters, and y is
    a float.
    :param params_guess: An initial guess of the fit parameters. The length of
    this list should be the same size as the number of arguments in fitfn - 1
    :param transform: The transformation to apply to the data before fitting
    :return: output of the leastsq function, i.e. (final_params, covariance_arr,
    infodict, message, integer_flag)
    """
    if len(params_guess) != fitfn.__code__.co_argcount - 1:
        raise FunctionDoesNotMatchParameterGuessException
    combined_x = list()
    combined_y = list()
    constants_lists = list()
    for p in plots:
        x, y, constants = p
        xt, yt = transform(x, y, *constants)
        combined_x.append(xt)
        combined_y.append(yt)
        constants_lists.append(constants)
    return leastsq(func=_mls, x0=params_guess,
                   args=(fitfn, combined_x, combined_y, constants_lists),
                   **lsqkwargs)


def _mls(params, fitfn, lox, loy, const_lists):
    """Meta least squares function to be minimized.

    :param params: the parameters to give to the fit function
    :param fitfn: the fit function, which is of the form
    f(x, a, b, ..., n, *const) -> y, where x is a float, a...n are parameters
    to vary, const is a list of constants, and y is a float.
    :param lox: x array of values
    :param loy: y array of values
    :param const_lists: list of constants associated with each
    :return: The difference between the flattened loy array and the flattened
    yfit array
    """
    yfit = list()
    for x in lox:
        args = list(params)
        args.extend(const_lists)
        yfit.extend(list(map(lambda xi: fitfn(xi, *args), x)))
    yflat = [item for y in loy for item in y]
    return np.array(yflat) - np.array(yfit)


class FunctionDoesNotMatchParameterGuessException(Exception):
    pass

'''
from fitfns import polyfit1 as f
from matplotlib import pyplot as plt
x1 = [1.0, 2.0, 3.0]
y1 = [2.0, 3.0, 4.0]
x2 = [1.0, 2.0, 3.0, 4.0]
y2 = [1.0, 4.0, 9.0, 16.0]
x3 = [1.0, 2.0, 3.0, 4.0, 5.0]
y3 = [2.0, 4.0, 8.0, 16.0, 32.0]
plots = [(x1, y1, []), (x2, y2, []), (x3, y3, [])]
pg = [1.0, 1.0]

A = _meta_fit(plots, f, pg)[0]

x = np.linspace(1, 5)
y = np.array(list(map(lambda xi: f(xi, *A), x)))

#plt.plot(x, y)
print(A)
'''