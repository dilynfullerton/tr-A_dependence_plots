from __future__ import print_function, division, unicode_literals

from Datum import Datum
from ncsm_out.State import State
from ncsm_out.parser import a_aeff_nhw_to_states_map

MSG1 = (
    '\nInsufficient keyword arguments to evaluate {}.'
    '\nPlease supply either a0 or (nshell and ncomponent) as keyword arguments.'
)

MSG2 = (
    '\nInsufficient keyword arguments to evaluate {}.'
    '\nEither nhw or nmax must be supplied as a keyword argument.'
)


def _get_a0(nshell, ncomponent):
    return int((nshell+2) * (nshell+1) * nshell/3 * ncomponent)


class IncompleteArgumentsException(Exception):
    pass


class DatumNcsmVceOut(Datum):
    """Stores data maps specific to a common set of NCSM out files, as
    identified by an ExpNcsmVceOut
    """
    def __init__(self, directory, exp, files):
        super(DatumNcsmVceOut, self).__init__(
            directory=directory, exp=exp, files=files
        )
        # maps
        self._a_aeff_nhw_to_states_map = dict()

        # setup methods
        self._set_maps()

    def _set_maps(self):
        self._set_a_aeff_nhw_to_states_map()

    def _set_a_aeff_nhw_to_states_map(self):
        a_aeff_nhw_to_states = a_aeff_nhw_to_states_map(filepaths=self.files)
        for k, v in sorted(a_aeff_nhw_to_states.items()):
            if len(v) > 0:
                self._a_aeff_nhw_to_states_map[k] = [State(*vi) for vi in v]

    def a_aeff_nmax_to_states_map(self, a0):
        a_aeff_nmax_to_states = dict()
        for k, v in self._a_aeff_nhw_to_states_map.items():
            a, aeff, nhw = k
            nmax = nhw - (a - a0)
            a_aeff_nmax_to_states[(a, aeff, nmax)] = v
        return a_aeff_nmax_to_states

    # maps for a given Nhw
    def _a_aeff_to_states_map_for_nhw(self, nhw):
        a_aeff_to_states = dict()
        for k, v in self._a_aeff_nhw_to_states_map.items():
            a0, aeff0, nhw0 = k
            if nhw0 != nhw:
                continue
            else:
                a_aeff_to_states[(a0, aeff0)] = v
        return a_aeff_to_states

    def _a_aeff_to_ground_state_map_for_nhw(self, nhw):
        return {k: v[0] for k, v in
                self._a_aeff_to_states_map_for_nhw(nhw).items()}

    def _aeff_exact_to_states_map_for_nhw(self, nhw):
        aeff_exact_to_states = dict()
        for k, v in self._a_aeff_to_states_map_for_nhw(nhw).items():
            if k[0] != k[1]:
                continue
            else:
                aeff_exact_to_states[k[0]] = v
        return aeff_exact_to_states

    def _aeff_exact_to_ground_state_map_for_nhw(self, nhw):
        return {k: v[0] for k, v in
                self._aeff_exact_to_states_map_for_nhw(nhw).items()}

    def _aeff_exact_to_ground_state_energy_map_for_nhw(self, nhw):
        return {k: v.E for k, v in
                self._aeff_exact_to_ground_state_map_for_nhw(nhw).items()}

    # maps for maximal Nhw
    def a_aeff_to_states_map_for_max_nhw(self):
        a_aeff_to_states = dict()
        a_aeff_to_nhw = dict()
        for k, v in self._a_aeff_nhw_to_states_map.items():
            a, aeff, nhw = k
            if (a, aeff) not in a_aeff_to_nhw or nhw > a_aeff_to_nhw[(a, aeff)]:
                a_aeff_to_nhw[(a, aeff)] = nhw
                a_aeff_to_states[(a, aeff)] = v
        return a_aeff_to_states

    def aeff_exact_to_states_map_for_max_nhw(self):
        aeff_exact_to_states = dict()
        for k, v in self.a_aeff_to_states_map_for_max_nhw().items():
            if k[0] != k[1]:
                continue
            else:
                aeff_exact_to_states[k[0]] = v
        return aeff_exact_to_states

    def aeff_exact_to_ground_state_map_for_max_nhw(self):
        return {k: v[0] for k, v in
                self.aeff_exact_to_states_map_for_max_nhw().items()}

    def aeff_exact_to_ground_state_energy_map_for_max_nhw(self):
        return {k: v.E for k, v in
                self.aeff_exact_to_ground_state_map_for_max_nhw().items()}

    # maps for a given Nmax
    def _a_aeff_to_states_map_for_nmax(self, nmax, a0):
        a_aeff_to_states = dict()
        for k, v in self.a_aeff_nmax_to_states_map(a0).items():
            a_i, aeff_i, nmax_i = k
            if nmax_i != nmax:
                continue
            else:
                a_aeff_to_states[(a_i, aeff_i)] = v
        return a_aeff_to_states

    def _a_aeff_to_ground_state_map_for_nmax(self, nmax, a0):
        return {k: v[0] for k, v in
                self.a_aeff_to_states_map(nmax=nmax, a0=a0).items()}

    def _aeff_exact_to_states_map_for_nmax(self, nmax, a0):
        aeff_exact_to_states = dict()
        for k, v in self._a_aeff_to_states_map_for_nmax(
                nmax=nmax, a0=a0
        ).items():
            if k[0] != k[1]:
                continue
            else:
                aeff_exact_to_states[k[0]] = v
        return aeff_exact_to_states

    def _aeff_exact_to_ground_state_map_for_nmax(self, nmax, a0):
        return {k: v[0] for k, v in
                self._aeff_exact_to_states_map_for_nmax(
                    nmax=nmax, a0=a0
                ).items()}

    def _aeff_exact_to_ground_state_energy_map_for_nmax(self, nmax, a0):
        return {k: v.E for k, v in
                self._aeff_exact_to_ground_state_map_for_nmax(
                    nmax=nmax, a0=a0
                ).items()}

    # user maps
    def a_aeff_to_states_map(
            self, nhw=None, nmax=None, a0=None, nshell=None, ncomponent=None,
    ):
        if nhw is not None:
            return self._a_aeff_to_states_map_for_nhw(nhw=nhw)
        elif nmax is not None:
            if a0 is not None:
                return self._a_aeff_to_states_map_for_nmax(nmax=nmax, a0=a0)
            elif nshell is not None and ncomponent is not None:
                return self._a_aeff_to_states_map_for_nmax(
                    nmax=nmax, a0=_get_a0(nshell=nshell, ncomponent=ncomponent)
                )
            else:
                raise IncompleteArgumentsException(MSG1.format(
                    'a_aeff_to_states_map'
                ))
        else:
            raise IncompleteArgumentsException(MSG2.format(
                'a_aeff_to_states_map'
            ))

    def a_aeff_to_ground_state_map(
            self, nhw=None, nmax=None, a0=None, nshell=None, ncomponent=None,
    ):
        if nhw is not None:
            return self._a_aeff_to_ground_state_map_for_nhw(nhw=nhw)
        elif nmax is not None:
            if a0 is not None:
                return self._a_aeff_to_ground_state_map_for_nmax(
                    nmax=nmax, a0=a0
                )
            elif nshell is not None and ncomponent is not None:
                return self._a_aeff_to_ground_state_map_for_nmax(
                    nmax=nmax, a0=_get_a0(nshell=nshell, ncomponent=ncomponent)
                )
            else:
                raise IncompleteArgumentsException(MSG1.format(
                    'a_aeff_to_ground_state_map'
                ))
        else:
            raise IncompleteArgumentsException(MSG2.format(
                'a_aeff_to_ground_state_map'
            ))

    def aeff_exact_to_states_map(
            self, nhw=None, nmax=None, a0=None, nshell=None, ncomponent=None,
    ):
        if nhw is not None:
            return self._aeff_exact_to_states_map_for_nhw(nhw=nhw)
        elif nmax is not None:
            if a0 is not None:
                return self._aeff_exact_to_states_map_for_nmax(nmax=nmax, a0=a0)
            elif nshell is not None and ncomponent is not None:
                return self._aeff_exact_to_states_map_for_nmax(
                    nmax=nmax, a0=_get_a0(nshell=nshell, ncomponent=ncomponent)
                )
            else:
                raise IncompleteArgumentsException(MSG1.format(
                    'aeff_exact_to_states_map'
                ))
        else:
            raise IncompleteArgumentsException(MSG2.format(
                'aeff_exact_to_states_map'
            ))

    def aeff_exact_to_ground_state_map(
            self, nhw=None, nmax=None, a0=None, nshell=None, ncomponent=None,
    ):
        if nhw is not None:
            return self._aeff_exact_to_ground_state_map_for_nhw(nhw=nhw)
        elif nmax is not None:
            if a0 is not None:
                return self._aeff_exact_to_ground_state_map_for_nmax(
                    nmax=nmax, a0=a0
                )
            elif nshell is not None and ncomponent is not None:
                return self._aeff_exact_to_ground_state_map_for_nmax(
                    nmax=nmax, a0=_get_a0(nshell=nshell, ncomponent=ncomponent)
                )
            else:
                raise IncompleteArgumentsException(MSG1.format(
                    'aeff_exact_to_ground_state_map'
                ))
        else:
            raise IncompleteArgumentsException(MSG2.format(
                'aeff_exact_to_ground_state_map'
            ))

    def aeff_exact_to_ground_state_energy_map(
            self, nhw=None, nmax=None, a0=None, nshell=None, ncomponent=None,
    ):
        if nhw is not None:
            return self._aeff_exact_to_ground_state_energy_map_for_nhw(nhw=nhw)
        elif nmax is not None:
            if a0 is not None:
                return self._aeff_exact_to_ground_state_energy_map_for_nmax(
                    nmax=nmax, a0=a0
                )
            elif nshell is not None and ncomponent is not None:
                return self._aeff_exact_to_ground_state_energy_map_for_nmax(
                    nmax=nmax, a0=_get_a0(nshell=nshell, ncomponent=ncomponent)
                )
            else:
                raise IncompleteArgumentsException(MSG1.format(
                    'aeff_exact_to_ground_state_energy_map'
                ))
        else:
            raise IncompleteArgumentsException(MSG2.format(
                'aeff_exact_to_ground_state_energy_map'
            ))
