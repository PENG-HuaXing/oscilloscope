import numpy as np
from PmtConstant import Fit
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
    def gauss(x: float, scale: float = 1, mean: float = 1, sigma: float = 1) -> float:
        return scale / (np.sqrt(2 * np.pi) * sigma) * np.exp(-(x - mean) ** 2 / (2 * sigma ** 2))

    @staticmethod
    def noise_exp(x: float, alpha: float, q0: float = 0) -> float:
        return np.heaviside(x-q0, 1) * alpha * np.exp(-alpha * (x - q0))

    @staticmethod
    def poisson(n: int, mu: float):
        n = int(n)
        return mu ** n * np.exp(-mu) / np.math.factorial(n)

    @staticmethod
    def s_ped(x: float, mu: float, q0: float, sigma0: float):
        s_ped = SpeHist.poisson(0, mu) * SpeHist.gauss(x, 1, q0, sigma0)
        return s_ped

    @staticmethod
    def s_ped_noise(x: float, w: float, alpha: float, mu: float, q0: float, sigma0: float):
        s_ped_noise = w * SpeHist.noise_exp(x, alpha, q0) + SpeHist.gauss(x, 1 - w, q0, sigma0)
        return SpeHist.poisson(0, mu) * s_ped_noise

    @staticmethod
    def n_gauss(x: float, mu: float, q0: float, q1: float, sigma1: float, n: int = 2, qsh: float = 0):
        n = int(n)
        return SpeHist.poisson(n, mu) * SpeHist.gauss(x, 1, q0 + qsh + n * q1, np.sqrt(n) * sigma1)

    @staticmethod
    def signal_n_spe(x: float, mu: float, q0: float, q1: float, sigma1: float, qsh: float = 0):
        n = 5
        value = 0
        for i in range(1, n + 1):
            value = value + SpeHist.poisson(i, mu) * SpeHist.gauss(x, 1, q0 + qsh + i * q1, np.sqrt(i) * sigma1)
        return value

    @staticmethod
    def global_model(x: float, amp: float, mu: float, q0: float, sigma0: float, q1:float, sigma1:float):
        term1 = SpeHist.s_ped(x, mu, q0, sigma0)
        term2 = SpeHist.signal_n_spe(x, mu, q0, q1, sigma1)
        return amp * (term1 + term2)

    @staticmethod
    def global_noise_model(x: float, amp: float, w: float, alpha: float, mu: float, q0: float, sigma0: float, q1: float,
                           sigma1: float):
        term1 = SpeHist.s_ped_noise(x, w, alpha, mu, q0, sigma0)
        term2 = SpeHist.signal_n_spe(x, mu, q0, q1, sigma1, w/alpha)
        return amp * (term1 + term2)

    def fit_spe(self, model=Fit.Gauss, interval1: float = None, interval2: float = None, *param) -> tuple:
        """
        拟合方法，可对指定区域进行gauss拟合，也可以
        对全域进行多种函数的复合拟合。返回数值为元组
        其中包含拟合参数,拟合参数的方差
        len(param) == 6                 len(param) == 8
        param[0][0]: amp                param[0][0]: amp
        param[1][0]: mu					param[1][0]: w
        param[2][0]: q0					param[2][0]: alpha
        param[3][0]: sigma0				param[3][0]: mu
        param[4][0]: q1					param[4][0]: q0
        param[5][0]: sigma1				param[5][0]: sigma0
                                        param[6][0]: q1
                                        param[7][0]: sigma1
        """
        mod = model
        if mod == Fit.Gauss:
            if interval1 is None or interval2 is None:
                print("Interval wrong!")
                return None, None
            elif len(param) == 3:
                par = []
                bounds = []
                for i in param:
                    par.append(i[0])
                    bounds.append((i[1], i[2]))
                fit_par, par_cov = curve_fit(SpeHist.gauss, self.scatter_x[self._interval2index(interval1, interval2)],
                                             self.scatter_y[self._interval2index(interval1, interval2)], par,
                                             bounds=list(zip(*bounds)))
                return fit_par, par_cov
            else:
                print("参数错误: {}".format(param))
                return None, None
        if mod == Fit.Global:
            if len(param) == 6:
                par = []
                bounds = []
                for i in param:
                    par.append(i[0])
                    bounds.append((i[1], i[2]))
                fit_par, par_cov = curve_fit(SpeHist.global_model, self.scatter_x, self.scatter_y, par,
                                             bounds=list(zip(*bounds)))
                return fit_par, par_cov
            else:
                print("参数错误: {}".format(param))
        if mod == Fit.GlobalNoise:
            if len(param) == 8:
                par = []
                bounds = []
                for i in param:
                    par.append(i[0])
                    bounds.append((i[1], i[2]))
                fit_par, par_cov = curve_fit(SpeHist.global_noise_model, self.scatter_x, self.scatter_y, par,
                                             bounds=list(zip(*bounds)))
                return fit_par, par_cov
            else:
                print("参数错误: {}".format(param))


