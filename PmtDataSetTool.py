import pandas as pd
import numpy as np
import PmtConstant as PmtC
from array import array
import os


class DataSetTool(object):
    def __init__(self):
        pass

    @staticmethod
    def check_file(file: str) -> bool:
        if os.path.exists(file) and os.access(file, os.R_OK) and os.access(file, os.W_OK):
            return True
        else:
            return False

    @staticmethod
    def read_wave(file: str, header: int = 4) -> tuple:
        if DataSetTool.check_file(file):
            pd_data = pd.read_csv(file, header=header)
            return pd_data["Time"].to_numpy(), pd_data["Ampl"].to_numpy()
        else:
            print("File can't access!")

    @staticmethod
    def read_file(file: str):
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


if __name__ == "__main__":
    # t, a = DataSetTool.read_wave("C4--w--07002.csv")
    DataSetTool.convert_format("C4--w--07002.csv", "pkl")
    data = DataSetTool.read_file("C4--w--07002.pkl")
    print(data)
    # print(t)
    # print(a)
