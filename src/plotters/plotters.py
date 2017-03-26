"""plotters.py
Various functions for plotting A-dependence data
"""
from __future__ import division, print_function, unicode_literals
from plotting import map_to_arrays
from data_maps import get_state_to_a_aeff_to_energy_map
from data_maps import get_a_aeff_to_ground_state_energy_map
from parsers.parse_files import parse_ncsd_out_files


def get_plots_aeff_exact_to_energy(parsed_ncsd_out_files):
    """Returns a list of plots in the form
            (xdata, ydata, const_list, const_dict),
    where A=Aeff is xdata, energy is ydata, and the const_dict constains
    the state list is generated from the data from the given NcsdOut objects
    :param parsed_ncsd_out_files: list of parsed NcsdOut objects from which
    to generate the map
    :return: [(a_array, energy_array, state)]
    """
    state_to_a_aeff_to_energy = get_state_to_a_aeff_to_energy_map(
        parsed_ncsd_out_files=parsed_ncsd_out_files)
    state_to_a_exact_to_energy = dict()
    for state, a_aeff_to_energy in state_to_a_aeff_to_energy.items():
        for a_aeff, energy in a_aeff_to_energy.items():
            if a_aeff[0] == a_aeff[1]:
                if state not in state_to_a_exact_to_energy:
                    state_to_a_exact_to_energy[state] = dict()
                state_to_a_exact_to_energy[state][a_aeff[0]] = energy
    list_of_plots = list()
    for state, a_to_energy in state_to_a_exact_to_energy.items():
        list_of_plots.append(
            map_to_arrays(a_to_energy) + (list(), {'state': state}))
    return list_of_plots


def get_plot_aeff_exact_to_ground_energy(parsed_ncsd_out_files):
    a_aeff_to_ground_state_energy = get_a_aeff_to_ground_state_energy_map(
        parsed_ncsd_out_files=parsed_ncsd_out_files)
    a_to_ground_state_energy = dict()
    for a_aeff, e in a_aeff_to_ground_state_energy.items():
        if a_aeff[0] == a_aeff[1]:
            a_to_ground_state_energy[a_aeff[0]] = e
    return map_to_arrays(a_to_ground_state_energy) + (list(), dict())


# test
dpath = '/Users/Alpha/workspace/triumf/tr-c-ncsm/old/results20170224/ncsd'
all_ncsd_files = sorted(parse_ncsd_out_files(dirpath=dpath))
he_ncsd_files = filter(lambda n: n.z == 2, all_ncsd_files)
# plots = get_plots_aeff_exact_to_energy(he_ncsd_files)
# for plot in sorted(plots, key=lambda p: p[3]['state']):
#     xarr, yarr, const_list, const_dict = plot
#     print('State = {}'.format(const_dict['state']))
#     for x, y in zip(xarr, yarr):
#         print('  {:4} {:8.4}'.format(x, y))
xarr, yarr, cl, cd = get_plot_aeff_exact_to_ground_energy(he_ncsd_files)
for x, y in zip(xarr, yarr):
    print('  {:4} {:8.4}'.format(x, y))
