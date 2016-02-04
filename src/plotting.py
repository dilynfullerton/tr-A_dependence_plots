"""Simple plots
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from os import path

import numpy as np
from matplotlib import pyplot as plt, colors, cm

from Exp import ExpInt
from FitFunction import FitFunction
from ImsrgDataMap import ImsrgDataMapInt, ImsrgDataMapLpt
from constants import DIR_SHELL_RESULTS
from constants import PLOT_CMAP, LEGEND_SIZE
from fit_transforms import identity


def plot_the_plots(plots, label, title, xlabel, ylabel,
                   data_line_style='-', fit_line_style='--',
                   sort_key=lambda plot: plot,
                   get_label_kwargs=None, idx_key=None, title_kwargs=None,
                   fig=None, ax=None, cmap_name=PLOT_CMAP, cmap=None,
                   dark=False,
                   show_fit=False, fit_params=None, fitfn=None, num_fit_pts=50,
                   include_legend=False, legend_size=LEGEND_SIZE,
                   savedir=None, savename=None, code=None):
    """A function for plotting plots. The given plots are plotted (against
    their fits of fit parameters and a fit function are provided)

    :param code:
    :param savename:
    :param savedir:
    :param show_fit:
    :param cmap:
    :param plots: A sequence of plots. These should be tuples where the first
    2 items are x and y and the remaining are constants (etc.) to be passed to
    the fit function as args (if, that is, a fit function and parameters are
    provided).
    :param label: The string (template) to label each plot in plots
    :param title: The title string (template)
    :param xlabel: The x axis label
    :param ylabel: The y axis label
    :param cmap_name: The name of the color map to use
    :param data_line_style: The style of the data lines (a string)
    :param fit_line_style: The style of the fit lines (a string)
    :param sort_key: The key by which to order the plots
    :param get_label_kwargs: A function for retrieving a set of keyword
    arguments for formatting the label string
    :param idx_key: An extra key to be provided to the get_label_kwargs
    function as an argument
    :param title_kwargs: The keyword arguments dictionary to use to format
    the plot title
    :param fig: A figure on which to do the plot. (One is created here if None)
    :param ax: A subplot on which to do the plot. (One is created here if None)
    :param dark: Use the dark theme?
    :param fit_params: Parameters to use to generate a fit. (Required in order
    to plot fits)
    :param fitfn: A fit function to use to generate fits. (Required in order
    to plot fits)
    :param num_fit_pts: The number of points to plot in the fit (linspace arg)
    :param include_legend: Whether a legend is to be included in the plot
    :param legend_size: The LegendSize object, which provides information on
    how to size the legend. If None, the default formatting is used.
    :return: the figure, subplot, and cmap objects
    """
    if dark:
        plt.style.use(b'dark_background')
    if fig is None:
        fig = plt.figure()
    if ax is None:
        ax = fig.add_subplot(111)
    # Make color map
    if cmap is None:
        cmap = plt.get_cmap(cmap_name)
    c_norm = colors.Normalize(vmin=0, vmax=len(plots) - 1)
    scalar_map = cm.ScalarMappable(norm=c_norm, cmap=cmap)
    # Do plots
    for p, i in zip(sorted(plots, key=sort_key),
                    range(len(plots))):
        x, y = p[0:2]
        if get_label_kwargs is not None:
            label_i = label.format(**get_label_kwargs(p, idx_key))
        cval = scalar_map.to_rgba(i)
        ax.plot(x, y, data_line_style, label=label_i, color=cval)
        # Do fits if parameters and function provided
        if show_fit:
            xfit = np.linspace(x[0], x[-1], num=num_fit_pts)
            if isinstance(fitfn, FitFunction):
                args = list([fit_params])
            else:
                args = list(fit_params)
            args.extend(p[2:])
            yfit = np.array(list(map(lambda xi: fitfn(xi, *args), xfit)))
            ax.plot(xfit, yfit, fit_line_style, color=cval)
    # Label plot
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if title_kwargs is not None:
        title = title.format(**title_kwargs)
    plt.title(title)
    # Add legend
    if include_legend:
        if legend_size is not None:
            l = len(plots)
            ncol = legend_size.num_cols(l)
            fontsize = legend_size.fontsize(l, ncol)
            box = ax.get_position()
            ax.set_position([box.x0, box.y0,
                             box.width * legend_size.width_scale(l, ncol,
                                                                 fontsize),
                             box.height])
            plt.legend(ncol=ncol, loc='upper left', bbox_to_anchor=(1.0, 1.0),
                       fontsize=fontsize)
        else:
            plt.legend()
    # Save
    if savedir is not None and savename is not None:
        savename_kwargs = {'t': title, 'c': code if code is not None else ''}
        plt.savefig(
            path.join(savedir, savename + '.png').format(**savename_kwargs))
    return fig, ax, cmap


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


def lpt_plot_energy_vs_n_for_mass(mass_num, directory=DIR_SHELL_RESULTS,
                                  exp_list=None, proton_num=None,
                                  transform=None):
    imsrg_data_map = ImsrgDataMapLpt(parent_directory=directory,
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
                   sort_key=lambda plot: plot[3]['exp'],
                   get_label_kwargs=lambda plot, idx: {'exp': plot[3]['exp']},
                   include_legend=True)
    plt.show()


def lpt_plot_energy_vs_mass_for_n(n, directory=DIR_SHELL_RESULTS,
                                  exp_list=None, proton_num=None,
                                  transform=None):
    imsrg_data_map = ImsrgDataMapLpt(parent_directory=directory,
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
                   label='{exp}',
                   title='Energy vs A for N={}'.format(n),
                   xlabel='A',
                   ylabel='Energy (MeV)',
                   sort_key=lambda plot: plot[3]['exp'],
                   get_label_kwargs=lambda plot, idx: {'exp': plot[3]['exp']},
                   include_legend=True)
    plt.show()


def map_to_arrays(m):
    """Convert a map of dimensionality 2 into an x and y array
    :param m: The map to refactor
    """
    length = len(m)
    x = np.empty(length)
    y = np.empty(length)
    for k, i in zip(sorted(m.keys()), range(length)):
        x[i] = k
        y[i] = m[k]
    return x, y
