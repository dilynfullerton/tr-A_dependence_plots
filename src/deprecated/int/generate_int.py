"""generate_int.py
Generate interaction files based on fits
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from os import mkdir, path
from FitFunction import FitFunction
from ExpInt import ExpInt
from metafitters_sp import single_particle_firstp_metafit
from metafitters_sp import single_particle_firstp_zbt_metafit
from metafitters_mp import multi_particle_firstp_metafit
from constants import STANDARD_IO_MAP
from constants import DPATH_FILES_INT, DPATH_GEN_INT
from constants import GEN_INT_DNAME_SUBDIR, GEN_INT_FNAME
from constants import GEN_INT_ROW_LINES_TITLE, GEN_INT_ROW_LINES_FIT_PARAMS
from constants import GEN_INT_ROW_ZERO_BODY_TERM, GEN_INT_ROW_INDEX_KEY_HEAD
from constants import GEN_INT_ROW_INDEX_KEY, GEN_INT_ROW_BLANK
from constants import GEN_INT_ROW_SINGLE_PARTICLE, GEN_INT_ROW_INTERACTION
from deprecated.int.DataMapInt import DataMapInt


def generate_int_file_from_fit(
        fitfn_zbt, fitfn_sp, fitfn_mp,
        exp_list, mass_range,
        std_io_map=STANDARD_IO_MAP,
        metafitter_zbt=single_particle_firstp_zbt_metafit,
        metafitter_sp=single_particle_firstp_metafit,
        metafitter_mp=multi_particle_firstp_metafit,
        dpath_source=DPATH_FILES_INT,
        **kwargs
):
    """Given fit functions for zbt, sp, and mp, as well as a set of e_hw_pairs,
    a range of mass numbers, and specific metafitter algorithms, generates
    fake interaction files_INT based on the fit functions
    :param fitfn_zbt: fit function for zero body term
    :param fitfn_sp: fit function for single particle
    :param fitfn_mp: fit function for interaction
    :param exp_list: e, hw, ... pairs used for the metafitters
    :param mass_range: range of masses for which to produces files_INT
    :param std_io_map: io_map for generating index-orbital keys
    :param metafitter_zbt: (Optional) zero body term fitter
    :param metafitter_sp: (Optional) single particle fitter
    :param metafitter_mp: (Optional) interactions fitter
    :param dpath_source: directory housing data files
    :param kwargs: (Optional) Additional keyword arguments to pass to the helper
    function
    """
    imsrg_data_map = DataMapInt(
        dpath_source, exp_list=exp_list, standard_indices=std_io_map)
    results_zbt = metafitter_zbt(
        fitfn_zbt, exp_list, imsrg_data_map=imsrg_data_map)
    results_sp = metafitter_sp(
        fitfn_sp, exp_list, imsrg_data_map=imsrg_data_map)
    results_mp = metafitter_mp(
        fitfn_mp, exp_list, imsrg_data_map=imsrg_data_map)
    generate_int_file_from_fit_results(
        results_zbt=results_zbt, results_sp=results_sp, results_mp=results_mp,
        exp_list=exp_list, io_map=std_io_map, mass_range=mass_range,
        **kwargs
    )


def generate_int_file_from_fit_results(
        results_zbt, results_sp, results_mp, mass_range, exp_list,
        io_map=STANDARD_IO_MAP,
        dpath_save=DPATH_GEN_INT,
        _file_save_subdir=GEN_INT_DNAME_SUBDIR,
        _file_save_name=GEN_INT_FNAME,
        _row_lines_title=GEN_INT_ROW_LINES_TITLE,
        _row_lines_subtitle=GEN_INT_ROW_LINES_FIT_PARAMS,
        _row_zbt=GEN_INT_ROW_ZERO_BODY_TERM,
        _row_idx_key_head=GEN_INT_ROW_INDEX_KEY_HEAD,
        _row_idx_key=GEN_INT_ROW_INDEX_KEY,
        _row_blank=GEN_INT_ROW_BLANK,
        _row_sp=GEN_INT_ROW_SINGLE_PARTICLE,
        _row_mp=GEN_INT_ROW_INTERACTION
):
    """Generate a set of .int interaction files from a set of sp results, mp
    results, and zbt results for a given mass range.
    :param results_zbt: Results of a zbt metafit. This should be an identity
    zbt fit with a standard io_map also passed to this function.
    :param results_sp: Results of a single particle metafit. This should be an
    identity fit, with a standard io_map, also passed to this function.
    :param results_mp: Results of a multi-particle metafit. This should be an
    identity fit with a standard io_map, also passed to this function.
    :param mass_range: range of mass numbers for which to generate files.
    :param exp_list: exp list for which to generate files
    :param io_map: standard io_map used in the above three metafits.
    :param dpath_save: (Optional) main directory in which generated files
    are to be saved
    :param _file_save_subdir: (Optional) subdirectory template string to use
    for a particular evaluation of this function. This can accept the
    following keyword arguments:
            mf1:  code for the zbt metafit
            ffn1: code for the zbt metafit fit function
            mf2:  sp metafit
            ffn2: sp fit function
            mf3:  mp metafit
            ffn3: mp fit function
    :param _file_save_name: (Optional) filename template string to use for
    each file. This can accept the following keyword arguments:
            [same as above]
            mass: the mass number
    :param _row_lines_title: (Optional) title lines for the beginning of the
    file.
    :param _row_lines_subtitle: (Optional) subtitle lines to directly follow
    the title.
    :param _row_zbt: (Optional) zbt line
    :param _row_idx_key_head: (Optional) index key header
    :param _row_idx_key: (Optional) index key template string (5 args)
    :param _row_blank: (Optinal) blank line
    :param _row_sp: (Optional) single particle row template (9 args)
    :param _row_mp: (Optional) interaction row template (7 args)
    """
    info_zbt = results_zbt[4]
    info_sp = results_sp[4]
    info_mp = results_mp[4]
    exp_list = sorted([ExpInt(*pair) for pair in exp_list])
    for ii in [info_zbt, info_sp, info_mp]:
        if sorted(ii['exp_list']) != exp_list:
            raise InconsistentDatasetsGivenToIntFileGeneratorException()
    e_hw_pairs_strings = [str(pair) for pair in exp_list]
    fname_args = {
        'ehw': '[' + ', '.join(e_hw_pairs_strings) + ']',
        'mf1': info_zbt['mf_code'], 'ffn1': info_zbt['ffn_code'],
        'mf2': info_sp['mf_code'], 'ffn2': info_sp['ffn_code'],
        'mf3': info_mp['mf_code'], 'ffn3': info_mp['ffn_code']
    }
    # MAKE DIRECTORY
    directory = str(dpath_save + _file_save_subdir.format(**fname_args))
    if not path.exists(directory):
        mkdir(directory)
    # MAKE FILES
    for x in mass_range:
        # GET LINES
        file_lines = _get_file_lines(
            x, results_zbt, results_sp, results_mp,
            io_map=io_map, exp_list=exp_list,
            row_lines_title=_row_lines_title,
            row_lines_subtitle=_row_lines_subtitle, row_zbt=_row_zbt,
            row_idx_key_head=_row_idx_key_head, row_idx_key=_row_idx_key,
            row_blank=_row_blank, row_sp=_row_sp, row_mp=_row_mp
        )
        # NAME FILE
        fname_args['mass'] = x
        fname = str(_file_save_name.format(**fname_args))
        fpath = str(directory + fname)
        # WRITE LINES TO FILE
        with open(fpath, 'w') as f:
            for line in file_lines:
                f.write(line)
                f.write(b'\n')


class InconsistentDatasetsGivenToIntFileGeneratorException(Exception):
    pass


def _get_file_lines(
        x, results_zbt, results_sp, results_mp, io_map, exp_list,
        row_lines_title, row_lines_subtitle, row_zbt, row_idx_key_head,
        row_idx_key, row_blank, row_sp, row_mp
):
    params_zbt = results_zbt[0][0]
    params_sp = results_sp[0][0]
    params_mp = results_mp[0][0]
    plots_zbt, fitfn_zbt, info_zbt = results_zbt[2:4]
    plots_sp, fitfn_sp, info_sp = results_sp[2:4]
    plots_mp, fitfn_mp, info_mp = results_mp[2:4]
    file_lines = list()
    # + TITLE
    file_lines.extend(_title_lines(
        row_lines_title, info_zbt, info_sp, info_mp, e_hw_pairs=exp_list))
    file_lines.append(row_blank)
    # + SUBTITLE
    file_lines.extend(_subtitle_lines(
        row_lines_subtitle, params_zbt, params_sp, params_mp))
    file_lines.append(row_blank)
    # + ZERO BODY TERM
    file_lines.append(_zbt_line(row_zbt, x, params_zbt, plots_zbt, fitfn_zbt))
    file_lines.append(row_blank)
    # + INDEX KEY
    file_lines.append(row_idx_key_head)
    file_lines.extend(_index_lines(row_idx_key, io_map))
    file_lines.append(row_blank)
    # + SINGLE PARTICLE
    file_lines.append(_single_particle_line(
        row_sp, x, params_sp, plots_sp, fitfn_sp))
    # + INTERACTIONS
    file_lines.extend(
            _interactions_lines(row_mp, x, params_mp, plots_mp, fitfn_mp))
    return file_lines


def _title_lines(row_lines_title, info_zbt, info_sp, info_mp, e_hw_pairs):
    for i, info in zip(range(1, 4), [info_zbt, info_sp, info_mp]):
        row_lines_title[i] = row_lines_title[i].format(
                mf=info['mf_name'], code=info['mf_code'],
                ffn=info['ffn_name'], ffn_code=info['ffn_code']
        )
    row_lines_title[5] = row_lines_title[5].format(ehw=e_hw_pairs)
    return row_lines_title


def _subtitle_lines(row_lines_subtitle, params_zbt, params_sp, params_mp):
    for i, params in zip(range(1, 4), [params_zbt, params_sp, params_mp]):
        row_lines_subtitle[i] = row_lines_subtitle[i].format(params)
    return row_lines_subtitle


def _zbt_line(row_zbt, mass_num, params_zbt, plots_zbt, fitfn_zbt):
    get_energy = _get_e1 if isinstance(fitfn_zbt, FitFunction) else _get_e2
    if len(plots_zbt) != 1:
        raise OverlapOfZbtDataException()
    else:
        plot = plots_zbt[0]
    x, y, const_list, const_dict = plot
    energy = get_energy(params_zbt, const_list, const_dict, fitfn_zbt, mass_num)
    return row_zbt.format(energy)


class OverlapOfZbtDataException(Exception):
    pass


def _index_lines(row_index_key, io_map):
    lines = list()
    for k, v in sorted(io_map.items()):
        n, l, j, tz = v
        lines.append(row_index_key.format(
            k, int(n), int(l), str(int(2 * j)) + '/2', str(int(2 * tz)) + '/2')
        )
    return lines


def _single_particle_line(row_sp, mass_num, params_sp, plots_sp, fitfn_sp):
    fmt_args = list()
    get_energy = _get_e1 if isinstance(fitfn_sp, FitFunction) else _get_e2
    indices = list()
    for plot in sorted(plots_sp, key=lambda p: p[3]['index']):
        x, y, const_list, const_dict = plot[0:4]
        index = const_dict['index']
        if index in indices:
            raise OverlapOfSingleParticleDataException()
        else:
            indices.append(index)
            fmt_args.append(get_energy(
                params_sp, const_list, const_dict, fitfn_sp, mass_num))
    others = plots_sp[0][3]['others']
    fmt_args.extend([int(others[0]), int(others[1]), float(others[2])])
    return row_sp.format(*fmt_args)


class OverlapOfSingleParticleDataException(Exception):
    pass


def _interactions_lines(row_mp, mass_num, params_mp, plots_mp, fitfn_mp):
    lines = list()
    get_energy = _get_e1 if isinstance(fitfn_mp, FitFunction) else _get_e2
    interactions = list()
    for plot in sorted(plots_mp, key=lambda p: p[3]['interaction']):
        fmt_args = list()
        x, y, const_list, const_dict = plot[0:4]
        interaction = const_dict['interaction']
        if interaction in interactions:
            raise OverlapOfInteractionDataException()
        else:
            interactions.append(interaction)
            fmt_args.extend([i for i in interaction])
            fmt_args.append(get_energy(
                params_mp, const_list, const_dict, fitfn_mp, mass_num))
            lines.append(row_mp.format(*fmt_args))
    return lines


class OverlapOfInteractionDataException(Exception):
    pass


def _get_e1(params, const_list, const_dict, fitfn, mass_num):
    args = [params, const_list, const_dict]
    return fitfn(mass_num, *args)


def _get_e2(params, const_list, const_dict, fitfn, mass_num):
    args = params
    args.extend([const_list, const_dict])
    return fitfn(mass_num, *args)
