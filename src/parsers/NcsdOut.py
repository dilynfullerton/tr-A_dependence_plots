"""NcsdOut.py
Store dat from NCSD output *.out files
"""
from __future__ import print_function, division, unicode_literals
from re import compile
from Parser import Parser
from NcsdEnergyLevel import NcsdEnergyLevel


RGX_SPLIT = compile(b'\s*[=#]\s*|\s+')
RGX_ZN_LINE = compile(b'.*Z\s*=\s*\d+\s+N\s*=\s*\d+')
RGX_BETA_CM_LINE = compile(b'\s*With(out)?\sthe\sc\.o\.m')
RGX_NHW_NMAX_LINE = compile(b'\s*Nhw\s*=\s*\d+\s+Nmax\s*=\s*\d+')
RGX_ENERGY_LEVELS_LINE = compile(b'\s*State\s*#\s*\d+')


class NcsdOut(Parser):
    def __init__(self, filepath):
        self.z = 0
        self.n = 0
        self.hw = 0
        self.beta_cm = 0
        self.nhw = 0
        self.nmax = 0
        self.energy_levels = list()
        super(NcsdOut, self).__init__(filepath)

    def _get_data_zn(self):
        def match_fn(line):
            split_line = RGX_SPLIT.split(line.strip())
            self.z = int(split_line[1])
            self.n = int(split_line[3])
            self.hw = int(float(split_line[5]))
        super(NcsdOut, self)._get_data_line_fn(
            line_regex=RGX_ZN_LINE, match_fn=match_fn,
            data_name='Z, N, and HW')

    def _get_data_beta_cm(self):
        def match_fn(line):
            split_line = line.strip().split()
            if str(split_line[0]) == 'Without':
                self.beta_cm = 0
            else:
                self.beta_cm = float(split_line[-1])
        super(NcsdOut, self)._get_data_line_fn(
            line_regex=RGX_BETA_CM_LINE, match_fn=match_fn,
            data_name='BETA CM')

    def _get_data_nhw_nmax(self):
        def match_fn(line):
            split_line = RGX_SPLIT.split(line.strip())
            self.nhw = int(split_line[1])
            self.nmax = int(split_line[3])
        super(NcsdOut, self)._get_data_line_fn(
            line_regex=RGX_NHW_NMAX_LINE, match_fn=match_fn,
            data_name='NHW and NMAX')

    def _get_data_energy_levels(self):
        def match_fn(line):
            split_line = RGX_SPLIT.split(line.strip())
            e = float(split_line[3])
            j = round(float(split_line[5]), 2)
            t = round(float(split_line[7]), 2)
            self.energy_levels.append(NcsdEnergyLevel(e, j, t))
        super(NcsdOut, self)._get_data_lines_fn(
            line_regex=RGX_ENERGY_LEVELS_LINE, match_fn=match_fn,
            data_name='ENERGY LEVELS'
        )

    def _get_data(self):
        self._get_data_zn()
        self._get_data_beta_cm()
        self._get_data_nhw_nmax()
        self._get_data_energy_levels()


# n = NcsdOut('/Users/Alpha/workspace/triumf/tr-c-ncsm/old/'
#             'results20160716/ncsd/'
#             'o-17_18_Nhw16_15_15/o-17_18_Nhw16_15_15.out')
# print('Z    = {}'.format(n.z))
# print('N    = {}'.format(n.n))
# print('HW   = {}'.format(n.hw))
# print('BETA = {}'.format(n.beta_cm))
# print('NHW  = {}'.format(n.nhw))
# print('NMAX = {}'.format(n.nmax))
# print('Energy levels:')
# for e in n.energy_levels:
#     print(e)
