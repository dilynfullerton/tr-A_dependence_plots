from __future__ import print_function, division, unicode_literals

import numpy as np
from matplotlib import pyplot as plt

from int.ExpInt import ExpInt
from int.ImsrgDataMapInt import ImsrgDataMapInt
from transforms import identity


def plot_energy_vs_mass_for_interactions(e, hw, filesdir, savedir,
                                         transform=identity,
                                         **kwargs):
    """For a single e, hw pair, along with the main parent directory,
    plots are created for the energy of each (a, b, c, d, j) tuple against
    its mass number.

    keyword arguments:
       verbose=True|False (default False)
           Indicates whether or not to print out the details of the plot.
       show=True|False (default False)
           Indicates whether or not to display the plot on screen
       savename=str (default same as plot title)
           The name to given the plot
           :param transform:
           :param savedir:
           :param filesdir:
           :param hw:
           :param e:
    """
    idm = ImsrgDataMapInt(filesdir)
    idat = idm.map[ExpInt(e=e, hw=hw)]
    iime_map = idat.interaction_index_mass_energy_map()

    fig = plt.figure()
    ax = fig.add_subplot(111)

    plot_map = dict()
    for tup in sorted(iime_map.keys()):
        x = list()
        y = list()
        label = str(tup)

        for mass_num in sorted(iime_map[tup].keys()):
            x.append(mass_num)
            y.append(iime_map[tup][mass_num])
            plot_map[tup] = (x, y)

        x, y = transform(np.array(x), np.array(y))[0:2]
        ax.plot(x, y, '-', label=label)

        if 'verbose' in kwargs and kwargs['verbose'] is True:
            print(tup)
            for p in zip(x, y):
                print(p)
            print()

    plt.xlabel('A')
    plt.ylabel('energy (MeV)')

    title = ('energy vs mass for interactions with '
             'e{e}, hw{hw}').format(e=e, hw=hw)
    plt.title(title)

    if 'savename' in kwargs:
        savename = kwargs['savename']
    else:
        savename = title
    plt.savefig(savedir + '/' + savename + '.png')

    if 'show' in kwargs and kwargs['show']:
        plt.show(block=True)

    return plot_map


def plot_energy_vs_mass_for_orbitals(e, hw, filesdir, savedir,
                                     transform=identity,
                                     **kwargs):
    """For a single (e, hw) pair, along with the main parent directory,
    plots are created for the energy of each orbital against its mass.

    keyword arguments:
       verbose=True|False (default False)
           Indicates whether or not to print out the details of the plot.
       show=True|False (default False)
           Indicates whether or not to display the plot on screen
       savename=str (default same as plot title)
           The name to given the plot
           :param transform:
           :param savedir:
           :param filesdir:
           :param hw:
           :param e:
    """
    idm = ImsrgDataMapInt(filesdir)
    idat = idm.map[ExpInt(e=e, hw=hw)]
    ime_map = idat.index_mass_energy_map()
    io_map = idat.index_orbital_map

    fig = plt.figure()
    ax = fig.add_subplot(111)

    plot_map = dict()
    for index in sorted(ime_map.keys()):
        x = list()
        y = list()
        label = '{i}: {qn}'.format(i=index, qn=io_map[index])

        for mass in sorted(ime_map[index].keys()):
            x.append(mass)
            y.append(ime_map[index][mass])
            plot_map[index] = (x, y)

        x, y = transform(np.array(x), np.array(y))[0:2]
        ax.plot(x, y, '-', label=label)

        if 'verbose' in kwargs and kwargs['verbose']:
            print(label)
            for p in zip(x, y):
                print(p)
            print()

    plt.xlabel('A')
    plt.ylabel('energy (MeV)')

    title = 'energy vs mass for orbitals with e{e}, hw{hw}'.format(e=e, hw=hw)
    plt.title(title)

    if 'savename' in kwargs:
        savename = kwargs['savename']
    else:
        savename = title
    plt.savefig(savedir + '/' + savename + '.png')

    if 'show' in kwargs and kwargs['show']:
        plt.show()

    return plot_map