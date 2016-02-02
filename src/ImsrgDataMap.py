class ImsrgDataMap(object):
    def __init__(self, parent_directory, exp_type, datum_type,
                 exp_list=None, **kwargs):
        self.parent_dir = parent_directory
        self.map = dict()
        if exp_list is not None:
            self.exp_list = [exp_type(*exp_item) for exp_item in exp_list]
        else:
            self.exp_list = None
        self.exp_type = exp_type
        self.datum_type = datum_type
        self.kwargs = kwargs
        self._set_maps()

    def _set_maps(self):
        files = self._get_files()
        for f in files:
            key = self.exp_type(*self._exp_from_file_path(f))
            if self.exp_list is not None and key not in self.exp_list:
                continue
            elif key not in self.map:
                value = self.datum_type(self.parent_dir, key,
                                        **self.kwargs)
                self.map[key] = value

    def _exp_from_file_path(self, f):
        raise NotImplemented

    def _get_files(self):
        raise NotImplemented
