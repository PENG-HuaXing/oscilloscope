import numpy as np
import PmtConstant as PmtC
from scipy.optimize import curve_fit


class SpeHist(object):
    def __init__(self, charge: np.ndarray, bins: np.ndarray = None, scale: float = 1):
        """
        此类是将SPE数据转化为histogram的类，初始化需要Q值，
        （可选：bins，scale）其中scale主要是为了更好的计
        算拟合参数
        """
        self.scale = scale
        self.scale_charge = scale * charge
        if bins is None:
            self.edge1 = self.scale_charge.min()
            self.edge2 = self.scale_charge.max()
            self.bin_num = 300
            self.bins = np.linspace(self.edge1, self.edge2, self.bin_num + 1)
            self.hist_content, _ = np.histogram(self.scale_charge, self.bins)
        else:
            self.edge1 = self.scale_charge.min()
            self.edge2 = self.scale_charge.max()
            self.bin_num = len(bins) - 1
            self.bins = bins
            self.hist_content, _ = np.histogram(self.scale_charge, self.bins)
        self.scatter_x = self.bins[1:] - (self.bins[1] - self.bins[0]) / 2
        self.scatter_y = self.hist_content

    def _interval2index(self, interval1: float, interval2: float) -> np.ndarray:
        """
        通过区间寻找响应的index列表
        """
        interval_index = np.where(np.fabs(self.scatter_x - interval1 - (interval2 - interval1)/2) < (interval2 - interval1)/2)[0]
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
    def signal_noise(x: float, omega: float, alpha: float, q_under_amp: float, sigma_under_amp: float):
        s_noise = omega * SpeHist.model_exp(x, alpha) + SpeHist.model_gauss(x, 1 - omega, q_under_amp, sigma_under_amp)
        return s_noise

    @staticmethod
    def signal_ped(x: float, mu: float, q0: float, sigma0: float):
        s_ped = np.exp(-mu) * SpeHist.model_gauss(x, 1, q0, sigma0)
        return s_ped

    @staticmethod
    def signal_spe(x: float, mu: float, q1: float, sigma1: float):
        s_spe = mu * np.exp(-mu) * SpeHist.model_gauss(x, 1, q1, sigma1)
        # return s_spe / (mu * np.exp(-mu))
        return SpeHist.model_gauss(x, 1, q1, sigma1)

    @staticmethod
    def model_qdc(x: float, p_scale: float, p_omega: float, p_alpha: float,
                  p_q_under_amp: float, p_sigma_under_amp: float, p_mu: float, p_q0: float,
                  p_sigma0: float, p_q1: float, p_sigma1: float, p_scale_noise: float) -> float:
        """
        S_QDC(q) = S_noise + S_ped + S_nSEP
        S_noise = omega * model_exp  + (1 - omega) * model_gaus
        S_ped = Poission(0) * model_gauss
        S_nSEP = Poission(n) * model_gauss
        come from
        https://doi.org/10.1007/s41605-018-0085-8
        """
        s_noise = SpeHist.signal_noise(x, p_omega, p_alpha, p_q_under_amp, p_sigma_under_amp)
        s_ped = SpeHist.signal_ped(x, p_mu, p_q0, p_sigma0)
        s_n_spe = SpeHist.signal_spe(x, p_mu, p_q1, p_sigma1)
        return p_scale * (s_ped + s_n_spe) + p_scale_noise * s_noise

    def fit_spe(self, model=PmtC.Fit.Gauss, interval1: float = None, interval2: float = None, *param) -> tuple:
        """
        拟合方法，可对指定区域进行gauss拟合，也可以
        对全域进行多种函数的复合拟合。返回数值为元组
        其中包含拟合参数,拟合参数的方差
        """
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
                print(len(param))
                print(param)
                ppot, pcov = curve_fit(SpeHist.model_qdc, self.scatter_x, self.scatter_y, param)
                return ppot, pcov
            else:
                print(len(param))
                print(param)
                print("parameter is wrong")
                return None, None


if __name__ == "__main__":
    from PmtSinglePhotonSpectrum import SinglePhotonSpectrum
    import matplotlib.pyplot as plt
    # 类初始化
    spe = SinglePhotonSpectrum.load_csv("1353V.csv")
    spe_hist = SpeHist(spe.get_charge(), scale=-1e11)
    cont, bins = spe_hist.get_hist()
    # 输出散点数据
    with open("scatter.txt", "w") as f:
        for i in range(len(spe_hist.get_scatter()[0])):
            row = str(spe_hist.get_scatter()[0][i]) + "\t" + str(spe_hist.get_scatter()[1][i]) + "\n"
            f.write(row)
    # 高斯拟合
    param, p_cov = spe_hist.fit_spe(PmtC.Fit.Gauss, 2, 6, 100, 2, 3)
    # 全域拟合
    global_param = [200, 0.4, 10, 0.1, 1, 0.1, 0.1, 0.5, 3, 1, 10]
    gp, gc = spe_hist.fit_spe(PmtC.Fit.QDC, 1, 1, *global_param)
    print("全域拟合参数: {}".format(gp))
    # 绘制曲线
    fig, ax = plt.subplots()
    ax.hist(spe_hist.get_scatter()[0], bins, weights=cont, histtype="step")
    ax.plot(bins, SpeHist.model_gauss(bins, *param))

    # 绘制论文曲线
    # pp = [6.28e4, 0.392, 38.7, 450.7, 8.941, 0.1055, 442.7, 1.732, 529.5, 28.36, 269.6]
    # x = np.linspace(400, 750, 300)
    # xx = np.linspace(400, 750, 1000)
    # 绘制曲线
    # f, a = plt.subplots()
    # a.plot(xx, SpeHist.model_qdc(xx, *pp))
    # a.plot(x, pp[0] * SpeHist.signal_ped(x, pp[5], pp[6], pp[7]))
    # a.plot(x, pp[0] * SpeHist.signal_spe(x, pp[5], pp[8], pp[9]))
    # a.plot(x, pp[10] * SpeHist.signal_noise(x, pp[1], pp[2], pp[3], pp[4]))

    plt.show()
    # 输出散点数据到txt文件中

