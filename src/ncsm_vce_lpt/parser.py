"""Functions for parsing *.lpt file data from a VCE *.int file. This amounts
simply to retrieving the information necessary to construct the exp, as
all *.lpt data is parsed by the parser in /nushellx_lpt
"""
from __future__ import division, print_function

from re import sub

from constants import F_PARSE_LPT_STR_CMNT as _STR_CMNT
from constants import F_PARSE_LPT_ROW_AZ as _ROW_AZ
from constants import FN_PARSE_INT_ELT_SPLIT as _CHR_SPLIT
from constants import FN_PARSE_NCSMVCE_LPT_RGX_PRESC as _RGX_PRESC
from constants import FN_PARSE_NCSMVCE_LPT_RGX_NMAX as _RGX_NMAX
from constants import FN_PARSE_NCSMVCE_LPT_RGX_NSHELL as _RGX_NSHELL
from constants import FN_PARSE_NCSMVCE_LPT_RGX_NCOMP as _RGX_NCOMP
from constants import FN_PARSE_NCSMVCE_LPT_RGX_SCALE as _RGX_SCALE
from parse import elt_from_felts, filename_elts_list
from nushellx_lpt.parser import interaction as datum_dirname
from nushellx_lpt.parser import a_z as a_z


# EXP
def _a_presc_from_delts(delts, regex_presc):
    a_presc_elt = elt_from_felts(felts=delts, elt_regex=regex_presc)
    a_presc_tuple_str = sub('[A-Za-z]', '', a_presc_elt)
    return tuple([int(x) for x in a_presc_tuple_str.split(',')])


def nmax_n1_n2_from_delts(delts, regex_nmax):
    nhw_elt = elt_from_felts(felts=delts, elt_regex=regex_nmax)
    if nhw_elt is None:
        return (None,)*3
    else:
        nhw_elt0 = sub('[A-Za-z]', '', nhw_elt)
        i = delts.index(nhw_elt)
        n1_elt, n2_elt = delts[i+1:i+3]
        nnn = [int(x) for x in [nhw_elt0, n1_elt, n2_elt]]
        # if nnn[0] % 2 == 1:
        #     nnn[0] -= 1
        return tuple(nnn)


def exp(filepath):
    z = a_z(filepath=filepath, comment_str=_STR_CMNT, row_az=_ROW_AZ)[1]
    dirname = datum_dirname(filepath=filepath)
    delts = filename_elts_list(
        filename=dirname, split_char=_CHR_SPLIT, remove_ext=False)
    a_presc = _a_presc_from_delts(delts=delts, regex_presc=_RGX_PRESC)
    nmax, n1, n2 = nmax_n1_n2_from_delts(delts=delts, regex_nmax=_RGX_NMAX)
    nshell = int(elt_from_felts(felts=delts, elt_regex=_RGX_NSHELL)[5:])
    ncomponent = int(elt_from_felts(felts=delts, elt_regex=_RGX_NCOMP)[3:])
    scale_elt = elt_from_felts(felts=delts, elt_regex=_RGX_SCALE)
    scalefactor = float(scale_elt[5:]) if scale_elt is not None else 1.0
    return z, a_presc, nmax, n1, n2, nshell, ncomponent, scalefactor
