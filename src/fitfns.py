from __future__ import division
from __future__ import print_function

import numpy as np


# SIMPLE FITS
def polyfit4(x, a, b, c, d, e, *constants):
    return _polyfitn(x, a, b, c, d, e)

def polyfit3(x, a, b, c, d, *constants):
    return _polyfitn(x, a, b, c, d)

def polyfit2(x, a, b, c, *constants):
    return _polyfitn(x, a, b, c)

def polyfit1(x, a, b, *constants):
    return _polyfitn(x, a, b)

def _polyfitn(x, *params):
    return np.polyval(params, x)

def expfit1(x, a, b, c, *constants):
    return a * np.exp(b * x) + c

def logfit1(x, a, b, c, *constants):
    return a * np.log(b ** 2 * x + 1) + c

def logbasefit1(x, a, b, c, *constants):
    return a * np.log(x) / np.log(b ** 2 + 1) + c

def powerfit1(x, a, b, c, *constants):
    return a * np.power(x, b) + c

def sqrtfit1(x, a, b, *constants):
    return a * np.sqrt(x) + b

def rel1(x, a, b, c, d, *constants):
    return a * np.sqrt(b * x ** 2 + c) + d

def invfit1(x, a, b, *constants):
    return a / (x + 1) + b

def linvfit1(x, a, b, *constants):
    return a * x / (x + 1) + b

def asymptote1(x, a, b, c, *constants):
    return a * (1 - b / x) + c

# INVOLVING CONSTANTS
def asymptote2_linear_joff2_tz_dependence(x, a, b1, b2, c, *constants):
    if len(constants) == 0:
        return a * (- 1 / x**2) + c
    else:
        const_list, const_dict = constants
        qnums = const_dict['qnums']
        n, l, j, tz = qnums
        joff2 = (j-1) * abs(j-1)
        return a*(-1/x**2)+(b1*joff2+b2*tz)*x+c

def linear_j_and_tz_dependence(x, a, b, c, d, *constants):
    if len(constants) == 0:
        return a * x + c
    else:
        const_list, const_dict = constants
        quantum_numbers = const_dict['qnums']
        j = quantum_numbers.j
        tz = quantum_numbers.tz
        return a * x + b * j * x + c * tz * x + d

def linear_fit_linear_n_j_tz_ephw_dependence_common_zero(
        x, c, c1, c3, c4, c5, d, *constants):
    xp = x - d
    if len(constants) == 0:
        return np.polyval([c, 0], xp)
    else:
        const_list, const_dict = constants
        qnums, e, hw = const_list[0:3]
        n, l, j, tz = qnums
        return np.polyval([c+c1*n+c3*j+c4*tz+c5*(e+hw), 0], xp)

def quadratic_j_and_tz_dependence(x, a, b, c, d, e, f, g, *constants):
    if len(constants) == 0:
        return np.polyval([a, d, g], x)
    else:
        const_list, const_dict = constants
        qnums = const_dict['qnums']
        j = qnums.j
        tz = qnums.tz
        return np.polyval([a + b*j + c*tz, d + e*j + f*tz, g], x)

# Fit function generators
def asymptote1_with_forced_zero(zero):
    def fn(x, a, *constants):
        return a * (1 / zero - 1 / x)
    fn.__name__ = ('asymptote1_with_forced_zero'
                   '_at_{z}').format(z=zero)
    return fn

def asymptote2_with_forced_zero(zero):
    def fn(x, a, *constants):
        return a * (1 / zero ** 2 - 1 / x ** 2)
    fn.__name__ = ('asymptote2_with_forced_zero'
                   '_at_{z}').format(z=zero)
    return fn

def asymptote_n_with_forced_zero(zero):
    def fn(x, a, n, *constants):
        return a * (1 / zero ** n - 1 / x ** n)
    fn.__name__ = ('asymptote_n_with_forced_zero'
                   '_at_{z}').format(z=zero)
    return fn

