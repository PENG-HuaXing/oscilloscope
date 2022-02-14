import numpy as np
import pandas as pd
import scipy.integrate as integrate
from Waveform import Waveform


class AfterPulse(object):
    def __init__(self, file: str, signal_trigger: float = 0, after_pulse_trigger: float = 0):
        self.after_pulse_trigger = after_pulse_trigger
        self.signal_trigger = signal_trigger
        self.origin_data = pd.read_csv(file)
        self.filter_data = None

    def get_filter_data(self):
        return self.filter_data

    def set_signal_trigger(self, trigger: float):
        self.signal_trigger = trigger

    def set_after_pulse_trigger(self, trigger: float):
        self.after_pulse_trigger = trigger

    def filter_under_Q(self):
        self.filter_data = self.origin_data[self.origin_data['Q'] < self.signal_trigger]

    def filter_over_Q(self):
        self.filter_data = self.origin_data[self.origin_data['Q'] > self.signal_trigger]

    def search_after_pulse(self, signal_file: str, after_pulse_region: float, integral_window: float, ped: float = 0):
        time = []
        ampl = []
        wave_data = pd.read_csv(signal_file, header=4)
        after_pulse_data = wave_data[wave_data["Time"] > after_pulse_region]
        after_pulse_time = after_pulse_data["Time"].to_numpy()
        after_pulse_ampl = after_pulse_data["Ampl"].to_numpy()
        index = list(np.where(after_pulse_ampl < self.after_pulse_trigger)[0])
        span = int(integral_window / (after_pulse_time[1] - after_pulse_time[0]))
        while True:
            integral_index = []
            if len(index) == 0:
                break
            else:
                index_end_of_window = index[0] + span
                # print("index_end_of_windows: {}".format(index_end_of_window))
                while True:
                    if index[0] < index_end_of_window:
                        integral_index.append(index[0])
                        index.pop(0)
                        if len(index) == 0:
                            break
                    else:
                        break
            # print(integral_index)
            if len(integral_index) == 1:
                local_min = after_pulse_ampl[integral_index[0]]
                local_min_index = integral_index[0]
            else:
                local_min = after_pulse_ampl[integral_index[0]: integral_index[-1]].min()
                local_min_index = np.where((after_pulse_ampl - local_min) < 1e-9)[0][0]
            begin_index = int(local_min_index - span/2)
            end_index = int(local_min_index + span/2)
            if begin_index >= 0 and end_index < len(after_pulse_time):
                value = integrate.trapezoid(after_pulse_ampl[begin_index: end_index] - ped, after_pulse_time[begin_index: end_index])
                time.append(after_pulse_time[local_min_index])
                ampl.append(value)
        return time, ampl

    def loop_and_save(self):
        after_pulse_data = []
        columns = ["File", "Time", "Q"]
        for i in range(len(self.filter_data)):
            print(self.filter_data["File"].iloc[i])
            tmp_t, tmp_a = self.search_after_pulse(self.filter_data["File"].iloc[i], 0, 100e-9, self.filter_data["pedestal"].iloc[i])
            t_a_data = list(zip(tmp_t, tmp_a))
            # print("t_a_data: {}".format(t_a_data))
            for j in t_a_data:
                row = list(j)
                row.insert(0, self.filter_data["File"].iloc[i])
                # print("row: {}".format(row))
                # print(row)
                after_pulse_data.append(row)
                # print(after_pulse_data)
            # print("after_pulse: {}".format(after_pulse_data))
        pd_data = pd.DataFrame(after_pulse_data, columns=columns)
        pd_data.to_csv("After_Pulse.csv")


if __name__ == "__main__":
    af = AfterPulse("/run/media/einstein/Elements/CR160_data/1353V.csv", -0.15e-10, -0.002)
    af.filter_under_Q()
    data = af.get_filter_data()
    # tim, amp = af.search_after_pulse("/run/media/einstein/Elements/CR160_data/CR160_-1353V_LED_3.7V_1kHz_29.8ns_20us_SyncTrigger/C4--w--00668.csv",0, 100e-9)
    af.loop_and_save()
    # print("time: {}".format(tim))
    # print("amp: {}".format(amp))

















