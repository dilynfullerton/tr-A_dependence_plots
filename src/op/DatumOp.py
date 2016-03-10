from __future__ import print_function, division, unicode_literals

from Datum import Datum
from constants import F_PARSE_OP_CMNT_CHAR as _CMNT_CHAR
from constants import F_PARSE_OP_REGEX_HERM as _REGEX_H
from constants import F_PARSE_OP_REGEX_0B as _REGEX_0BT
from constants import F_PARSE_OP_REGEX_1B as _REGEX_1BT
from constants import F_PARSE_OP_REGEX_2B as _REGEX_2BT
from op.TrelParticles import TrelParticles
from op.TrelParticlesInteraction import TrelParticlesInteraction
from op.QuantumNumbers import QuantumNumbers as Particle
from op.TwoBodyInteraction import TwoBodyInteraction as Interaction
from op.parse_op import get_data as data


class DatumOp(Datum):
    def __init__(self, directory, exp, files,
                 _comment_char=_CMNT_CHAR,
                 _regex_h=_REGEX_H,
                 _regex_0bt=_REGEX_0BT,
                 _regex_1bt=_REGEX_1BT,
                 _regex_2bt=_REGEX_2BT):
        super(DatumOp, self).__init__(directory=directory,
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

        self._set_maps()

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
        for k, v, in trel_1bt_map.iteritems():
            self._particles_to_1bt_trel_map[TrelParticles(*k)] = v
        self._particles_interaction_to_2bt_trel_map = dict()
        for k, v in trel_2bt_map.iteritems():
            next_k = TrelParticlesInteraction(Particle(*k[0]), Particle(*k[1]),
                                              Interaction(*k[2]))
            self._particles_interaction_to_2bt_trel_map[next_k] = v

    def h_head(self):
        return self._h_head

    def h_line(self):
        return self._h_line

    def zbt(self):
        return self._zbt

    def particles_to_1bt_trel_map(self):
        return dict(self._particles_to_1bt_trel_map)

    def particles_interaction_to_2bt_trel_map(self):
        return dict(self._particles_interaction_to_2bt_trel_map)

    def particles_to_interaction_to_2bt_trel_map(self):
        particles_iteraction_trel_map = dict()
        for k, v in self._particles_interaction_to_2bt_trel_map.iteritems():
            particles = TrelParticles(*k[0:2])
            interaction = k[2]
            if particles not in particles_iteraction_trel_map:
                particles_iteraction_trel_map[particles] = dict()
            particles_iteraction_trel_map[particles][interaction] = v
        return particles_iteraction_trel_map

    def interaction_to_particles_to_2bt_trel_map(self):
        pit_map = self.particles_to_interaction_to_2bt_trel_map()
        ipt_map = dict()
        for k, v in pit_map.iteritems():
            for kk, vv in v.iteritems():
                if kk not in ipt_map:
                    ipt_map[kk] = dict()
                ipt_map[kk][k] = vv
        return ipt_map

    def monopole(self, a, b, ipt_map=None):
        if ipt_map is None:
            ipt_map = self.interaction_to_particles_to_2bt_trel_map()
        try:
            i = Interaction(a, b, a, b)
            pt_map = ipt_map[i]
        except KeyError:
            raise InteractionNotFoundException('There is no data for the'
                                               'interaction {}'.format(i))
        num = 0
        denom = 0
        for k, v in pt_map.iteritems():
            j = k[0].j
            num += (2*j + 1) * v
            denom += (2*j + 1)
        return num / denom

    def interaction_monopole_map(self):
        ipt_map = self.interaction_to_particles_to_2bt_trel_map()
        interaction_monopole_map = dict()
        for k in filter(lambda i: i.a == i.c and i.b == i.d, ipt_map.keys()):
            monopole = self.monopole(a=k.a, b=k.b, ipt_map=ipt_map)
            interaction_monopole_map[k] = monopole
        return interaction_monopole_map


class InteractionNotFoundException(Exception):
    pass
