from __future__ import print_function, division, unicode_literals

from ImsrgDatum import ImsrgDatum
from constants import F_PARSE_OP_CMNT_CHAR as _CMNT_CHAR
from constants import F_PARSE_OP_REGEX_HERM as _REGEX_H
from constants import F_PARSE_OP_REGEX_0B as _REGEX_0BT
from constants import F_PARSE_OP_REGEX_1B as _REGEX_1BT
from constants import F_PARSE_OP_REGEX_2B as _REGEX_2BT
from op.TrelOneBody import TrelOneBody
from op.TrelTwoBody import TrelTwoBody
from op.QuantumNumbers import QuantumNumbers as Particle
from op.TwoBodyInteraction import TwoBodyInteraction as Interaction
from op.parse_op import get_data as data


class ImsrgDatumOp(ImsrgDatum):
    def __init__(self, directory, exp, files,
                 _comment_char=_CMNT_CHAR,
                 _regex_h=_REGEX_H,
                 _regex_0bt=_REGEX_0BT,
                 _regex_1bt=_REGEX_1BT,
                 _regex_2bt=_REGEX_2BT):
        super(ImsrgDatumOp, self).__init__(directory=directory,
                                           exp=exp,
                                           files=files)
        self._comment_char = _comment_char
        self._regex_h = _regex_h
        self._regex_0bt = _regex_0bt
        self._regex_1bt = _regex_1bt
        self._regex_2bt = _regex_2bt

        self._h_head = None
        self._h_line = None
        self._zbt = None
        self._particles_to_1bt_trel_map = None
        self._particles_interaction_to_2bt_trel_map = None

    def _set_maps(self):
        h_head, h_line, zbt, trel_1bt_map, trel_2bt_map = data(
            filepath=self.files[0],
            comment_char=self._comment_char,
            regex_h=self._regex_h,
            regex_0bt=self._regex_0bt,
            regex_1bt=self._regex_1bt,
            regex_2bt=self._regex_2bt
        )
        self._h_head = h_head
        self._h_line = h_line
        self._zbt = zbt
        self._particles_to_1bt_trel_map = dict()
        for k, v, in trel_1bt_map:
            self._particles_to_1bt_trel_map[TrelOneBody(*k)] = v
        self._particles_interaction_to_2bt_trel_map = dict()
        for k, v in trel_2bt_map:
            next_k = TrelTwoBody(Particle(*k[0]), Particle(*k[1]),
                                 Interaction(*k[2]))
            self._particles_interaction_to_2bt_trel_map[next_k] = v
