"""DatumLpt.py
Main file to store data from a *.lpt file. (see Datum.py)
"""
from __future__ import print_function, division, unicode_literals

from Datum import Datum
from nushellx_lpt.ExState import ExState
from nushellx_lpt.parser import mass_to_spe_line_data_map as mhd_map
from nushellx_lpt.parser import mass_to_n_to_state_data_map as mnbd_map
from nushellx_lpt.parser import mass_to_zbt_map as mass_zbt_map
from ncsm_out.DatumNcsmOut import get_ground_state_j


class GroundStateEnergyNotFoundException(Exception):
    pass


class DatumLpt(Datum):
    """Stores data maps from *.lpt files and methods for generating new maps
    from these.
    """
    def __init__(self, directory, exp, files):
        """Initializes the Datum. Typically this would be handled by the
        DataMap (e.g. DataMapNushellxLpt), so the user generally need
        not concern their self with this.
        :param directory: directory in which to initialize the datum
        :param exp: exp for the datum, which uniquely matches to its data
        :param files: list of relevant file paths to be parsed into the datum
        """
        super(DatumLpt, self).__init__(
            directory=directory, exp=exp, files=files)
        self._mass_to_spe_line_map = None
        self._mass_to_ex_states_map = None
        self._mass_to_zbt_map = None
        self._set_maps()

    def _set_maps(self):
        self._set_mass_to_spe_line_map()
        self._set_mass_to_ex_states_map()
        self._set_mass_to_zbt_map()

    def _set_mass_to_spe_line_map(self):
        try:
            self._mass_to_spe_line_map = mhd_map(self.files)
        except ValueError:
            self._mass_to_spe_line_map = None

    def _set_mass_to_ex_states_map(self):
        mass_n_body_map = mnbd_map(self.files)
        d = dict()
        for m, nb_map in mass_n_body_map.items():
            ex_states = list()
            for n, b in nb_map.items():
                ex_states.append(ExState(n, *b))
            d[m] = ex_states
        self._mass_to_ex_states_map = d

    def _set_mass_to_zbt_map(self):
        self._mass_to_zbt_map = mass_zbt_map(fpath_list=self.files)

    def mass_to_spe_line_map(self):
        """Returns a map
            A -> spe list,
        where the header list is the ordered list of items in the SPE line
        BEGINNING with the first SPE. (The initial 999. is not included)
        """
        if self._mass_to_spe_line_map is not None:
            return dict(self._mass_to_spe_line_map)
        else:
            return None

    def mass_to_ex_states_map(self):
        """Returns a map
            A -> N -> Excited state,
        where A is the mass number, N is the index for the state (beginning at
        one), and the object representing the state is that defined in
        nushellx_lpe/ExState.py
        """
        return dict(self._mass_to_ex_states_map)

    def mass_to_zbt_map(self):
        """Returns a map
            A -> zero body term
        """
        return dict(self._mass_to_zbt_map)

    def mass_to_n_to_ex_energy_map(self):
        """Returns a map
            A -> N -> energy
        This is similar to self.mass_n_exstate_map(), but instead of
        the whole state, the map's value is only the energy
        """
        d = dict()
        for m, ex_states in self._mass_to_ex_states_map.items():
            d[m] = {ex.N: ex.E for ex in ex_states}
        return d

    def mass_to_lowest_ex_energy_map(self):
        """Returns a map
            A -> energy,
        where energy is that associated with index 1.
        """
        return {k: v[1] for k, v in self.mass_to_n_to_ex_energy_map().items()}

    def mass_to_ground_ex_energy_map(self, nshell):
        """Given the shell, returns a map
            A -> ground energy
        Where ground energy is taken to be the first energy with the
        correct angular momentum as defined by get_ground_state_j().
        :param nshell: 0=s, 1=p, 2=sd,...
        """
        m = dict()
        for mass, ex_states in self.mass_to_ex_states_map().items():
            j0 = get_ground_state_j(mass=mass, nshell=nshell)
            for ex in sorted(ex_states):
                if j0 is None:
                    print(
                        'Ground state angular momentum not known for '
                        'A={}, nshell={}.\n'
                        'Using state with lowest energy.'.format(mass, nshell)
                    )
                    m[mass] = ex.E
                    break
                elif ex.J == j0:
                    m[mass] = ex.E
                    break
            else:
                files_str = '\n    '.join(self.files)
                message = (
                    'Ground state energy for A={} could not be found in \n'
                    '    {}'
                ).format(mass, files_str)
                raise GroundStateEnergyNotFoundException(message)
        return m

    def mass_to_ground_energy_map(self, nshell):
        """Returns a map
            A -> ground energy,
        where ground energy is that in mass_ground_ex_energy_map() plus the
        zero body term from mass_zbt_map()
        :param nshell: 0=s, 1=p, 2=sd, ...
        """
        mzbt = self.mass_to_zbt_map()
        # me0 = self.mass_lowest_ex_energy_map()
        me0 = self.mass_to_ground_ex_energy_map(nshell=nshell)
        mg = dict()
        for k in mzbt:
            if k in me0:
                mg[k] = mzbt[k] + me0[k]
        return mg

    def n_to_mass_to_ex_energy_map(self):
        """Returns a map
            N -> A -> energy
        This is essentially the same as the map returned by
        self.mass_n_energy_map(), only n and mass are switched, such that
        n is specified first, then mass
        """
        d = dict()
        mne_map = self.mass_to_n_to_ex_energy_map()
        for m, ne_map in mne_map.items():
            for n, e in ne_map.items():
                if n not in d:
                    d[n] = dict()
                d[n][m] = e
        return d

    def n_to_mass_to_energy_map(self):
        n_to_mass_to_energy_map = dict()
        for n, mass_to_ex_energy in self.n_to_mass_to_ex_energy_map().items():
            for mass, ex_energy in mass_to_ex_energy.items():
                if n not in n_to_mass_to_energy_map:
                    n_to_mass_to_energy_map[n] = dict()
                zbt = self._mass_to_zbt_map[mass]
                n_to_mass_to_energy_map[n][mass] = ex_energy + zbt
        return n_to_mass_to_energy_map

    def n_to_mass_to_j_energy_map(self):
        n_to_mass_to_j_energy_map = dict()
        for a, ex_states in self.mass_to_ex_states_map().items():
            zbt = self._mass_to_zbt_map[a]
            for ex in ex_states:
                n, j, e = ex.N, ex.J, ex.E
                if n not in n_to_mass_to_j_energy_map:
                    n_to_mass_to_j_energy_map[n] = dict()
                n_to_mass_to_j_energy_map[n][a] = (j, e + zbt)
        return n_to_mass_to_j_energy_map

