
from ImsrgDataMap import ImsrgDataMap
from ExpLpt import ExpLpt
from ImsrgDatumLpt import ImsrgDatumLpt


class ImsrgDataMapLpt(ImsrgDataMap):
    def __init__(self, parent_directory, exp_list):
        super(ImsrgDataMapLpt, self).__init__(
            parent_directory=parent_directory,
            exp_type=ExpLpt, datum_type=ImsrgDatumLpt,
            exp_list=exp_list)

    def _exp_from_file_path(self, f):
        # todo implement me
        pass

    def _get_files(self):
        # todo implement me
        pass
