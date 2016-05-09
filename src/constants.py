"""constants.py
Constants for use throughout the project
"""

from __future__ import unicode_literals

from LegendSize import LegendSize
from int.QuantumNumbers import QuantumNumbers

# Directory locations relative to src/
DPATH_FILES_INT = '../files_INT'
DPATH_FILES_INT_ORG = '../files_INT_org'
DPATH_FILES_OP = '../files_OP'
DPATH_FILES_OP_ORG = '../files_OP_org'
DPATH_PLOTS = '../plots'
DPATH_PLOTS_NCSMVCE = '../plots/vce_prescription_dependence'
DPATH_GEN_INT = '../gen_files_INT'
DPATH_SHELL_RESULTS = '../../tr-c-nushellx/results'
DPATH_NCSM_RESULTS = '../../tr-c-ncsm/results'

# File organization
ORG_FMT_INT_DNAME = 'sd-shell_{}_e{}_hw{}_O{}_Rp{}'
ORG_FMT_INT_FNAME = 'sd-shell_{}_e{}_hw{}_O{}_Rp{}_A{}.int'

# *.int filename parsing
FN_PARSE_INT_RGX_NAME = b'[a-z]+'
FN_PARSE_INT_RGX_MASS = b'A\d+'
FN_PARSE_INT_RGX_E = b'e\d+'
FN_PARSE_INT_RGX_HW = b'hw\d+'
FN_PARSE_INT_RGX_BASE = b'O\d+'
FN_PARSE_INT_RGX_RP = b'[a-z]+\d\.\d+Rp\d'
FN_PARSE_INT_RGX_EXT = b'.*\.int'
FN_PARSE_INT_STR_EXT = b'.int'
FN_PARSE_INT_ELT_SPLIT = b'_'

# *.int file content parsing
F_PARSE_INT_ROW_HEAD = 0
F_PARSE_INT_COL_START_ORBITAL = 1
F_PARSE_INT_NCOLS_ORBITALS = 6
F_PARSE_INT_CMNT_STR = b'!'
F_PARSE_INT_CMNT_INDEX = b'Index'
F_PARSE_INT_CMNT_ZBT = b'Zero body term'

# nushellx *.lpt filename parsing
FN_PARSE_LPT_RGX_FNAME = b'[a-z][a-z_]\d\d[a-z]\.lpt'
FN_PARSE_LPT_RGX_FNAME_INT = b'A\d+\.int|usdb\.int'
FN_PARSE_LPT_RGX_DNAME = b'files_org|gen_files|usdb'

# nushellx *.lpt file content parsing
F_PARSE_LPT_ROW_AZ = 1
F_PARSE_LPT_ROW_SPE = 2
F_PARSE_LPT_ROW_START_STATES = 4
F_PARSE_LPT_COL_START_SPE = 1
F_PARSE_LPT_NCOLS_STATE = 9
F_PARSE_LPT_COLS_INT = [0, 1, 6]
F_PARSE_LPT_COLS_FLOAT = [2, 3]
F_PARSE_LPT_COLS_HALF_INT = [4, 5]
F_PARSE_LPT_COLS_FLOAT_NONE = [7]
F_PARSE_LPT_COLS_STR = [8]
F_PARSE_LPT_STR_CMNT = b'!'

# ncsm/vce *.lpt filename parsing
FN_PARSE_NCSMVCE_LPT_RGX_DNAME = b'vce'
FN_PARSE_NCSMVCE_LPT_RGX_PRESC = b'presc\d+,\d+,\d+'
FN_PARSE_NCSMVCE_LPT_RGX_NMAX = b'Nmax\d+'
FN_PARSE_NCSMVCE_LPT_RGX_NSHELL = b'shell\d+'
FN_PARSE_NCSMVCE_LPT_RGX_NCOMP = b'dim\d+'
FN_PARSE_NCSMVCE_LPT_RGX_SCALE = b'scale\d+\.\d+'
FN_PARSE_NCSMVCE_LPT_RGX_IPROT = b'ip0'

# *.op filename parsing
FN_PARSE_OP_RGX_NAME = b'[A-Za-z]+'
FN_PARSE_OP_RGX_HW = FN_PARSE_INT_RGX_HW
FN_PARSE_OP_RGX_EXT = b'.*\.op'

# *.op file content parsing
F_PARSE_OP_RGX_HERM = b'[A-Za-z]+'
F_PARSE_OP_RGX_0B = b'\$ZeroBody:.*'
F_PARSE_OP_RGX_1B = b'\$OneBody:\s*'
F_PARSE_OP_RGX_2B = b'\$TwoBody:\s*'
F_PARSE_OP_ELT_SPLIT = FN_PARSE_INT_ELT_SPLIT
F_PARSE_OP_STR_CMNT = F_PARSE_INT_CMNT_STR

# NCSM/VCE *.out filename parsing
FN_PARSE_NCSMVCE_OUT_RGX_FNAME = (
    b'(([a-z][a-z_-])|(\d+-))\d+_\d+_Nhw\d+_\d+_\d+'
    b'(_ip0)?(_scale.+)?\.out')
