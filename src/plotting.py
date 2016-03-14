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


def plot_the_plots(
        plots, title, label, xlabel, ylabel,
        data_line_style='-', fit_line_style='--',
        sort_key=lambda plot: plot, sort_reverse=False,
        title_kwargs=None, get_label_kwargs=None, idx_key=None,
        fig=None, ax=None, figsize=PLOT_FIGSIZE,
        cmap_name=PLOT_CMAP, cmap=None, dark=False,
        show_fit=False, fit_params=None, fitfn=None, num_fit_pts=50,
        include_legend=False, legend_size=LEGEND_SIZE,
        code=None, savedir=None, savename=None, extension='.png',
        use_savename_kwargs=True,
        data_file_savedir=None, data_file_extension='.dat',
        data_file_comment_str=b''
        ):
    """A function for plotting plots. The given plots are plotted (against
    their fits of fit parameters and a fit function are provided)

    :param plots: A sequence of plots. These should be tuples where the first
    2 items are x and y and the remaining are constants (etc.) to be passed to
    the fit function as args (if, that is, a fit function and parameters are
    provided).
    :param title: Title string (template)
    :param label: String (template) to label each plot in plots
    :param xlabel: x axis label
    :param ylabel: y axis label
    :param data_line_style: (Optional) Style of the data lines (a string)
    :param fit_line_style: (Optional) Style of the fit lines (a string)
    :param sort_key: (Optional) Key by which to order the plots
    :param sort_reverse: (Optional) If true, reverses the sort order
    according to the sort key.
    :param title_kwargs: (Optional) Keyword arguments dictionary to use
    to format the plot title
    :param get_label_kwargs: (Optional) Function for retrieving a set
    of keyword arguments for formatting the label string
    :param idx_key: (Optional) Extra key to be provided to the
    get_label_kwargs function as an argument
    :param fig: (Optional) Figure on which to do the plot.
    (One is created here if None)
    :param ax: (Optional) Subplot on which to do the plot.
    (One is created here if None)
    :param figsize: (Optional) 2-tuple (width, height) for the size of the
    plot figure in inches?
    :param cmap_name: (Optional) Name of the color map to use
    :param cmap: (Optional) Cmap object for coloring the plot. If None,
    generates a Cmap based on cmap_name.
    :param dark: (Optional) Use the dark theme?
    :param show_fit: (Optional) If true, shows the fit based on the given
    fit function and fit parameters on the plot.
    :param fit_params: (Optional) Parameters to use to generate a fit.
    (Required in order to plot fits)
    :param fitfn: (Optional) Fit function to use to generate fits.
    (Required in order to plot fits)
    :param num_fit_pts: (Optional) Number of points to plot in the fit
    (linspace arg)
    :param include_legend: (Optional) Whether a legend is to be included
    in the plot
    :param legend_size: (Optional) LegendSize object, which provides
    information on how to size the legend. If None, the default
    formatting is used.
    :param code: (Optional) Code string to use in formatting the savename.
    :param savedir: (Optional) Directory in which to save the plot figure.
    If None, will not save a figure.
    :param savename: (Optional) Name by which the plot [and/or data file] is
    saved.
    :param extension: (Optional) Filename extension for the generated plot
    figure.
    :param use_savename_kwargs: (Optional) If True, formats the savename
    string with keyword arguments c=code and t=title.
    :param data_file_savedir: (Optional) Directory in which the data file is
    to be saved. If None, no data file will be generated.
    :param data_file_extension: (Optional) Extension for the generated data
    file.
    :param data_file_comment_str: (Optional) Character(s) to precede all titles,
    headings, etc. in the generated data file. If the empty string is given,
    no character will precede these fields.
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
            ax.set_position(
                [box.x0, box.y0,
                 box.width * legend_size.width_scale(l, ncol, fontsize),
                 box.height])
            plt.legend(ncol=ncol, loc='upper left', bbox_to_anchor=(1.0, 1.0),
                       fontsize=fontsize)
        else:
            plt.legend()
    # Save
    if savename is not None:
        if use_savename_kwargs:
            savename_kwargs = {'t': title,
                               'c': code if code is not None else ''}
            savename = savename.format(**savename_kwargs)
        if savedir is not None:
            plt.savefig(path.join(savedir, savename + extension))
        if data_file_savedir is not None:
            _make_plot_data_file(
                plots=plots, title=title, xlabel=xlabel, ylabel=ylabel,
                savedir=data_file_savedir, savename=savename,
                label=label, get_label_kwargs=get_label_kwargs,
                idx_key=idx_key, extension=data_file_extension,
                comment_str=data_file_comment_str)
    return fig, ax, cmap


def _make_plot_data_file(plots, title, xlabel, ylabel,
                         savedir, savename,
                         label, get_label_kwargs=None, idx_key=None,
                         extension='.dat',
                         comment_str=b''):
    writelines = list()
    writelines.append(comment_str + title)
    for p in plots:
        if get_label_kwargs is not None:
            writelines.append(
                comment_str + label.format(**get_label_kwargs(p, idx_key)))
        else:
            writelines.append(comment_str + label)
        writelines.append(comment_str +
                          b'{xl:>16} {yl:>16}'.format(xl=xlabel, yl=ylabel))
        x, y, = p[:2]
        for xi, yi in zip(x, y):
            writelines.append(b'{x:16.8f} {y:16.8f}'.format(x=xi, y=yi))
        writelines.append(b'')
    with open(path.join(savedir, savename + extension), 'w') as fw:
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
    :param m: map to refactor
    """
    length = len(m)
    x = np.empty(length)
    y = np.empty(length)
    for k, i in zip(sorted(m.keys()), range(length)):
        x[i] = k
        y[i] = m[k]
    return x, y
