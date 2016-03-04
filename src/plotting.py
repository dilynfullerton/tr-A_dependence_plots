"""Various functions for plotting in matplotlib
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from os import path

import numpy as np
from matplotlib import pyplot as plt, colors, cm

from FitFunction import FitFunction
from constants import PLOT_CMAP, LEGEND_SIZE, PLOT_FIGSIZE


def plot_the_plots(plots, label, title, xlabel, ylabel,
                   data_line_style='-', fit_line_style='--',
                   sort_key=lambda plot: plot,
                   sort_reverse=False,
                   get_label_kwargs=None, idx_key=None, title_kwargs=None,
                   fig=None, ax=None, cmap_name=PLOT_CMAP, cmap=None,
                   dark=False,
                   show_fit=False, fit_params=None, fitfn=None, num_fit_pts=50,
                   include_legend=False, legend_size=LEGEND_SIZE,
                   savedir=None, savename=None, code=None,
                   use_savename_kwargs=True,
                   extension='.png',
                   figsize=PLOT_FIGSIZE,
                   data_file_savedir=None,
                   data_file_extension='.dat',
                   data_file_comment=b''
                   ):
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
        fig = plt.figure(figsize=figsize)
    if ax is None:
        ax = fig.add_subplot(111)
    # Make color map
    if cmap is None:
        cmap = plt.get_cmap(cmap_name)
    c_norm = colors.Normalize(vmin=0, vmax=len(plots) - 1)
    scalar_map = cm.ScalarMappable(norm=c_norm, cmap=cmap)
    # Do plots
    for p, i in zip(sorted(plots, key=sort_key, reverse=sort_reverse),
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
    if savename is not None:
        if use_savename_kwargs:
            savename_kwargs = {'t': title, 'c': code if code is not None else ''}
            savename = savename.format(**savename_kwargs)
        if savedir is not None:
            plt.savefig(path.join(savedir, savename + extension))
        if data_file_savedir is not None:
            _make_plot_data_file(plots=plots, title=title,
                                 xlabel=xlabel, ylabel=ylabel,
                                 savedir=data_file_savedir, savename=savename,
                                 label=label, get_label_kwargs=get_label_kwargs,
                                 idx_key=idx_key, extension=data_file_extension,
                                 comment=data_file_comment)
    return fig, ax, cmap


def _make_plot_data_file(plots, title, xlabel, ylabel,
                         savedir, savename,
                         label, get_label_kwargs=None, idx_key=None,
                         extension='.dat',
                         comment=b''):
    writelines = list()
    writelines.append(comment + title)
    for p in plots:
        if get_label_kwargs is not None:
            writelines.append(
                comment + label.format(**get_label_kwargs(p, idx_key)))
        else:
            writelines.append(comment + label)
        writelines.append(comment +
                          b'{xl:>16}{yl:>16}'.format(xl=xlabel, yl=ylabel))
        x, y, = p[:2]
        for xi, yi in zip(x, y):
            writelines.append(b'{x:16.8f}{y:16.8f}'.format(x=xi, y=yi))
        writelines.append(b'')
    with open(path.join(savedir, savename+extension), 'w') as fw:
        fw.write(b'{0}\n'.format(b'\n'.join(writelines)))


# x = np.arange(11)
# y1 = x**2
# y2 = x**3
# plots = list()
# plots.append((x, y1, ['x^2']))
# plots.append((x, y2, ['x^3']))
# make_plot_data_file(plots=plots, title='powpow',
#                     xlabel='x', ylabel='f(x)',
#                     label_template='f(x) = {t}',
#                     get_label_kwargs=lambda p, i: {'t': p[2][0]},
#                     idx_key=1,
#                     savedir='../plots',
#                     savename='DATATATATATATATATATAT')


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
