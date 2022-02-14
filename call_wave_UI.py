from wave import Ui_Form
from Date_set import DataSet
from Waveform import Waveform
from AnalysisSPESpectrumData import AnalysisSPESpectrumData
from Canvas import MatPlotCanvas

import sys, os, time
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QAbstractItemView, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt, QStringListModel, QModelIndex, QThread
from PyQt5.Qt import QThreadPool
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



class WaveAnalysic(QWidget, Ui_Form):
    message = pyqtSignal(str)
    def __init__(self):
        super(WaveAnalysic, self).__init__()
        self.setupUi(self)
        self.message.connect(self.out_message)
        # UI setting
        self.radioButton_3.setChecked(True)
        self.pushButton.clicked.connect(self.load_target_directory)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listView.doubleClicked.connect(self.get_item)
        self.pushButton_2.clicked.connect(self.clear_list_view)
        self.lineEdit_2.setEnabled(False)
        self.radioButton_4.toggled.connect(self.multiple_interval)
        self.pushButton_3.clicked.connect(self.get_ped_parameters)
        self.pushButton_4.clicked.connect(self.reset_ped_setting)
        self.groupBox_2.setTitle("Integral Setting")
        self.comboBox.addItems(["trapz", "trapz_on_ped", "simpson"])
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.currentIndexChanged.connect(self.get_integral_method)
        self.pushButton_5.clicked.connect(self.get_int_parameters)
        self.pushButton_6.clicked.connect(self.reset_int_setting)
        self.comboBox_2.addItems(["MAX", "MIN", "OFF"])
        self.comboBox_2.setCurrentIndex(-1)
        self.comboBox_2.currentIndexChanged.connect(self.get_ext_flag)
        self.pushButton_7.clicked.connect(self.get_extremum_parameters)
        self.pushButton_8.clicked.connect(self.reset_ext_setting)
        self.comboBox_4.addItems(["above", "below", "OFF"])
        self.comboBox_4.setCurrentIndex(-1)
        self.comboBox_4.currentIndexChanged.connect(self.get_tri_flag)
        self.pushButton_14.clicked.connect(self.get_tri_parameters)
        self.pushButton_15.clicked.connect(self.reset_tri_setting)
        self.comboBox_3.addItems(["csv", "root"])
        self.comboBox_3.setCurrentIndex(-1)
        self.pushButton_9.clicked.connect(self.save_setting)
        self.frame.setHidden(True)
        self.lineEdit_7.setEnabled(False)
        self.lineEdit_8.setEnabled(False)
        self.pushButton_16.setEnabled(False)
        self.pushButton_17.setEnabled(False)
        self.checkBox_7.stateChanged.connect(self.active_lim)
        self.checkBox_8.stateChanged.connect(self.active_lim)
        self.pushButton_16.clicked.connect(self.set_xlim)
        self.pushButton_17.clicked.connect(self.set_ylim)
        self.pushButton_10.clicked.connect(self.start_thread)
        self.pushButton_11.clicked.connect(self.pause_thread)
        self.pushButton_12.clicked.connect(self.resume_thread)
        self.pushButton_13.clicked.connect(self.stop_thread)

        # Thread
        self.thread = ThreadWork(self.go)

        # Canvas
        self.mpc = MatPlotCanvas(self)
        self.mpc_ntb = NavigationToolbar(self.mpc, self)
        self.gridLayout_10.addWidget(self.mpc, 1, 0, 1, 7)
        self.gridLayout_10.addWidget(self.mpc_ntb, 2, 0, 1, 7)

        # init value
        # set self value
        self.dataset = None
        self.wave = None
        self.data_file_list = []
        self.wave_data_file = None
        self.ped_interval = []
        self.integral_method = None
        self.integral_interval = []
        self.ext_flag = None
        self.extremum_interval = []
        self.flag_seq_index = False
        self.flag_ampl = False
        self.flag_time = False
        self.tri_flag = None
        self.tri_voltage = None
        self.tri_interval = []
        self.flag_tri_bool = False
        self.flag_tri_index = False
        self.flag_tri_time = False
        self.save_file_name = None
        self.xlim_list = None
        self.ylim_list = None
        self.thread_flag = 1

    def out_message(self, message: str):
        self.textEdit.append(message)

    def load_target_directory(self):
        from PyQt5.QtWidgets import QFileDialog
        target_file = QFileDialog.getExistingDirectory(None, "get target directory", "/mnt/windows_file/DATA")
        print(target_file)
        if target_file == "":
            QMessageBox.warning(None, "Warning", "No directory selected", QMessageBox.Ok)
        else:
            self.dataset = DataSet(target_file)
            print(self.dataset.get_info())
            self.data_file_list.clear()
            self.data_file_list, num = self.dataset.get_data_file_with_abspath()
            if self.radioButton.isChecked():
                list_view = self.data_file_list
            elif self.radioButton_2.isChecked():
                list_view = list(map(os.path.relpath, self.data_file_list))
            else:
                list_view = list(map(os.path.basename, self.data_file_list))
            slm = QStringListModel()
            slm.setStringList(list_view)
            self.listView.setModel(slm)

            print(target_file)

    def get_item(self, index: QModelIndex):
        self.wave_data_file = self.data_file_list[index.row()]
        if self.wave is None:
            self.wave = Waveform(*DataSet.read_csv(self.wave_data_file))
        else:
            self.wave.reload(*DataSet.read_csv(self.wave_data_file))
        self.mpc.ax.cla()
        self.mpc.ax.grid(True)
        if self.checkBox_7.isChecked():
            if len(self.xlim_list) == 2:
                self.mpc.ax.set_xlim(self.xlim_list[0], self.xlim_list[1])
        if self.checkBox_8.isChecked():
            if len(self.ylim_list) == 2:
                self.mpc.ax.set_ylim(self.ylim_list[0], self.ylim_list[1])
        self.mpc.ax.plot(self.wave.get_time(), self.wave.get_amp())
        self.mpc.draw()

    def clear_list_view(self):
        self.data_file_list.clear()
        slm = QStringListModel()
        slm.setStringList(self.data_file_list)
        self.listView.setModel(slm)

    def multiple_interval(self):
        if self.radioButton_4.isChecked():
            self.lineEdit_2.setEnabled(True)
        else:
            self.lineEdit_2.setEnabled(False)

    def get_ped_parameters(self):
        interval1 = self.lineEdit.text()
        interval2 = self.lineEdit_2.text()
        if self.radioButton_4.isChecked():
            self.ped_interval.clear()
            self.ped_interval.append(float(interval1.split(",")[0]))
            self.ped_interval.append(float(interval1.split(",")[1]))
            self.ped_interval.append(float(interval2.split(",")[0]))
            self.ped_interval.append(float(interval2.split(",")[1]))
        else:
            self.ped_interval.clear()
            if len(interval1.split(",")) == 2:
                self.ped_interval.append(float(interval1.split(",")[0]))
                self.ped_interval.append(float(interval1.split(",")[1]))
            else:
                self.ped_interval.append(float(interval1))
        self.radioButton_4.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)

    def reset_ped_setting(self):
        self.radioButton_4.setEnabled(True)
        self.lineEdit.setEnabled(True)
        self.lineEdit_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)

    def get_integral_method(self):
        self.integral_method = self.comboBox.currentText()
        print(self.integral_method)

    def get_int_parameters(self):
        self.integral_interval.clear()
        tmp = self.lineEdit_3.text().split(",")
        self.integral_interval.append(float(tmp[0]))
        self.integral_interval.append(float(tmp[1]))
        print(self.integral_interval)
        self.lineEdit_3.setEnabled(False)
        self.pushButton_5.setEnabled(False)

    def reset_int_setting(self):
        self.lineEdit_3.setEnabled(True)
        self.pushButton_5.setEnabled(True)

    def get_extremum_parameters(self):
        tmp = self.lineEdit_4.text()
        self.extremum_interval.clear()
        self.extremum_interval.append(float(tmp.split(",")[0]))
        self.extremum_interval.append(float(tmp.split(",")[1]))
        self.lineEdit_4.setEnabled(False)
        self.checkBox.setEnabled(False)
        self.checkBox_2.setEnabled(False)
        self.checkBox_3.setEnabled(False)
        if self.checkBox.isChecked():
            self.flag_seq_index = True
        if self.checkBox_2.isChecked():
            self.flag_ampl = True
        if self.checkBox_3.isChecked():
            self.flag_time = True

        print(self.extremum_interval)
        print(self.flag_seq_index)
        print(self.flag_ampl)
        print(self.flag_time)

    def reset_ext_setting(self):
        self.lineEdit_4.setEnabled(True)
        self.checkBox.setEnabled(True)
        self.checkBox_2.setEnabled(True)
        self.checkBox_3.setEnabled(True)

    def get_ext_flag(self):
        self.ext_flag = self.comboBox_2.currentText()
        if self.comboBox_2.currentText() == "OFF":
            self.ext_flag = None

    def get_tri_flag(self):
        self.tri_flag = self.comboBox_4.currentText()
        if self.comboBox_4.currentText() == "OFF":
            self.tri_flag = None

    def get_tri_parameters(self):
        self.tri_voltage = float(self.lineEdit_6.text())
        self.tri_interval.clear()
        tmp = self.lineEdit_5.text()
        self.tri_interval.append(float(tmp.split(",")[0]))
        self.tri_interval.append(float(tmp.split(",")[1]))
        if self.checkBox_4.isChecked():
            self.flag_tri_bool = True
        if self.checkBox_5.isChecked():
            self.flag_tri_index = True
        if self.checkBox_6.isChecked():
            self.flag_tri_time = True
        self.lineEdit_6.setEnabled(False)
        self.lineEdit_5.setEnabled(False)
        self.checkBox_4.setEnabled(False)
        self.checkBox_5.setEnabled(False)
        self.checkBox_6.setEnabled(False)
        self.pushButton_14.setEnabled(False)
        self.message.emit("tri_voltage: {}\ntri_interval: {}\ntri_bool: {}\ntri_index: {}\ntri_time: {}".format(self.tri_voltage, self.tri_interval, self.flag_tri_bool, self.flag_tri_index, self.flag_tri_time))

    def reset_tri_setting(self):
        self.lineEdit_6.setEnabled(True)
        self.lineEdit_5.setEnabled(True)
        self.checkBox_4.setEnabled(True)
        self.checkBox_5.setEnabled(True)
        self.checkBox_6.setEnabled(True)
        self.pushButton_14.setEnabled(True)

    def save_setting(self):
        from PyQt5.QtWidgets import QFileDialog
        save_file_name = QFileDialog.getSaveFileName(None, "Save File", "./save_data.csv")
        if save_file_name[0] == "":
            QMessageBox.warning(self, "Warning", "Save file name is empty", QMessageBox.Ok)
        else:
            self.save_file_name = save_file_name[0]
            print(save_file_name[0])

    def active_lim(self):
        if self.checkBox_7.isChecked():
            self.lineEdit_7.setEnabled(True)
            self.pushButton_16.setEnabled(True)
        else:
            self.xlim_list = None
            self.lineEdit_7.setEnabled(False)
            self.pushButton_16.setEnabled(False)
        if self.checkBox_8.isChecked():
            self.lineEdit_8.setEnabled(True)
            self.pushButton_17.setEnabled(True)
        else:
            self.ylim_list = None
            self.lineEdit_8.setEnabled(False)
            self.pushButton_17.setEnabled(False)

    def set_xlim(self):
        lim_text = self.lineEdit_7.text()
        self.xlim_list = [float(lim_text.split(",")[0]), float(lim_text.split(",")[1])]

    def set_ylim(self):
        lim_text = self.lineEdit_8.text()
        self.ylim_list = [float(lim_text.split(",")[0]), float(lim_text.split(",")[1])]
        print(self.ylim_list)

    def go(self):
        if self.ext_flag is None and self.tri_flag is None:
            analysis = AnalysisSPESpectrumData(["File", "Q", "pedestal"])
            for i in self.data_file_list:
                print(i)
                wave = Waveform(*DataSet.read_csv(i))
                wave.define_pedestal(*self.ped_interval)
                integral_value = wave.integral_trapz_on_pedestal(*self.integral_interval)
                ped = wave.get_info()["pedestal"]
                self.message.emit(i)
                if self.save_file_name is not None:
                    analysis.add_row(i, integral_value, ped)
                if self.thread_flag == 1:
                    continue
                elif self.thread_flag == 0:
                    while True:
                        time.sleep(1)
                        if self.thread_flag == 0:
                            continue
                        else:
                            break
                else:
                    break
            analysis.save_as(self.save_file_name)
        if self.ext_flag is None and (self.tri_flag == "below" or self.tri_flag == "above"):
            analysis = AnalysisSPESpectrumData(["File", "Q", "pedestal", "tri_bool", "tri_index", "tri_time"])
            for i in self.data_file_list:
                print(i)
                wave = Waveform(*DataSet.read_csv(i))
                wave.define_pedestal(*self.ped_interval)
                integral_value = wave.integral_trapz_on_pedestal(*self.integral_interval)
                ped = wave.get_info()["pedestal"]
                tri_bool, tri_index = wave.trigger(self.tri_voltage, *self.tri_interval)
                self.message.emit(i)
                if self.save_file_name is not None:
                    analysis.add_row(i, integral_value, ped, tri_bool, tri_index, wave.get_time()[tri_index])
                if self.thread_flag == 1:
                    continue
                elif self.thread_flag == 0:
                    while True:
                        time.sleep(1)
                        if self.thread_flag == 0:
                            continue
                        else:
                            break
                else:
                    break
            analysis.save_as(self.save_file_name)
        if self.ext_flag == "MIN" and self.tri_flag is None:
            analysis = AnalysisSPESpectrumData(["File", "Q", "pedestal", "MIN_index", "MIN_amp", "MIN_time"])
            for i in self.data_file_list:
                print(i)
                wave = Waveform(*DataSet.read_csv(i))
                wave.define_pedestal(*self.ped_interval)
                integral_value = wave.integral_trapz_on_pedestal(*self.integral_interval)
                ped = wave.get_info()["pedestal"]
                ext_value, ext_index = wave.get_min_amp(*self.extremum_interval)
                self.message.emit(i)
                if self.save_file_name is not None:
                    analysis.add_row(i, integral_value, ped, tri_bool, ext_index, ext_value, wave.get_time()[ext_index])
                if self.thread_flag == 1:
                    continue
                elif self.thread_flag == 0:
                    while True:
                        time.sleep(1)
                        if self.thread_flag == 0:
                            continue
                        else:
                            break
                else:
                    break
            analysis.save_as(self.save_file_name)
        if self.ext_flag == "MIN" and (self.tri_flag == "below" or self.tri_flag == "above"):
            analysis = AnalysisSPESpectrumData(["File", "Q", "pedestal", "MIN_index", "MIN_amp", "MIN_time", "tri_bool", "tri_index", "tri_time"])
            for i in self.data_file_list:
                print(i)
                wave = Waveform(*DataSet.read_csv(i))
                wave.define_pedestal(*self.ped_interval)
                integral_value = wave.integral_trapz_on_pedestal(*self.integral_interval)
                ped = wave.get_info()["pedestal"]
                ext_value, ext_index = wave.get_min_amp(*self.extremum_interval)
                tri_bool, tri_index = wave.trigger(self.tri_voltage, *self.tri_interval)
                self.message.emit(i)
                if self.save_file_name is not None:
                    analysis.add_row(i, integral_value, ped, tri_bool, ext_index, ext_value, wave.get_time()[ext_index], tri_bool, tri_index, wave.get_time()[tri_index])
                if self.thread_flag == 1:
                    continue
                elif self.thread_flag == 0:
                    while True:
                        time.sleep(1)
                        if self.thread_flag == 0:
                            continue
                        else:
                            break
                else:
                    break
            analysis.save_as(self.save_file_name)
        if self.ext_flag == "MAX" and self.tri_flag is None:
            analysis = AnalysisSPESpectrumData(["File", "Q", "pedestal", "MAX_index", "MAX_amp", "MAX_time"])
            for i in self.data_file_list:
                print(i)
                wave = Waveform(*DataSet.read_csv(i))
                wave.define_pedestal(*self.ped_interval)
                integral_value = wave.integral_trapz_on_pedestal(*self.integral_interval)
                ped = wave.get_info()["pedestal"]
                ext_value, ext_index = wave.get_max_amp(*self.extremum_interval)
                self.message.emit(i)
                if self.save_file_name is not None:
                    analysis.add_row(i, integral_value, ped, tri_bool, ext_index, ext_value, wave.get_time()[ext_index])
                if self.thread_flag == 1:
                    continue
                elif self.thread_flag == 0:
                    while True:
                        time.sleep(1)
                        if self.thread_flag == 0:
                            continue
                        else:
                            break
                else:
                    break
            analysis.save_as(self.save_file_name)
        if self.ext_flag == "MAX" and (self.tri_flag == "below" or self.tri_flag == "above"):
            analysis = AnalysisSPESpectrumData(["File", "Q", "pedestal", "MIN_index", "MAX_amp", "MAX_time", "tri_bool", "tri_index", "tri_time"])
            for i in self.data_file_list:
                print(i)
                wave = Waveform(*DataSet.read_csv(i))
                wave.define_pedestal(*self.ped_interval)
                integral_value = wave.integral_trapz_on_pedestal(*self.integral_interval)
                ped = wave.get_info()["pedestal"]
                ext_value, ext_index = wave.get_max_amp(*self.extremum_interval)
                tri_bool, tri_index = wave.trigger(self.tri_voltage, *self.tri_interval)
                self.message.emit(i)
                if self.save_file_name is not None:
                    analysis.add_row(i, integral_value, ped, tri_bool, ext_index, ext_value, wave.get_time()[ext_index], tri_bool, tri_index, wave.get_time()[tri_index])
                if self.thread_flag == 1:
                    continue
                elif self.thread_flag == 0:
                    while True:
                        time.sleep(1)
                        if self.thread_flag == 0:
                            continue
                        else:
                            break
                else:
                    break
            analysis.save_as(self.save_file_name)

    def start_thread(self):
        self.thread_flag = 1
        self.thread.start()

    def pause_thread(self):
        self.thread_flag = 0

    def resume_thread(self):
        self.thread_flag = 1

    def stop_thread(self):
        self.thread_flag = 2

class ThreadWork(QThread):
    def __init__(self, fun, *args):
        super(ThreadWork, self).__init__()
        self.fun = fun
        self.args = args
    def run(self) -> None:
        self.fun(*self.args)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = WaveAnalysic()
    ui.show()
    sys.exit(app.exec_())
