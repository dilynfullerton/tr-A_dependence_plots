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

    tupleset = list()
    for v in miie_map.values():
        tupleset.extend(v.keys())
    tupleset = set(tupleset)
    
    plot_map = dict()
    for t in tupleset:
        x = list()
        y = list()
        label = str(t)
        
        for mass_num in sorted(miie_map.keys()):
            if t in miie_map[mass_num]:
                x.append(mass_num)
                y.append(miie_map[mass_num][t])

                print(t)
                for p in zip(x, y):
                    print(p)

                plot_map[t] = (x, y)
                plt.plot(x, y, '-', label=label)
        
    plt.show()

    return plot_map


plot_energy_vs_mass(12, 20, '../files/')
