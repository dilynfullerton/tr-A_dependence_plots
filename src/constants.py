"""Constants for use throughout the project
"""

from __future__ import unicode_literals
from QuantumNumbers import QuantumNumbers
from LegendSize import LegendSize

# Directories
DIR_FILES = '../files'
DIR_FILES_ORG = '../files_org'
DIR_PLOTS = '../plots'
DIR_GEN_INT = '../gen_files'

# File organization
ORG_FMT_DIR = 'sd-shell_{}_e{}_hw{}_O{}_Rp{}'
ORG_FMT_FILE = 'sd-shell_{}_e{}_hw{}_O{}_Rp{}_A{}.int'

# *.int filename parsing
FN_PARSE_INT_REGEX_NAME = b'[a-z]+'
FN_PARSE_INT_REGEX_MASS = b'A\d+'
FN_PARSE_INT_REGEX_E = b'e\d+'
FN_PARSE_INT_REGEX_HW = b'hw\d+'
FN_PARSE_INT_REGEX_BASE = b'O\d+'
FN_PARSE_INT_REGEX_RP = b'[a-z]+\d\.\d+Rp\d'
FN_PARSE_INT_REGEX_EXT = b'.*\.int'
FN_PARSE_INT_EXT = b'.int'
FN_PARSE_INT_ELT_SPLIT = b'_'

# File content parsing
F_PARSE_ROW_HEAD = 0
F_PARSE_COL_START_ORBITAL = 1
F_PARSE_NCOLS_ORBITALS = 6
F_PARSE_CMNT_CHAR = b'!'
F_PARSE_CMNT_INDEX = b'Index'
F_PARSE_CMNT_ZBT = b'Zero body term'

# Printing
P_TITLE = '\033[91m'
P_HEAD = '\033[95m'
P_SUB = '\033[36m'
P_BOLD = '\033[1m'
P_END = '\033[0m'
P_BREAK = '-' * 80

# Plotting
PLOT_CMAP = 'gnuplot'

# Legend
LEGEND_MAX_COLS = 6
LEGEND_MAX_SPACE = .5
LEGEND_ROWS_PER_COL = 75
LEGEND_MAX_FONTSIZE = 14
LEGEND_TOTAL_FONTSIZE = 480  # is divided by number of rows
LEGEND_SPACE_SCALE = 2
LEGEND_SIZE = LegendSize(
    max_cols=LEGEND_MAX_COLS,
    max_h_space=LEGEND_MAX_SPACE,
    max_fontsize=LEGEND_MAX_FONTSIZE,
    total_fontsize=LEGEND_TOTAL_FONTSIZE,
    rows_per_col=LEGEND_ROWS_PER_COL,
    space_scale=LEGEND_SPACE_SCALE)

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
# noinspection PyPep8
GEN_INT_SUBDIR = '/fit-generated-sd-shell_{ehw}_{mf1}-{ffn1}_{mf2}-{ffn2}_{mf3}-{ffn3}'
# noinspection PyPep8
GEN_INT_FILE_NAME = '/fit-generated-sd-shell_{ehw}_{mf1}-{ffn1}_{mf2}-{ffn2}_{mf3}-{ffn3}_A{mass}.int'
# noinspection PyPep8
GEN_INT_ROW_LINES_TITLE = [
    '! Interaction file generated from:',
    '!  +  zero body term fitter: {mf:<60} {code:<15}\n!        using fit function: {ffn:<60} {ffn_code:<15}',
    '!  + single particle fitter: {mf:<60} {code:<15}\n!        using fit function: {ffn:<60} {ffn_code:<15}',
    '!  +     interaction fitter: {mf:<60} {code:<15}\n!        using fit function: {ffn:<60} {ffn_code:<15}',
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