def asymptote2_asymptotic_y0_dependence_with_forced_zero(zero):
    def fn(x, a, a1, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            qnums = const_dict['qnums']
            y0 = const_dict['y0']
            return (a + a1*y0) * (1/zero**2 - 1/x**2)
    fn.__name__ = ('asymptote2_asymptotic_y0_dependence_with_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote2_asymptotic_y0pzbt0_dependence_with_forced_zero(zero):
    def fn(x, a, a1, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            qnums = const_dict['qnums']
            y0 = const_dict['y0']
            zbt0 = const_dict['zbt_arr'][0]
            return (a + a1*(y0+zbt0)) * (1/zero**2 - 1/x**2)
    fn.__name__ = ('asymptote2_asymptotic_y0pzbt0_dependence_with_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote2_asymptotic_joff2_dependence_with_forced_zero(zero):
    def fn(x, a, a1, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            qnums = const_dict['qnums']
            n, l, j, tz = qnums
            joff2 = (j - 1) * abs(j - 1)
            return (a + a1*joff2) * (1/zero**2 - 1/x**2)
    fn.__name__ = ('asymptote2_asymptotic_joff2_dependence_with_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote2_asymptotic_and_linear_y0_dependence_with_forced_zero(zero):
    def fn(x, a, a1, b1, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            qnums = const_dict['qnums']
            y0 = const_dict['y0']
            return (a + a1*y0) * (1/zero**2 - 1/x**2) + b1*y0*(x-zero)
    fn.__name__ = ('asymptote2_asymptotic_and_linear_y0_dependence_with_'
                   'forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote2_linear_y0_dependence_with_forced_zero(zero):
    def fn(x, a, b1, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            qnums = const_dict['qnums']
            y0 = const_dict['y0']
            return a * (1/zero**2 - 1/x**2) + (b1*y0) * (x-zero)
    fn.__name__ = ('asymptote2_linear_y0_dependence_with_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote2_linear_y0pzbt0_dependence_with_forced_zero(zero):
    def fn(x, a, b1, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            qnums = const_dict['qnums']
            y0 = const_dict['y0']
            zbt0 = const_dict['zbt_arr'][0]
            return a * (1/zero**2 - 1/x**2) + b1*(y0+zbt0)*(x-zero)
    fn.__name__ = ('asymptote2_linear_y0pzbt0_dependence_with_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote2_linear_y0_zbt0_dependence_with_forced_zero(zero):
    def fn(x, a, b1, b2, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            y0 = const_dict['y0']
            zbt0 = const_dict['zbt_arr'][0]
            return a*(1/zero**2 - 1/x**2) + (b1*y0 + b2*zbt0)*(x-zero)
    fn.__name__ = ('asymptote2_linear_y0_zbt0_dependence_with_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote2_linear_j_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            qnums = const_dict['qnums']
            n, l, j, tz = qnums
            return a * (1/zero**2 - 1/x**2) + (b*j + c*tz) * (x-zero)
    fn.__name__ = ('asymptote2_linear_j_tz_dependence_with_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote1_linear_joff2_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b1, b2, *constants):
        if len(constants) == 0:
            return a * (1 / zero - 1 / x)
        else:
            const_list, const_dict = constants
            qnums = const_dict['qnums']
            n, l, j, tz = qnums
            xp = x - zero
            joff2 = (j-1) * abs(j-1)
            return a*(1/zero-1/x)+(b1*joff2+b2*tz)*xp
    fn.__name__ = ('asymptote1_linear_joff2_tz_dependence_with_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote2_linear_joff2_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b1, b2, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            qnums = const_dict['qnums']
            n, l, j, tz = qnums
            xp = x - zero
            joff2 = (j-1) * abs(j-1)
            return a*(1/zero**2-1/x**2)+(b1*joff2+b2*tz)*xp
    fn.__name__ = ('asymptote2_linear_joff2_tz_dependence_with_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote12_linear_joff2_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c1, c2, *constants):
        if len(constants) == 0:
            return a*(1/zero**2 - 1/x**2) + b*(1/zero - 1/x)
        else:
            const_list, const_dict = constants
            qnums = const_dict['qnums']
            n, l, j, tz = qnums
            xp = x - zero
            joff2 = (j-1) * abs(j-1)
            return a*(1/zero**2-1/x**2)+b*(1/zero-1/x)+(c1*joff2+c2*tz)*xp
    fn.__name__ = ('asymptote12_linear_joff2_tz_dependence_with_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote2_linear_j_y0_dependence_with_forced_zero(zero):
    def fn(x, a, b1, b2, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            qnums = const_dict['qnums']
            y0 = const_dict['y0']
            n, l, j, tz = qnums
            return a * (1/zero**2 - 1/x**2) + (b1*j + b2*y0) * (x-zero)
    fn.__name__ = ('asymptote2_linear_j_y0_dependence_with_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote2_linear_joff2_y0_dependence_with_forced_zero(zero):
    def fn(x, a, b1, b2, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            qnums = const_dict['qnums']
            y0 = const_dict['y0']
            n, l, j, tz = qnums
            joff2 = (j - 1) * abs(j - 1)
            return a * (1/zero**2 - 1/x**2) + (b1*joff2 + b2*y0) * (x-zero)
    fn.__name__ = ('asymptote2_linear_joff2_y0_dependence_with_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote2_linear_j_tz_y0_dependence_with_forced_zero(zero):
    def fn(x, a, b1, b2, b3, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            qnums = const_dict['qnums']
            y0 = const_dict['y0']
            n, l, j, tz = qnums
            return a * (1/zero**2 - 1/x**2) + (b1*j + b2*tz + b3*y0) * (x-zero)
    fn.__name__ = ('asymptote2_linear_j_tz_y0_dependence_with_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote2_quadratic_j_linear_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c1, c2, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            qnums = const_list[0]
            n, l, j, tz = qnums
            xp = x - zero
            return a*(1/zero**2-1/x**2)+(b*j)*xp**2+(c1*j+c2*tz)*xp
    fn.__name__ = ('asymptote2_quadratic_j_linear_tz_dependence_with_forced_'
                   'zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote2_linear_with_linear_joff2_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, b1, b2, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            qnums = const_list[0]
            n, l, j, tz = qnums
            xp = x - zero
            joff2 = (j-1) * abs(j-1)
            return a*(1/zero**2-1/x**2)+(b+b1*joff2+b2*tz)*xp
    fn.__name__ = ('asymptote2_linear_with_linear_joff2_tz_dependence_with'
                   '_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote2_linear_jjoff_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b1, b2, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            qnums = const_list[0]
            n, l, j, tz = qnums
            xp = x - zero
            jjoff = (j-1) * j
            return a*(1/zero**2-1/x**2)+(b1*jjoff+b2*tz)*xp
    fn.__name__ = ('asymptote2_linear_jjoff_tz_dependence_with_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def asymptote2_quadratic_with_linear_joff2_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, c1, c2, *constants):
        if len(constants) == 0:
            return a * (1 / zero**2 - 1 / x**2)
        else:
            const_list, const_dict = constants
            qnums = const_dict['qnums']
            n, l, j, tz = qnums
            xp = x - zero
            joff2 = (j-1) * abs(j-1)
            return a*(1/zero**2-1/x**2)+b*xp**2+(c+c1*joff2+c2*tz)*xp
    fn.__name__ = ('asymptote2_quadratic_with_linear_joff2_tz_dependence_with'
                   '_forced_zero'
                   '_at_{}'.format(zero))
    return fn

def linear_fit_linear_n_j_tz_ephw_dependence_with_forced_zero(zero):
    def fn(x, c, c1, c3, c4, c5,
           *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([c, 0], xp)
        else:
            const_list, const_dict = constants
            qnums, e, hw = const_list[0:3]
            n, l, j, tz = qnums
            return np.polyval([c+c1*n+c3*j+c4*tz+c5*(e+hw), 0], xp)
    fn.__name__ = ('linear_fit_linear_n_j_tz_ephw_dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def quadratic_j_and_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, d, e, f, *constants):
        if len(constants) == 0:
            return a*(x - zero)**2 + d*(x - zero)
        else:
            const_list, const_dict = constants
            qnums = const_list[0]
            j = qnums.j
            tz = qnums.tz
            return (a + b*j + c*tz)*(x-zero)**2 + (d + e*j + f*tz)*(x-zero)
    fn.__name__ = ('quadratic_j_and_tz_dependence_with_force_zero_at_'
                   '{z}'.format(z=zero))
    return fn

def quadratic_fit_linear_j_tz_dependence_with_forced_zero(zero):
    def fn(x, a, d, e, f, *constants):
        if len(constants) == 0:
            return a*(x - zero)**2 + d*(x - zero)
        else:
            const_list, const_dict = constants
            qnums = const_list[0]
            j = qnums.j
            tz = qnums.tz
            return a*(x-zero)**2 + (d + e*j + f*tz)*(x-zero)
    fn.__name__ = ('quadratic_fit_linear_j_tz_dependence_with_forced_zero_at_'
                   '{z}'.format(z=zero))
    return fn

def quadratic_fit_quadratic_e_hw_linear_n_j_tz_dependence_with_forced_zero(zero):
    def fn(x, c, c1, c2, d, d1, d3, d4, d5, d6,
           *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums, e, hw = const_list[0:3]
            n, l, j, tz = qnums
            return np.polyval([c+c1*e+c2*hw, d+d1*n+d3*j+d4*tz+d5*e+d6*hw, 0],
                              xp)
    fn.__name__ = ('quadratic_fit_quadratic_e_hw_linear_n_j_tz_'
                   'dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def quadratic_fit_quadratic_j_tz_linear_ephw_dependence_with_forced_zero(zero):
    def fn(x, c, c1, c2, d, d1,
           *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums, e, hw = const_list[0:3]
            n, l, j, tz = qnums
            return np.polyval([c+c1*j+c2*tz,
                               d+d1*(e+hw),
                               0],
                              xp)
    fn.__name__ = ('quadratic_fit_quadratic_j_tz_linear_ephw_'
                   'dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def quadratic_fit_quadratic_j_tz_linear_n_ephw_dependence_with_forced_zero(zero):
    def fn(x, c, c1, c2, d, d1, d3,
           *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums, e, hw = const_list[0:3]
            n, l, j, tz = qnums
            return np.polyval([c+c1*j+c2*tz, d+d1*(e+hw)+d3*n, 0], xp)
    fn.__name__ = ('quadratic_fit_quadratic_j_tz_linear_n_ephw_'
                   'dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def quadratic_fit_quadratic_j_tz_linear_n_e_hw_dependence_with_forced_zero(zero):
    def fn(x, c, c1, c2, d, d1, d3, d4, d5, d6,
           *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums, e, hw = const_list[0:3]
            n, l, j, tz = qnums
            return np.polyval([c+c1*j+c2*tz, d+d1*n+d3*j+d4*tz+d5*e+d6*hw, 0],
                              xp)
    fn.__name__ = ('quadratic_fit_quadratic_j_tz_linear_n_e_hw_'
                   'dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def quadratic_fit_quadratic_n_j_tz_linear_e_hw_dependence_with_forced_zero(zero):
    def fn(x, c, c1, c3, c4, d, d1, d3, d4, d5, d6,
           *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums, e, hw = const_list[0:3]
            n, l, j, tz = qnums
            return np.polyval([c+c1*n+c3*j+c4*tz,
                               d+d1*n+d3*j+d4*tz+d5*e+d6*hw,
                               0],
                              xp)
    fn.__name__ = ('quadratic_fit_quadratic_n_j_tz_linear_e_hw_'
                   'dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def cubic_fit_linear_j_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, d, e, f, *constants):
        if len(constants) == 0:
            return a*(x - zero)**3 + b*(x-zero)**2 + d*(x - zero)
        else:
            const_list, const_dict = constants
            qnums = const_list[0]
            j = qnums.j
            tz = qnums.tz
            xp = x - zero
            return np.polyval([a, b, d + e*j + f*tz, 0], xp)
    fn.__name__ = ('cubic_fit_linear_j_tz_dependence_with_forced_zero_at_'
                   '{z}'.format(z=zero))
    return fn

def cubic_fit_linear_n_j_tz_e_hw_dependence_with_forced_zero(zero):
    def fn(x, a, b, d, d1, d3, d4, d5, d6,
           *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums, e, hw = const_list[0:3]
            n, l, j, tz = qnums
            return np.polyval([a, b, d+d1*n+d3*j+d4*tz+d5*e+d6*hw, 0], xp)
    fn.__name__ = ('cubic_fit_linear_n_j_tz_e_hw_dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def poly4_fit_linear_j_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, d, e, f, *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums = const_list[0]
            j = qnums.j
            tz = qnums.tz
            return np.polyval([a, b, c, d + e*j + f*tz, 0], xp)
    fn.__name__ = ('poly4_fit_linear_j_tz_dependence_with_forced_zero_at_'
                   '{z}'.format(z=zero))
    return fn

def poly4_fit_linear_j_tz_jtz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, d, d1, d2, d12, *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums = const_list[0]
            j = qnums.j
            tz = qnums.tz
            return np.polyval([a, b, c, d + d1*j + d2*tz + d12*j*tz, 0], xp)
    fn.__name__ = ('poly4_fit_linear_j_tz_jtz_dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def poly4_fit_linear_n_j_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, d, d1, d3, d4, *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums = const_list[0]
            n, l, j, tz = qnums
            return np.polyval([a, b, c, d+d1*n+d3*j+d4*tz, 0], xp)
    fn.__name__ = ('poly4_fit_linear_n_j_tz_dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def poly4_fit_quadratic_j_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, c1, c2, d, d1, d2, *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums = const_list[0]
            j = qnums.j
            tz = qnums.tz
            return np.polyval([a, b, c+c1*j+c2*tz, d+d1*j+d2*tz, 0], xp)
    fn.__name__ = ('poly4_fit_quadratic_j_tz_dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def poly4_fit_quadratic_j_tz_linear_n_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, c1, c2, d, d1, d3, d4,
           *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums, e, hw = const_list[0:3]
            n, l, j, tz = qnums
            return np.polyval([a, b, c+c1*j+c2*tz, d+d1*n+d3*j+d4*tz, 0], xp)
    fn.__name__ = ('poly4_fit_quadratic_j_tz_linear_n_'
                   'dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def poly4_fit_quadratic_n_j_tz_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, c1, c3, c4, d, d1, d3, d4, *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums = const_list[0]
            n, l, j, tz = qnums
            return np.polyval([a, b, c+c1*n+c3*j+c4*tz, d+d1*n+d3*j+d4*tz, 0],
                              xp)
    fn.__name__ = ('poly4_fit_quadratic_n_j_tz_dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def poly4_fit_linear_n_j_tz_e_hw_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, d, d1, d3, d4, d5, d6, *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums = const_list[0]
            e = const_list[1]
            hw = const_list[2]
            n, l, j, tz = qnums
            return np.polyval([a, b, c, d+d1*n+d3*j+d4*tz+d5*e+d6*hw, 0], xp)
    fn.__name__ = ('poly4_fit_linear_n_j_tz_e_hw_dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def poly4_fit_quadratic_j_tz_linear_n_ephw_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, c1, c2, d, d1, d3, d4, d5,
           *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums, e, hw = const_list[0:3]
            n, l, j, tz = qnums
            return np.polyval([a, b, c+c1*j+c2*tz, d+d1*n+d3*j+d4*tz+d5*(e+hw),
                               0],
                              xp)
    fn.__name__ = ('poly4_fit_quadratic_j_tz_linear_n_ephw_'
                   'dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def poly4_fit_quadratic_j_tz_linear_n_e_hw_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, c1, c2, d, d1, d3, d4, d5, d6,
           *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums, e, hw = const_list[0:3]
            n, l, j, tz = qnums
            return np.polyval([a, b, c+c1*j+c2*tz, d+d1*n+d3*j+d4*tz+d5*e+d6*hw,
                               0],
                              xp)
    fn.__name__ = ('poly4_fit_quadratic_j_tz_linear_n_e_hw_'
                   'dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def poly4_fit_quadratic_n_j_tz_linear_ephw_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, c1, c3, c4, d, d1, d3, d4, d5,
           *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums, e, hw = const_list[0:3]
            n, l, j, tz = qnums
            return np.polyval([a, b, c+c1*n+c3*j+c4*tz,
                               d+d1*n+d3*j+d4*tz+d5*(e+hw), 0],
                              xp)
    fn.__name__ = ('poly4_fit_quadratic_n_j_tz_linear_ephw_'
                   'dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def poly4_fit_quadratic_n_j_tz_linear_e_hw_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, c1, c3, c4, d, d1, d3, d4, d5, d6,
           *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums, e, hw = const_list[0:3]
            n, l, j, tz = qnums
            return np.polyval([a, b, c+c1*n+c3*j+c4*tz,
                               d+d1*n+d3*j+d4*tz+d5*e+d6*hw, 0],
                              xp)
    fn.__name__ = ('poly4_fit_quadratic_n_j_tz_linear_e_hw_'
                   'dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn

def poly4_fit_quadratic_n_j_tz_e_hw_dependence_with_forced_zero(zero):
    def fn(x, a, b, c, c1, c3, c4, c5, c6, d, d1, d3, d4, d5, d6,
           *constants):
        xp = x - zero
        if len(constants) == 0:
            return np.polyval([a, b, c, d, 0], xp)
        else:
            const_list, const_dict = constants
            qnums, e, hw = const_list[0:3]
            n, l, j, tz = qnums
            return np.polyval([a, b, c+c1*n+c3*j+c4*tz+c5*e+c6*hw,
                               d+d1*n+d3*j+d4*tz+d5*e+d6*hw, 0],
                              xp)
    fn.__name__ = ('poly4_fit_quadratic_n_j_tz_e_hw_'
                   'dependence_with_forced_zero'
                   '_at_{z}'.format(z=zero))
    return fn
