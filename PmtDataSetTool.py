import pandas as pd
import numpy as np
from array import array
from PyQt5.QtWidgets import *
import os


class DataSetTool(object):
    def __init__(self):
        pass

    @staticmethod
    def check_file(file: str) -> bool:
        """
        检查文件或者路径是否存在，是否
        可读取，是否可写入
        """
        if os.path.exists(file) and os.access(file, os.R_OK) and os.access(file, os.W_OK):
            return True
        else:
            return False

    @staticmethod
    def read_wave(file: str, header: int = 4) -> tuple:
        """
        读取波形数据，返回时间，幅度的numpy序列，
        鉴于目前波形数据的格式，暂时令文件头参数
        为4,以后不同波形文件可更改
        """
        if DataSetTool.check_file(file):
            pd_data = pd.read_csv(file, header=header)
            return pd_data["Time"].to_numpy(), pd_data["Ampl"].to_numpy()
        else:
            print("File can't access!")

    @staticmethod
    def read_file(file: str) -> pd.DataFrame:
        """
        单纯读取不同格式的文件(*.csv *.pkl *.root)
        ，返回值为pd.DataFrame数据类型
        """
        if DataSetTool.check_file(file):
            if file.endswith(".csv"):
                return pd.read_csv(file)
            if file.endswith(".pkl"):
                return pd.read_pickle(file)
            if file.endswith(".root"):
                pass
        else:
            print("File can't access!")

    @staticmethod
    def convert_format(read_file: str, file_type: str, out_file: str = "./", head: int = 4) -> None:
        """
        对不同类型的数据进行转换，由于波形的数据量比较大，
        所以该函数主要针对波形数据csv转其他格式的情况。
        当输入为csv数据，默认文件头为4.
        """
        if DataSetTool.check_file(read_file) and DataSetTool.check_file(out_file):
            if read_file.endswith(".csv"):
                pd_data = pd.read_csv(read_file, header=head)
            elif read_file.endswith(".pkl"):
                pd_data = pd.read_pickle(read_file)
            elif read_file.endswith(".root"):
                pd_data = None
                pass
            else:
                pd_data = None
            if pd_data is not None:
                if file_type == "csv":
                    pd_data.to_csv(os.path.join(out_file, read_file.split(".")[0] + ".csv"), index=False)
                elif file_type == "pkl":
                    pd_data.to_pickle(os.path.join(out_file, read_file.split(".")[0] + ".pkl"))
                elif file_type == "root":
                    pass
                else:
                    print("Format is wrong!")
            else:
                print("Format is wrong!")

    @staticmethod
    def check_interval(val_min: float, val_max: float, interval1: float, interval2: float) -> bool:
        if val_min <= interval1 <= interval2 <= val_max:
            return True
        else:
            return False

    @staticmethod
    def comma2interval(interval_comma: str) -> tuple:
        str_list = interval_comma.replace(" ", "").split(",")
        if len(str_list) == 2:
            try:
                a1 = float(str_list[0])
                a2 = float(str_list[1])
            except ValueError:
                print("interval is wrong!")
                return False, 0, 0
            if a1 < a2:
                return True, a1, a2
            else:
                print("interval is wrong!")
                return False, 0, 0
        else:
            print("interval is wrong!")
            return False, 0, 0



if __name__ == "__main__":
    # t, a = DataSetTool.read_wave("C4--w--07002.csv")
    # DataSetTool.convert_format("C4--w--07002.csv", "pkl")
    # data = DataSetTool.read_file("C4--w--07002.pkl")
    # print(data)
    # print(t)
    # print(a)
    DataSetTool.comma2interval("0e1, 200e-9")
