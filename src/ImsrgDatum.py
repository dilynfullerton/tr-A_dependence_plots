from __future__ import print_function
from __future__ import division
from collections import namedtuple
import parse


QuantumNumbers = namedtuple('QuantumNumbers', ['n', 'l', 'j', 'tz'])
InteractionTuple = namedtuple('InteractionTuple', ['a', 'b', 'c', 'd', 'j'])


class ImsrgDatum:
    def __init__(self, directory, e, hw, name=None):
        self.e = e
        self.hw = hw
        self.name = name
        self.dir = directory

        # Create maps initially empty
        self.index_orbital_map = dict()
        self.mass_index_energy_map = dict()
        self.mass_interaction_index_energy_map = dict()

        # Perform setup methods
        self._set_index_orbital_map()
        self._set_mass_index_energy_map()
        self._set_mass_interaction_index_energy_map()

    def _set_index_orbital_map(self):
        """Retrieves the index -> orbital map from a file in the directory
        and stores it in an instance variable
        """
        files = parse.files_with_ext_in_directory(directory=self.dir)

        # Assuming all files in a given directory have the same indexing...
        f0 = files[0]
        index_orbital_map = parse.index_tuple_map(f0)

        # Turn each tuple in the map into a named tuple
        for k in index_orbital_map.keys():
            v = index_orbital_map[k]
            nextv = QuantumNumbers(*v)
            index_orbital_map[k] = nextv
            
        self.index_orbital_map = index_orbital_map

    def _set_mass_index_energy_map(self):
        """Retrieves the
            mass number -> orbital index -> energy
        mapping for the directory
        """
        self.mass_index_energy_map = parse.mass_index_energy_map_map(self.dir)
        
    def _set_mass_interaction_index_energy_map(self):
        """Retrieves the
            mass number -> (a, b, c, d, j) -> energy
        mapping for the directory
        """
        miiem = parse.mass_interaction_tuple_energy_map_map(self.dir)

        # Turn each tuple into a named tuple
        for A in miiem.keys():
            tuple_energy_map = miiem[A]
            next_tuple_energy_map = dict()
            for k in tuple_energy_map.keys():
                v = tuple_energy_map[k]
                nextk = list()
                for stritem in k:
                    nextk.append(int(stritem))
                nextk = InteractionTuple(*nextk)
                next_tuple_energy_map[nextk] = v
            miiem[A] = next_tuple_energy_map
        
        self.mass_interaction_index_energy_map = miiem
        
    def folded_mass_interaction_index_energy_map(self):
        """Return a flat version of the map"""
        miie_map = self.mass_interaction_index_energy_map
        folded_map = list()
        for mass_num in miie_map.keys():
            for tup in miie_map[mass_num]:
                energy = miie_map[mass_num][tup]
                folded_map.append((mass_num, tup, energy))
        return folded_map

    def interaction_index_mass_energy_map(self):
        """From the mass -> interaction index -> energy map, creates a
        mapping from interaction index -> mass -> energy
        """
        miie_map = self.mass_interaction_index_energy_map
        iime_map = dict()
        for mass_num in miie_map.keys():
            for tup in miie_map[mass_num]:
                if tup not in iime_map.keys():
                    iime_map[tup] = dict()
                iime_map[tup][mass_num] = miie_map[mass_num][tup]
        return iime_map

    def index_mass_energy_map(self):
        """From the (mass -> orbital index -> energy) map produce an
        (orbital index -> mass -> energy) map
        """
        mie_map = self.mass_index_energy_map
        ime_map = dict()
        for mass in mie_map.keys():
            for index in mie_map[mass].keys():
                if index not in ime_map.keys():
                    ime_map[index] = dict()
                ime_map[index][mass] = mie_map[mass][index]
        return ime_map
                

'''
idx = ImsrgDatum(directory='../files/hw20/', e=12, hw=20)
print(idx.interaction_index_mass_energy_map())
'''
'''
fm = idx.folded_mass_interaction_index_energy_map()

for t in fm:
    print(t)
'''
'''
x = idx.mass_interaction_index_energy_map

for i in x.keys():
    print(str(i) + ': ')
    for j in x[i].keys():
        print('\t' + str(j) + ': ' + str(x[i][j]))
'''
