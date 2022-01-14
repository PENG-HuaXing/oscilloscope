import os

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Waveform import Waveform
from Date_set import DataSet
from AnalysisSPESpectrumData import AnalysisSPESpectrumData

if __name__ == "__main__":
    data = AnalysisSPESpectrumData.load_from_file("_-300V_-2200V_-2700V_LED_10KHz_9V_28ns_20us_2.5GHz.csv")
    data.draw_SPE_spectrum(-0.2e-1,1,300,scale=-1e11,show=False)
    data.fit_with_gaus(10,0.3,0.3,0.05,0.6)
    """
    file = os.listdir()
    datalist = []
    for i in file:
        if i.endswith("2.5GHz.csv"):
            datalist.append(i)

    bins = np.linspace(-1e-11, 0.2e-12, 300)
    f, a = plt.subplots()
    for j in datalist:
        data = AnalysisSPESpectrumData.load_from_file(j)
        Qdata = data.get_column("Q").to_numpy()
        a.hist(Qdata, bins, histtype="step")
        a.set_yscale("log")
        plt.savefig(j+".png", dpi=600)
        plt.cla()
    plt.show()
    """

    # data.draw_SPE_spectrum(show=False, scale=-1e13)
    # p,pc = data.fit_with_gaus(10, 1, 0.5, -2, 1)
    """
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
    """
