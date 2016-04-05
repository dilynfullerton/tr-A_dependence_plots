"""These definitions hold key-value maps to store data of different types.

For example, ImsrgDataMapInt stores a mapping from ExpInt to ImsrgDatumInt,
the data-type that stores data retrieved from *.int files.
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from os import path


class PathDoesNotExistException(Exception):
    pass


class DataMap(object):
    def __init__(self, parent_directory, exp_type, datum_type,
                 exp_list=None, exp_filter_fn=None, **kwargs):
        if path.exists(parent_directory):
            self.parent_dir = parent_directory
        else:
            raise PathDoesNotExistException(
                '\nDirectory not found: {}'.format(parent_directory))
        if exp_list is not None:
            self.exp_list = [exp_type(*exp_item) for exp_item in exp_list]
        else:
            self.exp_list = None
        self.exp_filter_fn = exp_filter_fn
        self.exp_type = exp_type
        self.datum_type = datum_type
        self.kwargs = kwargs
        self.map = dict()
        self._set_maps()

    def __getitem__(self, item):
        if not isinstance(item, self.exp_type):  # assume item is a tuple
            item = self.exp_type(*item)
        return self.map[item]

    def _set_maps(self):
        files = self._get_files()
        for f in files:
            key = self.exp_type(*self._exp_from_file_path(f))
            if self.exp_list is not None and key not in self.exp_list:
                continue
            elif self.exp_filter_fn is not None and not self.exp_filter_fn(key):
                continue
            elif key not in self.map:
                key_files = list(
                    filter(lambda ff: key == self._exp_from_file_path(ff),
                           files)
                )
                value = self.datum_type(
                    directory=self.parent_dir, exp=key, files=key_files,
                    **self.kwargs
                )
                self.map[key] = value

    def _exp_from_file_path(self, f):
        raise NotImplemented()

    def _get_files(self):
        raise NotImplemented()
