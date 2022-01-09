import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


class AnalysisSPESpectrumData:
    def __init__(self, columns_list: list, data_format: str = "csv"):
        self.columns = columns_list
        self.pandas_data = pd.DataFrame(columns=columns_list)
        self.SPE_spectrum_hist = None
        self.fig = None
        self.ax = None
        self.scale = None

    @classmethod
    def load_from_file(cls, file_path: str):
        read_from_csv_data = pd.read_csv(file_path)
        tmp = cls(read_from_csv_data.columns.to_list())
        for i in range(len(read_from_csv_data)):
            tmp.add_row(*read_from_csv_data.iloc[i].to_list())
        return tmp

    def convert_relpath(self, i_columns: int = 0) -> None:
        for i in range(len(self.pandas_data.iloc[:, i_columns])):
            self.pandas_data.iloc[i, i_columns] = os.path.relpath(self.pandas_data.iloc[i, i_columns])

    def add_row(self, *args: list):
        if len(args) == len(self.columns):
            tmp_dict = dict(zip(self.columns, args))
            self.pandas_data = self.pandas_data.append(tmp_dict, ignore_index=True)
        else:
            print("args is wrong")

    def clear_data(self):
        self.pandas_data.drop(index=self.pandas_data.index, inplace=True)

    def get_info(self):
        return {"shape:": self.pandas_data.shape, "columns_index": self.columns}

    def get_pandas(self):
        return self.pandas_data

    def get_row(self, i_row: int):
        return self.pandas_data.loc[i_row]

    def get_column(self, column: str):
        return self.pandas_data.loc[:, column]

    def draw_SPE_spectrum(self, b_bin: 'float' = None, e_bin: 'float' = None, n_bin=300, i_column: int = 1, show: bool = True, scale: float=1) -> tuple:
        self.scale = scale
        if b_bin is None or e_bin is None:
            b_bin = (scale * self.pandas_data.iloc[:, i_column]).min()
            e_bin = (scale * self.pandas_data.iloc[:, i_column]).max()
        np_bin = np.linspace(b_bin, e_bin, n_bin)
        np_data_set = self.pandas_data.iloc[:, i_column].to_numpy()
        self.fig, self.ax = plt.subplots()
        bin_content, bins, patches = self.ax.hist(self.scale_date(scale, np_data_set), bins=np_bin, histtype='step')
        # ax.hist(np.random.randn(10000), bins=np.linspace(-5, 5, 100))
        self.ax.set_xlabel("Q/C")
        self.ax.set_ylabel("count")
        self.ax.set_title("SPE spectrum")
        if show is True:
            plt.show()
        self.SPE_spectrum_hist = (bin_content, bins, patches)
        return self.SPE_spectrum_hist

    def save_as(self, save_name: str, format: str = "csv"):
        if format == "csv":
            if not save_name.endswith(".csv"):
                save_name = save_name + "." + format
            self.pandas_data.to_csv(save_name, index=False)

    def _model_gaus(self, x: float, p_scale: float=1, p_mean: float=1, p_sigma: float=1) -> float:
        return p_scale / (np.sqrt(2 * np.pi) * p_sigma) * np.exp(-(x - p_mean)**2 / (2 * p_sigma**2))

    def _model_exp(self, x: float, p_alpha: float) -> float:
        return p_alpha * np.exp(-p_alpha * x)

    def _model_QDC(self,x: float, p_scale: float, p_omega: float, p_alpha: float,
                   p_Q_under_amp: float, p_sigma_under_amp: float,
                   p_mu: float, p_Q0: float, p_sigma0: float, p_Q1: float, p_sigma1:float) -> float:
        """
        S_QDC(q) = S_noise + S_ped + S_nSEP
        S_noise = omega * model_exp  + (1 - omega) * model_gaus
        S_ped = Poission(0) * model_gaus
        S_nSEP = Poission(n) * model_gaus
        come from
        https://doi.org/10.1007/s41605-018-0085-8
        """
        S_noise = p_omega * self._model_exp(x, p_alpha) + self._model_gaus(x, 1-p_omega, p_Q_under_amp, p_sigma_under_amp)
        S_ped = np.exp(-p_mu) * self._model_gaus(x, 1, p_Q0, p_sigma0)
        S_nSEP = p_mu * np.exp(-p_mu) * self._model_gaus(x, 1, p_Q1, p_sigma1)
        return p_scale * (S_noise + S_ped + S_nSEP)

    def _value2index_np_left(self, np_data: np.ndarray, value: float) -> int:
        """
        返回的index得到的np_data数值总是在value的左侧
        """
        if value < np_data[0] or value > np_data[-1]:
            print("numpy index is wrong!!")
        else:
            delta = np_data[1] - np_data[0]
            index = int((value - np_data[0])/delta)
            return index

    def _value2index_np_right(self, np_data: np.ndarray, value: float) -> int:
        """
        返回的index得到的np_data数值总是在value的右侧
        """
        if value < np_data[0] or value > np_data[-1]:
            print("numpy index is wrong!!")
        else:
            delta = np_data[1] - np_data[0]
            index = int((value - np_data[0])/delta)
            return index + 1

    def scale_date(self, scale: float, np_data: np.ndarray) -> np.ndarray:
        return scale * np_data



    def fit_with_gaus(self, p0, p1, p2, *interval: float):
        if len(interval) == 2 and interval[0] < interval[1]:
            if self.SPE_spectrum_hist is not None:
                ydata = self.SPE_spectrum_hist[0]
                bins = self.SPE_spectrum_hist[1]
                xdata = ((bins[1]-bins[0])/2 + bins)[:len(bins)-1]
                lower_index = self._value2index_np_left(xdata, interval[0])
                upper_index = self._value2index_np_right(xdata, interval[1])
                xdata_in_interval = xdata[lower_index: upper_index]
                ydata_in_interval = ydata[lower_index: upper_index]
                popt, pcov = curve_fit(self._model_gaus, xdata_in_interval, ydata_in_interval, [p0, p1, p2])
                self.ax.plot(xdata_in_interval, self._model_gaus(xdata_in_interval, *popt))
                # self.ax.scatter(xdata_in_interval, ydata_in_interval, marker="o", color="g")
                plt.show()
                return popt, pcov
        else:
            print("interval is wrong!!")


if __name__ == "__main__":
    pdata = AnalysisSPESpectrumData.load_from_file("tmp_csv.csv")
    pdata.convert_relpath(0)
    aa = pdata.get_pandas()
    print(aa)
