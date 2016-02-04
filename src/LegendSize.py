from math import ceil


class LegendSize:
    def __init__(self, max_cols, max_h_space, max_fontsize, total_fontsize,
                 rows_per_col, space_scale):
        self.max_cols = max_cols
        self.max_h_space = max_h_space
        self.max_fontsize = max_fontsize
        self.total_fontsize = total_fontsize
        self.rows_per_col = rows_per_col
        self.space_scale = space_scale

        self.num_cols_map = dict()
        self.fontsize_map = dict()
        self.width_map = dict()

    def num_cols(self, num_plots):
        if num_plots in self.num_cols_map:
            return self.num_cols_map[num_plots]
        else:
            ans = int(
                max(min(ceil(num_plots / self.rows_per_col), self.max_cols), 1))
            self.num_cols_map[num_plots] = ans
            return ans

    def fontsize(self, num_plots, num_cols=None):
        if num_plots in self.fontsize_map:
            return self.fontsize_map[num_plots]
        else:
            if num_cols is None:
                num_cols = self.num_cols(num_plots)
            ans = min(num_cols * self.total_fontsize / num_plots,
                      self.max_fontsize)
            self.fontsize_map[num_plots] = ans
            return ans

    def width_scale(self, num_plots, num_cols=None, fontsize=None):
        if num_plots in self.width_map:
            return self.width_map[num_plots]
        else:
            if num_cols is None:
                num_cols = self.num_cols(num_plots)
            if fontsize is None:
                fontsize = self.fontsize(num_plots, num_cols)
            ans = (1 - (self.max_h_space * num_cols / self.max_cols) *
                   (fontsize / self.max_fontsize) * self.space_scale)
            self.width_map[num_plots] = ans
            return ans
