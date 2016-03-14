from __future__ import print_function, division, unicode_literals

import numpy as np
from matplotlib import pyplot as plt

from constants import DIR_SHELL_RESULTS
from nushellx_lpt.DataMapNushellxLpt import DataMapNushellxLpt
from plotting import map_to_arrays, plot_the_plots


def lpt_plot_energy_vs_n_for_mass(mass_num, directory=DIR_SHELL_RESULTS,
                                  exp_list=None, proton_num=None,
                                  transform=None):
    imsrg_data_map = DataMapNushellxLpt(parent_directory=directory,
                                        exp_list=exp_list).map
    plots = list()
    if proton_num is not None:
        items = filter(lambda item: item[0].Z == proton_num,
                       imsrg_data_map.iteritems())
    else:
        items = imsrg_data_map.iteritems()
    for k, v in items:
        mne_map = v.mass_n_energy_map()
        if mass_num in mne_map:
            n_e_map = mne_map[mass_num]
        else:
            continue
        x, y = map_to_arrays(n_e_map)
        const_list = list()
        const_dict = {'exp': k, 'A': mass_num}
        plots.append((x, y, const_list, const_dict))

    if transform is not None:
        plots = [transform(*plot) for plot in plots]

    plot_the_plots(plots,
                   label='{exp}',
                   title='Energy vs N for A={}'.format(mass_num),
                   xlabel='N',
                   ylabel='Energy (MeV)',
                   sort_key=lambda p: p[3]['exp'],
                   get_label_kwargs=lambda p, idx: {'exp': p[3]['exp']},
                   include_legend=True)
    plt.show()


def lpt_plot_energy_vs_mass_for_n(n, directory=DIR_SHELL_RESULTS,
                                  exp_list=None, proton_num=None,
                                  transform=None):
    imsrg_data_map = DataMapNushellxLpt(parent_directory=directory,
                                        exp_list=exp_list).map
    plots = list()
    if proton_num is not None:
        items = filter(lambda item: item[0].Z == proton_num,
                       imsrg_data_map.iteritems())
    else:
        items = imsrg_data_map.iteritems()
    for k, v in items:
        nme_map = v.n_mass_energy_map()
        if n in nme_map:
            me_map = nme_map[n]
        else:
            continue
        x, y = map_to_arrays(me_map)
        const_list = list()
        zbt = np.empty_like(y)
        x_arr, zbt_arr = map_to_arrays(v.mass_zbt_map())
        for xa, zbta, i in zip(x_arr, zbt_arr, range(len(x_arr))):
            if xa in x:
                zbt[i] = zbta
        const_dict = {'exp': k, 'N': n, 'zbt_arr': zbt}
        plots.append((x, y, const_list, const_dict))

    if transform is not None:
        plots = [transform(*plot) for plot in plots]

    plot_the_plots(plots,
                   label='{exp}', title='Energy vs A for N={}'.format(n),
                   xlabel='A', ylabel='Energy (MeV)',
                   sort_key=lambda p: p[3]['exp'],
                   get_label_kwargs=lambda p, idx: {'exp': p[3]['exp']},
                   include_legend=True)
    plt.show()
