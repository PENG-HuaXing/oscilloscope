import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Waveform import Waveform
from Date_set import DataSet
from AnalysisSPESpectrumData import AnalysisSPESpectrumData

if __name__ == "__main__":
    data = AnalysisSPESpectrumData.load_from_file("tmp+-50ns_withped_csv.csv")
    data.draw_SPE_spectrum(show=False, scale=-1e13)
    p,pc = data.fit_with_gaus(10, 1, 0.5, -2, 1)
    print(p)