from __future__ import division
from __future__ import print_function

from ImsrgDatum import ImsrgDatum
from Shell import Shell
from parse_lpt import mass_to_header_data_map, mass_to_n_to_body_data_map

from constants import F_PARSE_LPT_CMNT_CHAR as CMNT_CHAR
from constants import F_PARSE_LPT_ROW_AZ as ROW_AZ
from constants import F_PARSE_LPT_ROW_HEAD as ROW_HEAD
from constants import F_PARSE_LPT_COL_HEAD_DATA_START as COL_START
from constants import F_PARSE_LPT_ROW_START_DATA as ROW_BODY_START
from constants import F_PARSE_LPT_NCOLS_BODY as NCOLS_BODY


class ImsrgDatumLpt(ImsrgDatum):
    def __init__(self, directory, exp, files,
                 _comment_char=CMNT_CHAR,
                 _row_az=ROW_AZ,
                 _row_head=ROW_HEAD,
                 _col_start=COL_START,
                 _row_body_start=ROW_BODY_START,
                 _ncols_body=NCOLS_BODY):
        super(ImsrgDatumLpt, self).__init__(directory=directory, exp=exp,
                                            files=files)
        self._comment_char = _comment_char
        self._row_az = _row_az
        self._row_head = _row_head
        self._col_start = _col_start
        self._row_body_start = _row_body_start
        self._ncols_body = _ncols_body

        self._mass_header_map = None
        self._mass_n_body_map = None

        self._set_maps()

    def _set_maps(self):
        self._set_mass_header_map()
        self._set_mass_n_body_map()

    def _set_mass_header_map(self):
        self._mass_header_map = mass_to_header_data_map(
            self.files, comment_char=self._comment_char,
            row_az=self._row_az,
            row_head=self._row_head,
            col_start=self._col_start)

    def _set_mass_n_body_map(self):
        mass_n_body_map = mass_to_n_to_body_data_map(
            self.files, comment_char=self._comment_char,
            row_az=self._row_az,
            row_body_start=self._row_body_start,
            ncols_body=self._ncols_body)
        d = dict()
        for m, nb_map in mass_n_body_map.iteritems():
            if m not in d:
                d[m] = dict()
            for n, b in nb_map.iteritems():
                d[m][n] = Shell(*b)
        self._mass_n_body_map = d

    def mass_header_map(self):
        return dict(self._mass_header_map)

    def mass_n_body_map(self):
        return dict(self._mass_n_body_map)

    def mass_n_energy_map(self):
        d = dict()
        for m, nb_map in self._mass_n_body_map.iteritems():
            d[m] = {n: b.E for n, b in nb_map.iteritems()}
        return d

    def mass_n_excitation_map(self):
        d = dict()
        for m, nb_map in self._mass_n_body_map.iteritems():
            d[m] = {n: b.Ext for n, b in nb_map.iteritems()}
        return d

    def n_mass_energy_map(self):
        d = dict()
        mne_map = self.mass_n_energy_map()
        for m, ne_map in mne_map.iteritems():
            for n, e in ne_map.iteritems():
                if n not in d:
                    d[n] = dict()
                d[n][m] = e
        return d

    def n_mass_excitation_map(self):
        d = dict()
        mnext_map = self.mass_n_excitation_map()
        for m, n_ext_map in mnext_map.iteritems():
            for n, ext in n_ext_map.iteritems():
                if n not in d:
                    d[n] = dict()
                d[n][m] = ext
        return d
