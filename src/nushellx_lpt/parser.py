"""nushellx_lpt/parser.py
Functions for parsing *.lpt files and generating maps from the data
"""
from __future__ import division
from __future__ import print_function

from os import sep, path, walk
from warnings import warn
from constants import F_PARSE_LPT_STR_CMNT as _LPT_CMNT_STR
from constants import F_PARSE_LPT_ROW_AZ as _ROW_AZ
from constants import F_PARSE_LPT_ROW_SPE as _ROW_SPE
from constants import F_PARSE_LPT_COL_START_SPE as _COL_START_SPE
from constants import F_PARSE_LPT_ROW_START_STATES as _ROW_STATES_START
from constants import F_PARSE_LPT_NCOLS_STATE as _NCOLS_STATE
from constants import FN_PARSE_LPT_RGX_FNAME_INT as _RGX_FNAME_INT
from constants import F_PARSE_INT_CMNT_STR as _INT_CMNT_STR
from constants import F_PARSE_INT_CMNT_ZBT as _INT_CMNT_STR_ZBT
from parse import content_lines, comment_lines, fraction_str_to_float
from parse import matches_completely
from int.parser import zero_body_term, zero_body_term_line


# EXP
def _a_z_line(filepath):
    """Get the line from the *.lpt file that contains A (mass number) and
    Z (proton number)
    :param filepath: path to *.lpt file
    """
    return list(content_lines(filepath, _LPT_CMNT_STR))[_ROW_AZ]


def a_z(filepath):
    """Return A and Z from a list of lines, whose a_z_line has the format
            a = [A] z = [Z]
    :param filepath: path to the *.lpt file
    :return: A, Z
    """
    elts = _a_z_line(filepath).split()
    return int(elts[2]), int(elts[5])  # A, Z


def interaction(filepath):
    """Assumes the grandparent directory will be named according to the
    interaction(s) used to generate the *.nushellx_lpt file
    :param filepath: the path describing the *.nushellx_lpt file
    :return: the interaction name
    """
    return filepath.split(sep)[-3]


def exp(filepath):
    """Get the elements necessary to form the ExpLpt for the given filepath
    :param filepath: path to the file
    :return: the tuple representation of the ExpLpt, that is (Z, interaction)
    """
    return (
        a_z(filepath=filepath)[1],
        str(interaction(filepath=filepath))
    )


# OTHER
def _zbt_from_lpt(fpath_lpt, fname_int_regex):
    """From the file path to a *.lpt file (and assuming the associated
    interaction file is in the same directory), gets the zero body term
    from that interaction file
    :param fpath_lpt: path to the *.lpt file
    :param fname_int_regex: regular expression that will completely
    and uniquely match the file name of the interaction file associated
    with the given *.lpt file
    """
    dirpath = path.split(fpath_lpt)[0]
    root, dirs, files = next(walk(dirpath))
    for fname in files:
        if matches_completely(fname_int_regex, fname):
            filepath_int = path.join(root, fname)
            return zero_body_term(
                zero_body_term_line(
                    cmnt_lines=comment_lines(filepath=filepath_int,
                                             comment_str=_INT_CMNT_STR),
                    zbt_comment=_INT_CMNT_STR_ZBT
                )
            )
    else:
        return None


# DATA
def _spe_line(filepath):
    """Returns the line containing single particle energies, adding an
    extra space at the occurrence of a - sign, since the code that writes
    the file does not ensure numbers are separated by spaces for some reason
    :param filepath: path to the *.lpt file
    """
    return list(content_lines(
        filepath=filepath, comment_str=_LPT_CMNT_STR
    ))[_ROW_SPE].replace('-', ' -')


def _spe_line_data(spe_line):
    """Retrieves a list of single particle energies (and whatever follows
    them) in the SPE line
    :param spe_line: string representation of the SPE line from a *.lpt file
    """
    return [float(hd) for hd in spe_line.split()[_COL_START_SPE:]]


def _state_lines(filepath):
    """Returns a list of state lines from the given *.lpt file
    :param filepath: path to *.lpt file
    """
    cl = list(content_lines(filepath=filepath, comment_str=_LPT_CMNT_STR))
    row0 = _ROW_STATES_START
    if len(cl) < row0 + 1:
        return list([])
    else:
        return cl[row0:]


def _state_line_data(state_line):
    """Given a single state lines, returns a list of items in the line,
    in their correct data representations. (floats, ints, etc)
    :param state_line: string representation of a *.lpt state line
    """
    state_line_data = state_line.split()
    cbl = list()
    cbl.extend([int(bl) for bl in state_line_data[0:2]])
    cbl.extend([float(bl) for bl in state_line_data[2:4]])
    cbl.extend([fraction_str_to_float(bl) for bl in state_line_data[4:6]])
    cbl.append(int(state_line_data[6]))
    if len(state_line_data) == _NCOLS_STATE:
        cbl.extend([float(state_line_data[7]), state_line_data[8]])
    else:
        cbl.extend([None, state_line_data[7]])
    return cbl


def _state_lines_data(state_lines):
    """Given a list of state lines (raw string representations of the
    state lines), maps the function _state_line_data onto this list to get
    a list of states.
    :param state_lines: list of state lines, where a state line is just the
    raw string representation of a state line from a *.lpt file
    """
    cured_body_lists = list()
    parse_errors = list()
    for row in state_lines:
        try:
            state_line_data = _state_line_data(state_line=row)
            cured_body_lists.append(state_line_data)
        except ValueError:
            parse_errors += row
            continue
    return cured_body_lists, parse_errors


# MAPS
def mass_to_spe_line_data_map(fpath_list):
    """Returns a map
        A (mass number) -> list of SPE line elements,
    where the SPE line elements are just the white-space-separated values
    in the SPE line in a *.lpt file
    :param fpath_list: list of file paths to parse
    """
    mh_map = dict()
    for f in fpath_list:
        mass = a_z(filepath=f)[0]
        mh_map[mass] = _spe_line_data(spe_line=_spe_line(filepath=f))
    return mh_map


def _n_to_state_data_map(state_lines_data):
    """Returns a map from
       N (state index) -> State (list of state line data)
    where N uses the convention of the *.lpt files (beginning at 1 instead of
    0)
    :param state_lines_data: list of state line data
    """
    nb_map = dict()
    for cbl in state_lines_data:
        nb_map[cbl[0]] = cbl[1:]
    return nb_map


def mass_to_n_to_state_data_map(fpath_list):
    """Returns a map
        A (mass number) -> N (state index) -> State (list of state data)
    :param fpath_list: list of files to parse
    """
    mnb_map = dict()
    problem_files = list()
    for f in fpath_list:
        mass = a_z(f)[0]
        state_lines_data, parse_errors = _state_lines_data(
            state_lines=_state_lines(filepath=f))
        if len(parse_errors) > 0:
            problem_files.append(f)
        nb_map = _n_to_state_data_map(state_lines_data=state_lines_data)
        mnb_map[mass] = nb_map
    if len(problem_files) > 0:
        print('Problem parsing files:')
    for pf in problem_files:
        print('    {}'.format(pf))
    return mnb_map


def mass_to_zbt_map(fpath_list):
    """Returns a map
        A (mass number) -> zero body term
    :param fpath_list: list of files to parse
    """
    d = dict()
    for fp_lpt in fpath_list:
        mass = a_z(filepath=fp_lpt)[0]
        zbt = _zbt_from_lpt(fpath_lpt=fp_lpt, fname_int_regex=_RGX_FNAME_INT)
        d[mass] = zbt
    return d
