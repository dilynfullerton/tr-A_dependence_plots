from __future__ import print_function, division, unicode_literals

from Datum import Datum

from nushellx_lpt.Shell import Shell
from nushellx_lpt.parser import mass_to_header_data_map as mhd_map
from nushellx_lpt.parser import mass_to_n_to_body_data_map as mnbd_map
from nushellx_lpt.parser import mass_to_zbt_map as mass_zbt_map


class GroundStateEnergyNotFoundException(Exception):
    pass


class DatumLpt(Datum):
    """Stores data maps from *.lpt files and methods for generating new maps
    from these.
    """
    def __init__(self, directory, exp, files):
        super(DatumLpt, self).__init__(
            directory=directory, exp=exp, files=files)
        self._mass_header_map = None
        self._mass_n_body_map = None
        self._mass_zbt_map = None

        self._set_maps()

    def _set_maps(self):
        self._set_mass_header_map()
        self._set_mass_n_body_map()
        self._set_mass_zbt_map()

    def _set_mass_header_map(self):
        try:
            self._mass_header_map = mhd_map(self.files)
        except ValueError:
            self._mass_header_map = None

    def _set_mass_n_body_map(self):
        mass_n_body_map = mnbd_map(self.files)
        d = dict()
        for m, nb_map in mass_n_body_map.items():
            if m not in d and len(nb_map) > 0:
                d[m] = dict()
            for n, b in nb_map.items():
                d[m][n] = Shell(*b)
        self._mass_n_body_map = d

    def _set_mass_zbt_map(self):
        self._mass_zbt_map = mass_zbt_map(filtered_filepaths_lpt=self.files)

    def mass_header_map(self):
        if self._mass_header_map is not None:
            return dict(self._mass_header_map)
        else:
            return None

    def mass_n_exstate_map(self):
        return dict(self._mass_n_body_map)

    def mass_zbt_map(self):
        return dict(self._mass_zbt_map)

    def mass_n_energy_map(self):
        d = dict()
        for m, nb_map in self._mass_n_body_map.items():
            d[m] = {n: b.E for n, b in nb_map.items()}
        return d

    def mass_lowest_ex_energy_map(self):
        return {k: v[1] for k, v in self.mass_n_energy_map().items()}

    def mass_ground_ex_energy_map(self):
        m = dict()
        for mass, n_to_ex_state_map in self.mass_n_exstate_map().items():
            j0 = 0.0 if mass % 2 == 0 else 1.5  # todo is always true?
            for n, ex in sorted(n_to_ex_state_map.items(), key=lambda i: i[0]):
                if ex.J == j0:
                    m[mass] = ex.E
                    break
            else:
                print(repr(ex.J))
                raise GroundStateEnergyNotFoundException(
                    '\nGround state energy for A={} could not be found in {}'
                    ''.format(mass, self.files))
        return m

    def mass_ground_energy_map(self):
        mzbt = self.mass_zbt_map()
        # me0 = self.mass_lowest_ex_energy_map()
        me0 = self.mass_ground_ex_energy_map()  # todo is this right?
        mg = dict()
        for k in mzbt:
            if k in me0:
                mg[k] = mzbt[k] + me0[k]
        return mg

    def mass_n_excitation_map(self):
        d = dict()
        for m, nb_map in self._mass_n_body_map.items():
            d[m] = {n: b.Ex for n, b in nb_map.items()}
        return d

    def n_mass_energy_map(self):
        d = dict()
        mne_map = self.mass_n_energy_map()
        for m, ne_map in mne_map.items():
            for n, e in ne_map.items():
                if n not in d:
                    d[n] = dict()
                d[n][m] = e
        return d

    def n_mass_excitation_map(self):
        d = dict()
        mnext_map = self.mass_n_excitation_map()
        for m, n_ext_map in mnext_map.items():
            for n, ext in n_ext_map.items():
                if n not in d:
                    d[n] = dict()
                d[n][m] = ext
        return d
