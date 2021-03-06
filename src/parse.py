"""parse.py
Abstracted file parsing functions
"""

from __future__ import division, print_function
from re import match
from os import walk, path


def sub_directories(parent_dir):
    """Returns a list of all subdirectories of parent_dir
    """
    root, dirs, files = next(walk(parent_dir))
    return [path.join(root, sd) for sd in dirs]


def get_files(directory, filterfn=lambda x: True):
    """Get all the files that are direct children to the given directory and
    match the given filter function
    :param directory: the directory whose immediate children are to be returned
    :param filterfn: the function with which to filter files
    :return: a list of all of the file paths of the files that are direct
    children to the given directory and match the filter function
    """
    root, dirs, files = next(walk(directory))
    filepaths_list = [path.join(root, f) for f in files]
    return list(filter(filterfn, filepaths_list))


def get_files_r(directory, filterfn=lambda x: True):
    """Recursively yield all of the files that children (direct or indirect)
    to the given directory and match the given filter function
    :param directory: the directory whose children are to be returned
    :param filterfn: the filter function with which to filter the children
    :return: a generator of all of the file paths of the files that are children
    to the given directory and match the filter function
    """
    w = walk(directory)
    for root, dirs, files in w:
        for fpath in [path.join(root, f) for f in files]:
            if filterfn(fpath):
                yield fpath


# todo: does this really need to be its own function?
def has_extension(fname, ext):
    """Determine whether a file has the given extension
    :return true if the file has ext; false otherwise
    """
    return ext == _get_extension(fname)


# todo: does this really need to be its own function?
def _get_extension(fname):
    """Given a filename, if it has an extension (a period followed by other
    characters), return the extension. Else, return None
    """
    idx = fname.rfind('.')
    return fname[idx:] if idx != -1 else None


def filename_elts_list(filename, split_char, remove_ext=True):
    """Get a list of the elements in the filename where name elements are
    separated by split_char
    :param filename: Name of the file or directory to split
    :param split_char: Character by which to split the string
    :param remove_ext: if true, removes everything following the final '.'
    """
    ext_index = filename.rfind('.')
    dir_index = filename.rfind('/')
    if dir_index != -1 and ext_index != -1 and remove_ext:
        filename_woext = filename[dir_index + 1:ext_index]
    elif ext_index != -1 and remove_ext:
        filename_woext = filename[:ext_index]
    elif dir_index != -1:
        filename_woext = filename[dir_index + 1:]
    else:
        filename_woext = filename
    return filename_woext.split(split_char)


def matches_completely(regex, string):
    """Returns true if the regex matches the string completely,
    false otherwise
    :param regex: Regular expression pattern to match
    :param string: String to test
    """
    m = match(pattern=regex, string=string)
    if m is not None and m.group(0) == string:
        return True
    else:
        return False


def elt_from_felts(felts, elt_regex):
    """Given a list of filename "elements" and a regular expression, returns
    the first element that completely matches the regular expression. If no
    element matches, returns None.
    :param felts: list of filename elements (strings)
    :param elt_regex: regular expression that matches the desired element
    """
    for elt in felts:
        if matches_completely(regex=elt_regex, string=elt):
            return elt
    else:
        return None


def content_lines(filepath, comment_str):
    """Generator that yields lines that are not comments
    :param filepath: path to the file
    :param comment_str: string signifying a commented line
    """
    with open(filepath, 'r') as lines:
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            if line.find(comment_str) == 0:
                continue
            else:
                yield line


def comment_lines(filepath, comment_str):
    """Generator that yields lines that are comments
    :param filepath: path to the file
    :param comment_str: string signifying a commentd line
    """
    with open(filepath, 'r') as lines:
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            if line.find(comment_str) != 0:
                continue
            else:
                line = line.strip(comment_str).strip()
                if line == '':
                    continue
                else:
                    yield line


def index_of_line(lines, line_regex):
    """Returns the index of the first line in lines that completely matches
    the given regular expression
    :param lines: iterable sequence of lines
    :param line_regex: regular expression that completely matches the desired
    line
    :return: (index, line) for the first matching line. If no match is found,
    returns None.
    """
    for line, index in zip(lines, range(len(lines))):
        if matches_completely(regex=line_regex, string=line):
            return index, line
    else:
        return None


def fraction_str_to_float(string):
    """Converts a fraction string into a float.
    Example:
    > fraction_str_to_float('1/2')
    0.5
    :param string: string of digits, containing a single '/', which
    represents a valid fraction
    :return: decimal representation of the fraction
    """
    if '/' in string:
        a, b = string.split('/')
        return float(a) / float(b)
    else:
        return float(string)


def half_int_float_to_str(f):
    """Given the decimal representation of a half-integer or integer, returns
    the string fraction representation.
    Example:
    > half_int_float_to_str(1.5)
    '3/2'
    """
    if int(f) - f == 0:
        return str(int(f))
    else:
        return str(int(2 * f)) + '/2'
