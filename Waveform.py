import numpy as np
import scipy.integrate as integrate
from matplotlib import pyplot as plt


class Waveform:
    def __init__(self, np_time: np.ndarray, np_amp: np.ndarray):
        # data
        self.time = np_time
        self.amp = np_amp
        # info
        self.minTime = np_time[0]
        self.maxTime = np_time[-1]
        self.delta_Time = np_time[1] - np_time[0]
        self.pedestal = np.nan

    def reload(self, np_time: np.ndarray, np_amp: np.ndarray):
        self.time = np_time
        self.amp = np_amp
        self.minTime = np_time[0]
        self.maxTime = np_time[-1]
        self.delta_Time = np_time[1] - np_time[0]
        self.pedestal = np.nan

    def clear_all(self):
        self.time = np.zeros(0)
        self.amp = np.zeros(0)
        self.minTime = np.nan
        self.maxTime = np.nan
        self.delta_Time = np.nan

    def clear_info(self):
        self.minTime = np.nan
        self.maxTime = np.nan
        self.delta_Time = np.nan

    def clear_data(self):
        self.time = np.zeros(0)
        self.amp = np.zeros(0)

    def _value2index_lowerbound(self, lvalue: float) -> int:
        """
        函数的作用主要是将外部输入的时间数值上下限转换为np_Time的index
        其中下限np_Time[index]数值在输入数值的左侧
        """
        if lvalue <= self.minTime or lvalue >= self.maxTime:
            print("The lower bound out of range!!")
            return 0
        else:
            return int((lvalue - self.minTime) / self.delta_Time)

    def _value2index_upperbound(self, uvalue) -> int:
        """
        函数的作用主要是将外部输入的时间数值上下限转换为np_Time的index
        其中上限np_Time[index]的数值在输入数值的右侧
        """
        if uvalue <= self.minTime or uvalue >= self.maxTime:
            print("The upper bound out of range!!")
            return len(self.time) - 1
        else:
            return int((uvalue - self.minTime) / self.delta_Time + 1)

    def define_pedestal(self, *args: 'float, float'):
        _sum = 0
        if len(args) == 1:
            upper = self._value2index_upperbound(args[0])
            ped_integral = integrate.trapezoid(self.amp[:upper+1], self.time[:upper+1])
            self.pedestal = ped_integral / (self.time[upper] - self.time[0])
        elif len(args) == 2:
            lower = self._value2index_lowerbound(args[0])
            upper = self._value2index_upperbound(args[1])
            ped_integral = integrate.trapezoid(self.amp[lower:upper+1], self.time[lower:upper+1])
            self.pedestal = ped_integral / (self.time[upper] - self.time[lower])
        elif len(args) == 4:
            lower1 = self._value2index_lowerbound(args[0])
            lower2 = self._value2index_lowerbound(args[2])
            upper1 = self._value2index_upperbound(args[1])
            upper2 = self._value2index_upperbound(args[3])
            ped_integral1 = integrate.trapezoid(self.amp[lower1:upper1+1], self.time[lower1: upper1+1])
            ped_integral2 = integrate.trapezoid(self.amp[lower2:upper2+1], self.time[lower2: upper2+1])
            self.pedestal = ped_integral1 + ped_integral2 / (self.time[upper1] + self.time[upper2]-self.time[lower1]-self.time[lower2])
        else:
            print("Interval illegal!!")

    def integral_trapz(self, *interval: 'float, float') -> float:
        """:var
        python比较中需要注意is和==的差别
        特别是np.nan == np.nan返回为False 但是 np.nan is np.nan返回为True
        """
        if len(interval) == 0:
            return integrate.trapezoid(self.amp, self.time)
        elif len(interval) == 2 and interval[0] <= interval[1]:
            lower_index = self._value2index_lowerbound(interval[0])
            upper_index = self._value2index_upperbound(interval[1])
            return integrate.trapezoid(self.amp[lower_index:upper_index+1], self.time[lower_index:upper_index+1])
        else:
            print("Integrate is wrong!!")

    def integral_trapz_on_pedestal(self, *interval: 'float, float') -> float:
        if len(interval) == 2 and interval[0] <= interval[1]:
            lower_index = self._value2index_lowerbound(interval[0])
            upper_index = self._value2index_upperbound(interval[1])
            if self.pedestal is not np.nan:
                return integrate.trapezoid(self.amp[lower_index:upper_index+1]-self.pedestal, self.time[lower_index:upper_index+1])
            else:
                print("Pedestal is Nan!!")
        else:
            print("Integrate is wrong!!")

    def integral_simpson(self, *interval: 'float, float', pedestal: bool = False) -> float:
        if len(interval) == 0:
            return integrate.simpson(self.amp, self.time)
        elif len(interval) == 2 and interval[0] <= interval[1]:
            lower_index = self._value2index_lowerbound(interval[0])
            upper_index = self._value2index_upperbound(interval[1])
            if pedestal is False:
                return integrate.simpson(self.amp[lower_index:upper_index+1], self.time[lower_index:upper_index+1])
            elif pedestal is True and self.pedestal is not np.nan:
                return integrate.simpson(self.amp[lower_index:upper_index+1]-self.pedestal, self.time[lower_index:upper_index+1])
            else:
                print("Pedestal is Nan!!")
        else:
            print("Integrate is wrong!!")

    @staticmethod
    def static_integral_simpson(np_sample_y: np.array, np_sample_x: np.array, method: str = "trapziod") -> float:
        if method == "simpson":
            return integrate.simpson(np_sample_y, np_sample_x)
        elif method == "trapzoid":
            return integrate.trapezoid(np_sample_y, np_sample_x)
        else:
            print("Method is wrong!!")
            return 0

    def get_info(self):
        return {"minTime": self.minTime, "maxTime": self.maxTime, "delta_Time": self.delta_Time, "pedestal": self.pedestal}

    def get_time(self):
        return self.time

    def get_amp(self):
        return self.amp

    def get_ped(self):
        return self.pedestal

    def get_max_amp(self, *interval: 'float, float') -> tuple:
        if len(interval) == 0:
            max_value = np.max(self.amp)
            max_index = np.where(self.amp == max_value)[0][0]
            return max_value, max_index
        elif len(interval) == 2 and interval[0] <= interval[1]:
            lower_index = self._value2index_lowerbound(interval[0])
            upper_index = self._value2index_upperbound(interval[1])
            max_value = np.max(self.amp[lower_index:upper_index+1])
            relative_max_index = np.where(self.amp[lower_index:upper_index+1] == max_value)[0][0]
            max_index = relative_max_index + lower_index
            return max_value, max_index
        else:
            print("Interval is wrong!!")

    def get_min_amp(self, *interval: 'float, float') -> tuple:
        if len(interval) == 0:
            min_value = np.min(self.amp)
            min_index = np.where(self.amp == min_value)[0][0]
            return min_value, min_index
        elif len(interval) == 2 and interval[0] <= interval[1]:
            lower_index = self._value2index_lowerbound(interval[0])
            upper_index = self._value2index_upperbound(interval[1])
            min_value = np.min(self.amp[lower_index:upper_index+1])
            relative_min_index = np.where(self.amp[lower_index:upper_index+1] == min_value)[0][0]
            min_index = relative_min_index + lower_index
            return min_value, min_index
        else:
            print("Interval is wrong!!")

    def trigger(self, trigger_value: float, *args: 'float,float') -> 'bool, list':
        if len(args) == 0:
            index_array = np.where(self.amp < trigger_value)[0]
            if index_array.size > 0:
                trigger_bool = True
            else:
                trigger_bool = False
            return trigger_bool, index_array
        elif len(args) == 2 and args[0] < args[1]:
            lower_index = self._value2index_lowerbound(args[0])
            upper_index = self._value2index_upperbound(args[1])
            tmp_index_array = np.where(self.amp[lower_index:upper_index+1] < trigger_value)[0]
            if tmp_index_array.size > 0:
                trigger_bool = True
            else:
                trigger_bool = False
            return trigger_bool, lower_index + tmp_index_array
        else:
            print("Interval is wrong")

    def wave_draw(self, *interval):
        fig, ax = plt.subplots(1, 1)
        if len(interval) == 0:
            ax.plot(self.time, self.amp, marker=".")
        elif len(interval) == 2 and interval[0] < interval[1]:
            lower_index = self._value2index_lowerbound(interval[0])
            upper_index = self._value2index_upperbound(interval[1])
            ax.plot(self.time[lower_index:upper_index + 1], self.amp[lower_index:lower_index + 1], marker=".")
        else:
            print("Interval set wrong!!")
            ax.plot(self.time, self.amp)
        ax.grid(True)
        ax.set_xlabel("time/s")
        ax.set_ylabel("voltage/V")
        fig.tight_layout()
        plt.show()


if __name__ == "__main__":
    import csv
    file_path = "../_-300_-2300_-2800_LED_1KHz_9V_28ns_-656ns-2/C2--w--06193.csv"
    f = open(file_path, "r")
    csv_str_data = list(csv.reader(f))[5:]
    time_and_amp = list(map(list, zip(*csv_str_data)))
    time_data = np.array(list(map(float, time_and_amp[0])))
    amp_data = np.array(list(map(float, time_and_amp[1])))
    wave = Waveform(time_data, amp_data)
    wave.wave_draw()
    wave.define_pedestal(0, 1.1e-6)
    print(wave.get_info())
    print("tra integral method: {}".format(wave.integral_trapz(0, 100e-9)))
    print("tra integral on pedestal method: {}".format(wave.integral_trapz_on_pedestal(0, 100e-9)))
    print("simpson integral method: {}".format(wave.integral_simpson(0, 100e-9)))
    print("max value amp; {}".format(wave.get_max_amp(0, 100e-9)))
