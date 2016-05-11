"""DatumOp.py
Main type in which to store data from Trel *.op files. See Datum.py.
"""
from __future__ import print_function, division, unicode_literals

from Datum import Datum
from constants import F_PARSE_OP_RGX_HERM as _RGX_H
from constants import F_PARSE_OP_RGX_0B as _RGX_0BT
from constants import F_PARSE_OP_RGX_1B as _RGX_1BT
from constants import F_PARSE_OP_RGX_2B as _RGX_2BT
from op.TrelParticles import TrelParticles
from op.TrelParticlesInteraction import TrelParticlesInteraction
from op.QuantumNumbers import QuantumNumbers as Particle
from op.TwoBodyInteraction import TwoBodyInteraction as Interaction
from op.parser import get_data as data


class DatumOp(Datum):
    """Stores a specific subset of all acquired *.op data, as identified by
    the ExpOp
    """
    def __init__(
            self, directory, exp, files,
            _rgx_h=_RGX_H,
            _rgx_0bt=_RGX_0BT,
            _rgx_1bt=_RGX_1BT,
            _rgx_2bt=_RGX_2BT
    ):
        """
        :param directory: path to the main directory from which files were
        retrieved
        :param exp: ExpOp associated with this Datum
        :param files: list of relevant file paths
        :param _rgx_h: regular expression that matches the header line
        :param _rgx_0bt: regular expression that matches the zero body term
        line
        :param _rgx_1bt: regular expression that matches the one body term
        line
        :param _rgx_2bt: regular expression that matches the two body term
        line
        """
        super(DatumOp, self).__init__(
            directory=directory, exp=exp, files=files)
        self._rgx_h = _rgx_h
        self._rgx_0bt = _rgx_0bt
        self._rgx_1bt = _rgx_1bt
        self._rgx_2bt = _rgx_2bt

        self._h_head = None
        self._h_line = None
        self._zbt = None
        self._particles_to_1bt_trel_map = None
        self._particles_interaction_to_2bt_trel_map = None

        self._set_maps()

    def _set_maps(self):
        h_head, h_line, zbt, trel_1bt_map, trel_2bt_map = data(
            filepath=self.files[0],
            rgx_h=self._rgx_h,
            rgx_0bt=self._rgx_0bt,
            rgx_1bt=self._rgx_1bt,
            rgx_2bt=self._rgx_2bt
        )
        self._h_head = h_head
        self._h_line = h_line
        self._zbt = zbt
        self._particles_to_1bt_trel_map = dict()
        for k, v, in trel_1bt_map.items():
            self._particles_to_1bt_trel_map[TrelParticles(*k)] = v
        self._particles_interaction_to_2bt_trel_map = dict()
        for k, v in trel_2bt_map.items():
            next_k = TrelParticlesInteraction(
                Particle(*k[0]), Particle(*k[1]), Interaction(*k[2]))
            self._particles_interaction_to_2bt_trel_map[next_k] = v

    def h_head(self):
        """Returns the top line. I do not know what this is generally. In the
        one file I have, this is just "Hermitian"
        """
        return self._h_head

    def h_line(self):
        """Returns the line following the top header. I do not know what this
        represents generally. In the one file I ahve, this is "0 0 0".
        """
        return self._h_line

    def zbt(self):
        """Returns the zero body term
        """
        return self._zbt

    def particles_to_1bt_trel_map(self):
        """Returns a map from a 2-tuple of particle indices to the
        associated 1 body term
        """
        return dict(self._particles_to_1bt_trel_map)

    def particles_interaction_to_2bt_trel_map(self):
        """Returns a map from a 3-tuple representing the matrix
        element to the associated 2 body term.
            (particle1, particle2, interaction) -> 2 body term
        particle1 and particle2 are 3-tuples (j, p, Tz)
        interaction is a 4-tuple (a, b, c, d)
        """
        return dict(self._particles_interaction_to_2bt_trel_map)

    def particles_to_interaction_to_2bt_trel_map(self):
        """Returns a map
            (particle1, particle2) -> interaction -> 2 body term
        based on particles_interaction_to_2bt_trel_map
        """
        particles_iteraction_trel_map = dict()
        for k, v in self._particles_interaction_to_2bt_trel_map.items():
            particles = TrelParticles(*k[0:2])
            interaction = k[2]
            if particles not in particles_iteraction_trel_map:
                particles_iteraction_trel_map[particles] = dict()
            particles_iteraction_trel_map[particles][interaction] = v
        return particles_iteraction_trel_map

    def interaction_to_particles_to_2bt_trel_map(self):
        """Returns a map
            interaction -> (particle1, particle2) -> 2 body term
        """
        pit_map = self.particles_to_interaction_to_2bt_trel_map()
        ipt_map = dict()
        for k, v in pit_map.items():
            for kk, vv in v.items():
                if kk not in ipt_map:
                    ipt_map[kk] = dict()
                ipt_map[kk][k] = vv
        return ipt_map

    def monopole(self, a, b, ipt_map=None):
        """Calculates the monopole for <a b| V |a b>, based on the given
        a and b
        :param a: first particle index (must be the smaller one, if different)
        :param b: second particle index (must be the larger one, if different)
        :param ipt_map: alternative interaction -> particles -> 2bt map
        :return monopole
        """
        if ipt_map is None:
            ipt_map = self.interaction_to_particles_to_2bt_trel_map()
        try:
            i = Interaction(a, b, a, b)
            pt_map = ipt_map[i]
        except KeyError:
            raise InteractionNotFoundException(
                'There is no data for the interaction {}'.format(i))
        num = 0
        denom = 0
        for k, v in pt_map.items():
            j = k[0].j
            num += (2*j + 1) * v
            denom += (2*j + 1)
        return num / denom

    def interaction_monopole_map(self):
        """Constructs and returns a map from each interaction of the form
            <a b|V|a b> -> monopole
        """
        ipt_map = self.interaction_to_particles_to_2bt_trel_map()
        interaction_monopole_map = dict()
        for k in filter(lambda i: i.a == i.c and i.b == i.d, ipt_map.keys()):
            monopole = self.monopole(a=k.a, b=k.b, ipt_map=ipt_map)
            interaction_monopole_map[k] = monopole
        return interaction_monopole_map


class InteractionNotFoundException(Exception):
    pass
