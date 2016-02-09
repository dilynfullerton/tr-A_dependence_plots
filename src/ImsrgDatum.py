"""These definitions store data from particular file types of IMSRG data

For example, ImsrgDatumInt stores a bunch of maps generated based on *.int
files.
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from os import path, mkdir, link

from Shell import Shell
from TwoBodyInteraction import TwoBodyInteraction
from QuantumNumbers import QuantumNumbers

from parse_int import index_tuple_map
from parse_int import mass_index_energy_map_map
from parse_int import mass_interaction_tuple_energy_map_map
from parse_int import mass_zero_body_term_map
from parse_int import name_from_filename
from parse_int import other_constants_from_filename
from parse_int import mass_number_from_filename

from parse_lpt import mass_to_header_data_map
from parse_lpt import mass_to_n_to_body_data_map
from parse_lpt import mass_to_zbt_map

from constants import DIR_FILES_ORG, ORG_FMT_DIR, ORG_FMT_FILE
from constants import F_PARSE_INT_CMNT_CHAR as CMNT_CHAR_INT
from constants import F_PARSE_INT_CMNT_ZBT as CMNT_ZBT
from constants import F_PARSE_LPT_CMNT_CHAR as _CMNT_CHAR
from constants import F_PARSE_LPT_ROW_AZ as _ROW_AZ
from constants import F_PARSE_LPT_ROW_HEAD as _ROW_HEAD
from constants import F_PARSE_LPT_COL_HEAD_DATA_START as _COL_START
from constants import F_PARSE_LPT_ROW_START_DATA as _ROW_BODY_START
from constants import F_PARSE_LPT_NCOLS_BODY as _NCOLS_BODY
from constants import FN_PARSE_LPT_REGEX_FILENAME_INT as REGEX_FILENAME_INT


class _ImsrgDatum(object):
    def __init__(self, directory, exp, files):
        self.exp = exp
        self.dir = directory
        self.files = files

    def _set_maps(self):
        raise NotImplemented()


class ImsrgDatumInt(_ImsrgDatum):
    """Stores maps generated from *.int files and methods for generating new
    maps from this data
    """
    def __init__(self, directory, exp, files, std_io_map=None,
                 standardize_io_map=True, organize_files=True,
                 org_file_dir=DIR_FILES_ORG,
                 directory_format=ORG_FMT_DIR,
                 file_format=ORG_FMT_FILE):
        super(ImsrgDatumInt, self).__init__(directory=directory, exp=exp,
                                            files=files)
        self.name = None
        self.standardized_indexing = False
        self.files_organized = False

        # Create maps initially empty
        self.standard_index_orbital_map = std_io_map
        self._particular_index_orbital_map = None
        self._index_orbital_map = dict()
        self._mass_index_energy_map = dict()
        self._mass_interaction_index_energy_map = dict()
        self._mass_zero_body_term_map = dict()
        self._other_constants = None
        self._unorg_files = None

        # Perform setup methods
        self._set_maps()
        self._set_name()
        self._set_other_constants()
        if self.standard_index_orbital_map is not None and standardize_io_map:
            self._standardize_indexing()
            self.standardized_indexing = True
        if organize_files:
            self._organize_files(org_file_dir, directory_format, file_format)

    def _set_maps(self):
        self._set_index_orbital_map()
        self._set_mass_index_energy_map()
        self._set_mass_interaction_index_energy_map()
        self._set_zero_body_term_map()

    def _set_index_orbital_map(self):
        """Retrieves the index -> orbital map from a file in the directory
        and stores it in an instance variable
        """
        # Assuming all files characteristic have the same indexing...
        index_orbital_map = index_tuple_map(self.files[0])

        # Turn each tuple in the map into a named tuple
        for k in index_orbital_map.keys():
            v = index_orbital_map[k]
            nextv = QuantumNumbers(*_qnums_to_list(v))
            index_orbital_map[k] = nextv

        self._index_orbital_map = index_orbital_map

    def _set_mass_index_energy_map(self):
        """Retrieves the
            mass number -> orbital index -> energy
        mapping for the directory
        """
        self._mass_index_energy_map = (
            mass_index_energy_map_map(self.dir, filtered_files=self.files))

    def _set_mass_interaction_index_energy_map(self):
        """Retrieves the
            mass number -> (a, b, c, d, j) -> energy
        mapping for the directory
        """
        miiem = (
            mass_interaction_tuple_energy_map_map(self.dir,
                                                  filtered_files=self.files))

        # Turn each tuple into a named tuple
        for A in miiem.keys():
            tuple_energy_map = miiem[A]
            next_tuple_energy_map = dict()
            for k in tuple_energy_map.keys():
                v = tuple_energy_map[k]
                nextk = list()
                for stritem in k:
                    nextk.append(int(stritem))
                nextk = TwoBodyInteraction(*nextk)
                next_tuple_energy_map[nextk] = v
            miiem[A] = next_tuple_energy_map

        self._mass_interaction_index_energy_map = miiem

    def _set_zero_body_term_map(self):
        self._mass_zero_body_term_map = (
            mass_zero_body_term_map(self.dir, filtered_files=self.files))

    def _set_name(self):
        """Sets the incidence name variable
        """
        self.name = name_from_filename(self.files[0])

    def _set_other_constants(self):
        """Sets other heading constants. Assumes all files in a given directory
        have the same constants
        """
        self._other_constants = other_constants_from_filename(self.files[0])

    def _organize_files(self, directory, dir_fmt, file_fmt):
        """Give the files standardized names and put them in a similarly-named
        directory
        :param dir_fmt: the string template for the directory name, should
        allow for the same number of arguments as the length of self.exp
        :param file_fmt: the string template for the file name. This should
        allow for the same number of arguments as the length of self.exp +1 for
        the mass number
        """
        next_files = list()
        arg_list = ([self.name] +
                    [str(i) if i is not None else '' for i in self.exp])
        d = path.join(directory, dir_fmt.format(*arg_list))
        if not path.exists(d):
            mkdir(d)
        for f in self.files:
            mass_num = mass_number_from_filename(f)
            new_f = path.join(d,
                              file_fmt.format(*(arg_list + [mass_num])))
            next_files.append(new_f)
            if not path.exists(new_f):
                link(f, new_f)
        self._unorg_files, self.files = self.files, next_files

    def _standardize_indexing(self):
        self._standardize_mass_index_energy_map_indexing()
        self._standardize_mass_interaction_index_energy_map_indexing()
        self._particular_index_orbital_map = self._index_orbital_map
        self._index_orbital_map = self.standard_index_orbital_map

    def _standardize_mass_index_energy_map_indexing(self):
        """Reformat the mass -> index -> energy map indices to be with respect
        to the standard io_map
        """
        mie_map = self._mass_index_energy_map
        std_mie_map = dict()
        for m, ie_map in mie_map.iteritems():
            std_ie_map = dict()
            for idx, energy in ie_map.iteritems():
                next_idx = self._standard_index(idx)
                std_ie_map[next_idx] = energy
            std_mie_map[m] = std_ie_map
        self._mass_index_energy_map = std_mie_map

    def _standardize_mass_interaction_index_energy_map_indexing(self):
        miie_map = self._mass_interaction_index_energy_map
        std_miie_map = dict()
        for m, iie_map in miie_map.iteritems():
            std_iie_map = dict()
            for ii, energy in iie_map.iteritems():
                next_ii = self._standardize_interaction_index_tuple(ii)
                std_iie_map[next_ii] = energy
            std_miie_map[m] = std_iie_map
        self._mass_interaction_index_energy_map = std_miie_map

    def _standard_orbital_index_map(self):
        return {v: k for k, v in self.standard_index_orbital_map.iteritems()}

    def _standardize_interaction_index_tuple(self, ii_tuple):
        next_tuple = [self._standard_index(i) for i in ii_tuple[0:4]]
        next_tuple += tuple(ii_tuple[4:])
        return TwoBodyInteraction(*next_tuple)

    def _standard_index(self, i):
        io_map = self._index_orbital_map
        soi_map = self._standard_orbital_index_map()
        return soi_map[io_map[i]]

    def index_orbital_map(self):
        return dict(self._index_orbital_map)

    def mass_index_energy_map(self):
        return dict(self._mass_index_energy_map)

    def mass_interaction_index_energy_map(self):
        return dict(self._mass_interaction_index_energy_map)

    def mass_zero_body_term_map(self):
        return dict(self._mass_zero_body_term_map)

    def other_constants(self):
        return list(self._other_constants)

    def folded_mass_interaction_index_energy_map(self):
        """Return a flat version of the map"""
        miie_map = self._mass_interaction_index_energy_map
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
        miie_map = self._mass_interaction_index_energy_map
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
        mie_map = self._mass_index_energy_map
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
            qnums = self._index_orbital_map[index]
            next_tup += qnums
        next_tup += ii.j
        return TwoBodyInteraction(*next_tup)


def _qnums_to_list(qnums):
    qn_list = list()
    for n in qnums:
        if '/' in n:
            sn = n.split('/')
            qn_list.append(float(sn[0]) / float(sn[1]))
        else:
            qn_list.append(float(n))
    return qn_list


class ImsrgDatumLpt(_ImsrgDatum):
    """Stores data maps from *.lpt files and methods for generating new maps
    from these.
    """
    def __init__(self, directory, exp, files,
                 _comment_char_lpt=_CMNT_CHAR,
                 _row_az=_ROW_AZ,
                 _row_head=_ROW_HEAD,
                 _col_start=_COL_START,
                 _row_body_start=_ROW_BODY_START,
                 _ncols_body=_NCOLS_BODY,
                 _regex_filename_int=REGEX_FILENAME_INT,
                 _comment_char_int=CMNT_CHAR_INT,
                 _comment_zbt=CMNT_ZBT):
        super(ImsrgDatumLpt, self).__init__(directory=directory, exp=exp,
                                            files=files)
        self._comment_char_lpt = _comment_char_lpt
        self._row_az = _row_az
        self._row_head = _row_head
        self._col_start = _col_start
        self._row_body_start = _row_body_start
        self._ncols_body = _ncols_body
        self._regex_filename_int = _regex_filename_int
        self._comment_char_int = _comment_char_int
        self._comment_zbt = _comment_zbt

        self._mass_header_map = None
        self._mass_n_body_map = None
        self._mass_zbt_map = None

        self._set_maps()

    def _set_maps(self):
        self._set_mass_header_map()
        self._set_mass_n_body_map()
        self._set_mass_zbt_map()

    def _set_mass_header_map(self):
        self._mass_header_map = mass_to_header_data_map(
            self.files, comment_char=self._comment_char_lpt,
            row_az=self._row_az,
            row_head=self._row_head,
            col_start=self._col_start)

    def _set_mass_n_body_map(self):
        mass_n_body_map = mass_to_n_to_body_data_map(
            self.files, comment_char=self._comment_char_lpt,
            row_az=self._row_az,
            row_body_start=self._row_body_start,
            ncols_body=self._ncols_body)
        d = dict()
        for m, nb_map in mass_n_body_map.iteritems():
            if m not in d:
                d[m] = dict()
            for n, b in nb_map.iteritems():
                d[m][n] = Shell(*b)
        self._mass_n_body_map = d

    def _set_mass_zbt_map(self):
        self._mass_zbt_map = mass_to_zbt_map(
            filtered_filepaths_lpt=self.files,
            filename_int_regex=self._regex_filename_int,
            row_az=self._row_az,
            comment_char_lpt=self._comment_char_lpt,
            comment_char_int=self._comment_char_int,
            zbt_comment=self._comment_zbt)

    def mass_header_map(self):
        return dict(self._mass_header_map)

    def mass_n_body_map(self):
        return dict(self._mass_n_body_map)

    def mass_zbt_map(self):
        return dict(self._mass_zbt_map)

    def mass_n_energy_map(self):
        d = dict()
        for m, nb_map in self._mass_n_body_map.iteritems():
            d[m] = {n: b.E for n, b in nb_map.iteritems()}
        return d

    def mass_n_excitation_map(self):
        d = dict()
        for m, nb_map in self._mass_n_body_map.iteritems():
            d[m] = {n: b.Ext for n, b in nb_map.iteritems()}
        return d

    def n_mass_energy_map(self):
        d = dict()
        mne_map = self.mass_n_energy_map()
        for m, ne_map in mne_map.iteritems():
            for n, e in ne_map.iteritems():
                if n not in d:
                    d[n] = dict()
                d[n][m] = e
        return d

    def n_mass_excitation_map(self):
        d = dict()
        mnext_map = self.mass_n_excitation_map()
        for m, n_ext_map in mnext_map.iteritems():
            for n, ext in n_ext_map.iteritems():
                if n not in d:
                    d[n] = dict()
                d[n][m] = ext
        return d
