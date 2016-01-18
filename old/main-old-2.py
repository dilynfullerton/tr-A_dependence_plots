from __future__ import print_function

import glob

from matplotlib import pyplot as plt
from numpy import *

# Constants
FILES_DIR = '../files/'
FILE_EXT = '.int'
HEADER_POS = 0
ORBITAL_ENERGY_START_INDEX = 1
MAX_NUM_ORBITALS = 6
START_INDEX = 1
NUM_ORBITALS = 6
COMMENT_CHAR = '!'
INDEX_COMMENT = 'Index'


# Functions
def files_with_ext_in_directory(directory, extension=FILE_EXT):
    """Returns a list of the filenames of all the files in the given
    directory with the given extension
    :param extension:
    :param directory: """
    filenames = list(glob.glob(os.path.join(directory, '*' + extension)))
    return filenames


def mass_number_from_filename(filename):
    """Gets the mass number from the file name. Assumes files are named
    according to the convention *A[mass number][file extension]
    :param filename:
    """
    index_of_extension = filename.rfind('.')
    filename = filename[:index_of_extension]
    index_of_mass_number = filename.rfind('A') + 1
    mass_number = int(filename[index_of_mass_number:])
    return mass_number


def _get_lines(filename):
    """Returns all of the lines read from the given file in a list (with
    line separators and blank lines removed
    """
    with open(filename) as f:
        lines = f.readlines()
    # Remove line separators
    lines = list(map(lambda x: x.strip(), lines))
    # Remove blank lines
    lines = list(filter(lambda x: x[0] is not '', lines))
    return lines


def content_lines(filename, comment_char=COMMENT_CHAR):
    """Returns a list of all of the lines that are not comments
    :param comment_char:
    :param filename:
    """
    lines = _get_lines(filename)
    return list(filter(lambda x: x[0] is not comment_char, lines))


def comment_lines(filename, comment_char=COMMENT_CHAR):
    """Returns all of the lines read from the given filename that are
    descriptive comments
    :param comment_char:
    :param filename:
    """
    lines = _get_lines(filename)
    lines = filter(lambda x: x[0] is comment_char, lines)
    lines = map(lambda x: x.strip('!').strip(), lines)
    lines = list(filter(lambda x: x is not '', lines))
    return lines


def index_lines(cmnt_lines, index_comment=INDEX_COMMENT):
    """From the set of comment lines taken from a data file, returns the
    lines that relate the orbital indices to their quantum numbers. Assumes
    these lines always occur at the end of the commented section and are
    directly preceded with a line beginning with the word "Index"
    :param index_comment:
    :param cmnt_lines:
    """
    start_index = -1
    for cl, index in zip(cmnt_lines, range(len(cmnt_lines) + 1)):
        if cl.find(index_comment) is 0:
            start_index = index + 1
            break
    return cmnt_lines[start_index:]


def index_map(idx_lines):
    """Returns a map from the orbital index to its descriptive quantum
    numbers
    :param idx_lines:
    """
    idx_map = dict()
    for line in idx_lines:
        row = line.split()
        row[0] = int(row[0])
        idx_map[row[0]] = tuple(row[1:])
    return idx_map


def header_list(lines, header_pos=HEADER_POS):
    """Returns the line containing the header in the form of an list
    :param header_pos:
    :param lines:
    """
    header_line = lines[header_pos]
    return header_line.split()


def index_tuple_map(filename):
    """Given a data file name, gets the mapping from orbital index to
    (n, l, j, tz) tuple
    :param filename:
    """
    return index_map(index_lines(comment_lines(filename)))


def orbital_energies(header_items_list,
                     start_index=ORBITAL_ENERGY_START_INDEX,
                     num_orbitals=MAX_NUM_ORBITALS):
    """Returns the orbital energies from the given header list
    :param num_orbitals:
    :param start_index:
    :param header_items_list:
    """
    return header_items_list[start_index: start_index + num_orbitals]


def orbital_energies_from_filename(filename):
    """Returns the orbital energies from the given filename through
    functional composition
    :param filename: """
    return orbital_energies(header_list(content_lines(filename)))


def mass_energy_map(file_dir, sub_dir):
    """Returns a map from atomic mass to orbital energy arrays
    :param sub_dir:
    :param file_dir:
    """
    d = dict()
    files = files_with_ext_in_directory(file_dir + sub_dir)
    for f in files:
        mass_number = mass_number_from_filename(f)
        orbital_energies_list = orbital_energies_from_filename(f)
        d[mass_number] = orbital_energies_list
    return d


def mass_index_tuple_map_map(file_dir, sub_dir):
    """Returns a map from the mass number to the associated index -> tuple
    map
    :param sub_dir:
    :param file_dir:
    """
    d = dict()
    files = files_with_ext_in_directory(file_dir + sub_dir)
    for f in files:
        mass_number = mass_number_from_filename(f)
        itm = index_tuple_map(f)
        d[mass_number] = itm
    return d


def plot_orbital_vs_mass_number(file_dir, sub_dir, orbital_index):
    """Returns the x points and y points for a plot of the orbital energies
    against mass number for the data files in the given directory and
    subdirectory
    :param orbital_index:
    :param sub_dir:
    :param file_dir:
    """
    me_map = mass_energy_map(file_dir, sub_dir)
    mit_map_map = mass_index_tuple_map_map(file_dir, sub_dir)
    x_points = list(sort(me_map.keys()))
    y_points = list()
    for mass_num in x_points:
        y_points.append(me_map[mass_num][orbital_index - 1])
    return x_points, y_points, mit_map_map[mass_num]


def plot_orbitals_vs_mass_number(file_dir, sub_dir,
                                 start_index=START_INDEX,
                                 num_orbitals=NUM_ORBITALS):
    """Plots the x and y points for all orbitals in a single plot
    :param num_orbitals:
    :param start_index:
    :param sub_dir:
    :param file_dir:
    """
    # Make a subplot
    ax = plt.subplot(111)
    for index in range(start_index, start_index + num_orbitals):
        x_points, y_points, labels = plot_orbital_vs_mass_number(file_dir,
                                                                 sub_dir,
                                                                 index)
        ax.plot(x_points, y_points, '-o',
                label=(str(sub_dir[:-1]) + ' ' + str(index) + ': ' +
                       str(labels[index]).replace("'", '')))
    plt.title('Energies for orbitals')
    plt.xlabel('Atomic mass A (amu)')
    plt.ylabel('Orbital energy (MeV)')

    # Shrink plot width and add legend
    plot_pos = ax.get_position()
    ax.set_position([plot_pos.x0, plot_pos.y0,
                     plot_pos.width * .8, plot_pos.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


plot_orbitals_vs_mass_number(file_dir=FILES_DIR, sub_dir='hw20/')

plot_orbitals_vs_mass_number(file_dir=FILES_DIR, sub_dir='e14_hw20/')

# plot_orbitals_vs_mass_number(file_dir=FILES_DIR, sub_dir='e14_hw24/')

plt.show()
