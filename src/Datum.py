"""These definitions store data from particular file types of IMSRG data

For example, ImsrgDatumInt stores a bunch of maps generated based on *.int
files.
"""
from __future__ import division, print_function, unicode_literals


class Datum(object):
    def __init__(self, directory, exp, files):
        self.exp = exp
        self.dir = directory
        self.files = files

    def _set_maps(self):
        raise NotImplemented()
