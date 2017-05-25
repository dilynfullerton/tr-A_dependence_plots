"""data_maps.py
Functions for retrieving various data maps from parsed files
"""
from __future__ import division, unicode_literals, print_function
from os import path


class NoUniqueMapError(RuntimeError):
    pass


# todo: make this general
# def _get_ground_state_j(mass, z):
#     """Get the j for the ground state for the given mass number and shell.
#     :param mass: mass number
#     :param z: proton num
#     """
#     if mass % 2 == 0:
#         return 0.0
#     elif z == 2:
#         return 1.5
#     elif z == 3:
#         return 1.5
#     elif z == 16:
#         return 2.5
#     else:
#         return None


# def _get_ground_state(states, energies, j_list, j0=None):
#     """Gets the ground state and ground energy from the list of states,
#     energies, and angular momenta. This is chosen by finding the state with
#     lowest associated energy for which angular momentum matches j0
#     :param states: list of energy states
#     :param energies: list of energies assocated with `states`
#     :param j_list: list of J associated with `states`
#     :return ground state, ground energy if found; returns None, None
#     """
#     states_sorted = sorted(
#         list(zip(states, energies, j_list)), key=lambda x: x[1])
#     for s, e, j in states_sorted:
#         if j == j0:
#             return s, e
#     else:
#         return None, None
#         # s0, e0, j0 = states_sorted[0]
#         # return s0, e


def get_a_aeff_to_ncsd_out_map(parsed_ncsd_out_files):
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


# def get_a_aeff_to_state_to_energy_map(parsed_ncsd_out_files):
#     """Given a list of NcsdOut and optional arguments nmax and z, returns a map
#         (a, aeff) -> (j, t) -> energy
#     """
#     a_aeff_to_state_to_energy = dict()
#     for a_aeff, ncsd_out in get_a_aeff_to_ncsd_out_map(
#             parsed_ncsd_out_files).items():
#         state_to_energy = dict()
#         for state, e in sorted(ncsd_out.energy_levels.items(),
#                                key=lambda i: i[1]):
#             if state not in state_to_energy:
#                 state_to_energy[state] = e
#         a_aeff_to_state_to_energy[a_aeff] = state_to_energy
#     return a_aeff_to_state_to_energy


# def get_state_to_a_aeff_to_energy_map(parsed_ncsd_out_files):
#     a_aeff_to_state_to_energy = get_a_aeff_to_state_to_energy_map(
#         parsed_ncsd_out_files=parsed_ncsd_out_files)
#     state_to_a_aeff_to_energy = dict()
#     for a_aeff, state_to_energy in a_aeff_to_state_to_energy.items():
#         for state, energy in state_to_energy.items():
#             if state not in state_to_a_aeff_to_energy:
#                 state_to_a_aeff_to_energy[state] = dict()
#             state_to_a_aeff_to_energy[state][a_aeff] = energy
#     return state_to_a_aeff_to_energy


# def get_a_aeff_to_ground_state_energy_map(parsed_ncsd_out_files):
#     a_aeff_to_ground_state_energy = dict()
#     for a_aeff, ncsd_out in get_a_aeff_to_ncsd_out_map(
#             parsed_ncsd_out_files=parsed_ncsd_out_files
#     ).items():
#         states = ncsd_out.energy_levels.keys()
#         energies = [ncsd_out.energy_levels[s] for s in states]
#         j_list = [s.J for s in states]
#         j0 = _get_ground_state_j(mass=a_aeff[0], z=ncsd_out.z)
#         s0, e0 = _get_ground_state(states=states, energies=energies,
#                                    j_list=j_list, j0=j0)
#         if e0 is not None:
#             a_aeff_to_ground_state_energy[a_aeff] = e0
#     return a_aeff_to_ground_state_energy


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


def get_presc_a_to_int_and_lpt_map(parsed_int_files, parsed_lpt_files):
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


# def _get_presc_a_to_state_to_energy_map(parsed_int_files, parsed_lpt_files):
#     presc_a_to_int_and_lpt = get_presc_a_to_int_and_lpt_map(
#         parsed_int_files, parsed_lpt_files)
#     presc_a_to_state_to_energy = dict()
#     for presc_a, int_and_lpt in presc_a_to_int_and_lpt.items():
#         intfile, lptfile = int_and_lpt
#         state_to_energy = dict()
#         for state in lptfile.energy_levels:
#             state_to_energy[state] = state.E + intfile.zero_body_term
#         presc_a_to_state_to_energy[presc_a] = state_to_energy
#     return presc_a_to_state_to_energy


# def get_state_to_presc_a_to_energy_map(parsed_int_files, parsed_lpt_files):
#     presc_a_to_state_to_energy = _get_presc_a_to_state_to_energy_map(
#         parsed_int_files=parsed_int_files, parsed_lpt_files=parsed_lpt_files)
#     state_to_presc_a_to_energy = dict()
#     for presc_a, state_to_energy in presc_a_to_state_to_energy.items():
#         for state, energy in state_to_energy.items():
#             if state not in state_to_presc_a_to_energy:
#                 state_to_presc_a_to_energy[state] = dict()
#             state_to_presc_a_to_energy[state][presc_a] = energy
#     return state_to_presc_a_to_energy


# def get_presc_a_to_ground_state_energy_map(parsed_int_files, parsed_lpt_files):
#     presc_a_to_ground_state_energy = dict()
#     presc_a_to_int_and_lpt = get_presc_a_to_int_and_lpt_map(
#         parsed_int_files=parsed_int_files, parsed_lpt_files=parsed_lpt_files)
#     for presc_a, int_lpt in presc_a_to_int_and_lpt.items():
#         states = int_lpt[1].energy_levels
#         energies = [s.E for s in states]
#         j_list = [s.J for s in states]
#         j0 = _get_ground_state_j(mass=presc_a[1], z=int_lpt[1].z)
#         s0, e0 = _get_ground_state(states=states, energies=energies,
#                                    j_list=j_list, j0=j0)
#         if e0 is not None:
#             presc_a_to_ground_state_energy[presc_a] = (
#                 e0 + int_lpt[0].zero_body_term)
#     return presc_a_to_ground_state_energy


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
