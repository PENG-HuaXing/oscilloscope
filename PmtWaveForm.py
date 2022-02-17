import PmtConstant as PC
import numpy as np
from scipy.integrate import trapezoid
import pandas as pd


class WaveForm(object):
    def __init__(self, time: np.ndarray, ampl: np.ndarray):
        """
        信号波形类，记录波形的时间幅度信息，提供一些基本的方法
        1. 特定区间内积分
        2. 特定区间内计算基线
        3. 特定区域内寻找极值
        4. 特定区间内触发判选
        """
        self.time = time
        self.ampl = ampl
        self.bound1 = time[0]
        self.bound2 = time[-1]
        self.delta_time = time[1] - time[0]

    @classmethod
    def load_from_csv(cls, file: str):
        tmp_data = pd.read_csv(file, header=4)
        tmp_t = tmp_data["Time"]
        tmp_a = tmp_data["Ampl"]
        return cls(tmp_t, tmp_a)

    def _value2index(self, value: float) -> int:
        """
        由数值寻找Time序列的index，最终找到的index在
        value值的右侧
        """
        return np.where(self.time > value)[0][0]

    def _interval2index(self, interval1: float, interval2: float) -> np.ndarray:
        """
        通过区间寻找响应的index列表
        """
        interval_index = np.where((self.time - interval1 - (interval2 - interval1)/2) < (interval2 - interval1)/2)[0]
        return interval_index

    def get_time(self) -> np.ndarray:
        return self.time

    def get_ampl(self) -> np.ndarray:
        return self.ampl

    def get_time_bound(self) -> tuple:
        return self.bound1, self.bound2

    def get_delta_time(self) -> float:
        return self.delta_time

    def integrate(self, interval1: float, interval2: float, pedestal: float = 0, method=PC.Wave.Trapezoid):
        """
        对指定区域进行积分，其中枚举TRAPZ为梯形
        积分法；枚举RIEMANN为矩形积分法
        """
        interval_index = self._interval2index(interval1, interval2)
        int_method = method
        if int_method == PC.Wave.Trapezoid:
            int_value = trapezoid(self.ampl[interval_index] - pedestal, self.time[interval_index])
            return int_value
        if int_method == PC.Wave.Riemann:
            int_value = 0
            for i in self.ampl[interval_index]:
                int_value += (i - pedestal)
            return int_value * self.delta_time

    def max_ampl(self, interval1: float, interval2: float) -> tuple:
        interval_index = self._interval2index(interval1, interval2)
        var = self.ampl[interval_index].max()
        index = np.where[np.fabs(self.ampl - var) < 1e-7][0][0]
        return var, index

    def min_ampl(self, interval1: float, interval2: float) -> tuple:
        interval_index = self._interval2index(interval1, interval2)
        var = self.ampl[interval_index].min()
        index = np.where[np.fabs(self.ampl - var) < 1e-7][0][0]
        return var, index

    def trigger(self, threshold: float, interval1, interval2, method=PC.Wave.Below) -> bool:
        """
        在指定区间内判断是否触发，分为两种，分别是上触发
        和下触发。默认情况是下触发，既幅度低于阈值发生触
        发
        """
        tri_method = method
        if tri_method == PC.Wave.Below:
            if self.ampl[self._interval2index(interval1, interval2)].min() < threshold:
                return True
            else:
                return False
        if tri_method == PC.Wave.Above:
            if self.ampl[self._interval2index(interval1, interval2)].max() > threshold:
                return True
            else:
                return False

    def pedestal(self, interval1: float, interval2: float = None, method=PC.Wave.Trapezoid) -> float:
        """
        计算基线，默认使用梯形积分法计算指定区域基线的平均值。
        也可以指定使用矩形积分法计算积分后除以区间长度得到平
        均值。不过积分区间的长度和真正积分区间的长度有所差别
        ，忽略不计
        """
        int_method = method
        if int_method == PC.Wave.Trapezoid:
            value = self.integrate(interval1, interval2, 0, PC.Wave.Trapezoid)
            return value / (interval2 - interval1)
        if int_method == PC.Wave.Riemann:
            value = self.integrate(interval1, interval2, 0, PC.Wave.Riemann)
            return value / (interval2 - interval1)


if __name__ == "__main__":
    data = pd.read_csv("C4--w--07002.csv", header=4)
    wave = WaveForm(data["Time"].to_numpy(), data["Ampl"].to_numpy())
    ped1 = wave.pedestal(wave.get_time_bound()[0], -200e-9)
    ped2 = wave.pedestal(wave.get_time_bound()[0], -200e-9, PC.Wave.Riemann)
    val1 = wave.integrate(-200e-9, 0, 0)
    val2 = wave.integrate(-200e-9, 0, 0, PC.Wave.Riemann)
    pval1 = wave.integrate(-200e-9, 0, ped1)
    pval2 = wave.integrate(-200e-9, 0, ped2, PC.Wave.Riemann)
    print("ped1: {}".format(ped1))
    print("ped2: {}".format(ped2))
    print("method1: {}".format(val1))
    print("method2: {}".format(val2))
    print("method ped1: {}".format(pval1))
    print("method ped2: {}".format(pval2))
