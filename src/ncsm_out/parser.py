"""ncsm_out/parser.py
Functions to parse data from NCSD *.out files and construct maps from it
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
from constants import FN_PARSE_NCSMVCE_OUT_RGX_IPROT as _RGX_IPROT
from constants import FN_PARSE_NCSMVCE_OUT_CHR_ELT_SPLIT as _CHR_SPLIT
from parse import content_lines, filename_elts_list, elt_from_felts
from ncsm_vce_lpt.parser import nmax_n1_n2_from_delts as nhw_n1_n2_from_felts


# EXP
def _z_from_filepath(filepath, comment_str, rgx_line_z):
    """From the given file path, get the proton number (Z)
    :param filepath: file path
    :param comment_str: string signifying a comment line
    :param rgx_line_z: regular expression that matches the line containing Z
    :return proton number, or None if not found
    """
    for line in content_lines(filepath=filepath, comment_str=comment_str):
        if match(rgx_line_z, line) is not None:
            return int(line.split()[2])
    else:
        return None


def exp(filepath):
    """Get the tuple representation of the ExpNcsmOut for the given file
    """
    z = _z_from_filepath(filepath=filepath, comment_str=_CMNT_STR,
                         rgx_line_z=_RGX_LINE_Z)
    felts = filename_elts_list(filename=filepath, split_char=_CHR_SPLIT)
    nhw, n1, n2 = nhw_n1_n2_from_felts(delts=felts, regex_nmax=_RGX_NHW)
    incl_protons = elt_from_felts(felts=felts, elt_regex=_RGX_IPROT) is None
    scale_elt = elt_from_felts(felts=felts, elt_regex=_RGX_SCALE)
    if scale_elt is None:
        scalefactor = 1.0
    else:
        scalefactor = float(scale_elt[5:])
    return z, n1, n2, scalefactor, incl_protons


# FILENAME DATA
def _a_aeff_nhw(filepath, split_char):
    """Gets (A, Aeff, Nhw) from the given file path
    :param filepath: path to file
    :param split_char: character that splits elements in the file name
    """
    felts = filename_elts_list(filename=filepath, split_char=split_char)
    if len(felts[0]) > 1:  # he4
        return tuple([int(x) for x in [felts[0][2:], felts[1], felts[2][3:]]])
    else:  # o
        felts = felts[1:]
        return tuple([int(x) for x in [felts[0], felts[1], felts[2][3:]]])


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
