from __future__ import print_function, division, unicode_literals

from constants import FN_PARSE_LPT_REGEX_FILENAME as _RGX_FNAME
from constants import FN_PARSE_NCSMVCE_LPT_REGEX_DNAME as _RGX_DNAME_GGP
from ncsm_vce_lpt.ExpNcsmVceLpt import ExpNcsmVceLpt
from ncsm_vce_lpt.parser import exp
from nushellx_lpt.DataMapNushellxLpt import DataMapNushellxLpt


class DataMapNcsmVceLpt(DataMapNushellxLpt):
    """Data type that stores a map to *.lpt file data, generated by NuShellX
    on interaction files from a VCE of NCSM results
    """
    # noinspection PyUnusedLocal
    def __init__(
            self, parent_directory, exp_list=None, exp_filter_fn=None,
            _regex_filename=_RGX_FNAME, _regex_ggparent_dir=_RGX_DNAME_GGP,
            **kwargs
    ):
        super(DataMapNcsmVceLpt, self).__init__(
            parent_directory=parent_directory,
            exp_list=exp_list, exp_filter_fn=exp_filter_fn,
            _exp_type=ExpNcsmVceLpt,
            _regex_filename=_regex_filename,
            _regex_ggparent_dir=_regex_ggparent_dir
        )

    def _exp_from_file_path(self, f):
        return exp(filepath=f)
