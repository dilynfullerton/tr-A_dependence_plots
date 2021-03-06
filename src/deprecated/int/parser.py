"""int/parser.py
Functions for parsing interaction files and extracting information from
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
from constants import F_PARSE_INT_ROW_SPE as ROW_SPE
from constants import F_PARSE_INT_CMNT_STR as CMNT_STR


# ............................................................
# File name parsing
# ............................................................
def e_level_from_filename(filename, split_char=ELT_SPLIT,
                          e_regex=REGEX_E):
    """Gets the e_max truncation number from the file name.
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
    """Gets the base A-number (that normal-ordering was done WRT)
    from the filename.
    Assumes that the base number is the first element (from left to right) that
    will be matched by the base_regex.
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
    """Gets the Rp (proton radius?) label from the file name, returns None if
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
    """Gets the method name (e.g. magnus) from the filename.
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
    """Returns a 4-tuple representing the exp (see int/ExpInt.py)
    :param filename: name of the interaction file
    :param split_char: character that separates filename elements
    :param e_regex: regular expression that matches the e_max element
    :param hw_regex: regular expression that matches the hw element
    :param b_regex: regular expression that matches the normal ordering element
    :param rp_regex: regular expression that matches the rp element
    :return: (emax, hw, b, rp)
    """
    felts = filename_elts_list(filename, split_char)
    return (_e_from_felts(felts, e_regex), _hw_from_felts(felts, hw_regex),
            _base_from_felts(felts, b_regex), _rp_from_felts(felts, rp_regex))


# ............................................................
# File content parsing
# ............................................................
# todo: Some of this could be done a lot better
def index_lines(commnt_lines, index_comment=CMNT_INDEX):
    """From the set of comment lines taken from a data file, returns the
    lines that relate the orbital indices to their quantum numbers. Assumes
    these lines always occur at the end of the commented section and are
    directly preceded with a line beginning with the word "Index"
    :param commnt_lines: lines commented out
    :param index_comment: comment string that indicates the start of the
    index -> orbital key
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


def spe_list(lines, spe_line_pos=ROW_SPE):
    """Returns the line containing the header in the form of an list
    :param spe_line_pos: position of the SPE line WRT to non-empty,
    non-comment lines
    :param lines: content lines
    """
    header_line = lines[spe_line_pos]
    return header_line.split()


def tbme_data_array(lines, interaction_start=ROW_SPE + 1):
    """Returns the lines containing the interaction data in the form of an 
    array (list of lists)
    :param lines: file content lines
    :param interaction_start: position of first TBME with respect to
    non-empty, non-commented file lines
    """
    data_lines = lines[interaction_start:]
    for i in range(len(data_lines)):
        data_lines[i] = data_lines[i].split()
    return data_lines


def orbital_energies(
        spe_line_items_list, start_index=COL_START_ORBITAL,
        num_orbitals=NCOLS_ORBITALS
):
    """Returns the orbital energies from the given header list
    :param num_orbitals: number of orbitals for which to gather lines
    :param start_index: position of first SPE in SPE line
    :param spe_line_items_list: list of split items in SPE line
    """
    return spe_line_items_list[start_index: start_index + num_orbitals]


def other_constants(
        spe_line_items_list, start_index=COL_START_ORBITAL,
        num_orbitals=NCOLS_ORBITALS
):
    """Return the other values in the header items list, following the SPE's
    :param spe_line_items_list: list of items in the SPE line
    :param start_index: index of first SPE in line
    :param num_orbitals: number of SPE's
    """
    return spe_line_items_list[start_index + num_orbitals:]


def orbital_energies_from_filename(filepath):
    """Returns the orbital energies from the given filename through
    functional composition
    :param filepath: path to the file
    """
    return orbital_energies(spe_list(
        lines=list(content_lines(filepath, CMNT_STR))))


def other_constants_from_filename(filepath):
    """Given a filename, returns all of the items in the header items list
    following the orbital energies
    :param filepath: path to the file
    """
    return other_constants(spe_list(
        lines=list(content_lines(filepath, CMNT_STR))))


# ............................................................
# Map construction
# ............................................................
def index_map(idx_lines):
    """Returns a map from the orbital index to its descriptive quantum
    numbers
    :param idx_lines: lines defining the index -> orbital key
    """
    idx_map = dict()
    for line in idx_lines:
        row = line.split()
        row[0] = int(row[0])
        idx_map[row[0]] = tuple(row[1:])
    return idx_map


