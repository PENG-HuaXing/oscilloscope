import numpy as np
import PmtConstant as PmtC
from scipy.optimize import curve_fit


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

    def _interval2index(self, interval1: float, interval2: float) -> np.ndarray:
        """
        通过区间寻找响应的index列表
        """
        interval_index = np.where((self.scatter_x - interval1 - (interval2 - interval1)/2) < (interval2 - interval1)/2)[0]
        return interval_index

    def get_scatter(self) -> tuple:
        return self.scatter_x, self.scatter_y

    def get_hist(self) -> tuple:
        return self.hist_content, self.bins

    def get_info(self) -> dict:
        return {"bound1": self.edge1, "bound2": self.edge2, "bin_num": self.bin_num, "scale": self.scale}

    @staticmethod
    def model_gauss(x: float, p_scale: float = 1, p_mean: float = 1, p_sigma: float = 1) -> float:
        return p_scale / (np.sqrt(2 * np.pi) * p_sigma) * np.exp(-(x - p_mean) ** 2 / (2 * p_sigma ** 2))

    @staticmethod
    def model_exp(x: float, p_alpha: float) -> float:
        return p_alpha * np.exp(-p_alpha * x)

    @staticmethod
    def model_QDC(self, x: float, p_scale: float, p_omega: float, p_alpha: float,
                  p_Q_under_amp: float, p_sigma_under_amp: float, p_mu: float, p_Q0: float,
                  p_sigma0: float, p_Q1: float, p_sigma1: float) -> float:
        """
        S_QDC(q) = S_noise + S_ped + S_nSEP
        S_noise = omega * model_exp  + (1 - omega) * model_gaus
        S_ped = Poission(0) * model_gaus
        S_nSEP = Poission(n) * model_gaus
        come from
        https://doi.org/10.1007/s41605-018-0085-8
        """
        S_noise = p_omega * SpeHist.model_exp(x, p_alpha) + self._model_gaus(x, 1 - p_omega, p_Q_under_amp,
                                                                             p_sigma_under_amp)
        S_ped = np.exp(-p_mu) * SpeHist.model_gauss(x, 1, p_Q0, p_sigma0)
        S_nSEP = p_mu * np.exp(-p_mu) * SpeHist.model_gauss(x, 1, p_Q1, p_sigma1)
        return p_scale * (S_noise + S_ped + S_nSEP)

    def fit_spe(self, model=PmtC.Fit.Gauss, interval1: float = None, interval2: float = None, *param) -> tuple:
        mod = model
        if mod == PmtC.Fit.Gauss:
            if interval1 is None or interval2 is None:
                print("Interval wrong!")
                return None, None
            else:
                ppot, pcov = curve_fit(SpeHist.model_gauss, self.scatter_x[self._interval2index(interval1, interval2)],
                                       self.scatter_y[self._interval2index(interval1, interval2)],
                                       param)
                return ppot, pcov
        if mod == PmtC.Fit.QDC:
            if len(param) >= 10:
                ppot, pcov = curve_fit(SpeHist.model_QDC, self.scatter_x, self.scatter_y, param)
                return ppot, pcov
            else:
                print("parameter is wrong")
                return None, None


if __name__ == "__main__":
    print("Hello")
    pass
