import pandas as pd
from PmtDataSetTool import DataSetTool
import numpy as np


class SinglePhotonSpectrum(object):
    def __init__(self, pd_data: pd.DataFrame):
        self.pd_data = pd_data
        self.max = self.pd_data["Q"].max()
        self.min = self.pd_data["Q"].min()
        self.num = len(pd_data)

    @classmethod
    def load_csv(cls, file: str):
        if DataSetTool.check_file(file):
            pd_data = pd.read_csv(file)
            return cls(pd_data)
        else:
            print("File is wrong!")

    def get_pandas_data(self) -> pd.DataFrame:
        return self.pd_data

    def proportion(self, division: float) -> tuple:
        part1 = self.pd_data[self.pd_data["Q"] < division]
        part2 = self.pd_data[self.pd_data["Q"] > division]
        return len(part1), len(part2)