def index_to_qnums_map(fpath):
    """Given a data file name, gets the mapping from orbital index to
    (n, l, j, tz) tuple
    :param fpath: path to the file
    """
    return index_map(index_lines(commnt_lines=comment_lines(fpath, CMNT_STR)))


def mass_spe_data_map(dpath, filterfn=lambda x: True, fpath_list=None):
    """Returns a map from mass number to orbital energy arrays
    :param dpath: the directory which is a direct parent to the files to use
    :param filterfn: the function to use to filter the file names in the
    directory
    :param fpath_list: relevant file paths
    """
    if fpath_list is None:
        fpath_list = get_files_r(dpath, filterfn)
    d = dict()
    for f in fpath_list:
        mass_number = mass_number_from_filename(f)
        orbital_energies_list = orbital_energies_from_filename(f)
        d[mass_number] = orbital_energies_list
    return d


def mass_to_index_to_energy_map(dpath, filterfn=lambda x: True,
                                fpath_list=None):
    """Given a directory, creates a mapping
        mass number -> (index -> energy)
    using the files in that directory
    :param fpath_list:
    :param dpath: the directory that is a direct parent to the files from
    which the map is to be constructed
    :param filterfn: the filter to apply to the files prior to constructing the
    map
    """
    mea_map = mass_spe_data_map(dpath, filterfn, fpath_list)
    for k in mea_map.keys():
        v = mea_map[k]
        nextv = dict()
        for i in range(1, 1 + len(v)):
            nextv[i] = float(v[i - 1])
        mea_map[k] = nextv
    return mea_map


def _mass_tbme_data_map(dpath, filterfn=lambda x: True, fpath_list=None):
    """Creates a mapping from mass number to an array of interaction data
    for each file in the directory
    """
    if fpath_list is None:
        fpath_list = get_files_r(dpath, filterfn)
    mida_map = dict()
    for f in fpath_list:
        mass_number = mass_number_from_filename(f)
        ida = tbme_data_array(lines=list(content_lines(f, CMNT_STR)))
        mida_map[mass_number] = ida
    return mida_map


def mass_to_tbint_to_energy_map(dpath, filterfn=lambda x: True,
                                fpath_list=None):
    """Given a directory, creates a mapping
        mass number -> ( a, b, c, d, j -> energy )
    using the files in the directory
    :param fpath_list:
    :param dpath: the directory which is a direct parent to the files from
    which to generate the map
    :param filterfn: the filter function to apply to the files before
    constructing the map
    """
    mida_map = _mass_tbme_data_map(
        dpath, filterfn, fpath_list)
    for k in mida_map.keys():
        v = mida_map[k]
        nextv = dict()
        for row in v:
            tup = tuple(row[0:6])
            energy = float(row[6])
            nextv[tup] = energy
        mida_map[k] = nextv
    return mida_map


def mass_to_zbt_map(dpath, filterfn=lambda x: True, fpath_list=None):
    """Given a directory, creates a mapping
            mass -> zero body term
    using the files in the directory
    :param dpath: the directory that is a direct parent to the files from
    which to construct the map
    :param filterfn: the filter to apply to the files before constructing the
    map
    :param fpath_list: filepaths from which to gather data. If None, looks
    in whole directory
    """
    if fpath_list is None:
        fpath_list = get_files_r(dpath, filterfn)
    mzbt_map = dict()
    for f in fpath_list:
        mass_number = mass_number_from_filename(f)
        zbt = zero_body_term(
            zero_body_term_line(cmnt_lines=comment_lines(f, CMNT_STR)))
        mzbt_map[mass_number] = zbt
    return mzbt_map


def mass_other_constants_map(dpath, filterfn=lambda x: True, fpath_list=None):
    """Given a directory, creates a mapping from mass number to the other
    constants following the orbital energies in the first line of data
    :param dpath: main directory
    :param filterfn: filter to apply to files before constructing the map
    :param fpath_list: if not None, this is used instead of getting files
    in the directory
    """
    if fpath_list is None:
        fpath_list = get_files_r(dpath, filterfn)
    moc_map = dict()
    for f in fpath_list:
        mass_number = mass_number_from_filename(f)
        oc = other_constants_from_filename(f)
        moc_map[mass_number] = oc
    return moc_map
