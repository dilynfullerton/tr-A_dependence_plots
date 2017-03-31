"""NushellxInt.py
Store dat from Nushell Interaction *.int files
"""
from __future__ import print_function, division, unicode_literals
from re import compile
from Parser import Parser, ItemNotFoundInFileException
from NushellOrbital import NushellOrbital
from NushellTbme import NushellTbme


RGX_ZERO_BODY_TERM = compile('.*Zero\sbody\sterm:')
RGX_INDEX_LINE = compile('^\s*!(\s+\d+){5}')
RGX_SINGLE_PARTICLE_ENERGIES = compile('-999')
RGX_TWO_BODY_MATRIX_ELEMENTS = compile('\s*(\d+\s+){6}-?\d+\.\d+')
RGX_PRESC_LINE = compile('^\s*!\s*Effective')
RGX_PRESC_STR = compile('.*\s*\d+,\s*\d+,\s*\d+\s*.*')


class NushellxInt(Parser):
    def __init__(self, filepath):
        self.a_prescription = None
        self.zero_body_term = 0
        self.index_map = dict()
        self.single_particle_energies = list()
        self.two_body_matrix_elements = dict()
        super(NushellxInt, self).__init__(filepath)

    def _get_a_prescription(self):
        def match_fn(line):
            presc_str = compile('=').split(line.strip())[-1]
            if RGX_PRESC_STR.match(presc_str):
                stripped = presc_str.strip('[]() ')
                presc = compile('\s*,\s*').split(stripped)
                self.a_prescription = tuple([int(p) for p in presc])
            else:
                self.a_prescription = (int(presc_str.strip()),) * 3
        try:
            super(NushellxInt, self)._get_data_line_fn(
                line_regex=RGX_PRESC_LINE, match_fn=match_fn,
                data_name='A PRESCRIPTION')
        except ItemNotFoundInFileException:
            pass

    def _get_zero_body_term(self):
        def match_fn(line):
            self.zero_body_term = float(line.strip().split(' ')[-1])
        super(NushellxInt, self)._get_data_line_fn(
            line_regex=RGX_ZERO_BODY_TERM, match_fn=match_fn,
            data_name='ZERO BODY TERM')

    def _get_index_map(self):
        def match_fn(line):
            nums = map(lambda s: int(s), line.strip().split()[1:])
            self.index_map[nums[0]] = NushellOrbital(*nums[1:])
        super(NushellxInt, self)._get_data_lines_fn(
            line_regex=RGX_INDEX_LINE, match_fn=match_fn,
            data_name='INDEX MAP')

    def _get_single_particle_energies(self):
        def match_fn(line):
            nums = map(lambda s: float(s), line.strip().split()[1:])
            self.single_particle_energies.extend(nums[:len(self.index_map)])
        super(NushellxInt, self)._get_data_lines_fn(
            line_regex=RGX_SINGLE_PARTICLE_ENERGIES, match_fn=match_fn,
            data_name='SINGLE PARTICLE ENERGIES')

    def _get_two_body_matrix_elements(self):
        def match_fn(line):
            tbme = map(lambda s: int(s), line.strip().split()[:6])
            value = float(line.strip().split()[-1])
            self.two_body_matrix_elements[NushellTbme(*tbme)] = value
        super(NushellxInt, self)._get_data_lines_fn(
            line_regex=RGX_TWO_BODY_MATRIX_ELEMENTS, match_fn=match_fn,
            data_name='TWO BODY MATRIX ELEMENTS')

    def _get_data(self):
        self._get_a_prescription()
        self._get_zero_body_term()
        self._get_index_map()
        self._get_single_particle_energies()
        self._get_two_body_matrix_elements()


# n = NushellxInt('/Users/Alpha/workspace/triumf/tr-c-nushellx/old/'
#                 'results20160716/Z8/vce/'
#                 'vce_presc16,17,18_Nmax2_15_15_shell2_dim2/A20/A20.int')
#
# print('Zero body term = {}'.format(n.zero_body_term))
# print('Index map:')
# for k, v in n.index_map.items():
#     print('  {}: {}'.format(k, v))
# print('Single particle energies:')
# for spe in n.single_particle_energies:
#     print('  {}'.format(spe))
# print('Two body matrix elements:')
# for k, v in n.two_body_matrix_elements.items():
#     print('  {}: {}'.format(k, v))
