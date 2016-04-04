"""Functions for parsing interaction files and extracting information from
their file names
"""

from __future__ import print_function

from parse import get_files_r, filename_elts_list, elt_from_felts
from parse import content_lines, comment_lines
from constants import FN_PARSE_INT_ELT_SPLIT as ELT_SPLIT
from constants import FN_PARSE_INT_RGX_BASE as REGEX_BASE
from constants import FN_PARSE_INT_RGX_E as REGEX_E
from constants import FN_PARSE_INT_RGX_HW as REGEX_HW
from constants import FN_PARSE_INT_RGX_MASS as REGEX_MASS
from constants import FN_PARSE_INT_RGX_NAME as REGEX_NAME
from constants import FN_PARSE_INT_RGX_RP as REGEX_RP
from constants import F_PARSE_INT_CMNT_INDEX as CMNT_INDEX
from constants import F_PARSE_INT_CMNT_ZBT as CMNT_ZBT
from constants import F_PARSE_INT_COL_START_ORBITAL as COL_START_ORBITAL
from constants import F_PARSE_INT_NCOLS_ORBITALS as NCOLS_ORBITALS
from constants import F_PARSE_INT_ROW_HEAD as ROW_HEAD
from constants import F_PARSE_INT_CMNT_STR as CMNT_STR


# ............................................................
# File name parsing
# ............................................................
def e_level_from_filename(filename, split_char=ELT_SPLIT,
                          e_regex=REGEX_E):
    """Gets the e-level number from the file name. 
    Assumes files are named accoding to the convention:
        ..._[...]_e[e-level]_[...]_...
    Also assumes that the name element containing th e-level is the last
    element which begins with an e.
    Returns None if not found.

    :param filename: the name of the file
    :param split_char: the character with which filename elements are separated
    :param e_regex: the regex that fully matches the element with e
    """
    return _e_from_felts(
        filename_elts_list(filename, split_char), e_regex)


def _e_from_felts(felts, e_regex):
    e = elt_from_felts(felts, e_regex)
    return int(e[1:]) if e is not None else None


def hw_from_filename(filename, split_char=ELT_SPLIT,
                     hw_regex=REGEX_HW):
    """Gets the hw frequency number from the file name. Returns None if not
    found.
    + Assumes files are named according to the convention:
          ..._[...]_hw[hw number]_[...]_...
    + Assumes that the instance of the string 'hw' in the beginning of the
    element containing the number is the last instance of such that begins
    an element.
    :param filename: the name of the file
    :param split_char: the character with which filename elements are separated
    :param hw_regex: the regex that fully matches the element with hw
    """
    return _hw_from_felts(
        filename_elts_list(filename, split_char), hw_regex)


def _hw_from_felts(felts, hw_regex):
    hw = elt_from_felts(felts, hw_regex)
    return int(hw[2:]) if hw is not None else None


def base_from_filename(filename, split_char=ELT_SPLIT,
                       base_regex=REGEX_BASE):
    """Gets the base A-number from the filename

    Assumes that the base number is the first element (from left to right) that
    will be matched by the base_regex

    :param filename: the name of the file
    :param split_char: the character that separates file elements
    :param base_regex: the regular expression which will entirely match the
    element
    :return: the integer value of the base or None, if not found
    """
    return _base_from_felts(
        filename_elts_list(filename, split_char), base_regex)


def _base_from_felts(felts, base_regex):
    b = elt_from_felts(felts, base_regex)
    return int(b[1:]) if b is not None else None


def rp_from_filename(filename, split_char=ELT_SPLIT,
                     rp_regex=REGEX_RP):
    """Gets the Rp (proton radius) label from the file name, returns None if
    not found.

    :param filename: the name of the file to parse
    :param split_char: the character which separates filename elements
    :param rp_regex: the regex that fully matches the rp element
    :return: the Rp (integer) label, if found, otherwise returns None
    """
    return _rp_from_felts(
        reversed(filename_elts_list(filename, split_char)), rp_regex)


def _rp_from_felts(felts, rp_regex):
    rp = elt_from_felts(felts, rp_regex)
    return int(rp[rp.find('Rp')+2]) if rp is not None else None


def mass_number_from_filename(filename, split_char=ELT_SPLIT,
                              mass_regex=REGEX_MASS):
    """Gets the mass number from the file name. Assumes files are named
    according to the convention *A[mass number][file extension]

    :param filename: the filename from which to get the mass number
    :param split_char: the character that separates name elements
    :param mass_regex: the regex that fully matches the mass element
    """
    filename_elts = reversed(filename_elts_list(filename, split_char))
    mass = elt_from_felts(filename_elts, mass_regex)
    return int(mass[1:]) if mass is not None else None


