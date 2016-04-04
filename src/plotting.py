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


# todo this function is very grody, can we fix it? yes we can!
# todo abstract the plotting part outside of this function; plot_the_plots
# todo   can remain as a wrapper for compatibility
def plot_the_plots(
        plots, title, label, xlabel, ylabel,
        data_line_style='-',
        fit_line_style='--',
        sort_key=lambda plot: plot,
        sort_reverse=False,
        # todo move all string formatting outside of this function
        # todo use const_dict to hold plot-specific labels instead
        title_kwargs=None,  # todo get rid of this parameter
        get_label_kwargs=None,  # todo get rid of this parameter
        idx_key=None,  # todo get rid of this parameter
        fig=None,
        ax=None,
        figsize=PLOT_FIGSIZE,
        cmap_name=PLOT_CMAP,
        cmap=None,
        dark=False,
        # todo remove fit-generation from this method
        # todo calculation and plotting should be entirely disjoint
        show_fit=False,  # todo get rid of this parameter
        fit_params=None,  # todo get rid of this parameter
        fitfn=None,  # todo get rid of this parameter
        num_fit_pts=50,  # todo get rid of this parameter
        include_legend=False,
        legend_size=LEGEND_SIZE,
        code=None,  # todo get rid of this parameter
        savedir=None,  # todo get rid of this parameter
        savename=None,  # todo replace with plot_savepath
        extension='.png',  # todo get rid of this parameter
        use_savename_kwargs=True,  # todo get rid of this parameter
        data_file_savedir=None,  # todo replace with data_file_savepath
        data_file_extension='.dat',  # todo get rid of this parameter
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
        # todo change this so that fits are NOT done inside this function
        # todo instead, they should be included as an extra parameter fit_plots
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
            _set_legend(num_plots=len(plots), legend_size=legend_size, ax=ax)
        else:
            plt.legend()
    # Save
    if savename is not None:
        if use_savename_kwargs:
            # todo no string formatting inside this function
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


def save_plot_figure(
        data_plots, title, xlabel, ylabel, savepath,
        fit_plots=None,
        data_labels=None, fit_labels=None,
        data_line_style='-', fit_line_style='--',
        ax=None, fig=None,
        cmap=None, cmap_name=PLOT_CMAP, dark=False,
        legendsize=LEGEND_SIZE, figsize=PLOT_FIGSIZE,
):
    category_to_plots_map = {'data': data_plots}
    if fit_plots is not None:
        category_to_plots_map.update({'fit': fit_plots})

    category_to_labels_map = dict()
    if data_labels is not None:
        category_to_labels_map.update({'data': data_labels})
    if fit_labels is not None:
        category_to_labels_map.update({'fit': fit_labels})

    category_to_line_style_map = dict()
    if data_line_style is not None:
        category_to_line_style_map.update({'data': data_line_style})
    if fit_line_style is not None:
        category_to_line_style_map.update({'fit': fit_line_style})

    return save_plot_figure_categorical(
        category_to_plots_map=category_to_plots_map,
        category_to_labels_map=category_to_labels_map,
        category_to_line_style_map=category_to_line_style_map,
        title=title, xlabel=xlabel, ylabel=ylabel, savepath=savepath,
        ax=ax, fig=fig, cmap=cmap, cmap_name=cmap_name, dark=dark,
        legendsize=legendsize, figsize=figsize,
    )


def save_plot_figure_categorical(
        category_to_plots_map, title, xlabel, ylabel, savepath,
        category_to_labels_map=None, category_to_line_style_map=None,
        ax=None, fig=None, cmap=None, cmap_name=PLOT_CMAP, dark=False,
        legendsize=LEGEND_SIZE, figsize=PLOT_FIGSIZE,
        _default_line_style='-',
):
    include_legend = category_to_labels_map is not None
    if category_to_labels_map is None:
        category_to_labels_map = dict()
    if category_to_line_style_map is None:
        category_to_line_style_map = dict()
    plot_list_list = list()
    label_list_list = list()
    line_style_list_list = list()
    for category, plot_list in category_to_plots_map.items():
        plot_list_list.append(plot_list)
        if category in category_to_labels_map:
            label_list_list.append(category_to_labels_map[category])
        else:
            label_list_list.append(None)
        if category in category_to_line_style_map:
            line_style_list_list.append(category_to_line_style_map[category])
        else:
            line_style_list_list.append(_default_line_style)

    if fig is None and ax is None:
        fig = plt.figure(figsize=figsize)
    if ax is None:
        ax = fig.add_subplot(111)
    if cmap is None:
        cmap = plt.get_cmap(name=cmap_name)
    if dark:
        plt.style.use(b'dark_background')

    return _save_plot_figure(
        plot_list_list=plot_list_list,
        label_list_list=label_list_list,
        line_style_list_list=line_style_list_list,
        title=title, xlabel=xlabel, ylabel=ylabel,
        savepath=savepath, ax=ax, cmap=cmap, legendsize=legendsize,
        include_legend=include_legend
    )


def _save_plot_figure(
        plot_list_list, title, xlabel, ylabel, savepath,
        label_list_list, line_style_list_list,
        ax, cmap, legendsize, include_legend
):
    num_plots = len(plot_list_list[0])
    c_norm = colors.Normalize(vmin=0, vmax=num_plots-1)
    scalar_map = cm.ScalarMappable(norm=c_norm, cmap=cmap)
    for lop, lol, lols, i in (zip(*plot_list_list), zip(*label_list_list),
                              zip(*line_style_list_list), range(num_plots)):
        for plot, label, line_style in zip(lop, lol, lols):
            x, y = plot[:2]
            ax.plot(x, y, line_style, label=label, color=scalar_map.to_rgba(i))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if include_legend:
        if legendsize is not None:
            _set_legend(num_plots=num_plots, legend_size=legendsize, ax=ax)
        else:
            plt.legend()
    plt.savefig(savepath)


def _set_legend(num_plots, legend_size, ax):
    l = num_plots
    ncol = legend_size.num_cols(l)
    fontsize = legend_size.fontsize(l, ncol)
    box = ax.get_position()
    ax.set_position(
        [box.x0, box.y0,
         box.width * legend_size.width_scale(l, ncol, fontsize),
         box.height])
    plt.legend(ncol=ncol, loc='upper left', bbox_to_anchor=(1.0, 1.0),
               fontsize=fontsize)


def _make_plot_data_file(
        plots, title, xlabel, ylabel, savedir, savename, label,
        get_label_kwargs=None, idx_key=None,
        extension='.dat', comment_str=b''
):
    """Write a data file with the given plot data
    :param plots: sequence containing plots, where each plot is defined as a
    four tuple consisting of (x_array, y_array, const_list, const_dict)
    :param title: title of the plot
    :param xlabel: x axis label
    :param ylabel: y axis label
    :param savedir: directory in which to save the file
    :param savename: name of the file (without extension)
    :param label: label string [template] to be used for each plot
    :param get_label_kwargs: function that when given a plot and a idx_key,
    returns a dictionary mapping label string kwargs to their values for
    formatting
    :param idx_key: something that does something
    :param extension: extension to be used for the data file
    :param comment_str: string to be used to 'comment out' headings and labels
    in the data file
    """
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
