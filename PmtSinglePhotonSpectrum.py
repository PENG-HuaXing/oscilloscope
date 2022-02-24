import numpy as np
import pandas as pd
from PmtDataSetTool import DataSetTool


class SinglePhotonSpectrum(object):
    def __init__(self, pd_data: pd.DataFrame, scale: float = 1):
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
        self.scale = scale

    @classmethod
    def load_csv(cls, file: str):
        if DataSetTool.check_file(file):
            pd_data = pd.read_csv(file)
            return cls(pd_data)
        else:
            print("File is wrong!")

    def get_info(self, scale: float = 1):
        if scale == 1:
            return {"min": self.min, "max": self.max, "num": self.num}
        else:
            scale_q = self.get_charge(scale)
            return {"min": scale_q.min(), "max": scale_q.max(), "num": self.num}

    def get_pandas_data(self) -> pd.DataFrame:
        return self.pd_data

    def get_charge(self, scale: float = 1) -> np.ndarray:
        return scale * self.pd_data["Q"].to_numpy()

    def get_scale(self):
        return self.scale

    def proportion(self, division: float, scale: float = 1) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        返回一个组元，其中分别为低于指定电荷量的数据
        和高于指定电荷量的数据
        """
        if scale == 1:
            part1 = self.pd_data[self.pd_data["Q"] < division]
            part2 = self.pd_data[self.pd_data["Q"] > division]
            return part1, part2
        else:
            scale_pd = scale * self.pd_data["Q"]
            part1 = scale_pd[scale_pd < division]
            part2 = scale_pd[scale_pd > division]
            return part1, part2


if __name__ == "__main__":
    from PmtDataSetTool import DataSetTool
    spe = SinglePhotonSpectrum(DataSetTool.read_file("./source/1353V.csv"))
    print(spe.get_info(-1e11)["min"])
    p1, p2 = spe.proportion(2, -1e11)
    print(p1, p2)