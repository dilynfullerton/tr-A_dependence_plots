"""Parser.py
General class for parsing text files
"""
from __future__ import print_function, division, unicode_literals
from re import match
from os import path


class ItemNotFoundInFileException(Exception):
    pass


class Parser(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self._get_data()

    def __repr__(self):
        return (super(Parser, self).__repr__() + ' at ' +
                path.relpath(self.filepath))

    def _lines(self):
        with open(self.filepath) as f:
            for line in f:
                yield line

    def _get_data(self):
        """Update constants with file information
        """
        raise NotImplementedError()

    def _get_data_line_fn(self, line_regex, match_fn, data_name):
        for line in self._lines():
            if match(line_regex, line):
                match_fn(line)
                break
        else:
            raise ItemNotFoundInFileException(
                'Did not find {} in {}'.format(data_name, self.filepath))

    def _get_data_lines_fn(self, line_regex, match_fn, data_name):
        matched = False
        for line in self._lines():
            if match(line_regex, line):
                match_fn(line)
                matched = True
        if not matched:
            raise ItemNotFoundInFileException(
                'Did not find {} in {}'.format(data_name, self.filepath))
