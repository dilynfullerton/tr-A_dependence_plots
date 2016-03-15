from __future__ import print_function, division

from re import match
from constants import F_PARSE_NCSMVCE_OUT_CMNT_STR as _CMNT_STR
from constants import F_PARSE_NCSMVCE_OUT_RGX_LINE_Z as _RGX_LINE_Z
from constants import F_PARSE_NCSMVCE_OUT_RGX_LINE_STATE as _RGX_LINE_STATE
from constants import (F_PARSE_NCSMVCE_OUT_RGX_LINE_SPECTRUM as
                       _RGX_LINE_SPECTRUM)
from constants import FN_PARSE_NCSMVCE_OUT_RGX_NHW as _RGX_NHW
from constants import FN_PARSE_NCSMVCE_OUT_CHR_ELT_SPLIT as _CHR_SPLIT
from parse import content_lines, filename_elts_list
from ncsm_vce_lpt.parser import nhw_n1_n2_from_delts as nhw_n1_n2_from_felts


# EXP
def _z_from_filepath(filepath, _comment_str, _rgx_line_z):
    for line in content_lines(filepath=filepath, comment_str=_comment_str):
        if match(_rgx_line_z, line) is not None:
            return int(line.split()[2])
    else:
        return None


def exp(filepath,
        _comment_str=_CMNT_STR, _split_char=_CHR_SPLIT,
        _rgx_line_z=_RGX_LINE_Z, _rgx_nhw=_RGX_NHW):
    z = _z_from_filepath(filepath=filepath, _comment_str=_comment_str,
                         _rgx_line_z=_rgx_line_z)
    felts = filename_elts_list(filename=filepath, split_char=_split_char)
    nhw, n1, n2 = nhw_n1_n2_from_felts(delts=felts, regex_nhw=_rgx_nhw)
    return z, nhw, n1, n2


# FILENAME DATA
def _a_aeff(filepath, split_char):
    felts = filename_elts_list(filename=filepath, split_char=split_char)
    return tuple([int(x) for x in [felts[0][2:], felts[1]]])


# MAPS
def a_aeff_to_states_map(
        filepaths,
        _split_char=_CHR_SPLIT,
        _comment_str=_CMNT_STR,
        _rgx_line_state=_RGX_LINE_STATE,
        _rgx_line_spectrum=_RGX_LINE_SPECTRUM
):
    """Based on a given list of *.out filepaths, constructs a map from
    (A, Aeff) to the ordered list of states, each a tuple of energy (E),
    excited energy (Ex), angular momentum (J), and isospin (T).
    :param filepaths: list of filepaths from which to construct the mapping
    :param _split_char: character that separates filename elements
    :param _comment_str: string representing a commented line
    :param _rgx_line_state: regular expression that matches the beginning of
    the lines containing information about a state
    :param _rgx_line_spectrum: regular expression that matches the beginning
    of the lines containing a spectrum entry
    """
    a_aeff_to_states = dict()
    for f in filepaths:
        a, aeff = _a_aeff(filepath=f, split_char=_split_char)
        cl = content_lines(filepath=f, comment_str=_comment_str)
        state_lines, spectrum_lines = list(), list()
        for line in cl:
            if match(_rgx_line_state, line) is not None:
                state_lines.append(line)
            elif match(_rgx_line_spectrum, line) is not None:
                spectrum_lines.append(line)
        states_list = list()
        for state_ln, spect_ln in zip(state_lines, spectrum_lines):
            state_elts = state_ln.split()
            i = state_elts.index('=') + 1
            e, j, t = [float(x) for x in state_elts[i::3]]
            ex = float(spect_ln.split()[3])
            states_list.append((e, ex, j, t))
        a_aeff_to_states[(a, aeff)] = states_list
    return a_aeff_to_states
