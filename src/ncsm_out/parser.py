"""Functions to parse data from NCSD *.out files and construct maps from it
"""
from __future__ import print_function, division

from re import match
from constants import F_PARSE_NCSMVCE_OUT_CMNT_STR as _CMNT_STR
from constants import F_PARSE_NCSMVCE_OUT_RGX_LINE_Z as _RGX_LINE_Z
from constants import F_PARSE_NCSMVCE_OUT_RGX_LINE_STATE as _RGX_LINE_STATE
from constants import (F_PARSE_NCSMVCE_OUT_RGX_LINE_SPECTRUM as
                       _RGX_LINE_SPECTRUM)
from constants import FN_PARSE_NCSMVCE_OUT_RGX_NHW as _RGX_NHW
from constants import FN_PARSE_NCSMVCE_OUT_RGX_SCALE as _RGX_SCALE
from constants import FN_PARSE_NCSMVCE_OUT_CHR_ELT_SPLIT as _CHR_SPLIT
from parse import content_lines, filename_elts_list, elt_from_felts
from ncsm_vce_lpt.parser import nmax_n1_n2_from_delts as nhw_n1_n2_from_felts


# EXP
def _z_from_filepath(filepath, comment_str, rgx_line_z):
    for line in content_lines(filepath=filepath, comment_str=comment_str):
        if match(rgx_line_z, line) is not None:
            return int(line.split()[2])
    else:
        return None


def exp(filepath):
    z = _z_from_filepath(filepath=filepath, comment_str=_CMNT_STR,
                         rgx_line_z=_RGX_LINE_Z)
    felts = filename_elts_list(filename=filepath, split_char=_CHR_SPLIT)
    nhw, n1, n2 = nhw_n1_n2_from_felts(delts=felts, regex_nmax=_RGX_NHW)
    scale_elt = elt_from_felts(felts=felts, elt_regex=_RGX_SCALE)
    if scale_elt is None:
        scalefactor = None
    else:
        scalefactor = float(scale_elt[5:])
    return z, n1, n2, scalefactor


# FILENAME DATA
def _a_aeff_nhw(filepath, split_char):
    felts = filename_elts_list(filename=filepath, split_char=split_char)
    return tuple([int(x) for x in [felts[0][2:], felts[1], felts[2][3:]]])


# MAPS
def a_aeff_nhw_to_states_map(filepaths):
    """Based on a given list of *.out filepaths, constructs a map from
    (A, Aeff, Nhw) to the ordered list of states, each a tuple of
    energy (E), excited energy (Ex), angular momentum (J), and isospin (T).
    :param filepaths: list of filepaths from which to construct the mapping
    """
    a_aeff_nhw_to_states = dict()
    for f in filepaths:
        a, aeff, nhw = _a_aeff_nhw(filepath=f, split_char=_CHR_SPLIT)
        cl = content_lines(filepath=f, comment_str=_CMNT_STR)
        state_lines, spectrum_lines = list(), list()
        for line in cl:
            if match(_RGX_LINE_STATE, line) is not None:
                state_lines.append(line)
            elif match(_RGX_LINE_SPECTRUM, line) is not None:
                spectrum_lines.append(line)
        states_list = list()
        for state_ln, spect_ln in zip(state_lines, spectrum_lines):
            state_elts = state_ln.split()
            i = state_elts.index('=') + 1
            e, j, t = [float(x) for x in state_elts[i::3]]
            ex = float(spect_ln.split()[3])
            states_list.append((e, ex, j, t))
        a_aeff_nhw_to_states[(a, aeff, nhw)] = states_list
    return a_aeff_nhw_to_states
