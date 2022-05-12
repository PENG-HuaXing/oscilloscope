import numpy as np
import pandas as pd
import scipy.integrate as integrate
from PmtDataSetTool import DataSetTool
from PmtConstant import AfterPulse as Ap
import PmtWaveForm


class AfterPulse(object):
    def __init__(self, pd_data: pd.DataFrame, ap_trigger: float, ap_window: float, ap_region1: float,
                 ap_region2: float, ped_flag=Ap.Pedestal):
        self.pd_data = pd_data
        self.ap_trigger = ap_trigger
        self.ap_window = ap_window
        self.ap_region = [ap_region1, ap_region2]
        self.ped_flag = ped_flag

    @staticmethod
    def search_after_pulse(signal_file: str, after_pulse_trigger: float, after_pulse_region: float,
                           integral_window: float, ped: float = 0) -> tuple:
        """
        该静态方法几个参数signal_file: 波形文件名；after_pulse_region: 后脉冲
        时间区域（从该参数到时间末尾的区域）；interval_window: 积分时间窗口长度
        ；ped: 基线参数
        函数的主要思想分为以下几步
        1. 读取波形文件，寻找Ampl小于after_pulse_trigger的时间index并记录在
        index列表中
        2. 计算出integral_window时间内的波形时间index跨度，记录为span
        3. 将index内span跨度的index为一组作为integral_index，并且寻找
        出该时间index跨度内ampl的极小值，作为后脉冲的时间点local_min_index
        4. 在local_min_index前后找半个span的index，作为计算积分时候所用的
        时间和信号幅度索引
        """
        time = []
        ampl = []
        print(signal_file)
        waveclass = PmtWaveForm.WaveForm.load_from_file(signal_file)
        wave_data = pd.DataFrame({"Time": waveclass.get_time(), "Ampl": waveclass.get_ampl()})
        after_pulse_data = wave_data[wave_data["Time"] > after_pulse_region]
        after_pulse_time = after_pulse_data["Time"].to_numpy()
        after_pulse_ampl = after_pulse_data["Ampl"].to_numpy()
        index = list(np.where(after_pulse_ampl < after_pulse_trigger)[0])
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
                local_min_index = np.where(np.fabs(after_pulse_ampl - local_min) < 1e-9)[0][0]
            begin_index = int(local_min_index - span / 2)
            end_index = int(local_min_index + span / 2)
            if begin_index >= 0 and end_index < len(after_pulse_time):
                value = integrate.trapezoid(after_pulse_ampl[begin_index: end_index] - ped,
                                            after_pulse_time[begin_index: end_index])
                time.append(after_pulse_time[local_min_index])
                ampl.append(value)
        return time, ampl

    @staticmethod
    def zip_data(file_name: str, data_time: list, data_ampl: list) -> list:
        """
        本函数主要对search_after_pulse得到的时间，幅度列表进行转换
        初始的时间，幅度数据[time1, time2, time3], [amp1, amp2, amp3]，并且无)
        波形文件参数，经过本函数转换后得到的数据形式为：
        [[file1, time1, amp1],
         [file1, time2, amp2],
         [file1, time3, amp3]]
         更加容易写入到pandas数据中
        """
        after_pulse_data = []
        t_a_data = list(zip(data_time, data_ampl))
        for i in t_a_data:
            row = list(i)
            row.insert(0, file_name)
            after_pulse_data.append(row)
        return after_pulse_data

    def loop_all(self, save_file: str) -> None:
        data_list = []
        columns = ["File", "Time", "Q"]
        for i in range(len(self.pd_data)):
            file_name = self.pd_data["File"].iloc[i]
            print(file_name)
            if self.ped_flag == Ap.Pedestal:
                tmp_t, tmp_a = AfterPulse.search_after_pulse(file_name, self.ap_trigger, self.ap_region[0],
                                                             self.ap_window)
            else:
                tmp_t, tmp_a = AfterPulse.search_after_pulse(file_name, self.ap_trigger, self.ap_region[0],
                                                             self.ap_window, self.pd_data["ped"].iloc[i])
            tmp_data_list = AfterPulse.zip_data(file_name, tmp_t, tmp_a)
            for row in tmp_data_list:
                data_list.append(row)
        output_data = pd.DataFrame(data_list, columns=columns)
        output_data.to_csv(save_file)


if __name__ == "__main__":
    # from PmtSinglePhotonSpectrum import SinglePhotonSpectrum
    # spe = SinglePhotonSpectrum.load_csv("/run/media/einstein/Elements/CR160_data/1353V.csv")
    # filter_data = spe.proportion(-0.15e-10)[0]
    # af = AfterPulse(filter_data, -0.002, 200e-9, 0, 2e-5)2
    # af.loop_all("af_data.csv")
    t, a = AfterPulse.search_after_pulse("/run/media/einstein/Elements/2022_5_10_CR160_data/1300V_afterpulse/C2--w--00000.trc", -0.004, 500e-9, 300e-9, -0.0032779750781358787)
    print(t)
    print(a)

