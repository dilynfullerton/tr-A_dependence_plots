"""mf_compare.py
Various tools to compare multiple meta-fits of functional forms based on
their parameter variance, regression agreement, etc.

Definitions:
    metafitter:
        function that given a fitfn, an exp, and optional keyword arguments,
        fits onto all the plots that match that exp simultaneously
        Form:
            f(fitfn, exp, **kwargs) ->
                (mf_results, lr_results, plots, fitfn, info_dict)
    fitfn:
        function that when given and x value, a list of parameters, and
        constants, deterministically returns a y value (the fit)
        Form:
            f(x, params, const_list, const_dict) -> y
    exp:
        namedtuple object that uniquely identifies a sequence of input files
        to use for plotting.
"""

from __future__ import division
from __future__ import print_function

from itertools import combinations

import numpy as np
from int.ExpInt import ExpInt

from constants import DPATH_FILES_INT, STANDARD_IO_MAP
from constants import P_TITLE, P_BREAK, P_END, P_HEAD
from deprecated.int.DataMapInt import DataMapInt


def max_r2_value(
        metafitter, fitfns, e_hw_pairs, print_r2_results=False,
        dpath_source=DPATH_FILES_INT, std_io_map=STANDARD_IO_MAP, **kwargs
):
    """Returns the fit function (and its optimized results) that produces the
    largest total r^2 value
    :param dpath_source: the directory from which to retrieve the data
    :param print_r2_results: whether to print the results of this analysis
    :param metafitter: the metafitter method (e.g.
    single_particle_relative_metafigt)
    :param fitfns: the list of fitfns to test
    :param e_hw_pairs: the (e, hw) pairs to optimize
    :param std_io_map: A standard io-mapping scheme to use
    :param kwargs: keyword arguments to pass to the metafitter
    :return: best fit function, results
    """
    exp_list = [ExpInt(*e_hw_pair) for e_hw_pair in e_hw_pairs]
    imsrg_data_map = DataMapInt(
        parent_directory=dpath_source, exp_list=exp_list,
        standard_indices=std_io_map
    )
    fn_res_r2_map = dict()
    for fitfn in fitfns:
        try:
            res = metafitter(
                fitfn, exp_list, imsrg_data_map=imsrg_data_map, **kwargs)
        except TypeError:
            continue
        lg_res = res[1]
        r2 = 0
        for v in lg_res.values():
            r = v.rvalue
            r2 += r ** 2
        r2 /= len(lg_res)
        fn_res_r2_map[fitfn] = (res, r2)
    rank_map = dict()
    result_map = dict()
    for fitfn, i in zip(
            sorted(fn_res_r2_map.keys(),
                   key=lambda f: -1 * fn_res_r2_map[f][1]),
            range(len(fn_res_r2_map))
    ):
        res, r2 = fn_res_r2_map[fitfn]
        rank_map[i + 1] = (fitfn, r2)
        result_map[fitfn] = res
    if print_r2_results is True:
        _printer_for_max_r2_value(rank_map, metafitter, exp_list)
    return rank_map[1][0], rank_map[1][1], rank_map, result_map


def _printer_for_max_r2_value(rank_map, metafitter, e_hw_pairs):
    e_hw_pairs = [tuple(e_hw_pair) for e_hw_pair in e_hw_pairs]
    title_str = (
        '\nR^2 values for fit functions under metafit {mf} for '
        '{ehw}\n'.format(mf=metafitter.__name__, ehw=e_hw_pairs)
    )
    print(P_TITLE + title_str + P_BREAK + P_END)
    template_str = '{r:>4}\t{fn:>100}\t{r2:>15}'
    head_str = template_str.format(r='Rank', fn='Fit function', r2='R^2')
    print(P_HEAD + head_str + P_END)
    for k in sorted(rank_map.keys()):
        body_str = template_str.format(r=k, fn=rank_map[k][0].__name__,
                                       r2=rank_map[k][1])
        print(body_str)


def compare_params(
        metafitter, fitfn, e_hw_pairs, depth, statfn=np.std,
        print_compare_results=False, dpath_source=DPATH_FILES_INT,
        std_io_map=STANDARD_IO_MAP, **kwargs
):
    """Compare parameter results for a given metafitter on a given fitfn using
    combinations of the given e_hw_pairs to the depth given by depth. The
    method of comparison is given by the statistical function statfn, whose
    default is the standard deviation.
    :param metafitter: meta-fitting method to use (e.g.
    single_particle_relative_metafit)
    :param fitfn: fit function to use
    :param e_hw_pairs: set of (e, hw) pairs to look at
    :param depth: depth of sub-combinations of e_hw_pairs to look at.
    For example, if e_hw_pairs = {(1, 1), (2, 2), (3, 3), (4, 4)} and depth is
    2, all of the length 4, length 3, and length 2 sub-combinations will be
    added to the analysis
    :param statfn: comparison function to perform on the distribution of
    single-parameter results. Must take a single ndarray object as input and
    return a float output.
    :param print_compare_results: whether to print the results in a neat table
    :param dpath_source: directory from which to retrieve the files
    :param std_io_map: a standard index -> orbital mapping scheme to use fo the
    generated imsrg_data_map
    :param kwargs: keyword arguments to be passed to the metafitter
    :return: a list of (param, result, relative result) 3-tuples
    """
    exp_list = [ExpInt(*e_hw_pair) for e_hw_pair in e_hw_pairs]
    imsrg_data_map = DataMapInt(
        dpath_source, exp_list=exp_list, standard_indices=std_io_map)
    if depth > len(e_hw_pairs) - 1:
        depth = len(e_hw_pairs) - 1
    params = metafitter(fitfn, e_hw_pairs,
                        imsrg_data_map=imsrg_data_map, **kwargs)[0][0]
    all_params_lists = list([params])
    for length in range(len(e_hw_pairs) - 1, len(e_hw_pairs) - depth - 1, -1):
        for sub_e_hw_pairs in combinations(e_hw_pairs, length):
            mod_params = metafitter(fitfn, sub_e_hw_pairs,
                                    imsrg_data_map=imsrg_data_map)[0][0]
            all_params_lists.append(mod_params)
    individual_params_lists = _distributions_from_lol(all_params_lists)
    param_result_list = list()
    for param, param_list in zip(params, individual_params_lists):
        param_array = np.array(param_list)
        result = statfn(param_array)
        rel_result = abs(result / param)
        param_result_list.append((param, result, rel_result))
    if print_compare_results is True:
        _printer_for_compare_params(
            param_result_list, depth, statfn.__name__,
            e_hw_pairs, metafitter, fitfn)
    return param_result_list


def _distributions_from_lol(lol):
    sublist_size = len(lol[0])
    distributions_list = list()
    for i in range(sublist_size):
        distributions_list.append(list(map(lambda sl: sl[i], lol)))
    return distributions_list


def _printer_for_compare_params(
        params_result_list, depth, statfn, e_hw_pairs, metafitter, fitfn
):
    title_str = (
        '\nDepth {d} comparison of {sfn} for {ehw} using meta-fitter '
        '{mf} and fit function {ffn}'
    ).format(
        d=depth, sfn=statfn, ehw=e_hw_pairs,
        mf=metafitter.__name__, ffn=fitfn.__name__
    )
    print(P_TITLE + title_str + '\n' + P_BREAK + P_END)
    temp_str = '{p:>20}\t{std:>20}\t{rel:>20}'
    print(P_HEAD +
          temp_str.format(
              p='Parameter val', std='Compare result',
              rel='Rel compare result') +
          P_END)
    for p, std, rel in params_result_list:
        print(temp_str.format(p=p, std=std, rel=rel))
