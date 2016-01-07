from __future__ import print_function
from numpy import *
from matplotlib import pyplot as plt

# Constants
FILES_DIR = '../files/'
FILENAME_PREFIX = 'SD_magnus_e12_s100_hw20_A'
MIN_MASS = 17
MAX_MASS = 28
FILENAME_SUFFIX = '.int'
HEADER_START_INDEX = 1
NUM_ORBITALS = 6

# Functions
def generate_filename(mass_number,
                      directory,
                      prefix,
                      suffix):
    return directory + prefix + str(mass_number) + suffix


def get_header_array(filename):
    header_line = get_content_lines(get_lines(filename))[0]
    header_list = header_line.split()
    header_array = array(header_list)
    return header_array


def get_lines(filename):
    with open(filename) as f:
        lines = f.readlines();
    lines = list(map(lambda x: x.strip(), lines)) # Remove line separators
    return lines


def get_content_lines(lines):
    return list(filter(lambda x: x[0] is not '!', lines))


def orbital_energy_values(filename, start_index, num_orbitals):
    header_array = get_header_array(filename)
    return header_array[start_index : start_index + num_orbitals]


def orbital_energy_values_dict(min_mass_num, 
                               max_mass_num,
                               file_directory,
                               filename_prefix,
                               filename_suffix,
                               orbital_start_index,
                               num_orbitals):
    d = dict()
    for mass_number in range(min_mass_num, max_mass_num + 1):
        oev = orbital_energy_values(
            generate_filename(mass_number,
                              directory=file_directory,
                              prefix=filename_prefix,
                              suffix=filename_suffix),
            orbital_start_index,
            num_orbitals)
        d[mass_number] = oev
    return d


def plot_orbital_energy_values_vs_mass(min_mass,
                                       max_mass,
                                       file_directory,
                                       filename_prefix,
                                       filename_suffix,
                                       orbital_start_index,
                                       num_orbitals):
    energy_mass_map = orbital_energy_values_dict(min_mass, 
                                                 max_mass,
                                                 file_directory,
                                                 filename_prefix,
                                                 filename_suffix,
                                                 orbital_start_index,
                                                 num_orbitals)
    x_points = energy_mass_map.keys()
    for index in range(1):
        y_points = list()
        label = str(index + 1)
        for mass_number in x_points:
            y_points.append(energy_mass_map[mass_number][index])
        plt.plot(x_points, y_points, '-o', label=label)
    plt.legend()
    plt.title('Energies for orbitals 1 to 6')
    plt.xlabel('Atomic mass A (amu)')
    plt.ylabel('Orbital energy (MeV)')
    plt.show()


plot_orbital_energy_values_vs_mass(MIN_MASS, 
                                   MAX_MASS,
                                   file_directory=FILES_DIR,
                                   filename_prefix=FILENAME_PREFIX,
                                   filename_suffix=FILENAME_SUFFIX,
                                   orbital_start_index=HEADER_START_INDEX,
                                   num_orbitals=NUM_ORBITALS)



