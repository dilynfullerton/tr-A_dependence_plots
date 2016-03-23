from __future__ import print_function, division, unicode_literals
from os import sep
from DataMap import DataMap
from constants import FN_PARSE_NCSMVCE_OUT_RGX_FNAME as _RGX_FNAME
from parse import matches_completely, get_files_r
from ncsm_out.DatumNcsmVceOut import DatumNcsmVceOut
from ncsm_out.ExpNcsmVceOut import ExpNcsmVceOut
from ncsm_out.parser import exp


class DataMapNcsmVceOut(DataMap):
    """Stores map containing data retrieved from NCSD *.out files
    """
    # noinspection PyUnusedLocal
    def __init__(self, parent_directory, exp_list=None, exp_filter_fn=None,
                 _rgx_fname=_RGX_FNAME, **kwargs):
        self._rgx_fname = _rgx_fname
        super(DataMapNcsmVceOut, self).__init__(
            parent_directory=parent_directory,
            exp_type=ExpNcsmVceOut, datum_type=DatumNcsmVceOut,
            exp_list=exp_list, exp_filter_fn=exp_filter_fn
        )

    def _exp_from_file_path(self, f):
        return exp(filepath=f)

    def _get_files(self):
        def ncsmvce_out_file_filter(filepath):
            filename = filepath[filepath.rfind(sep)+1:]
            return matches_completely(regex=self._rgx_fname, string=filename)

        return get_files_r(directory=self.parent_dir,
                           filterfn=ncsmvce_out_file_filter)

    def aeff_exact_to_ground_state_energy_map(self):
        """Combines the 'aeff_exact_to_ground_state_energy_map' functions
        from all of the map values by taking those with the largest Nhw values
        """
        aeff_energy_map = dict()
        aeff_nhw_map = dict()
        for m in self.map.values():
            for k, v in m.aeff_exact_to_ground_state_energy_map().iteritems():
                if k not in aeff_energy_map or m.exp.Nhw > aeff_nhw_map[k]:
                    aeff_energy_map[k] = v
                    aeff_nhw_map[k] = m.exp.Nhw
        return aeff_energy_map

    def aeff_exact_to_ground_state_energy_map_from_exp(self, exp0):
        """Combines the aeff_exact_to_ground_state_energy_map from the given
        exp0 and that with Nhw one greater.
        :param exp0: exp value
        """
        exp0 = self.exp_type(*exp0)
        # noinspection PyProtectedMember
        kwargs = exp0._asdict()
        kwargs.update({'Nhw': exp0.Nhw + 1})
        exp1 = self.exp_type(**kwargs)
        if exp0 not in self.map or exp1 not in self.map:
            return None
        else:
            dat0 = self.map[exp0]
            dat1 = self.map[exp1]
            m = dat0.aeff_exact_to_ground_state_energy_map()
            m.update(dat1.aeff_exact_to_ground_state_energy_map())
            return m
