class ImsrgDatum(object):
    def __init__(self, directory, exp, files):
        self.exp = exp
        self.dir = directory
        self.files = files

    def _set_maps(self):
        raise NotImplemented
