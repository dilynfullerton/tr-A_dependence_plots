"""parse_files.py
Functions to parse files of certain types in given directories
"""
from __future__ import division, print_function, unicode_literals
from os import walk, path
from re import match, compile
from Parser import ItemNotFoundInFileException
from NcsdOut import NcsdOut
from NushellxInt import NushellxInt
from NushellxLpt import NushellxLpt


def _parse_files_in_dir(dirpath, fname_regex, parser):
    parsed_files = list()
    for root, dnames, fnames in walk(dirpath):
        for fname in fnames:
            if match(fname_regex, fname):
                try:
                    parsed_files.append(parser(path.join(root, fname)))
                except ItemNotFoundInFileException:
                    continue
    return parsed_files


def parse_ncsd_out_files(dirpath):
    return _parse_files_in_dir(
        dirpath=dirpath, fname_regex=compile('.*\.out'), parser=NcsdOut)


def parse_nushellx_int_files(dirpath):
    return _parse_files_in_dir(
        dirpath=dirpath, fname_regex=compile('.*\.int'), parser=NushellxInt)


def parse_nushellx_lpt_files(dirpath):
    return _parse_files_in_dir(
        dirpath=dirpath, fname_regex=compile('.*y\.lpt'), parser=NushellxLpt)
