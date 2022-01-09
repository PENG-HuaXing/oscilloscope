import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Waveform import Waveform
from Date_set import DataSet
from AnalysisSPESpectrumData import AnalysisSPESpectrumData

if __name__ == "__main__":
    count = 0
    data_file = "../_-300V_-1800V_-2300V_LED_10KHz_9V_28ns_20us_2.5GHz"
    wave_data = DataSet(data_file)
    print(wave_data.get_info())
    data_file_list, num = wave_data.get_data_file_with_abspath()
    analysis_file = AnalysisSPESpectrumData(["File", "Q", "Trigger", "pedestal"])
    for i in data_file_list:
        print(count, end="\t")
        count += 1
        time_and_ampl = DataSet.read_csv(i)
        wave_form = Waveform(time_and_ampl[0], time_and_ampl[1])
        print(wave_form.get_min_amp(0, 200e-9)[0])
        wave_form.define_pedestal(-50e-9)
        ped = wave_form.get_ped()
        Q = wave_form.integral_trapz_on_pedestal(-50e-9, 50e-9) / 50
        t_bool, index = wave_form.trigger(-0.005, 0, 200e-9)
        analysis_file.add_row(i, Q, t_bool, ped)
    print(analysis_file.get_pandas())
    # analysis_file = AnalysisSPESpectrumData.load_from_file("tmp_csv.csv")
    analysis_file.save_as("tmp+-50ns_withped_csv")
    analysis_file.draw_SPE_spectrum()




