"""Functions for parsing *.lpt files and generating maps from the data
"""
from __future__ import division
from __future__ import print_function

from os import sep, path, walk
from re import match

from constants import F_PARSE_LPT_CMNT_STR as _CMNT_STR
from constants import F_PARSE_LPT_ROW_AZ as _ROW_AZ
from constants import F_PARSE_LPT_ROW_HEAD as _ROW_HEAD
from constants import F_PARSE_LPT_COL_HEAD_DATA_START as _COL_START
from constants import F_PARSE_LPT_ROW_START_DATA as _ROW_BODY_START
from constants import F_PARSE_LPT_NCOLS_BODY as _NCOLS_BODY
from constants import FN_PARSE_LPT_REGEX_FILENAME_INT as _REGEX_FILENAME_INT
from constants import F_PARSE_INT_CMNT_STR as _INT_CMNT_STR
from constants import F_PARSE_INT_CMNT_ZBT as _INT_CMNT_ZBT
from parse import content_lines, comment_lines, half_int_str_to_float
from int.parser import zero_body_term, zero_body_term_line


# EXP
def _a_z_line(filepath, comment_str, row_az):
    return list(content_lines(filepath, comment_str))[row_az]


def a_z(filepath, comment_str=_CMNT_STR, row_az=_ROW_AZ):
    """Return A and Z from a list of lines, whose a_z_line has the format
            a = [A] z = [Z]
    :param filepath: path to the *.lpt file
    :param comment_str: character preceding commented lines
    :param row_az: index of the row containing A and Z, with respect to
    meaningful (content) lines
    :return: A, Z
    """
    elts = _a_z_line(filepath, comment_str, row_az).split()
    return int(elts[2]), int(elts[5])  # A, Z


def interaction(filepath):
    """Assumes the grandparent directory will be named according to the
    interaction(s) used to generate the *.nushellx_lpt file
    :param filepath: the path describing the *.nushellx_lpt file
    :return: the interaction name
    """
    return filepath.split(sep)[-3]


def exp(filepath, comment_str=_CMNT_STR, row_az=_ROW_AZ):
    """Get the elements necessary to form the ExpLpt for the given filepath
    :param filepath: path to the file
    :param comment_str: character representing a commented line
    :param row_az: the index of the a, z row with respect to content lines
    :return: the tuple representation of the ExpLpt, that is
            (Z, interaction)
    """
    return (a_z(filepath=filepath, comment_str=comment_str, row_az=row_az)[1],
            str(interaction(filepath=filepath)))


# OTHER
def _zbt_from_lpt(
        filepath_lpt, filename_int_regex, comment_str_int, zbt_comment
):
    dirpath = path.split(filepath_lpt)[0]
    root, dirs, files = next(walk(dirpath))
    for fname in files:
        m = match(filename_int_regex, fname)
        if m is not None and m.group(0) == fname:
            filepath_int = path.join(root, fname)
            return zero_body_term(
                zero_body_term_line(
                    cmnt_lines=comment_lines(filepath=filepath_int,
                                             comment_str=comment_str_int),
                    zbt_comment=zbt_comment
                )
            )
    else:
        return None


# DATA
def _header_line(filepath, comment_str, row_head):
    return list(content_lines(
        filepath=filepath, comment_str=comment_str))[row_head]


def _header_data(header_line, col_start):
    return header_line.split()[col_start:]


def _cured_header_data(header_data):
    return [float(hd) for hd in header_data]


def _body_lines(filepath, comment_str, row_body_start):
    cl = list(content_lines(filepath=filepath, comment_str=comment_str))
    if len(cl) < row_body_start + 1:
        return list([])
    else:
        return cl[row_body_start:]


def _body_lists(body_lines):
    return [line.split() for line in body_lines]


def _cured_body_list(body_list, ncols_body):
    cbl = list()
    cbl.extend([int(bl) for bl in body_list[0:2]])
    cbl.extend([float(bl)for bl in body_list[2:4]])
    cbl.extend([half_int_str_to_float(bl) for bl in body_list[4:6]])
    cbl.append(int(body_list[6]))
    if len(body_list) == ncols_body:
        cbl.extend([float(body_list[7]), body_list[8]])
    else:
        cbl.extend([None, body_list[7]])
    return cbl


def _cured_body_lists(body_lists, ncols_body):
    return [_cured_body_list(row, ncols_body) for row in body_lists]


# MAPS
def mass_to_header_data_map(
        filtered_filepaths,
        _comment_str=_CMNT_STR,
        _row_az=_ROW_AZ, row_head=_ROW_HEAD,
        _col_start=_COL_START
):
    mh_map = dict()
    for f in filtered_filepaths:
        mass = a_z(filepath=f, comment_str=_comment_str, row_az=_row_az)[0]
        mh_map[mass] = _cured_header_data(
            _header_data(header_line=_header_line(f, _comment_str, row_head),
                         col_start=_col_start))
    return mh_map


def _n_to_body_data_map(cured_body_lists):
    nb_map = dict()
    for cbl in cured_body_lists:
        nb_map[cbl[0]] = cbl[1:]
    return nb_map


def mass_to_n_to_body_data_map(
        filtered_filepaths,
        _comment_str=_CMNT_STR,
        _row_az=_ROW_AZ, row_body_start=_ROW_BODY_START,
        _ncols_body=_NCOLS_BODY
):
    mnb_map = dict()
    for f in filtered_filepaths:
        mass = a_z(f, _comment_str, _row_az)[0]
        nb_map = _n_to_body_data_map(
            _cured_body_lists(
                body_lists=_body_lists(
                    body_lines=_body_lines(f, _comment_str, row_body_start)),
                ncols_body=_ncols_body))
        mnb_map[mass] = nb_map
    return mnb_map


def mass_to_zbt_map(
        filtered_filepaths_lpt,
        _filename_int_regex=_REGEX_FILENAME_INT,
        _row_az=_ROW_AZ,
        _comment_str_lpt=_CMNT_STR,
        _comment_str_int=_INT_CMNT_STR,
        _zbt_comment=_INT_CMNT_ZBT
):
    d = dict()
    for fp_lpt in filtered_filepaths_lpt:
        mass = a_z(filepath=fp_lpt, comment_str=_comment_str_lpt,
                   row_az=_row_az)[0]
        zbt = _zbt_from_lpt(
            filepath_lpt=fp_lpt, filename_int_regex=_filename_int_regex,
            comment_str_int=_comment_str_int, zbt_comment=_zbt_comment
        )
        d[mass] = zbt
        print('{}: {}'.format(mass, zbt))
    return d
