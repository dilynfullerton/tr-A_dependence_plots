from __future__ import print_function, division, unicode_literals

from ImsrgDatum import ImsrgDatum

from constants import F_PARSE_LPT_CMNT_CHAR as _CMNT_CHAR
from constants import F_PARSE_LPT_ROW_AZ as _ROW_AZ
from constants import F_PARSE_LPT_ROW_HEAD as _ROW_HEAD
from constants import F_PARSE_LPT_COL_HEAD_DATA_START as _COL_START
from constants import F_PARSE_LPT_ROW_START_DATA as _ROW_BODY_START
from constants import F_PARSE_LPT_NCOLS_BODY as _NCOLS_BODY
from constants import FN_PARSE_LPT_REGEX_FILENAME_INT as _REGEX_FILENAME_INT
from constants import F_PARSE_INT_CMNT_CHAR as _INT_CMNT_CHAR
from constants import F_PARSE_INT_CMNT_ZBT as _INT_CMNT_ZBT

from lpt.Shell import Shell
from lpt.parse_lpt import mass_to_header_data_map as mass_hd_map
from lpt.parse_lpt import mass_to_n_to_body_data_map as mass_nbd_map
from lpt.parse_lpt import mass_to_zbt_map as mass_zbt_map


class ImsrgDatumLpt(ImsrgDatum):
    """Stores data maps from *.lpt files and methods for generating new maps
    from these.
    """
    def __init__(self, directory, exp, files,
                 _comment_char_lpt=_CMNT_CHAR,
                 _row_az=_ROW_AZ,
                 _row_head=_ROW_HEAD,
                 _col_start=_COL_START,
                 _row_body_start=_ROW_BODY_START,
                 _ncols_body=_NCOLS_BODY,
                 _regex_filename_int=_REGEX_FILENAME_INT,
                 _comment_char_int=_INT_CMNT_CHAR,
                 _comment_zbt=_INT_CMNT_ZBT):
        super(ImsrgDatumLpt, self).__init__(directory=directory, exp=exp,
                                            files=files)
        self._comment_char_lpt = _comment_char_lpt
        self._row_az = _row_az
        self._row_head = _row_head
        self._col_start = _col_start
        self._row_body_start = _row_body_start
        self._ncols_body = _ncols_body
        self._regex_filename_int = _regex_filename_int
        self._comment_char_int = _comment_char_int
        self._comment_zbt = _comment_zbt

        self._mass_header_map = None
        self._mass_n_body_map = None
        self._mass_zbt_map = None

        self._set_maps()

    def _set_maps(self):
        self._set_mass_header_map()
        self._set_mass_n_body_map()
        self._set_mass_zbt_map()

    def _set_mass_header_map(self):
        self._mass_header_map = mass_hd_map(
            self.files, comment_char=self._comment_char_lpt,
            row_az=self._row_az,
            row_head=self._row_head,
            col_start=self._col_start)

    def _set_mass_n_body_map(self):
        mass_n_body_map = mass_nbd_map(
            self.files, comment_char=self._comment_char_lpt,
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

    def _set_mass_zbt_map(self):
        self._mass_zbt_map = mass_zbt_map(
            filtered_filepaths_lpt=self.files,
            filename_int_regex=self._regex_filename_int,
            row_az=self._row_az,
            comment_char_lpt=self._comment_char_lpt,
            comment_char_int=self._comment_char_int,
            zbt_comment=self._comment_zbt)

    def mass_header_map(self):
        return dict(self._mass_header_map)

    def mass_n_body_map(self):
        return dict(self._mass_n_body_map)

    def mass_zbt_map(self):
        return dict(self._mass_zbt_map)

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
