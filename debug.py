import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Waveform import Waveform
from Date_set import DataSet
from AnalysisSPESpectrumData import AnalysisSPESpectrumData

if __name__ == "__main__":
    data = AnalysisSPESpectrumData.load_from_file("tmp+-50ns_withped_csv.csv")
    # data.draw_SPE_spectrum(show=False, scale=-1e13)
    # p,pc = data.fit_with_gaus(10, 1, 0.5, -2, 1)
    time, amp = DataSet.read_csv("../_-300V_-1800V_-2300V_LED_10KHz_9V_28ns_20us_2.5GHz/C1--w--01782.csv")
    wave = Waveform(time, amp)
    dep = wave.define_pedestal(5.4e-6, 5.5e-6, 5.6e-6, 5.7e-6)
    I = wave.integral_trapz_on_pedestal(5.5e-6, 5.6e-6)
    print("dep value: {}".format(wave.get_ped()))
    print("I value: {}".format(I))
    dep_s = wave.define_pedestal(-50e-9)
    I_s = wave.integral_trapz_on_pedestal(-50e-9, 50e-9)
    print("signal_dep value: {}".format(wave.get_ped()))
    print("signal_I value: {}".format(I_s))
    wave.wave_draw()
