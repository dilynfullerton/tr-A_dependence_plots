"""Functions for parsing *.op data files and generating maps from the data
"""
from __future__ import print_function, division


from parse import elt_from_felts, filename_elts_list, index_of_line


# EXP
def exp_from_filepath(filepath, split_char,
                      regex_name, regex_hw):
    felts = filename_elts_list(filename=filepath, split_char=split_char)
    name = elt_from_felts(felts=felts, elt_regex=regex_name)
    hw = int(elt_from_felts(felts=felts, elt_regex=regex_hw)[2:])
    return name, hw


# DATA
def _ordered_lines(content_lines, regex_h, regex_0bt, regex_1bt, regex_2bt):
    """Returns the string representations of the header lines (list of str),
    zero body line (str), one body lines (list of str), two body lines
    (list of str)
    :param content_lines: op file lines not including comments
    :param regex_h: regular expression to fully match the first header line
    :param regex_0bt: regular expression to fully match the zero body line
    :param regex_1bt: regular expression to fully match the header beginning the
    one body lines
    :param regex_2bt: regular expression to fully match the header beginning
    the two body lines
    :return: a 4-tuple containing the header lines, the zero body line, the
    one body lines, and the two body lines
    """
    idx_h, h_line_nm = index_of_line(content_lines, line_regex=regex_h)
    idx_0bt, line_0bt = index_of_line(content_lines, line_regex=regex_0bt)
    idx_1bt = index_of_line(content_lines, line_regex=regex_1bt)[0]
    idx_2bt = index_of_line(content_lines, line_regex=regex_2bt)[0]
    h_line = content_lines[idx_h + 1]
    lines_1bt = content_lines[idx_1bt + 1:idx_2bt]
    lines_2bt = content_lines[idx_2bt + 1:]
    return [h_line_nm, h_line], line_0bt, lines_1bt, lines_2bt


def _ordered_lists(ordered_lines):
    """Given a 4-tuple of ordered *.op file lines, returns a 4-tuple of those
    lines, where each line is converted to a list of elements where appropriate
    """
    h_lines, line_0bt, lines_1bt, lines_2bt = ordered_lines
    h_lists = h_lines[0], h_lines[1].split()
    zbt = line_0bt.split()[1]
    lists_1bt = [line.split() for line in lines_1bt]
    lists_2bt = [line.split() for line in lines_2bt]
    return h_lists, zbt, lists_1bt, lists_2bt


def _ordered_lists_cured(ordered_lists):
    """Given a 4-tuple of lists of *.op file data, cures the elements of each
    line (list) by converting to integers, floats, etc, where appropriate
    based on the file format:

    (string) [HEADER]
    (float) (float) (float)
    (string) (float) [ZERO BODY]
    (string) [ONE BODY HEADER]
    (int) (int) (float) [ONE BODY DATA]
    ...
    (string) [TWO BODY HEADER]
    (int) * 10 (float)
    ...
    """
    h_lists, zbt, lists_1bt, lists_2bt = ordered_lists
    h_lists_cured = h_lists[0], [float(x) for x in h_lists[1]]
    zbt_cured = float(zbt)
    lists_1bt_cured = list()
    for lox in lists_1bt:
        lists_1bt_cured.append([int(lox[0]), int(lox[1]), float(lox[2])])
    lists_2bt_cured = list()
    for lox in lists_2bt:
        lists_2bt_cured.append([int(x) for x in lox[:10]] + [float(lox[10])])
    return h_lists_cured, zbt_cured, lists_2bt_cured, lists_2bt_cured