if __name__ == "__main__":
    from PmtSinglePhotonSpectrum import SinglePhotonSpectrum
    import matplotlib.pyplot as plt
    # 类初始化
    bins = np.linspace(-4, 25, 300)
    spe = SinglePhotonSpectrum.load_csv("/run/media/einstein/Elements/2022_2_25_CR160_data/windows_0_250ns_spe.csv")
    spe_hist = SpeHist(spe.get_charge(), bins, scale=-1e11)
    cont, bins = spe_hist.get_hist()
    # 全局拟合无噪声
    # global_par, _ = spe_hist.fit_spe(Fit.Global, 1, 1, [3000, -np.inf, np.inf], [0.5, 0, 1], [0, -np.inf, np.inf], [0.1, 0, np.inf], [5, -np.inf, np.inf], [1, 0, np.inf])
    # print("双高斯拟合参数: {}".format(global_par))
    # 全局拟合有噪声
    global_par, _ = spe_hist.fit_spe(Fit.GlobalNoise, 1, 1, [3100, -np.inf, np.inf], [0.4, 0, 1], [5, -np.inf, np.inf], [0.5, 0, 1], [0.1, -np.inf, np.inf], [0.4, 0, np.inf], [4.6, 4, 5], [1.5, 0, 2])
    print("拟合参数: {}".format(global_par))

    # 绘制曲线
    fig, ax = plt.subplots()
    ax.hist(spe_hist.get_scatter()[0], bins, weights=cont, histtype="step")
    bins = np.linspace(-4, 25, 1000)
    ax.plot(bins, SpeHist.global_noise_model(bins, *global_par))
    ax.plot(bins, global_par[0] * (1-global_par[1]) * SpeHist.s_ped(bins, global_par[3], global_par[4], global_par[5]), "--")
    ax.plot(bins, global_par[0] * global_par[1] * SpeHist.poisson(0, global_par[3]) * SpeHist.noise_exp(bins, global_par[2], global_par[4]), "--")
    ax.plot(bins, global_par[0] * SpeHist.n_gauss(bins, global_par[3], global_par[4], global_par[6], global_par[7], 1), "--")
    ax.plot(bins, global_par[0] * SpeHist.n_gauss(bins, global_par[3], global_par[4], global_par[6], global_par[7], 2), "--")
    ax.plot(bins, global_par[0] * SpeHist.n_gauss(bins, global_par[3], global_par[4], global_par[6], global_par[7], 3), "--")
    ax.plot(bins, global_par[0] * SpeHist.n_gauss(bins, global_par[3], global_par[4], global_par[6], global_par[7], 4), "--")
    ax.plot(bins, global_par[0] * SpeHist.n_gauss(bins, global_par[3], global_par[4], global_par[6], global_par[7], 5), "--")
    plt.show()
    # 输出散点数据到txt文件中

