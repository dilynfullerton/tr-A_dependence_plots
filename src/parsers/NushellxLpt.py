"""NushellxLpt.py
Store dat from Nushell output *.lpt files
"""
from __future__ import print_function, division, unicode_literals
from re import compile
from Parser import Parser
from LptEnergyLevel import LptEnergyLevel
from Parser import ItemNotFoundInFileException

RGX_SPLIT = compile(b'\s*[=#]\s*|\s+')
RGX_AZ_LINE = compile(b'.*a\s*=\s*\d+\s+z\s*=\s*\d+')
RGX_SPE_LINE = compile(b'\s*\w+(\s+-?\d+\.\d+\w+){3,}')
RGX_ENERGY_LEVEL_LINE = compile(b'.*\d+\s+\d+(\s+-?\d+\.\d+){2}')


class NushellxLpt(Parser):
    def __init__(self, filepath):
        self.a = 0
        self.z = 0
        self.single_particle_energies = list()
        self.energy_levels = list()
        super(NushellxLpt, self).__init__(filepath)

    def _get_data_az(self):
        def match_fn(line):
            self.a = int(RGX_SPLIT.split(line.strip())[1])
            self.z = int(RGX_SPLIT.split(line.strip())[3])
        try:
            super(NushellxLpt, self)._get_data_line_fn(
                line_regex=RGX_AZ_LINE, match_fn=match_fn, data_name='A and Z')
        except ItemNotFoundInFileException as e:
            print(e.message)
            raise  # critical issue: raise

    def _get_data_spe(self):
        def match_fn(line):
            try:
                nums = map(lambda s: float(s), line.strip().split()[3:-1])
            except ValueError:
                raise ItemNotFoundInFileException(
                    'Could not parse single particle energies')
            self.single_particle_energies.extend(nums)
        try:
            super(NushellxLpt, self)._get_data_lines_fn(
                line_regex=RGX_SPE_LINE, match_fn=match_fn,
                data_name='SINGLE PARTICLE ENERGIES'
            )
        except ItemNotFoundInFileException as e:
            print(e.message)  # non-critical: continue

    def _get_data_energy_levels(self):
        def match_fn(line):
            split_line = line.strip().split()
            n = int(split_line[0])
            nj = int(split_line[1])
            e = float(split_line[2])
            p = int(split_line[6])
            if '/' in split_line[4]:
                j = (float(split_line[4].split('/')[0]) /
                     float(split_line[4].split('/')[1]))
            else:
                j = float(split_line[4])
            if '/' in split_line[5]:
                t = (float(split_line[5].split('/')[0]) /
                     float(split_line[5].split('/')[1]))
            else:
                t = float(split_line[5])
            self.energy_levels.append(LptEnergyLevel(n, nj, e, j, t, p))
        try:
            super(NushellxLpt, self)._get_data_lines_fn(
                line_regex=RGX_ENERGY_LEVEL_LINE, match_fn=match_fn,
                data_name='ENERGY LEVELS'
            )
        except ItemNotFoundInFileException as exc:
            print(exc.message)  # non-critical issue: continue
        self.energy_levels = sorted(self.energy_levels, key=lambda x: x.E)

    def _get_data(self):
        self._get_data_az()
        self._get_data_spe()
        self._get_data_energy_levels()


# n = NushellxLpt('~/workspace/triumf/tr-c-nushellx/old/'
#                 'results20160716/Z8/vce/'
#                 'vce_presc16,17,18_Nmax2_15_15_shell2_dim2/A20/o_20y.lpt')
# print('A = {}'.format(n.a))
# print('Z = {}'.format(n.z))
# print('Single particle energies:')
# for spe in n.single_particle_energies:
#     print(spe)
# print('Energy levels:')
# for e in n.energy_levels:
#     print(e)
