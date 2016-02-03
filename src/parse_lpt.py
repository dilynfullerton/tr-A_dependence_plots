from __future__ import division

from os import sep

from constants import F_PARSE_LPT_CMNT_CHAR as CMNT_CHAR
from constants import F_PARSE_LPT_ROW_AZ as ROW_AZ
from parse import content_lines, half_int_str_to_float


# EXP
def _a_z_line(filepath, comment_char, row_az):
    return content_lines(filepath, comment_char)[row_az]


def _a_z(filepath, comment_char=CMNT_CHAR, row_az=ROW_AZ):
    """Return A and Z from a list of lines, whose a_z_line has the format
            a = [A] z = [Z]

    :param content_lines: file lines without comments or blanks
    :param a_z_line: index of the line containing A and Z
    :return: A, Z
    """
    elts = _a_z_line(filepath, comment_char, row_az).split()
    return int(elts[2]), int(elts[5])  # A, Z


def _a(filepath, comment_char, row_az):
    return _a_z(filepath, comment_char, row_az)[0]


def _interaction(filepath):
    """Assumes the grandparent directory will be named according to the
    interaction(s) used to generate the *.lpt file
    :param filepath: the path describing the *.lpt file
    :return: the interaction name
    """
    return filepath.split(sep)[-3]


def exp(filepath, comment_char, row_az):
    """Get the elements necessary to form the ExpLpt for the given filepath
    :param filepath: path to the file
    :param comment_char: character representing a commented line
    :param row_az: the index of the a, z row with respect to content lines
    :return: the tuple representation of the ExpLpt, that is
            (Z, interaction)
    """
    return _a_z(filepath, comment_char, row_az)[1], _interaction(filepath)


# DATA
def _header_line(filepath, comment_char, row_head):
    return content_lines(filepath, comment_char)[row_head]


def _header_data(header_line, col_start):
    return header_line.split()[col_start:]


def _cured_header_data(header_data):
    return [float(hd) for hd in header_data]


def _body_lines(filepath, comment_char, row_body_start):
    return content_lines(filepath, comment_char)[row_body_start]


def _body_lists(body_lines):
    return list(map(lambda line: line.split(), body_lines))


def _cured_body_list(body_list, ncols_body):
    cbl = list()
    cbl[0:2] = [int(bl) for bl in body_list[0:2]]
    cbl[2:4] = [float(bl)for bl in body_list[2:4]]
    cbl[4:6] = [half_int_str_to_float(bl) for bl in body_list[4:6]]
    cbl[7] = int(body_list[7])
    cbl[8] = float(body_list(8)) if len(body_list) == ncols_body else None
    cbl[9] = body_list[9]
    return cbl


def _cured_body_lists(body_lists, ncols_body):
    return [_cured_body_list(row, ncols_body) for row in body_lists]


# MAPS
def mass_to_header_data_map(filtered_filepaths, comment_char,
                            row_az, row_head, col_start):
    mh_map = dict()
    for f in filtered_filepaths:
        mass = _a(f, comment_char, row_az)
        mh_map[mass] = _cured_header_data(
            _header_data(_header_line(f, comment_char, row_head), col_start))
    return mh_map


def _n_to_body_data_map(cured_body_lists):
    nb_map = dict()
    for cbl in cured_body_lists:
        nb_map[cbl[0]] = cbl[1:]
    return nb_map


def mass_to_n_to_body_data_map(filtered_filepaths, comment_char, row_az,
                               row_body_start, ncols_body):
    mnb_map = dict()
    for f in filtered_filepaths:
        mass = _a(f, comment_char, row_az)
        nb_map = _n_to_body_data_map(
            _cured_body_lists(
                _body_lists(_body_lines(f, comment_char, row_body_start)),
                ncols_body))
        mnb_map[mass] = nb_map
    return mnb_map
