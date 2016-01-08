from __future__ import print_function
from __future__ import division
from collections import namedtuple
from matplotlib import pyplot as plt
from ImsrgDataMap import ImsrgDataMap
from ImsrgDataMap import Exp
from ImsrgDatum import ImsrgDatum


def plot_energy_vs_mass(e, hw, directory):
    """For a single e, hw pair, along with the main parent directory, 
    plots are created for the energy of each (a, b, c, d, j) tuple against
    its mass number
    """
    idm = ImsrgDataMap(directory)
    idat = idm.map[Exp(e=e, hw=hw)]
    
    miie_map = idat.mass_interaction_index_energy_map
    '''
    fold_miie = idat.folded_mass_interaction_index_energy_map()
    s2 = sorted(fold_miie, key=lambda x: x[1][4])
    s3 = sorted(s2, key=lambda x: x[1][3])
    s4 = sorted(s3, key=lambda x: x[1][2])
    s5 = sorted(s4, key=lambda x: x[1][1])
    s6 = sorted(s5, key=lambda x: x[1][0])
    
    for line in s6:
        print(line)
    '''
    for tup_energy_map in miie_map.values():
        plot_map = dict()
        for tup in tup_energy_map.keys():
            x = list()
            y = list()
            label = str(tup)
            
            for mass_num in miie_map.keys():
                if tup in miie_map[mass_num].keys():
                    x.append(mass_num)
                    y.append(tup_energy_map[tup])
            
            plot_map[tup] = (x, y)
            plt.plot(x, y, '-', label=label)
    plt.show()


plot_energy_vs_mass(14, 24, '../files/')
