import time
from CallDialog import AfterPulseDialog
from UiAfterPulse import Ui_Form
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Canvas import MatPlotCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import os, datetime
from PmtSinglePhotonSpectrum import SinglePhotonSpectrum
from PmtDataSetTool import DataSetTool
from PmtWaveForm import WaveForm
import PmtConstant
from PmtConstant import Processing
from PmtAfterPulse import AfterPulse
import pandas as pd


class CallUiAfterPulse(QWidget, Ui_Form):
    text_message = pyqtSignal(str)

    def __init__(self):
        super(CallUiAfterPulse, self).__init__()
        self.setupUi(self)
        # 设置各个控件的初始状态
        self.switch_filter_setting(False)
        self.switch_after_pulse_setting(False)
        self.switch_save_file(False)
        self.switch_graph_setting(False)
        self.switch_process(False)
        self.pushButton_12.setVisible(False)
        self.pushButton_13.setVisible(False)
        # 添加文件
        self.pushButton_4.clicked.connect(self.add_files)
        # 移除文件
        self.pushButton_3.clicked.connect(self.remove_file)
        # listView 单击选择spe文件
        self.listView.clicked.connect(self.select_spe)
        # 初始化comboBox内容
        self.comboBox.addItems(["Q <", "Q >"])
        sci_validator = QRegExpValidator(self)
        sci_reg = QRegExp(r"^(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)")
        sci_validator.setRegExp(sci_reg)
        interval_reg = QRegExpValidator(self)
        reg = QRegExp(r"^(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)\s*,"
                      r"\s*(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)")
        interval_reg.setRegExp(reg)
        self.lineEdit.setValidator(sci_validator)
        self.lineEdit_7.setValidator(sci_validator)
        self.lineEdit_6.setValidator(sci_validator)
        self.lineEdit_8.setValidator(interval_reg)
        self.lineEdit_10.setValidator(interval_reg)
        self.lineEdit_11.setValidator(interval_reg)
        # 筛选信号文件
        self.pushButton_7.clicked.connect(self.filter)
        # 选择波形文件
        self.listView_2.clicked.connect(self.show_wave)
        self.listView_2.installEventFilter(self)
        # 设置计算后脉冲参数
        self.pushButton.clicked.connect(self.set_after_pulse_setting)
        # 重置计算后脉冲参数
        self.pushButton_2.clicked.connect(self.reset_after_pulse_setting)
        # 设置保存文件路径， 名称
        self.pushButton_5.clicked.connect(self.select_save_file)
        # Run循环计算寻找后脉冲
        self.pushButton_6.clicked.connect(self.start_thread)
        # 进程管理
        self.pushButton_8.clicked.connect(lambda: self.set_processing_flag(self.pushButton_8))
        self.pushButton_9.clicked.connect(lambda: self.set_processing_flag(self.pushButton_9))
        self.pushButton_10.clicked.connect(lambda: self.set_processing_flag(self.pushButton_10))

        # 单独读取后脉冲文件
        self.pushButton_11.clicked.connect(self.select_ap_file)
        # 绘制读取的后脉冲文件
        self.pushButton_12.clicked.connect(self.draw_ap_file)
        # 计算后脉冲率
        self.pushButton_13.clicked.connect(self.apr_dialog)
        self.text_message.connect(self.show_message)

        # thread
        self.my_thread = WorkThread(self.run)
        self.my_thread.finished.connect(self.thread_finish)
        self.my_thread.started.connect(lambda: self.switch_process(True))

        # var
        self.spe_files_list = []
        self.processing_flag = Processing.Go

        # Canvas
        self.canvas1 = MatPlotCanvas(self)
        self.ntb1 = NavigationToolbar(self.canvas1, self)
        self.canvas2 = MatPlotCanvas(self)
        self.ntb2 = NavigationToolbar(self.canvas2, self)
        self.gridLayout_3.addWidget(self.ntb1, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.canvas1, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.ntb2, 4, 0, 1, 1)
        self.gridLayout_3.addWidget(self.canvas2, 5, 0, 1, 1)

    def switch_after_pulse_setting(self, widget: bool, clear: bool = False):
        self.lineEdit_6.setEnabled(widget)
        self.lineEdit_7.setEnabled(widget)
        self.lineEdit_8.setEnabled(widget)
        self.pushButton.setEnabled(widget)
        self.pushButton_2.setEnabled(widget)
        self.checkBox_3.setEnabled(widget)
        if clear is True:
            self.lineEdit_6.clear()
            self.lineEdit_7.clear()
            self.lineEdit_8.clear()
            self.checkBox_3.setChecked(False)

    def switch_save_file(self, widget: bool):
        if widget is True:
            self.lineEdit_9.setText("./after.csv")
        else:
            self.lineEdit_9.clear()
        self.lineEdit_9.setEnabled(widget)
        self.pushButton_5.setEnabled(widget)
        self.pushButton_6.setEnabled(widget)

    def switch_graph_setting(self, widget: bool):
        self.checkBox.setEnabled(widget)
        self.checkBox_2.setEnabled(widget)
        self.lineEdit_10.setEnabled(widget)
        self.lineEdit_11.setEnabled(widget)

    def switch_filter_setting(self, widget: bool):
        if widget is False:
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            self.lineEdit_14.clear()
        self.comboBox.setEnabled(widget)
        self.pushButton_7.setEnabled(widget)
        self.lineEdit.setEnabled(widget)
        self.lineEdit_3.setEnabled(widget)
        self.lineEdit_4.setEnabled(widget)
        self.lineEdit_5.setEnabled(widget)
        self.lineEdit_14.setEnabled(widget)

        slm = QStringListModel()
        slm.setStringList([])
        self.listView_2.setModel(slm)

    def switch_process(self, widget: bool):
        self.pushButton_8.setEnabled(widget)
        self.pushButton_9.setEnabled(widget)
        self.pushButton_10.setEnabled(widget)

    def add_files(self):
        files, filetype = QFileDialog.getOpenFileNames(parent=self, caption="选择文件",
                                                       directory="/mnt/windows_file/DATA/", filter="csvFile (*csv)")
        self.spe_files_list = files
        if len(files) == 0:
            print(len(files))
            QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)
        else:
            base_name = list(map(os.path.basename, files))
            slm = QStringListModel()
            slm.setStringList(base_name)
            self.listView.setModel(slm)

    def remove_file(self):
        current_model_index = self.listView.currentIndex()
        if current_model_index.row() == -1:
            QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)
        else:
            self.spe_files_list.pop(current_model_index.row())
            base_name = list(map(os.path.basename, self.spe_files_list))
            slm = QStringListModel()
            slm.setStringList(base_name)
            self.listView.setModel(slm)
        self.switch_filter_setting(False)
        self.switch_graph_setting(False)
        self.switch_after_pulse_setting(False, True)
        self.switch_save_file(False)

    def select_spe(self, index: QModelIndex):
        self.lineEdit_2.setText(os.path.dirname(self.spe_files_list[index.row()]))
        self.switch_filter_setting(True)

    def filter(self):
        index = self.listView.currentIndex()
        print("current index: {}".format(index))
        if index == -1:
            QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)
        elif self.lineEdit.text() == "":
            QMessageBox.warning(self, "警告", "未选择设定筛选阈值", QMessageBox.Ok)
        else:
            pd_data = DataSetTool.read_file(self.spe_files_list[index.row()])
            spe = SinglePhotonSpectrum(pd_data)
            part1, part2 = spe.proportion(float(self.lineEdit.text()))
            print(part1)
            if len(part1) == 0:
                tmp_file = part2["File"].iloc[0]
            else:
                tmp_file = part1["File"].iloc[0]
            print("tmp file: {}".format(tmp_file))
            wave = WaveForm.load_from_file(tmp_file)
            self.lineEdit_3.setText(os.path.dirname(tmp_file))
            self.lineEdit_4.setText(str(format(wave.get_time_bound()[0], '.3e')))
            self.lineEdit_5.setText(str(format(wave.get_time_bound()[1], '.3e')))
            file_list = []
            if self.comboBox.currentIndex() == 0:
                for i in part1["File"]:
                    file_list.append(i)
            if self.comboBox.currentIndex() == 1:
                for i in part2["File"]:
                    file_list.append(i)
            base_name = list(map(os.path.basename, file_list))
            slm = QStringListModel()
            slm.setStringList(base_name)
            self.listView_2.setModel(slm)
            self.lineEdit_14.setText(str(len(file_list)))
            if len(file_list) != 0:
                self.switch_after_pulse_setting(True)
                self.switch_graph_setting(True)
            else:
                QMessageBox.warning(self, "警告", "筛选结果为0", QMessageBox.Ok)

    def show_wave(self, index: QModelIndex):
        base_name = index.data()
        self.canvas1.ax.cla()
        self.canvas1.ax.grid(True)
        wave = WaveForm.load_from_file(os.path.join(self.lineEdit_3.text(), base_name))
        self.canvas1.ax.plot(wave.get_time(), wave.get_ampl())
        if self.checkBox.isChecked():
            x_check, a1, a2 = DataSetTool.comma2interval(self.lineEdit_10.text())
            if x_check:
                self.canvas1.ax.set_xlim(a1, a2)
        if self.checkBox_2.isChecked():
            y_check, b1, b2 = DataSetTool.comma2interval(self.lineEdit_11.text())
            if y_check:
                self.canvas1.ax.set_ylim(b1, b2)
        self.canvas1.draw()

    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a0 is self.listView_2:
            if a1.type() == QEvent.KeyPress:
                current_model_index = self.listView_2.currentIndex()
                print(current_model_index.data())
                if a1.key() == Qt.Key_Up:
                    up_model_index = current_model_index.siblingAtRow(current_model_index.row() - 1)
                    print("Up: {}".format(up_model_index.data()))
                    if up_model_index.data() is None:
                        self.show_wave(current_model_index)
                    else:
                        self.show_wave(up_model_index)
                if a1.key() == Qt.Key_Down:
                    down_model_index = current_model_index.siblingAtRow(current_model_index.row() + 1)
                    print("Down: {}".format(down_model_index.data()))
                    if down_model_index.data() is None:
                        self.show_wave(current_model_index)
                    else:
                        self.show_wave(down_model_index)
        return QWidget.eventFilter(self, a0, a1)

    def set_after_pulse_setting(self):
        self.switch_after_pulse_setting(False)
        self.pushButton_2.setEnabled(True)
        self.switch_save_file(True)

    def reset_after_pulse_setting(self):
        self.switch_after_pulse_setting(True)
        self.switch_save_file(False)
        self.lineEdit_9.clear()

    def select_save_file(self):
        save_file, file_type = QFileDialog.getSaveFileName(self, "保存文件", "./after_pulse.csv", "csv文件 (*csv)")
        print("保存文件: {}".format(save_file))
        print("文件格式: {}".format(file_type))
        if DataSetTool.check_file(os.path.dirname(save_file)):
            self.lineEdit_9.setText(save_file)
        else:
            QMessageBox.warning(self, "警告", "文件夹无效", QMessageBox.Ok)

    def run(self):
        param = self.collect_param()
        if param is not None:
            data_list = []
            ap_file_list = []
            columns = ["File", "Time", "Q"]
            for i in range(len(param["data"])):
                file_name = param["data"]["File"].iloc[i]
                print(file_name)
                self.text_message.emit(file_name)
                if param["ped_flag"] == PmtConstant.AfterPulse.Pedestal:
                    tmp_t, tmp_a = AfterPulse.search_after_pulse(file_name, param["threshold"], param["interval1"],
                                                                 param["windows"])
                else:
                    tmp_t, tmp_a = AfterPulse.search_after_pulse(file_name, param["threshold"], param["interval1"],
                                                                 param["windows"], param["data"]["ped"].iloc[i])
                tmp_data_list = AfterPulse.zip_data(file_name, tmp_t, tmp_a)
                for row in tmp_data_list:
                    data_list.append(row)
                if self.processing_flag == Processing.Go:
                    continue
                if self.processing_flag == Processing.Pause:
                    while self.processing_flag == Processing.Pause:
                        time.sleep(1)
                if self.processing_flag == Processing.Stop:
                    break
            self.text_message.emit("信号文件数目：{}\n后脉冲文件数目：{}\n后脉冲率：{}".format(len(param["data"]), len(ap_file_list), len(ap_file_list) / len(param["data"])))
            output_data = pd.DataFrame(data_list, columns=columns)
            print("data list: {}".format(data_list))
            print("output_data: {}".format(output_data))
            print(output_data)
            self.canvas2.ax.cla()
            self.canvas2.ax.grid(True)
            self.canvas2.ax.scatter(output_data["Time"].to_numpy(), output_data["Q"].to_numpy())
            self.canvas2.draw()
            if DataSetTool.check_file(os.path.dirname(param["save_file"])):
                output_data.to_csv(param["save_file"], index=False)
            else:
                QMessageBox.warning(self, "警告", "保存文件设置错误", QMessageBox.Ok)
        else:
            self.text_message.emit("参数设置有误!!")

    def collect_param(self):
        # self.switch_after_pulse_setting(True)
        param_dict = dict()
        param_dict["threshold"] = float(self.lineEdit_7.text())
        check, interval1, interval2 = DataSetTool.comma2interval(self.lineEdit_8.text())
        param_dict["interval1"] = interval1
        param_dict["interval2"] = interval2
        param_dict["windows"] = float(self.lineEdit_6.text())
        if self.checkBox_3.isChecked():
            ped_flag = PmtConstant.AfterPulse.Pedestal
        else:
            ped_flag = PmtConstant.AfterPulse.NoPedestal
        param_dict["ped_flag"] = ped_flag
        # 获取filter后的文件列表
        # 至于为什么要从SPE文件列表开始重新Filter信号文件。
        # 实际上有可能Run之前用户没有选择任何listView_2内的文件
        # 如果用户没有选择， GUI从当前的界面中无法获取listView_2文件列表
        if self.listView.currentIndex() != -1:
            current_spe = self.listView.currentIndex().data()
            spe_file = os.path.join(self.lineEdit_2.text(), current_spe)
            pd_data = DataSetTool.read_file(spe_file)
            spe = SinglePhotonSpectrum(pd_data)
            part1, part2 = spe.proportion(float(self.lineEdit.text()))
            if self.comboBox.currentIndex() == 0:
                run_data = part1
            elif self.comboBox.currentIndex() == 1:
                run_data = part2
            else:
                QMessageBox.warning(self, "警告", "Wrong", QMessageBox.Ok)
            param_dict["data"] = run_data
            param_dict["save_file"] = self.lineEdit_9.text()
            # self.switch_after_pulse_setting(False)
            # self.pushButton_2.setEnabled(True)
            print(param_dict)
            return param_dict
        else:
            QMessageBox.warning(self, "警告", "SPE文件选择错误", QMessageBox.Ok)

    def start_thread(self):
        self.my_thread.start()

    def show_message(self, message):
        self.textEdit.append(datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")+": "+message)

    def thread_finish(self):
        self.textEdit.append("完成！！")
        self.switch_process(False)
        self.pushButton_13.setVisible(True)
        self.pushButton_12.setVisible(False)
        self.lineEdit_12.clear()

    def set_processing_flag(self, btn: QPushButton):
        if btn is self.pushButton_8:
            self.processing_flag = Processing.Go
        if btn is self.pushButton_9:
            self.processing_flag = Processing.Pause
        if btn is self.pushButton_10:
            self.processing_flag = Processing.Stop

    def select_ap_file(self):
        ap_file_name, file_type = QFileDialog.getOpenFileName(self, "添加文件", "/mnt/windows_file/DATA/",
                                                              "csvFile (*csv)")
        if ap_file_name == "":
            QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)
        elif DataSetTool.check_file(ap_file_name):
            self.lineEdit_12.setText(ap_file_name)
            self.pushButton_12.setVisible(True)
            self.pushButton_13.setVisible(False)
        else:
            QMessageBox.warning(self, "警告", "载入文件无效", QMessageBox.Ok)

    def draw_ap_file(self):
        if self.lineEdit_12.text() != "" and DataSetTool.check_file(self.lineEdit_12.text()):
            try:
                pd_data = pd.read_csv(self.lineEdit_12.text())
                time_column = pd_data["Time"]
                q_column = pd_data["Q"]
                print(q_column)
                self.canvas2.ax.cla()
                self.canvas2.ax.grid("True")
                self.canvas2.ax.scatter(time_column.to_numpy(), q_column.to_numpy())
                self.canvas2.draw()
            except KeyError:
                QMessageBox.warning(self, "警告", "键值错误", QMessageBox.Ok)

    def apr_dialog(self):
        dialog = AfterPulseDialog(self)
        dialog.show()


class WorkThread(QThread):
    def __init__(self, fun, *args):
        super(WorkThread, self).__init__()
        self.fun = fun
        self.args = args

    def run(self) -> None:
        self.fun(*self.args)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = CallUiAfterPulse()
    win.show()
    sys.exit(app.exec_())