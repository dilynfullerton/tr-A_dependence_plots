"""data_maps.py
Functions for retrieving various data maps from parsed files
"""
from __future__ import division, unicode_literals, print_function
from os import path


class NoUniqueMapError(RuntimeError):
    pass


# todo: make this general
def _get_ground_state_j(mass, z):
    """Get the j for the ground state for the given mass number and shell.
    :param mass: mass number
    :param z: proton num
    """
    if mass % 2 == 0:
        return 0.0
    elif z == 2:
        return 1.5
    elif z == 3:
        return 2.5  # todo is this correct?
    elif z == 16:
        return 2.5
    else:
        return None


def _get_ground_state_rounded(mass, states, z, round_place=4):
    j0 = _get_ground_state_j(mass=mass, z=z)
    if round_place < 0:
        print('Could not find state with J={} for A={}'.format(j0, mass))
        return None
    for state in states:
        if round(state.J, round_place) == j0:
            return state
    else:
        return _get_ground_state_rounded(
            mass=mass, states=states, z=z, round_place=round_place - 1)


# todo: This only filters out incorrect ground states for some cases
# todo: Extend to make general
def _get_ground_state(mass, states, z):
    """Given a mass number, a list of states, and the shell, returns the
    ground states (defined here to be the lowest energy with the correct J)
    :param mass: mass number (A)
    :param states: list of State (see State.py)
    :param z: proton num
    """
    j0 = _get_ground_state_j(mass=mass, z=z)
    if len(states) == 0:
        print('Could not find ground state for A={}'.format(mass))
        return None
    elif j0 is None:
        print(
            '\nGround state angular momentum not known for A={}, z={}.'
            'Using state with lowest energy.'.format(mass, z))
        return states[0]
    else:
        for state in states:
            if state.J == j0:
                return state
        else:
            print(
                (
                    '\nCould not find converged state with J={} for A={}'
                    '\nAttempting to find approximate solution by rounding'
                ).format(j0, mass))
            return _get_ground_state_rounded(
                mass=mass, states=states, z=z)


def _get_a_aeff_to_ncsd_out_map(parsed_ncsd_out_files):
    """Returns a map (A, Aeff) -> NcsdOut from the given NcsdOut if it is
    possible to form the map uniquely
    """
    a_aeff_to_parsed_file = dict()
    for ncsd_out in parsed_ncsd_out_files:
        a = ncsd_out.z + ncsd_out.n
        aeff = ncsd_out.aeff
        if (a, aeff) not in a_aeff_to_parsed_file:
            a_aeff_to_parsed_file[(a, aeff)] = ncsd_out
        else:
            raise NoUniqueMapError(
                'Multiple files with (A, Aeff) = ({}, {}) in given list'
                ''.format(a, aeff))
    return a_aeff_to_parsed_file


def get_a_aeff_to_state_to_energy_map(parsed_ncsd_out_files):
    """Given a list of NcsdOut and optional arguments nmax and z, returns a map
        (a, aeff) -> (j, t) -> energy
    """
    a_aeff_to_state_to_energy = dict()
    for a_aeff, ncsd_out in _get_a_aeff_to_ncsd_out_map(
            parsed_ncsd_out_files).items():
        state_to_energy = dict()
        for state, e in sorted(ncsd_out.energy_levels.items(),
                               key=lambda i: i[1]):
            if state not in state_to_energy:
                state_to_energy[state] = e
        a_aeff_to_state_to_energy[a_aeff] = state_to_energy
    return a_aeff_to_state_to_energy


def get_state_to_a_aeff_to_energy_map(parsed_ncsd_out_files):
    a_aeff_to_state_to_energy = get_a_aeff_to_state_to_energy_map(
        parsed_ncsd_out_files=parsed_ncsd_out_files)
    state_to_a_aeff_to_energy = dict()
    for a_aeff, state_to_energy in a_aeff_to_state_to_energy.items():
        for state, energy in state_to_energy.items():
            if state not in state_to_a_aeff_to_energy:
                state_to_a_aeff_to_energy[state] = dict()
            state_to_a_aeff_to_energy[state][a_aeff] = energy
    return state_to_a_aeff_to_energy


