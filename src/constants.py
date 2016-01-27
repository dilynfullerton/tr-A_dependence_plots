from ImsrgDatum import QuantumNumbers

# Directories
FILES_DIR = '../files'
PLOTS_DIR = '../plots'

# Printing
P_TITLE = '\033[91m'
P_HEAD = '\033[95m'
P_SUB = '\033[36m'
P_BOLD = '\033[1m'
P_END = '\033[0m'
P_BREAK = '-' * 80

# Plotting
PLOT_CMAP = 'gnuplot'
LEGEND_MAX_COLS = 6
LEGEND_MAX_SPACE = .5
LEGEND_ROWS_PER_COL = 75
LEGEND_MAX_FONTSIZE = 14
LEGEND_TOTAL_FONTSIZE = 480  # is divided by number of rows
LEGEND_SPACE_SCALE = 2

STANDARD_IO_MAP = {
    1: QuantumNumbers(0.0, 2.0, 2.5, -0.5),
    2: QuantumNumbers(0.0, 2.0, 1.5, -0.5),
    3: QuantumNumbers(1.0, 0.0, 0.5, -0.5),
    4: QuantumNumbers(0.0, 2.0, 2.5, 0.5),
    5: QuantumNumbers(0.0, 2.0, 1.5, 0.5),
    6: QuantumNumbers(1.0, 0.0, 0.5, 0.5)
}
