"""ncsm_vce_lpt/parser.py
Functions for parsing *.lpt file data from a VCE *.int file. This amounts
simply to retrieving the information necessary to construct the exp, as
all *.lpt data is parsed by the parser in /nushellx_lpt
"""
from __future__ import division, print_function

from re import sub

from constants import FN_PARSE_INT_ELT_SPLIT as _CHR_SPLIT
from constants import FN_PARSE_NCSMVCE_LPT_RGX_PRESC as _RGX_PRESC
from constants import FN_PARSE_NCSMVCE_LPT_RGX_NMAX as _RGX_NMAX
from constants import FN_PARSE_NCSMVCE_LPT_RGX_NSHELL as _RGX_NSHELL
from constants import FN_PARSE_NCSMVCE_LPT_RGX_NCOMP as _RGX_NCOMP
from constants import FN_PARSE_NCSMVCE_LPT_RGX_SCALE as _RGX_SCALE
from constants import FN_PARSE_NCSMVCE_LPT_RGX_IPROT as _RGX_IPROT
from parse import elt_from_felts, filename_elts_list
from nushellx_lpt.parser import interaction as datum_dirname
from nushellx_lpt.parser import a_z as a_z


# EXP
def _a_presc_from_delts(delts, regex_presc):
    """Get the A-prescription tuple from directory name elements
    :param delts: list of ordered directory name elements
    :param regex_presc: regular expression that fully matches the
    A-prescription element
    :return A-prescription element, if found; else, return None
    """
    a_presc_elt = elt_from_felts(felts=delts, elt_regex=regex_presc)
    if a_presc_elt is not None:
        a_presc_tuple_str = sub('[A-Za-z]', '', a_presc_elt)
        return tuple([int(x) for x in a_presc_tuple_str.split(',')])
    else:
        return None


def nmax_n1_n2_from_delts(delts, regex_nmax):
    """Gets a 3-tuple containing (Nmax, N1, N2) from the given directory name
    elements list
    :param delts: list of directory name elements
    :param regex_nmax: regular expression that fully matches the Nmax element.
    N1 and N2 are assumed to be the next two elements
    :return: 3-tuple (Nmax, N1, N2) if found; else return (None, None, None)
    """
    nmax_elt = elt_from_felts(felts=delts, elt_regex=regex_nmax)
    if nmax_elt is None:
        return (None,)*3
    else:
        nhw_elt0 = sub('[A-Za-z]', '', nmax_elt)
        i = delts.index(nmax_elt)
        n1_elt, n2_elt = delts[i+1:i+3]
        nnn = [int(x) for x in [nhw_elt0, n1_elt, n2_elt]]
        # if nnn[0] % 2 == 1:
        #     nnn[0] -= 1
        return tuple(nnn)


def exp(filepath):
    """From the given file path, returns the ordered tuple necessary to
    generate the file's ExpNcsmVceLpt
    :param filepath: path to the file
    """
    z = a_z(filepath=filepath)[1]
    dirname = datum_dirname(filepath=filepath)
    delts = filename_elts_list(
        filename=dirname, split_char=_CHR_SPLIT, remove_ext=False)
    a_presc = _a_presc_from_delts(delts=delts, regex_presc=_RGX_PRESC)
    nmax, n1, n2 = nmax_n1_n2_from_delts(delts=delts, regex_nmax=_RGX_NMAX)
    nshell = int(elt_from_felts(felts=delts, elt_regex=_RGX_NSHELL)[5:])
    ncomponent = int(elt_from_felts(felts=delts, elt_regex=_RGX_NCOMP)[3:])
    scale_elt = elt_from_felts(felts=delts, elt_regex=_RGX_SCALE)
    scalefactor = float(scale_elt[5:]) if scale_elt is not None else 1.0
    incl_prot = elt_from_felts(felts=delts, elt_regex=_RGX_IPROT) is None
    return z, a_presc, nmax, n1, n2, nshell, ncomponent, scalefactor, incl_prot
