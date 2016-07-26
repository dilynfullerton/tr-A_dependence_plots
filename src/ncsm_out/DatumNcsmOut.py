"""DatumNcsmOut.py
Particular Datum for Ncsm *.out files.
"""
from __future__ import print_function, division, unicode_literals

from warnings import warn
from Datum import Datum
from ncsm_out.State import State
from ncsm_out.parser import a_aeff_nhw_to_states_map

MSG1 = (
    '\nInsufficient keyword arguments to evaluate {}.'
    '\nPlease supply either nhw or (nmax and z) as keyword arguments'
)

MSG2 = (
    '\nInsufficient keyword arguments to evaluate {}.'
    '\nEither nhw or nmax must be supplied as a keyword argument.'
)


def _get_a0(nshell, ncomponent):
    """Return the first mass number in the given shell
    :param nshell: shell (0=s, 1=p, 2=sd, ...)
    :param ncomponent: 1 -> neutrons, 2 -> protons & neutrons
    """
    return int((nshell+2) * (nshell+1) * nshell/3 * ncomponent)


# todo: make this general
def get_ground_state_j(mass, nshell):
    """Get the j for the ground state for the given mass number and shell.
    :param mass: mass number
    :param nshell: (0=s, 1=p, 2=sd, ...)
    """
    if mass % 2 == 0:
        return 0.0
    elif nshell == 1:
        return 1.5
    elif nshell == 2:
        return 2.5
    else:
        return None


class GroundStateNotFoundException(Exception):
    pass


# todo: This only filters out incorrect ground states for some cases
# todo: Extend to make general
def _get_ground_state(mass, states, nshell):
    """Given a mass number, a list of states, and the shell, returns the
    ground states (defined here to be the lowest energy with the correct J)
    :param mass: mass number (A)
    :param states: list of State (see State.py)
    :param nshell: (0=s, 1=p, 2=sd, ...)
    """
    if len(states) == 0:
        raise GroundStateNotFoundException(
            'Could not find ground state for A={}'.format(mass))
    j0 = get_ground_state_j(mass=mass, nshell=nshell)
    if j0 is None:
        warn(
            '\nGround state angular momentum not known for A={}, nshell={}.'
            'Using state with lowest energy.'.format(mass, nshell))
        return states[0]
    else:
        for state in states:
            if state.J == j0:
                return state
        else:
            warn(
                (
                    '\nCould not find converged state with J={} for A={}'
                    '\nAttempting to find approximate solution by rounding'
                ).format(j0, mass)
            )
            return _get_ground_state_rounded(
                mass=mass, states=states, nshell=nshell)


def _get_ground_state_rounded(mass, states, nshell, round_place=4):
    j0 = get_ground_state_j(mass=mass, nshell=nshell)
    if round_place < 0:
        raise GroundStateNotFoundException(
            'Could not find state with J={} for A={}'.format(j0, mass))
    for state in states:
        if round(state.J, round_place) == j0:
            return state
    else:
        return _get_ground_state_rounded(
            mass=mass, states=states, nshell=nshell, round_place=round_place-1)


class IncompleteArgumentsException(Exception):
    pass


def _min_orbitals(z):
    """Get the minimum number of harmonic oscillator orbitals for a given Z.
    This is a port from the function Nmin_HO in it-code-111815.f.
    :param z: proton or neutron number
    :return: minimum number of harmonic oscillator orbitals
    """
    z_rem = z
    n_min = 0
    n = 0
    while True:
        n_min += n * min((n+1)*(n+2), z_rem)
        z_rem -= (n+1)*(n+2)
        if z_rem <= 0:
            break
        n += 1
    return n_min


