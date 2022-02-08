import numpy as np
import pandas as pd
import os
from Waveform import Waveform


class DataSet:
    def __init__(self, data_path: str, work_path: str = "./", data_format: str = "csv"):
        self.target_path = ""
        self.work_path = ""
        self.data_format = data_format
        self.data_file_list = []
        # 设置目标文件夹路径
        if os.path.exists(data_path) and os.access(data_path, os.W_OK) and os.access(data_path, os.W_OK) and os.access(data_path, os.X_OK):
            self.target_path = os.path.abspath(data_path)
        else:
            print("target path set failed!!")
        # 设置工作文件夹路径
        if os.path.exists(work_path):
            self.work_path = os.path.abspath(work_path)
        else:
            self.work_path = "./"
        # 获取数据文件名称
        for i in os.listdir(self.target_path):
            if i.endswith(data_format):
                self.data_file_list.append(i)

    def set_target_path(self, path: str):
        if os.path.exists(path) and os.access(path, os.W_OK) and os.access(path, os.W_OK) and os.access(path, os.X_OK):
            self.target_path = os.path.abspath(path)
            # 获取数据文件名称
            self.data_file_list.clear()
            for i in os.listdir(self.target_path):
                if i.endswith(self.data_format):
                    self.data_file_list.append(i)
        else:
            print("target path set failed!!")

    def set_work_path(self, path: str):
        if os.path.exists(path) and os.access(path, os.W_OK) and os.access(path, os.W_OK) and os.access(path, os.X_OK):
            self.work_path = os.path.abspath(path)
        else:
            print("target path set failed!!")

    def get_info(self):
        return {"target_directory": self.target_path, "work_directory": self.work_path, "data_format": self.data_format}

    def get_data_file(self, header: int = None):
        header_num = header
        if header_num is None:
            return self.data_file_list, len(self.data_file_list)
        elif header_num <= len(self.data_file_list):
            tmp_file_list = self.data_file_list
            tmp_file_list.sort()
            return tmp_file_list[:header_num], header_num
        else:
            print("Something is wrong!!")

    def get_data_file_with_abspath(self, header: int = None):
        data_file_with_abspath = []
        for i in self.get_data_file(header)[0]:
            data_file_with_abspath.append(os.path.join(self.target_path, i))
        return data_file_with_abspath, len(data_file_with_abspath)

    def get_data_file_with_relpath(self, header: int = None):
        data_file_with_relpath = []
        for i in self.get_data_file_with_abspath(header)[0]:
            data_file_with_relpath.append(os.path.relpath(i))
        return data_file_with_relpath, len(data_file_with_relpath)

    @staticmethod
    def read_csv(abs_path: str, header_line: int = 4, key1: str = "Time", key2: str = "Ampl") -> (np.ndarray, np.ndarray):
        waveform_data = pd.read_csv(abs_path, header=header_line)
        return waveform_data[key1].to_numpy(), waveform_data[key2].to_numpy()


if __name__ == "__main__":
    data = DataSet("1MHz_100mV_erjinzhi")
    file_list, num = data.get_data_file_with_abspath(5)
    print("Total file number is: {}".format(num))
    print(file_list)
    print(data.get_info())
    for i in file_list:
        A = Waveform(*DataSet.read_csv(i))
        A.wave_draw()
    print(data.data_file_list)