FN_PARSE_NCSMVCE_OUT_RGX_NHW = b'Nhw\d+'
FN_PARSE_NCSMVCE_OUT_RGX_SCALE = b'scale\d+\.\d+'
FN_PARSE_NCSMVCE_OUT_RGX_IPROT = FN_PARSE_NCSMVCE_LPT_RGX_IPROT
FN_PARSE_NCSMVCE_OUT_CHR_ELT_SPLIT = b'_'

# NCSM/VCE *.out file content parsing
F_PARSE_NCSMVCE_OUT_CMNT_STR = b'***'
F_PARSE_NCSMVCE_OUT_RGX_LINE_Z = b'Z\s+=\s+\d+.*'
F_PARSE_NCSMVCE_OUT_RGX_LINE_STATE = b'State\s#\s?\d+.*'
F_PARSE_NCSMVCE_OUT_RGX_LINE_SPECTRUM = b'\d+(\s+[\d\.]+){3,3}'


# Printing
# noinspection PyClassHasNoInit
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


P_TITLE = Color.YELLOW
P_HEAD = Color.PURPLE
P_SUB = Color.DARKCYAN
P_BOLD = Color.BOLD
P_END = Color.END
P_BREAK = '-' * 80

# Plotting
PLOT_CMAP = 'gnuplot'
PLOT_FIGSIZE = (16, 12)  # width, height

# Legend
LEGEND_MAX_COLS = 10
LEGEND_MAX_SPACE = .5
LEGEND_ROWS_PER_COL = 75
LEGEND_MAX_FONTSIZE = 14
LEGEND_MIN_FONTSIZE = 6
LEGEND_TOTAL_FONTSIZE = 480  # is divided by number of rows
LEGEND_SPACE_SCALE = 2
LEGEND_SIZE = LegendSize(
    max_cols=LEGEND_MAX_COLS,
    max_h_space=LEGEND_MAX_SPACE,
    max_fontsize=LEGEND_MAX_FONTSIZE,
    min_fontsize=LEGEND_MIN_FONTSIZE,
    total_fontsize=LEGEND_TOTAL_FONTSIZE,
    rows_per_col=LEGEND_ROWS_PER_COL,
    space_scale=LEGEND_SPACE_SCALE
)

STANDARD_IO_MAP = {
    1: QuantumNumbers(0.0, 2.0, 2.5, -0.5),
    2: QuantumNumbers(0.0, 2.0, 1.5, -0.5),
    3: QuantumNumbers(1.0, 0.0, 0.5, -0.5),
    4: QuantumNumbers(0.0, 2.0, 2.5, 0.5),
    5: QuantumNumbers(0.0, 2.0, 1.5, 0.5),
    6: QuantumNumbers(1.0, 0.0, 0.5, 0.5)
}

# Combining fit functions:
FF_NAME_PREF = '['
FF_NAME_SEP = ', '
FF_NAME_SUFF = ']'
FF_CODE_PREF = '['
FF_CODE_SEP = ','
FF_CODE_SUFF = ']'

# File generating
GEN_INT_DNAME_SUBDIR = ('/fit-generated-sd-shell_'
                        '{ehw}_{mf1}-{ffn1}_{mf2}-{ffn2}_{mf3}-{ffn3}')
GEN_INT_FNAME = ('/fit-generated-sd-shell_'
                 '{ehw}_{mf1}-{ffn1}_{mf2}-{ffn2}_{mf3}-{ffn3}_A{mass}.int')
GEN_INT_ROW_LINES_TITLE = [
    '! Interaction file generated from:',
    '!  +  zero body term fitter: {mf:<60} {code:<15}\n!'
    '        using fit function: {ffn:<60} {ffn_code:<15}',
    '!  + single particle fitter: {mf:<60} {code:<15}\n!'
    '        using fit function: {ffn:<60} {ffn_code:<15}',
    '!  +     interaction fitter: {mf:<60} {code:<15}\n!'
    '        using fit function: {ffn:<60} {ffn_code:<15}',
    '!',
    '! Fit performed on: {ehw}']
GEN_INT_ROW_LINES_FIT_PARAMS = [
    '! Fit params: ',
    '!  +  zero body term fit: {}',
    '!  + single particle fit: {}',
    '!  +    interactions fit: {}']
GEN_INT_ROW_ZERO_BODY_TERM = (
    '! Zero body term: {:.3f}')
GEN_INT_ROW_INDEX_KEY_HEAD = (
    '! Index   n l j tz')
GEN_INT_ROW_INDEX_KEY = (
    '!  {}   {} {} {} {}')
GEN_INT_ROW_BLANK = (
    '!')
GEN_INT_ROW_SINGLE_PARTICLE = (
    '-999  {:6f}  {:6f}  {:6f}  {:6f}  {:6f}  {:6f}    {}  {}  {:5f}'
)
GEN_INT_ROW_INTERACTION = (
    '{:4}{:4}{:4}{:4}{:8}{:5}{:19.6f}')
