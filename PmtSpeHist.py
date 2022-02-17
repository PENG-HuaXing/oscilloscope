import numpy as np
import pandas as pd


class SpeHist(object):
    def __init__(self, charge: np.ndarray, bins: np.ndarray = None, scale: float = 1):
        self.scale = scale
        self.scale_charge = scale * charge
        if bins is None:
            self.edge1 = self.scale_charge.min()
            self.edge2 = self.scale_charge.max()
            self.bin_num = 300
            self.bins = scale * np.linspace(self.edge1, self.edge2, self.bin_num + 1)
            self.hist_content, _ = np.histogram(charge, bins)
        else:
            self.edge1 = self.scale_charge.min()
            self.edge2 = self.scale_charge.max()
            self.bin_num = len(bins) - 1
            self.bins = bins
            self.hist_content, _ = np.histogram(charge, bins)
        self.scatter_x = bins[1:] - (bins[1] - bins[0]) / 2
        self.scatter_y = self.hist_content

    def get_scatter(self):
        return self.scatter_x, self.scatter_y

    def get_hist(self):



