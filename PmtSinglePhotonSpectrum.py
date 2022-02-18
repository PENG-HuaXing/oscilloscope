import numpy as np
import pandas as pd
from PmtDataSetTool import DataSetTool


class SinglePhotonSpectrum(object):
    def __init__(self, pd_data: pd.DataFrame):
        """
        此类为SPE类，功能比较简单，主要有两种方式读取SPE数据：
        1. 使用pandas初始化
        2. 读取csv文件初始化
        主要方法通过电荷量来计算出信号数量站总事例数的份额
        """
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

    def get_info(self):
        return {"min": self.min, "max": self.max, "num": self.num}

    def get_pandas_data(self) -> pd.DataFrame:
        return self.pd_data

    def get_charge(self) -> np.ndarray:
        return self.pd_data["Q"].to_numpy()

    def proportion(self, division: float) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        返回一个组元，其中分别为低于指定电荷量的数据
        和高于指定电荷量的数据
        """
        part1 = self.pd_data[self.pd_data["Q"] < division]
        part2 = self.pd_data[self.pd_data["Q"] > division]
        return part1, part2