def name_from_filename(filename, split_char=ELT_SPLIT,
                       name_regex=REGEX_NAME):
    """Gets the analysis method name from the filename

    Assumes that the name is the first element (from left to right) that will
    be entirely matched by name_regex

    :param filename: the name of the data file
    :param split_char: the split character for name
    :param name_regex: the regular expression which should be entirely matched
    by the name
    :return: name
    """
    felts_list = filename_elts_list(filename, split_char)
    return elt_from_felts(felts_list, name_regex)


def exp(filename, split_char=ELT_SPLIT, e_regex=REGEX_E, hw_regex=REGEX_HW,
        b_regex=REGEX_BASE, rp_regex=REGEX_RP):
    felts = filename_elts_list(filename, split_char)
    return (_e_from_felts(felts, e_regex), _hw_from_felts(felts, hw_regex),
            _base_from_felts(felts, b_regex), _rp_from_felts(felts, rp_regex))


# ............................................................
# File content parsing
# ............................................................


def index_lines(commnt_lines, index_comment=CMNT_INDEX):
    """From the set of comment lines taken from a data file, returns the
    lines that relate the orbital indices to their quantum numbers. Assumes
    these lines always occur at the end of the commented section and are
    directly preceded with a line beginning with the word "Index"
    :param commnt_lines: lines commented out
    :param index_comment:
    """
    start_index = -1
    for cl, index in zip(commnt_lines, range(len(commnt_lines) + 1)):
        if cl.find(index_comment) == 0:
            start_index = index + 1
            break
    return list(commnt_lines)[start_index:]


def zero_body_term_line(cmnt_lines, zbt_comment=CMNT_ZBT):
    """From the set of comment lines taken from a data file, returns the line
    that tells the zero body term.

    :param cmnt_lines: lines that are comments in the data file
    :param zbt_comment: the descriptive flag that indicates that the given line
    is the zero body term line
    :return: The zero body term line, as a string
    """
    for cl in reversed(list(cmnt_lines)):
        if cl.find(zbt_comment) == 0:
            return cl
    else:
        return None


def zero_body_term(zbt_line):
    if zbt_line is not None:
        return float(zbt_line.split(':')[1].strip())
    else:
        return None


# todo docstring
def header_list(lines, header_pos=ROW_HEAD):
    """Returns the line containing the header in the form of an list
    :param header_pos:
    :param lines:
    """
    header_line = lines[header_pos]
    return header_line.split()


# todo docstring
def interaction_data_array(lines, interaction_start=ROW_HEAD + 1):
    """Returns the lines containing the interaction data in the form of an 
    array (list of lists)
    :param lines:
    :param interaction_start:
    """
    data_lines = lines[interaction_start:]
    for i in range(len(data_lines)):
        data_lines[i] = data_lines[i].split()
    return data_lines


# todo docstring
def orbital_energies(
        header_items_list, start_index=COL_START_ORBITAL,
        num_orbitals=NCOLS_ORBITALS
):
    """Returns the orbital energies from the given header list
    :param num_orbitals:
    :param start_index:
    :param header_items_list:
    """
    return header_items_list[start_index: start_index + num_orbitals]


# todo docstring
def other_constants(
        header_items_list, start_index=COL_START_ORBITAL,
        num_orbitals=NCOLS_ORBITALS
):
    """Return the other values in the header items list, following the
    orbital energies

    :param header_items_list:
    :param start_index:
    :param num_orbitals:
    :return:
    """
    return header_items_list[start_index + num_orbitals:]


def orbital_energies_from_filename(filepath, comment_str=CMNT_STR):
    """Returns the orbital energies from the given filename through
    functional composition
    :param filepath: path to the file
    :param comment_str: string signifying a commented line
    """
    return orbital_energies(header_list(
        lines=list(content_lines(filepath, comment_str))))


# todo docstring
def other_constants_from_filename(filepath, comment_str=CMNT_STR):
    """Given a filename, returns all of the items in the header items list
    following the orbital energies
    :param filepath: path to the file
    :param comment_str: string signifying a commented line
    :return:
    """
    return other_constants(header_list(
        lines=list(content_lines(filepath, comment_str))))