def get_a_aeff_to_ground_state_energy_map(parsed_ncsd_out_files):
    a_aeff_to_ground_state_energy = dict()
    for a_aeff, ncsd_out in _get_a_aeff_to_ncsd_out_map(
            parsed_ncsd_out_files=parsed_ncsd_out_files
    ).items():
        for state, e in sorted(ncsd_out.energy_levels.items()):
            if state.J == _get_ground_state_j(mass=a_aeff[0], z=ncsd_out.z):
                a_aeff_to_ground_state_energy[a_aeff] = e
                break
    return a_aeff_to_ground_state_energy


# todo: add data maps for nushellx energy and interaction files
def _get_fpath_to_parsed_file_map(parsed_files):
    """Creates a map: filepath -> Parser from the given list of Parser
    """
    fpath_to_file = dict()
    for f in parsed_files:
        fpath_to_file[f.filepath] = f
    return fpath_to_file


def _get_dpath_to_parsed_file_map(parsed_files):
    """Creates a map: dirpath -> Parser from the given list of Parser, where
    dirpath is the full path to the directory containing the file represented
    by the associated Parser
    """
    dpath_to_file = dict()
    for fpath, parser in _get_fpath_to_parsed_file_map(parsed_files).items():
        dpath = path.split(fpath)[0]
        dpath_to_file[dpath] = parser
    return dpath_to_file


def _get_presc_a_to_int_and_lpt_map(parsed_int_files, parsed_lpt_files):
    dpath_to_int = _get_dpath_to_parsed_file_map(parsed_int_files)
    dpath_to_lpt = _get_dpath_to_parsed_file_map(parsed_lpt_files)
    presc_a_to_int_and_lpt = dict()
    for dpath, intfile in dpath_to_int.items():
        presc = intfile.a_prescription
        if presc is not None and dpath in dpath_to_lpt:
            lptfile = dpath_to_lpt[dpath]
            a = lptfile.a
            presc_a_to_int_and_lpt[(presc, a)] = (intfile, lptfile)
    return presc_a_to_int_and_lpt


def _get_presc_a_to_state_to_energy_map(parsed_int_files, parsed_lpt_files):
    presc_a_to_int_and_lpt = _get_presc_a_to_int_and_lpt_map(
        parsed_int_files, parsed_lpt_files)
    presc_a_to_state_to_energy = dict()
    for presc_a, int_and_lpt in presc_a_to_int_and_lpt.items():
        intfile, lptfile = int_and_lpt
        state_to_energy = dict()
        for state in lptfile.energy_levels:
            state_to_energy[state] = state.E + intfile.zero_body_term
        presc_a_to_state_to_energy[presc_a] = state_to_energy
    return presc_a_to_state_to_energy


def get_state_to_presc_a_to_energy_map(parsed_int_files, parsed_lpt_files):
    presc_a_to_state_to_energy = _get_presc_a_to_state_to_energy_map(
        parsed_int_files=parsed_int_files, parsed_lpt_files=parsed_lpt_files)
    state_to_presc_a_to_energy = dict()
    for presc_a, state_to_energy in presc_a_to_state_to_energy.items():
        for state, energy in state_to_energy.items():
            if state not in state_to_presc_a_to_energy:
                state_to_presc_a_to_energy[state] = dict()
            state_to_presc_a_to_energy[state][presc_a] = energy
    return state_to_presc_a_to_energy


def get_presc_a_to_ground_state_energy_map(parsed_int_files, parsed_lpt_files):
    presc_a_to_ground_state_energy = dict()
    for presc_a, int_lpt in _get_presc_a_to_int_and_lpt_map(
        parsed_int_files=parsed_int_files, parsed_lpt_files=parsed_lpt_files
    ).items():
        for state in sorted(int_lpt[1].energy_levels):
            if state.J == _get_ground_state_j(mass=presc_a[1], z=int_lpt[1].z):
                presc_a_to_ground_state_energy[presc_a] = (
                    state.E + int_lpt[0].zero_body_term)
                break
    return presc_a_to_ground_state_energy


# # test
# dpath = '~/workspace/triumf/tr-c-ncsm/old/results20170224/ncsd'
# ncsd_files = sorted(parse_ncsd_out_files(dpath))
# a_aeff_to_ground_state_energy = get_a_aeff_to_ground_state_energy_map(
#     ncsd_files,
#     ground_state=NcsdEnergyLevel(3., 0.),
#     z=3
# )
# for a_aeff, e in sorted(a_aeff_to_ground_state_energy.items()):
#     a, aeff = a_aeff
#     print('A = {:2}, Aeff = {:2} --> e = {}'.format(a, aeff, e))
