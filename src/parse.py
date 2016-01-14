from __future__ import print_function
import os
import glob

# ======================================================================
# Constants
# ======================================================================
FILES_DIR = '../files/'
FILE_EXT = '.int'
FILENAME_SPLIT = '_'
HEADER_POS = 0
ORBITAL_ENERGY_START_INDEX = 1
MAX_NUM_ORBITALS = 6
COMMENT_CHAR = '!'
INDEX_COMMENT = 'Index'


# ======================================================================
# Functions
# ======================================================================
def files_with_ext_in_directory(directory, extension=FILE_EXT):
    """Returns a list of the filenames of all the files in the given
    directory with the given extension
    :param extension:
    :param directory: """
    filenames = list(glob.glob(os.path.join(directory, '*' + extension)))
    return filenames


# ............................................................
# File name parsing
# ............................................................
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


def _filename_elts_list(filename, split_char):
    """Get a list of the elements in the filename where name elements are
    separated by split_char
    """
    ext_index = filename.rfind('.')
    filename_woext = filename[:ext_index]
    return filename_woext.split(split_char)


def e_level_from_filename(filename, split_char=FILENAME_SPLIT):
    """Gets the e-level number from the file name. 
    Assumes files are named accoding to the convention:
        ..._[...]_e[e-level]_[...]_...
    Also assumes that the name element containing th e-level is the last
    element which begins with an e.
    Returns -1 if not found.
    :param split_char:
    :param filename:
    """
    filename_elts_list = _filename_elts_list(filename, split_char)
    for elt in reversed(filename_elts_list):
        if str(elt[0]) == 'e':
            return int(elt[1:])
    return -1


def hw_from_filename(filename, split_char=FILENAME_SPLIT):
    """Gets the hw frequency number from the file name. Returns -1 if not
    found.
    + Assumes files are named according to the convention:
          ..._[...]_hw[hw number]_[...]_...
    + Assumes that the instance of the string 'hw' in the beginning of the
    element containing the number is the last instance of such that begins
    an element.
    :param split_char:
    :param filename:
    """
    filename_elts_list = _filename_elts_list(filename, split_char)
    for elt in reversed(filename_elts_list):
        if str(elt[0:2]) == 'hw':
            return int(elt[2:])
    return -1


# ............................................................
# File content parsing
# ............................................................
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


def index_lines(comment_lines, index_comment=INDEX_COMMENT):
    """From the set of comment lines taken from a data file, returns the
    lines that relate the orbital indices to their quantum numbers. Assumes
    these lines always occur at the end of the commented section and are
    directly preceded with a line beginning with the word "Index"
    :param index_comment:
    :param comment_lines:
    """
    start_index = -1
    for cl, index in zip(comment_lines, range(len(comment_lines) + 1)):
        if cl.find(index_comment) is 0:
            start_index = index + 1
            break
    return comment_lines[start_index:]


def header_list(lines, header_pos=HEADER_POS):
    """Returns the line containing the header in the form of an list
    :param header_pos:
    :param lines:
    """
    header_line = lines[header_pos]
    return header_line.split()


def interaction_data_array(lines, interaction_start=HEADER_POS + 1):
    """Returns the lines containing the interaction data in the form of an 
    array (list of lists)
    :param interaction_start:
    :param lines:
    """
    data_lines = lines[interaction_start:]
    for i in range(len(data_lines)):
        data_lines[i] = data_lines[i].split()
    return data_lines


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


# ............................................................
# Map construction
# ............................................................ 
def index_map(index_lines):
    """Returns a map from the orbital index to its descriptive quantum
    numbers
    :param index_lines:
    """
    index_map = dict()
    for line in index_lines:
        row = line.split()
        row[0] = int(row[0])
        index_map[row[0]] = tuple(row[1:])
    return index_map


def index_tuple_map(filename):
    """Given a data file name, gets the mapping from orbital index to
    (n, l, j, tz) tuple
    :param filename:
    """
    return index_map(index_lines(comment_lines(filename)))


def mass_energy_array_map(directory):
    """Returns a map from atomic mass to orbital energy arrays
    :param directory:
    """
    d = dict()
    files = files_with_ext_in_directory(directory)
    for f in files:
        mass_number = mass_number_from_filename(f)
        orbital_energies_list = orbital_energies_from_filename(f)
        d[mass_number] = orbital_energies_list
    return d


def mass_index_energy_map_map(directory):
    """Given a directory, creates a mapping
        mass number -> (index -> energy)
    using the files in that directory
    :param directory:
    """
    mea_map = mass_energy_array_map(directory)
    for k in mea_map.keys():
        v = mea_map[k]
        nextv = dict()
        for i in range(1, 1 + len(v)):
            nextv[i] = float(v[i - 1])
        mea_map[k] = nextv
    return mea_map


def _mass_interaction_data_array_map(directory):
    """Creates a mapping from mass number to an array of interaction data
    for each file in the directory
    """
    mida_map = dict()
    files = files_with_ext_in_directory(directory)
    for f in files:
        mass_number = mass_number_from_filename(f)
        ida = interaction_data_array(content_lines(f))
        mida_map[mass_number] = ida
    return mida_map


def mass_interaction_tuple_energy_map_map(directory):
    """Given a directory, creates a mapping
        mass number -> ( a, b, c, d, j -> energy )
    using the files in the directory
    :param directory:
    """
    mida_map = _mass_interaction_data_array_map(directory)
    for k in mida_map.keys():
        v = mida_map[k]
        nextv = dict()
        for row in v:
            tup = tuple(row[0:5])
            energy = float(row[6])
            nextv[tup] = energy
        mida_map[k] = nextv
    return mida_map