# ............................................................
# Map construction
# ............................................................
# todo docstring
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


def index_to_tuple_map(filepath, comment_str=CMNT_STR):
    """Given a data file name, gets the mapping from orbital index to
    (n, l, j, tz) tuple
    :param filepath: path to the file
    :param comment_str: string signifying a commented line
    """
    return index_map(index_lines(
        commnt_lines=comment_lines(filepath, comment_str)))


# todo docstring
def mass_energy_array_map(directory, filterfn=lambda x: True,
                          filtered_files=None):
    """Returns a map from atomic mass to orbital energy arrays
    :param filtered_files:
    :param directory: the directory which is a direct parent to the files to use
    :param filterfn: the function to use to filter the file names in the
    directory
    """
    if filtered_files is None:
        filtered_files = get_files_r(directory, filterfn)
    d = dict()
    for f in filtered_files:
        mass_number = mass_number_from_filename(f)
        orbital_energies_list = orbital_energies_from_filename(f)
        d[mass_number] = orbital_energies_list
    return d


def mass_to_index_to_energy_map(directory, filterfn=lambda x: True,
                                filtered_files=None):
    """Given a directory, creates a mapping
        mass number -> (index -> energy)
    using the files in that directory
    :param filtered_files:
    :param directory: the directory that is a direct parent to the files from
    which the map is to be constructed
    :param filterfn: the filter to apply to the files prior to constructing the
    map
    """
    mea_map = mass_energy_array_map(directory, filterfn, filtered_files)
    for k in mea_map.keys():
        v = mea_map[k]
        nextv = dict()
        for i in range(1, 1 + len(v)):
            nextv[i] = float(v[i - 1])
        mea_map[k] = nextv
    return mea_map


def _mass_interaction_data_array_map(
        directory, filterfn=lambda x: True, filtered_files=None,
        comment_str=CMNT_STR
):
    """Creates a mapping from mass number to an array of interaction data
    for each file in the directory
    """
    if filtered_files is None:
        filtered_files = get_files_r(directory, filterfn)
    mida_map = dict()
    for f in filtered_files:
        mass_number = mass_number_from_filename(f)
        ida = interaction_data_array(lines=list(content_lines(f, comment_str)))
        mida_map[mass_number] = ida
    return mida_map


def mass_to_interaction_to_energy_map(directory, filterfn=lambda x: True,
                                      filtered_files=None):
    """Given a directory, creates a mapping
        mass number -> ( a, b, c, d, j -> energy )
    using the files in the directory
    :param filtered_files:
    :param directory: the directory which is a direct parent to the files from
    which to generate the map
    :param filterfn: the filter function to apply to the files before
    constructing the map
    """
    mida_map = _mass_interaction_data_array_map(
        directory, filterfn, filtered_files)
    for k in mida_map.keys():
        v = mida_map[k]
        nextv = dict()
        for row in v:
            tup = tuple(row[0:6])
            energy = float(row[6])
            nextv[tup] = energy
        mida_map[k] = nextv
    return mida_map


def mass_to_zbt_map(directory, filterfn=lambda x: True,
                    filtered_files=None, comment_str=CMNT_STR):
    """Given a directory, creates a mapping
            mass -> zero body term
    using the files in the directory
    :param directory: the directory that is a direct parent to the files from
    which to construct the map
    :param filterfn: the filter to apply to the files before constructing the
    map
    :param filtered_files: filepaths from which to gather data. If None, looks
    in whole directory
    :param comment_str: String signifying a commented line.
    """
    if filtered_files is None:
        filtered_files = get_files_r(directory, filterfn)
    mzbt_map = dict()
    for f in filtered_files:
        mass_number = mass_number_from_filename(f)
        zbt = zero_body_term(
            zero_body_term_line(cmnt_lines=comment_lines(f, comment_str)))
        mzbt_map[mass_number] = zbt
    return mzbt_map


# todo docstring
def mass_other_constants_map(directory, filterfn=lambda x: True,
                             filtered_files=None):
    """Given a directory, creates a mapping from mass number to the other
    constants following the orbital energies in the first line of data

    :param filtered_files:
    :param directory:
    :param filterfn:
    :return:
    """
    if filtered_files is None:
        filtered_files = get_files_r(directory, filterfn)
    moc_map = dict()
    for f in filtered_files:
        mass_number = mass_number_from_filename(f)
        oc = other_constants_from_filename(f)
        moc_map[mass_number] = oc
    return moc_map
