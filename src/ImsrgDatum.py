from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import namedtuple

import parse


# noinspection PyClassHasNoInit
class QuantumNumbers(namedtuple('QuantumNumbers', ['n', 'l', 'j', 'tz'])):
    __slots__ = ()

    def __str__(self):
        n = str(int(self.n))
        l = str(int(self.l))
        j = str(int(2*self.j)) + '/2'
        tz = str(int(2*self.tz)) + '/2'
        tz = '+' + tz if self.tz > 0 else tz
        return '(n={n}, l={l}, j={j}, tz={tz})'.format(n=n, l=l, j=j, tz=tz)


# noinspection PyClassHasNoInit
class InteractionTuple(namedtuple('InteractionTuple',
                                  ['a', 'b', 'c', 'd', 'j'])):
    __slots__ = ()

    def __str__(self):
        a = str(self.a)
        b = str(self.b)
        c = str(self.c)
        d = str(self.d)
        j = str(self.j)
        sep = unichr(9474).strip()
        left = unichr(12296).strip()
        right = unichr(12297).strip()
        # sep = '|'
        # left = '<'
        # right = '>'
        return ('({left}{a},{b}{s}'
                'V'
                '{s}{c},{d}{right}, j={j})'
                '').format(a=a, b=b, c=c, d=d, j=j,
                           left=left, right=right,
                           s=sep)


class ImsrgDatum:
    def __init__(self, directory, e, hw, b=None, rp=None, std_io_map=None,
                 standardize=True):
        self.e = e
        self.hw = hw
        self.b = b
        self.rp = rp

        self.name = None
        self.dir = directory
        self._fname_filter = None
        self.standardized = False

        # Create maps initially empty
        self.standard_index_orbital_map = std_io_map
        self._particular_index_orbital_map = None
        self.index_orbital_map = dict()
        self.mass_index_energy_map = dict()
        self.mass_interaction_index_energy_map = dict()
        self.mass_zero_body_term_map = dict()
        self.other_constants = None

        # Perform setup methods
        self._set_fname_filter()
        self._set_maps()
        self._set_name()
        self._set_other_constants()
        if self.standard_index_orbital_map is not None and standardize is True:
            self._standardize_indexing()
            self.standardized = True

    def _set_maps(self):
        self._set_index_orbital_map()
        self._set_mass_index_energy_map()
        self._set_mass_interaction_index_energy_map()
        self._set_zero_body_term_map()

    def _set_index_orbital_map(self):
        """Retrieves the index -> orbital map from a file in the directory
        and stores it in an instance variable
        """
        files = parse.files_with_ext_in_directory(directory=self.dir)

        # Assuming all files in a given directory have the same indexing...
        f0 = list(filter(self._fname_filter, files))[0]
        index_orbital_map = parse.index_tuple_map(f0)

        # Turn each tuple in the map into a named tuple
        for k in index_orbital_map.keys():
            v = index_orbital_map[k]
            nextv = QuantumNumbers(*qnums_to_list(v))
            index_orbital_map[k] = nextv

        self.index_orbital_map = index_orbital_map

    def _set_mass_index_energy_map(self):
        """Retrieves the
            mass number -> orbital index -> energy
        mapping for the directory
        """
        self.mass_index_energy_map = (
            parse.mass_index_energy_map_map(self.dir, self._fname_filter))

    def _set_mass_interaction_index_energy_map(self):
        """Retrieves the
            mass number -> (a, b, c, d, j) -> energy
        mapping for the directory
        """
        miiem = (
            parse.mass_interaction_tuple_energy_map_map(self.dir,
                                                        self._fname_filter))

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

    def _set_zero_body_term_map(self):
        self.mass_zero_body_term_map = (
            parse.mass_zero_body_term_map(self.dir, self._fname_filter))

    def _set_name(self):
        """Sets the incidence name variable
        """
        files = parse.files_with_ext_in_directory(self.dir)
        f0 = list(filter(self._fname_filter, files))[0]
        self.name = parse.name_from_filename(f0)

    def _set_fname_filter(self):
        """Returns a filter function that filters a set of filenames such that
        only those that have the same signature (e, hw, rp) values as self
        """
        def f(fname):
            return (parse.e_level_from_filename(fname) == self.e and
                    parse.hw_from_filename(fname) == self.hw and
                    parse.rp_from_filename(fname) == self.rp and
                    parse.base_from_filename(fname) == self.b)
        self._fname_filter = f

    def _set_other_constants(self):
        """Sets other heading constants. Assumes all files in a given directory
        have the same constants
        """
        files = parse.files_with_ext_in_directory(self.dir)
        f0 = list(filter(self._fname_filter, files))[0]
        self.other_constants = parse.other_constants_from_filename(f0)

    def _standardize_indexing(self):
        self._standardize_mass_index_energy_map_indexing()
        self._standardize_mass_interaction_index_energy_map_indexing()
        self._particular_index_orbital_map = self.index_orbital_map
        self.index_orbital_map = self.standard_index_orbital_map

    def _standardize_mass_index_energy_map_indexing(self):
        """Reformat the mass -> index -> energy map indices to be with respect
        to the standard io_map
        """
        mie_map = self.mass_index_energy_map
        std_mie_map = dict()
        for m, ie_map in mie_map.iteritems():
            std_ie_map = dict()
            for idx, energy in ie_map.iteritems():
                next_idx = self._standard_index(idx)
                std_ie_map[next_idx] = energy
            std_mie_map[m] = std_ie_map
        self.mass_index_energy_map = std_mie_map

    def _standardize_mass_interaction_index_energy_map_indexing(self):
        miie_map = self.mass_interaction_index_energy_map
        std_miie_map = dict()
        for m, iie_map in miie_map.iteritems():
            std_iie_map = dict()
            for ii, energy in iie_map.iteritems():
                next_ii = self._standardize_interaction_index_tuple(ii)
                std_iie_map[next_ii] = energy
            std_miie_map[m] = std_iie_map
        self.mass_interaction_index_energy_map = std_miie_map

    def _standard_orbital_index_map(self):
        return {v: k for k, v in self.standard_index_orbital_map.iteritems()}

    def _standardize_interaction_index_tuple(self, ii_tuple):
        next_tuple = [self._standard_index(i) for i in ii_tuple[0:4]]
        next_tuple.append(ii_tuple[4])
        return InteractionTuple(*next_tuple)

    def _standard_index(self, i):
        io_map = self.index_orbital_map
        soi_map = self._standard_orbital_index_map()
        return soi_map[io_map[i]]

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

    def interaction_qnums_mass_energy_map(self):
        iqme_map = dict()
        iime_map = self.interaction_index_mass_energy_map()
        for interaction_tuple in sorted(iime_map.keys()):
            inter_qnums = self.interaction_indices_to_interaction_qnums(
                    interaction_tuple)
            iqme_map[inter_qnums] = iime_map[interaction_tuple]
        return iqme_map

    def interaction_indices_to_interaction_qnums(self, ii):
        next_tup = tuple()
        for index in ii[0:4]:
            qnums = self.index_orbital_map[index]
            next_tup += qnums
        next_tup += ii.j
        return InteractionTuple(*next_tup)


def qnums_to_list(qnums):
    qn_list = list()
    for n in qnums:
        if '/' in n:
            sn = n.split('/')
            qn_list.append(float(sn[0]) / float(sn[1]))
        else:
            qn_list.append(float(n))
    return qn_list
