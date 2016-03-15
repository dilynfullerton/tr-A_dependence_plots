from __future__ import print_function, division, unicode_literals

from Datum import Datum

from nushellx_lpt.Shell import Shell
from nushellx_lpt.parser import mass_to_header_data_map as mhd_map
from nushellx_lpt.parser import mass_to_n_to_body_data_map as mnbd_map
from nushellx_lpt.parser import mass_to_zbt_map as mass_zbt_map


class DatumLpt(Datum):
    """Stores data maps from *.lpt files and methods for generating new maps
    from these.
    """
    def __init__(self, directory, exp, files):
        super(DatumLpt, self).__init__(directory=directory, exp=exp,
                                       files=files)
        self._mass_header_map = None
        self._mass_n_body_map = None
        self._mass_zbt_map = None

        self._set_maps()

    def _set_maps(self):
        self._set_mass_header_map()
        self._set_mass_n_body_map()
        self._set_mass_zbt_map()

    def _set_mass_header_map(self):
        self._mass_header_map = mhd_map(self.files)

    def _set_mass_n_body_map(self):
        mass_n_body_map = mnbd_map(self.files)
        d = dict()
        for m, nb_map in mass_n_body_map.iteritems():
            if m not in d:
                d[m] = dict()
            for n, b in nb_map.iteritems():
                d[m][n] = Shell(*b)
        self._mass_n_body_map = d

    def _set_mass_zbt_map(self):
        self._mass_zbt_map = mass_zbt_map(filtered_filepaths_lpt=self.files)

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

    def mass_lowest_energy_map(self):
        return {k: v[1] for k, v in self.mass_n_energy_map().iteritems()}

    def mass_n_excitation_map(self):
        d = dict()
        for m, nb_map in self._mass_n_body_map.iteritems():
            d[m] = {n: b.Ex for n, b in nb_map.iteritems()}
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
