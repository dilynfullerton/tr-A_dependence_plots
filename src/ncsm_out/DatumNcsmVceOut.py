from __future__ import print_function, division, unicode_literals

from Datum import Datum
from ncsm_out.State import State
from ncsm_out.parser import a_aeff_to_states_map


class DatumNcsmVceOut(Datum):
    """Stores data maps specific to a common set of NCSM out files, as
    identified by an ExpNcsmVceOut
    """
    def __init__(self, directory, exp, files):
        super(DatumNcsmVceOut, self).__init__(
            directory=directory, exp=exp, files=files
        )
        # maps
        self._a_aeff_to_states_map = dict()

        # setup methods
        self._set_maps()

    def _set_maps(self):
        self._set_a_aeff_to_states_map()

    def _set_a_aeff_to_states_map(self):
        a_aeff_to_states = a_aeff_to_states_map(filepaths=self.files)
        for k, v in a_aeff_to_states.iteritems():
            self._a_aeff_to_states_map[k] = [State(*vi) for vi in v]

    def a_aeff_to_states_map(self):
        return dict(self._a_aeff_to_states_map)

    def a_aeff_to_ground_state_map(self):
        return {k: v[0] for k, v in self._a_aeff_to_states_map.iteritems()}

    def a_eff_to_ground_state_energy_map(self):
        return {k: v.E for k, v in self.a_aeff_to_ground_state_map()}

    def a_to_aeff_to_states_map(self):
        a_to_aeff_to_states = dict()
        for k, v in self._a_aeff_to_states_map.iteritems():
            a, aeff = k
            if a not in a_to_aeff_to_states:
                a_to_aeff_to_states[a] = {a: {aeff: v}}
            else:
                a_to_aeff_to_states[a][aeff] = v
        return a_to_aeff_to_states

    def aeff_to_a_to_states_map(self):
        aeff_to_a_to_states = dict()
        for k, v in self._a_aeff_to_states_map.iteritems():
            a, aeff = k
            if aeff not in aeff_to_a_to_states:
                aeff_to_a_to_states[aeff] = {aeff: {a: v}}
            else:
                aeff_to_a_to_states[aeff][a] = v
        return aeff_to_a_to_states

    def aeff_exact_to_states_map(self):
        aeff_exact_to_states = dict()
        for k, v in self._a_aeff_to_states_map.iteritems():
            if k[0] != k[1]:
                continue
            else:
                aeff_exact_to_states[k[0]] = v
        return aeff_exact_to_states

    def aeff_exact_to_ground_state_map(self):
        return {k: v[0] for k, v in
                self.aeff_exact_to_states_map().iteritems()}

    def aeff_exact_to_ground_state_energy_map(self):
        return {k: v.E for k, v in
                self.aeff_exact_to_ground_state_map().iteritems()}
