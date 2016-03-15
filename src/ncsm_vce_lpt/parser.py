"""Functions for parsing *.lpt file data from a VCE *.int file. This amounts
simply to retrieving the information necessary to construct the exp, as
all *.lpt data is parsed by the parser in /nushellx_lpt
"""
from __future__ import division, print_function

from re import sub

from constants import F_PARSE_LPT_CMNT_STR as _STR_CMNT
from constants import F_PARSE_LPT_ROW_AZ as _ROW_AZ
from constants import FN_PARSE_INT_ELT_SPLIT as _CHR_SPLIT
from constants import FN_PARSE_NCSMVCE_LPT_REGEX_PRESC as _RGX_PRESC
from constants import FN_PARSE_NCSMVCE_LPT_REGEX_NHW as _RGX_NHW
from parse import elt_from_felts, filename_elts_list
from nushellx_lpt.parser import interaction as datum_dirname
from nushellx_lpt.parser import a_z as a_z


# EXP
def _a_presc_from_delts(delts, regex_presc):
    a_presc_elt = elt_from_felts(felts=delts, elt_regex=regex_presc)
    a_presc_tuple_str = sub('[A-Za-z]', '', a_presc_elt)
    return tuple([int(x) for x in a_presc_tuple_str.split(',')])


def nhw_n1_n2_from_delts(delts, regex_nhw):
    nhw_elt = elt_from_felts(felts=delts, elt_regex=regex_nhw)
    if nhw_elt is None:
        return (None,)*3
    else:
        nhw_elt0 = sub('[A-Za-z]', '', nhw_elt)
        i = delts.index(nhw_elt)
        n1_elt, n2_elt = delts[i+1:i+3]
        return tuple([int(x) for x in [nhw_elt0, n1_elt, n2_elt]])


def exp(filepath,
        _comment_str=_STR_CMNT, _row_az=_ROW_AZ, _split_char=_CHR_SPLIT,
        _regex_presc=_RGX_PRESC, _regex_nhw=_RGX_NHW):
    z = a_z(filepath=filepath, comment_str=_comment_str, row_az=_row_az)[1]
    dirname = datum_dirname(filepath=filepath)
    delts = filename_elts_list(filename=dirname, split_char=_split_char)
    a_presc = _a_presc_from_delts(delts=delts, regex_presc=_regex_presc)
    nhw, n1, n2 = nhw_n1_n2_from_delts(delts=delts, regex_nhw=_regex_nhw)
    return z, a_presc, nhw, n1, n2
