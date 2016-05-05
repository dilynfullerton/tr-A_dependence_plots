"""LegendSize.py
Class definition for LegendSize, which specifies how a legend should be
sized for matplotlib plots
"""
from __future__ import division
from math import ceil


class LegendSize:
    """A class to store the constants and methods for generating a nice legend
    outside the subplot area (matplotlib)
    """
    def __init__(self, max_cols, max_h_space, max_fontsize, min_fontsize,
                 total_fontsize, rows_per_col, space_scale):
        """Initialize a LegendSize instance
        :param max_cols: maximum allowed number of columns for the legend
        :param max_h_space: maximum proportion of horizontal space to be
        apportioned to the legend
        :param max_fontsize: maximum font size for legend labels
        :param min_fontsize: minimum font size for legend labels
        :param total_fontsize: value of font size * number of rows
        :param rows_per_col: number of rows in a column
        :param space_scale: some sort of scale factor or something
        """
        self.max_cols = max_cols
        self.max_h_space = max_h_space
        self.max_fontsize = max_fontsize
        self.min_fontsize = min_fontsize
        self.total_fontsize = total_fontsize
        self.rows_per_col = rows_per_col
        self.space_scale = space_scale

    def num_cols(self, num_plots):
        """Returns the number of columns the legend will have
        :param num_plots: number of plots
        """
        if self.max_cols is not None:
            return int(
                max(min(ceil(num_plots / self.rows_per_col), self.max_cols), 1))
        else:
            return int(max(ceil(num_plots / self.rows_per_col), 1))

    def fontsize(self, num_plots, num_cols=None):
        """Returns the font size for labels in the legend
        :param num_plots: number of plots
        :param num_cols: number of columns for the legend
        """
        if num_cols is None:
            num_cols = self.num_cols(num_plots)
        if num_plots > 0:
            return max(min(num_cols * self.total_fontsize / num_plots,
                           self.max_fontsize), self.min_fontsize)
        else:
            return self.min_fontsize

    def width_scale(self, num_plots, num_cols=None, fontsize=None):
        """Returns the scale factor for the width of the axis box
        :param num_plots: number of plots
        :param num_cols: number of columns in the legend
        :param fontsize: legend label font size
        """
        if num_cols is None:
            num_cols = self.num_cols(num_plots)
        if fontsize is None:
            fontsize = self.fontsize(num_plots, num_cols)
        if self.max_cols is not None:
            return (1 - (self.max_h_space * num_cols / self.max_cols) *
                    (fontsize / self.max_fontsize) * self.space_scale)
        else:
            return 1 - self.max_h_space * (fontsize / self.max_fontsize)
