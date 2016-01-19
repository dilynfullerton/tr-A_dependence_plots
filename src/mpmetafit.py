from __future__ import division
from __future__ import print_function

from spmetafit import *


def _multiparticle_metafit(fitfn, e_hw_pairs, sourcedir, savedir,
                           transform=identity,
                           print_key=False,
                           print_mf_results=False,
                           show_plot=False,
                           sort_key=lambda k: k,
                           code='',
                           xlabel='A',
                           ylabel='Energy (MeV)',
                           cmap='brg'):
    all_data_map = ImsrgDataMap(parent_directory=sourcedir)

    plots = list()
    for e, hw in sorted(e_hw_pairs):
        data_maps = all_data_map.map[Exp(e, hw)]
        io_map = data_maps.index_orbital_map
        iime_map = data_maps.interaction_index_mass_energy_map()

        if print_key is True:
            print_io_key(io_map, sort_key,
                         'Index key for e={e} hw={hw}'.format(e=e, hw=hw))

        # Get list of plots
        for ii in sorted(iime_map.keys()):
            me_map = iime_map[ii]
            iqnums = data_maps.interaction_indices_to_interaction_qnums(ii)

            x, y = map_to_arrays(me_map)
            plots.append(transform(x, y, [iqnums, e, hw, ii]))

            # todo: finish me