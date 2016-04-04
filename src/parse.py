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
    :param filename: Name of the file or directory to split
    :param split_char: Character by which to split the string
    """
    ext_index = filename.rfind('.')
    dir_index = filename.rfind('/')
    if dir_index != -1 and ext_index != -1:
        filename_woext = filename[dir_index+1:ext_index]
    elif ext_index != -1:
        filename_woext = filename[:ext_index]
    elif dir_index != -1:
        filename_woext = filename[dir_index+1:]
    else:
        filename_woext = filename
    return filename_woext.split(split_char)


def elt_from_felts(felts, elt_regex):
    for elt in felts:
        if matches_completely(regex=elt_regex, string=elt):
            return elt
    else:
        return None


def _get_lines(filepath):
    """Same as _get_lines, except returns a generator object
    :param filepath: path to the file
    """
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) > 0:
                yield line
            else:
                continue


def content_lines(filepath, comment_str):
    """Generator that yields lines that are not comments
    :param filepath: path to the file
    :param comment_str: string signifying a commented line
    """
    lines = _get_lines(filepath)
    for line in lines:
        if line.find(comment_str) == 0:
            continue
        else:
            yield line


def comment_lines(filepath, comment_str):
    """Generator that yields lines that are comments
    :param filepath: path to the file
    :param comment_str: string signifying a commentd line
    """
    lines = _get_lines(filepath)
    for line in lines:
        if line.find(comment_str) != 0:
            continue
        else:
            line = line.strip(comment_str).strip()
            if line == '':
                continue
            else:
                yield line


def index_of_line(lines, line_regex):
    for line, index in zip(lines, range(len(lines))):
        if matches_completely(regex=line_regex, string=line):
            return index, line
    else:
        return None


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


def half_int_str_to_float(string):
    if '/' in string:
        a, b = string.split('/')
        return int(a) / int(b)
    else:
        return int(string)


def half_int_float_to_str(f):
    if int(f) - f == 0:
        return str(int(f))
    else:
        return str(int(2 * f)) + '/2'