class DatumNcsmOut(Datum):
    """Stores data maps specific to a common set of NCSM out files, as
    identified by an ExpNcsmVceOut
    """
    def __init__(self, directory, exp, files):
        """Initializes the Datum. Typically this would be handled by the
        DataMap (e.g. DataMapNcmOut), so the user generally need not concern
        their self with this.
        :param directory: directory in which to initialize the datum
        :param exp: exp for the datum, which uniquely matches to its data
        :param files: list of relevant file paths to be parsed into the datum
        """
        super(DatumNcsmOut, self).__init__(
            directory=directory, exp=exp, files=files)
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

    def a_aeff_nmax_to_states_map(self, z):
        """Returns map
            (A, Aeff, Nmax) -> list of states
        :param z: proton number (Z)
        """
        a_aeff_nmax_to_states = dict()
        for k, v in self._a_aeff_nhw_to_states_map.items():
            a, aeff, nhw = k
            nmax = nhw - (_min_orbitals(z) + _min_orbitals(a - z))
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

    def _a_aeff_to_ground_state_map_for_nhw(self, nhw, nshell):
        return {k: _get_ground_state(mass=k[0], states=v, nshell=nshell)
                for k, v in self._a_aeff_to_states_map_for_nhw(nhw).items()}

    def _aeff_exact_to_states_map_for_nhw(self, nhw):
        aeff_exact_to_states = dict()
        for k, v in self._a_aeff_to_states_map_for_nhw(nhw).items():
            if k[0] != k[1]:
                continue
            else:
                aeff_exact_to_states[k[0]] = v
        return aeff_exact_to_states

    def _aeff_exact_to_ground_state_map_for_nhw(self, nhw, nshell):
        return {k: _get_ground_state(mass=k, states=v, nshell=nshell)
                for k, v in self._aeff_exact_to_states_map_for_nhw(nhw).items()}

    def _aeff_exact_to_ground_state_energy_map_for_nhw(self, nhw, nshell):
        return {
            k: v.E for k, v in
            self._aeff_exact_to_ground_state_map_for_nhw(
                nhw=nhw, nshell=nshell).items()
            }

    # maps for a given Nmax
    def _a_aeff_to_states_map_for_nmax(self, nmax, z):
        a_aeff_to_states = dict()
        for k, v in self.a_aeff_nmax_to_states_map(z=z).items():
            a_i, aeff_i, nmax_i = k
            if nmax_i != nmax:
                continue
            else:
                a_aeff_to_states[(a_i, aeff_i)] = v
        return a_aeff_to_states

    def _a_aeff_to_ground_state_map_for_nmax(self, nmax, z, nshell):
        return {k: _get_ground_state(mass=k[0], states=v, nshell=nshell)
                for k, v in self.a_aeff_to_states_map(nmax=nmax, z=z).items()}

    def _aeff_exact_to_states_map_for_nmax(self, nmax, z):
        aeff_exact_to_states = dict()
        for k, v in self._a_aeff_to_states_map_for_nmax(
                nmax=nmax, z=z).items():
            if k[0] != k[1]:
                continue
            else:
                aeff_exact_to_states[k[0]] = v
        return aeff_exact_to_states

    def _aeff_exact_to_ground_state_map_for_nmax(self, nmax, z, nshell):
        return {
            k: _get_ground_state(mass=k, states=v, nshell=nshell)
            for k, v in
            self._aeff_exact_to_states_map_for_nmax(nmax=nmax, z=z).items()
            }

    def _aeff_exact_to_ground_state_energy_map_for_nmax(self, nmax, z, nshell):
        return {k: v.E for k, v in
                self._aeff_exact_to_ground_state_map_for_nmax(
                    nmax=nmax, z=z, nshell=nshell).items()}

    # user maps
    def a_aeff_to_states_map(self, nhw=None, nmax=None, z=None):
        """Returns a map
            (A, Aeff) -> list of state
        for the given Nhw or Nmax and Z.
        Either nhw or (nmax and z) must be provided.
        :param nhw: major oscillator truncation
        :param nmax: major oscillator truncation minus min number orbitals.
        :param z: proton number (Z)
        """
        if nhw is not None:
            return self._a_aeff_to_states_map_for_nhw(nhw=nhw)
        elif nmax is not None:
            if z is not None:
                return self._a_aeff_to_states_map_for_nmax(nmax=nmax, z=z)
            else:
                raise IncompleteArgumentsException(MSG1.format(
                    'a_aeff_to_states_map'
                ))
        else:
            raise IncompleteArgumentsException(MSG2.format(
                'a_aeff_to_states_map'
            ))

    def a_aeff_to_ground_state_map(self, nshell, nhw=None, nmax=None, z=None):
        """Returns a map
            (A, Aeff) -> ground state
        for a given shell.
        Either nhw or (nmax and z) must be provided.
        :param nshell: (0=s, 1=p, 2=sd, ...)
        :param nhw: major oscillator truncation
        :param nmax: major oscillator truncation relative to min required
        orbitals
        :param z: proton number (Z)
        """
        if nhw is not None:
            return self._a_aeff_to_ground_state_map_for_nhw(
                nhw=nhw, nshell=nshell)
        elif nmax is not None:
            if z is not None:
                return self._a_aeff_to_ground_state_map_for_nmax(
                    nmax=nmax, z=z, nshell=nshell)
            else:
                raise IncompleteArgumentsException(MSG1.format(
                    'a_aeff_to_ground_state_map'
                ))
        else:
            raise IncompleteArgumentsException(MSG2.format(
                'a_aeff_to_ground_state_map'
            ))

    def a_aeff_to_ground_state_energy_map(
            self, nshell, nhw=None, nmax=None, z=None):
        """Returns a map
            (A, Aeff) -> ground energy
        for a given shell and truncation level.
        :param nshell: shell (0=s, 1=p, 2=sd)
        :param nhw: major oscillator truncation
        :param nmax: major oscillator truncation relative to minimum requried
        orbitals
        :param z: proton number (Z)
        """
        try:
            a_aeff_to_gnd_state = self.a_aeff_to_ground_state_map(
                nhw=nhw, nmax=nmax, z=z, nshell=nshell)
        except IncompleteArgumentsException:
            raise
        return {k: v.E for k, v in a_aeff_to_gnd_state.items()}

    def aeff_exact_to_ground_state_energy_map(
            self, nshell, nhw=None, nmax=None, z=None):
        """Returns a map
            A=Aeff -> ground energy
        from mass number to ground energy in the case where Aeff=A.
        Either nhw or (nmax and z) is required
        :param nshell: shell (0=s, 1=p, 2=sd, ...)
        :param nhw: major oscillator truncation
        :param nmax: major oscillator truncation relative to minimum required
        number of orbitals
        :param z: proton number (Z)
        """
        if nhw is not None:
            return self._aeff_exact_to_ground_state_energy_map_for_nhw(
                nhw=nhw, nshell=nshell)
        elif nmax is not None:
            if z is not None:
                return self._aeff_exact_to_ground_state_energy_map_for_nmax(
                    nmax=nmax, z=z, nshell=nshell)
            else:
                raise IncompleteArgumentsException(MSG1.format(
                    'aeff_exact_to_ground_state_energy_map'))
        else:
            raise IncompleteArgumentsException(MSG2.format(
                'aeff_exact_to_ground_state_energy_map'))
