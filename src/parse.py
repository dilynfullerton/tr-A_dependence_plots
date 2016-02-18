"""Abstracted file parsing functions
"""

from re import match
from os import walk, path


def sub_directories(parent_dir):
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
    """Recursively get all of the files that children (direct or indirect) to
    the given directory and match the given filter function

    :param directory: the directory whose children are to be returned
    :param filterfn: the filter function with which to filter the children
    :return: a list of all of the file paths of the files that are children
    to the given directory and match the filter function
    """
    w = walk(directory)
    filepaths_list = list()
    for root, dirs, files in w:
        filepaths_list.extend([path.join(root, f) for f in files])
    return list(filter(filterfn, filepaths_list))


def has_extension(fname, ext):
    return ext == _get_extension(fname)


def _get_extension(fname):
    return fname[fname.rfind('.'):]


def filename_elts_list(filename, split_char):
    """Get a list of the elements in the filename where name elements are
    separated by split_char
    :param split_char:
    :param filename:
    """
    ext_index = filename.rfind('.')
    dir_index = filename.rfind('/')
    if dir_index != -1:
        filename_woext = filename[dir_index:ext_index]
    else:
        filename_woext = filename[:ext_index]
    return filename_woext.split(split_char)


def elt_from_felts(felts, elt_regex):
    for elt in felts:
        m = match(elt_regex, elt)
        if m is not None and m.group(0) == elt:
            return elt
    else:
        return None


def _get_lines(filename):
    """Returns all of the lines read from the given file in a list (with
    line separators and blank lines removed
    """
    with open(filename) as f:
        lines = f.readlines()
    # Remove line separators
    lines = map(lambda x: x.strip(), lines)
    # Remove blank lines
    lines = filter(lambda x: len(x) > 0, lines)
    return list(lines)


def content_lines(filename, comment_char):
    """Returns a list of all of the lines that are not comments
    :param comment_char:
    :param filename:
    """
    lines = _get_lines(filename)
    return list(filter(lambda x: x[0] is not comment_char, lines))


def comment_lines(filename, comment_char):
    """Returns all of the lines read from the given filename that are
    descriptive comments
    :param comment_char:
    :param filename:
    """
    lines = _get_lines(filename)
    lines = filter(lambda x: x[0] is comment_char, lines)
    lines = map(lambda x: x.strip(comment_char).strip(), lines)
    lines = filter(lambda x: x is not '', lines)
    return list(lines)


def index_of_line(lines, line_regex):
    for line, index in zip(lines, range(len(lines))):
        m = match(line_regex, line)
        if m is not None and m.group(0) == line:
            return index, line
    else:
        return None


def half_int_str_to_float(string):
    if '/' in string:
        return reduce(lambda a, b: int(a)/int(b), string.split('/'))
    else:
        return int(string)


def half_int_float_to_str(f):
    if int(f) - f == 0:
        return str(int(f))
    else:
        return str(int(2 * f)) + '/2'
