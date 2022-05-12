import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from UiSPE import Ui_Form
from Canvas import MatPlotCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import time, os, datetime
from PmtSinglePhotonSpectrum import SinglePhotonSpectrum
from PmtSpeHist import SpeHist
from PmtDataSetTool import DataSetTool
from PmtConstant import Fit
from CallDialog import FitDialog, PandasModel, TableDialog
import matplotlib.pyplot as plt


class CallUiSPE(Ui_Form, QWidget):
    out_message = pyqtSignal(str)

    def __init__(self):
        super(CallUiSPE, self).__init__()
        self.setupUi(self)
        self.pushButton_2.setVisible(False)
        self.checkBox_3.setTristate(True)
        # 初始控件状态
        self.switch_portion(False)
        self.switch_hist_setting(False)
        self.switch_fit_setting(False)
        self.switch_graph_setting(False)
        # 载入文件
        self.pushButton.clicked.connect(self.add_files)
        # 移除文件和清空文件
        self.pushButton_3.clicked.connect(self.remove_file)
        self.pushButton_4.clicked.connect(self.clear_listview)
        # 选择文件动作
        self.listView.clicked.connect(self.show_file_info)
        self.listView.doubleClicked.connect(self.show_table_data)
        self.listView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.lineEdit_5.setText("1")
        self.radioButton.toggled.connect(self.switch_bin_setting)
        interval_reg = QRegExp(r"^(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)\s*,"
                               r"\s*(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)")
        sci_reg = QRegExp(r"^(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)")
        interval_validator = QRegExpValidator(self)
        interval_validator.setRegExp(interval_reg)
        sci_validator = QRegExpValidator(self)
        sci_validator.setRegExp(sci_reg)
        int_validator = QIntValidator(self)
        int_validator.setRange(0, 2147483647)
        self.lineEdit_5.setValidator(sci_validator)
        self.lineEdit_6.setValidator(interval_validator)
        self.lineEdit_7.setValidator(int_validator)
        # 绘制谱图
        self.pushButton_8.clicked.connect(self.draw_hist)
        self.lineEdit_8.setValidator(sci_validator)
        # 事例数比例设置
        self.lineEdit_8.editingFinished.connect(self.proportion)
        self.comboBox.addItems(["单高斯拟合", "全局拟合", "全局拟合(含噪声)"])
        # x label
        self.comboBox_2.addItems(["None", "C", "mC", "uC", "nC", "pC", "fC"])
        self.comboBox_2.currentIndexChanged.connect(self.refresh)
        # 引出拟合参数设置对话框
        self.pushButton_6.clicked.connect(self.set_fit_param)
        # 绘制拟合曲线
        self.pushButton_7.clicked.connect(self.refresh)
        self.checkBox.toggled.connect(self.refresh)
        # 输出信号绑定browser_text显示拟合参数
        self.out_message.connect(self.show_message)
        # checkBox
        self.checkBox_2.toggled.connect(self.refresh)
        self.checkBox_3.stateChanged.connect(self.refresh)
        self.checkBox_4.toggled.connect(self.refresh)

        # var
        self.files_list = []
        self.spe = []
        self.hist = []
        self.fit = {"model": Fit.NoFit, "param": None}

        # Canvas
        self.canvas = MatPlotCanvas(self, width=5, height=5)
        self.tool_bar = NavigationToolbar(self.canvas, self)
        canvas_size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas_size_policy.setHorizontalStretch(0)
        canvas_size_policy.setVerticalStretch(2)
        self.canvas.setSizePolicy(canvas_size_policy)
        self.gridLayout_5.addWidget(self.tool_bar, 1, 1, 1, 1)
        self.gridLayout_5.addWidget(self.canvas, 2, 1, 1, 1)

    def switch_hist_setting(self, status: bool, clear: bool = False):
        if clear is True:
            self.lineEdit_6.clear()
            self.lineEdit_7.clear()
        self.lineEdit_6.setEnabled(status)
        self.lineEdit_7.setEnabled(status)
        self.pushButton_8.setEnabled(status)

    def switch_bin_setting(self):
        print("enter radio")
        if self.radioButton.isChecked():
            self.switch_hist_setting(False, True)
            self.pushButton_8.setEnabled(True)
        else:
            self.switch_hist_setting(True)

    def switch_fit_setting(self, status: bool):
        self.comboBox.setEnabled(status)
        self.pushButton_6.setEnabled(status)
        self.pushButton_7.setEnabled(status)

    def switch_portion(self, status: bool, clear: bool = False):
        if clear is True:
            self.lineEdit_8.clear()
            self.lineEdit_9.clear()
            self.lineEdit_10.clear()
            self.lineEdit_11.clear()
        self.lineEdit_8.setEnabled(status)
        self.lineEdit_9.setEnabled(status)
        self.lineEdit_10.setEnabled(status)
        self.lineEdit_11.setEnabled(status)

    def switch_graph_setting(self, status: bool):
        self.checkBox.setEnabled(status)
        self.checkBox_2.setEnabled(status)
        self.checkBox_3.setEnabled(status)
        self.checkBox_4.setEnabled(status)
        self.comboBox_2.setEnabled(status)

    def add_files(self):
        files, filetype = QFileDialog.getOpenFileNames(parent=self, caption="添加文件",
                                                       directory="/mnt/windows_file/DATA/", filter="csvFile (*csv)")
        if len(files) == 0:
            print(len(files))
            QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)
        else:
            self.files_list = self.files_list + files
            base_name = list(map(os.path.basename, self.files_list))
            slm = QStringListModel()
            slm.setStringList(base_name)
            self.listView.setModel(slm)

    def remove_file(self):
        qmi = self.listView.currentIndex()
        if qmi.row() == -1:
            QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)
        else:
            index = qmi.row()
            self.files_list.pop(index)
            base_name = list(map(os.path.basename, self.files_list))
            slm = QStringListModel()
            slm.setStringList(base_name)
            self.listView.setModel(slm)
            self.pushButton_8.setEnabled(False)

    def clear_listview(self):
        self.files_list.clear()
        slm = QStringListModel()
        slm.setStringList([])
        self.listView.setModel(slm)
        self.switch_hist_setting(False, True)
        self.switch_graph_setting(False)
        self.switch_portion(False, True)
        self.switch_fit_setting(False)

    def show_file_info(self, index: QModelIndex):
        file = self.files_list[index.row()]
        if index.row() != -1:
            self.pushButton_8.setEnabled(True)
        pd_data = DataSetTool.read_file(file)
        self.lineEdit_2.setText(os.path.basename(file))
        self.lineEdit.setText(os.path.dirname(file))
        self.lineEdit_3.setText(str(len(pd_data)) + " X " + str(len(pd_data.columns)))
        self.lineEdit_4.setText(str(format(os.path.getsize(file) / 1024, '.2f')) + " kB")
        self.fit["model"] = Fit.NoFit

    def draw_hist(self):
        self.canvas.initial(x_label="integral value", y_label="count", title="signal photon spectra")
        # 清空成员变量中spe列表内容和hist的列表内容
        # 列表中存储这后续将要绘制，或者拟合的电子谱图
        self.spe.clear()
        self.hist.clear()
        scale = float(self.lineEdit_5.text())
        bound = []
        # 判断在listView中是否有文件被选中
        if len(self.listView.selectedIndexes()) != 0:
            for i in self.listView.selectedIndexes():
                spe = SinglePhotonSpectrum(DataSetTool.read_file(self.files_list[i.row()]), scale)
                self.spe.append(spe)
                bound.append(spe.get_info(spe.get_scale())["min"])
                bound.append(spe.get_info(spe.get_scale())["max"])
            default_bins = np.linspace(np.array(bound).min(), np.array(bound).max(), 301)
            print("default bin: {}".format(default_bins))
            if self.radioButton.isChecked():
                # 默认bins
                for i in self.spe:
                    self.hist.append(SpeHist(i.get_charge(), default_bins, scale))
            else:
                # 自定义bins
                comma2interval = DataSetTool.comma2interval(self.lineEdit_6.text())
                if comma2interval[0] and self.lineEdit_7.text() != "":      # bins填写正确
                    print(comma2interval)
                    custom_bin = np.linspace(comma2interval[1], comma2interval[2], int(self.lineEdit_7.text()) + 1)
                    for i in self.spe:
                        self.hist.append(SpeHist(i.get_charge(), custom_bin, scale))
                else:
                    # bin填写错误
                    QMessageBox.warning(None, "警告", "区间设置错误", QMessageBox.Ok)
            for i in self.hist:
                if self.checkBox.isEnabled() and not self.checkBox.isChecked():
                    self.canvas.ax.hist(i.get_scatter()[0], i.get_hist()[1], weights=i.get_hist()[0], histtype="step")
                else:
                    self.canvas.ax.hist(i.get_scatter()[0], i.get_hist()[1], weights=i.get_hist()[0])
            self.canvas.draw()
            self.switch_graph_setting(True)
            # 判断一个图谱还是多个图谱， 多个图谱fit控件关闭， 一个谱图fit控件开启
            if len(self.spe) == 1:
                self.switch_fit_setting(True)
                self.switch_portion(True, True)
                self.checkBox.setEnabled(True)
                self.checkBox_4.setEnabled(False)
                self.checkBox_2.setEnabled(True)
                self.checkBox_3.setEnabled(False)
            else:
                self.switch_fit_setting(False)
                self.switch_portion(False, True)
                self.checkBox.setEnabled(True)
                self.checkBox_4.setEnabled(True)
                self.checkBox_2.setEnabled(False)
                self.checkBox_3.setEnabled(False)
        else:
            QMessageBox.warning(None, "警告", "未选择任何文件", QMessageBox.Ok)

    def proportion(self):
        threshold = float(self.lineEdit_8.text())
        part1, part2 = self.spe[0].proportion(threshold, self.spe[0].get_scale())
        total = len(part1) + len(part2)
        self.lineEdit_11.setText(str(total))
        self.lineEdit_9.setText(str(format(len(part1) / total, ".5f")))
        self.lineEdit_10.setText(str(format(len(part2) / total, ".5f")))

    def set_fit_param(self):
        if self.comboBox.currentIndex() == 0:
            dialog = FitDialog(self, Fit.Gauss)
            dialog.out_message.connect(self.fitting)
            dialog.show()
        elif self.comboBox.currentIndex() == 1:
            dialog = FitDialog(self, Fit.Global)
            dialog.out_message.connect(self.fitting)
            dialog.show()
        elif self.comboBox.currentIndex() == 2:
            dialog = FitDialog(self, Fit.GlobalNoise)
            dialog.out_message.connect(self.fitting)
            dialog.show()
        else:
            QMessageBox.warning(None, "警告", "拟合选项错误", QMessageBox.Ok)

    def fitting(self, dict_data: dict):
        self.fit["model"] = Fit.NoFit
        print(dict_data["model"])
        if dict_data["model"] == Fit.Gauss:
            flag, interval1, interval2 = DataSetTool.comma2interval(dict_data["interval"])
        if dict_data["model"] == Fit.Gauss and len(self.hist) == 1 and flag:
            print("param setting: {}".format(dict_data))
            fit_par, fit_cov = self.hist[0].fit_spe(dict_data["model"], interval1, interval2, *dict_data["param"])
            self.fit["param"] = fit_par
            self.fit["model"] = Fit.Gauss
        elif dict_data["model"] == Fit.Global and len(self.hist) == 1:
            fit_par, fit_cov = self.hist[0].fit_spe(dict_data["model"], 1, 1, *dict_data["param"])
            self.fit["param"] = fit_par
            self.fit["model"] = Fit.Global
        elif dict_data["model"] == Fit.GlobalNoise and len(self.hist) == 1:
            fit_par, fit_cov = self.hist[0].fit_spe(dict_data["model"], 1, 1, *dict_data["param"])
            self.fit["param"] = fit_par
            self.fit["model"] = Fit.GlobalNoise
        else:
            print("Fit is wrong")
        print("拟合参数为：\n{}".format(self.fit["param"]))
        if self.fit["model"] != Fit.NoFit:
            # 开启hist控件， 关闭归一化控件， 开启散点控件， 开启fit控件
            self.checkBox.setEnabled(True)
            self.checkBox_4.setEnabled(False)
            self.checkBox_2.setEnabled(True)
            self.checkBox_3.setEnabled(True)
        # 拟合参数格式化输出
        emit_message = "=" * 6 + "拟合结果为" + "=" * 6 + "\n"
        print("emit message")
        print("len: {}".format(len(self.fit["param"])))
        print("param: {}".format(self.fit["param"]))
        for i in range(len(self.fit["param"])):
            emit_message = emit_message + "param{0}: {1: .6g}".format(i, self.fit["param"][i]) + "\n"
        print(emit_message)
        self.out_message.emit(emit_message)

    def collect_param(self):
        print(self.fit)
        collection = {"hist": False, "normal": False, "scatter": False, "fitting": 0}
        if self.checkBox.isEnabled() and self.checkBox.isChecked():
            collection["hist"] = True
            print("hist status: {}".format(collection["hist"]))
        if self.checkBox_4.isEnabled() and self.checkBox_4.isChecked():
            collection["normal"] = True
        if self.checkBox_2.isEnabled() and self.checkBox_2.isChecked():
            collection["scatter"] = True
            print("scatter status: {}".format(collection["scatter"]))
        if self.checkBox_3.isEnabled() and self.checkBox_3.isChecked() and self.fit["model"] != Fit.NoFit:
            collection["fitting"] = self.checkBox_3.checkState()
            print("fit model: {}".format(self.fit["model"]))
        return collection

    def refresh(self):
        if self.comboBox_2.currentIndex() == 0:
            self.canvas.initial(x_label="integral value", y_label="count", title="single photon spectra")
        elif self.comboBox_2.currentIndex() > 0:
            self.canvas.initial(x_label=self.comboBox_2.currentText(), y_label="count", title="single photon spectra")
        else:
            self.canvas.initial(x_label="integral value", y_label="count", title="single photon spectra")
        collection = self.collect_param()
        if len(self.hist) != 0:
            # 直方图checkBox检测
            if collection["hist"] is True:
                for i in self.hist:
                    # 归一化checkBox检测
                    if collection["normal"] is True:
                        self.canvas.ax.hist(i.get_scatter()[0], i.get_hist()[1],
                                            weights=(i.get_hist()[0] / i.get_hist()[0].sum()))
                    else:
                        self.canvas.ax.hist(i.get_scatter()[0], i.get_hist()[1], weights=i.get_hist()[0])
            else:
                for i in self.hist:
                    # 归一化checkBox检测
                    if collection["normal"] is False:
                        self.canvas.ax.hist(i.get_scatter()[0], i.get_hist()[1], weights=i.get_hist()[0],
                                            histtype="step")
                    else:
                        self.canvas.ax.hist(i.get_scatter()[0], i.get_hist()[1],
                                            weights=(i.get_hist()[0] / i.get_hist()[0].sum()), histtype="step")
            # 散点checkBox检测
            if collection["scatter"] is True:
                for i in self.hist:
                    self.canvas.ax.scatter(i.get_scatter()[0], i.get_scatter()[1])
            if collection["fitting"] != 0 and self.fit["model"] != Fit.NoFit:
                self.draw_fit(self.checkBox_3.checkState())
            self.canvas.draw()

    def draw_fit(self, check_status: int = 0):
        if self.fit["model"] != Fit.NoFit:
            x = self.hist[0].get_scatter()[0]
            if self.fit["model"] == Fit.Gauss and (check_status == 1 or check_status == 2):
                self.canvas.ax.plot(x, SpeHist.gauss(x, *self.fit["param"]))
            if self.fit["model"] == Fit.Global:
                self.canvas.ax.plot(x, SpeHist.global_model(x, *self.fit["param"]))
                if check_status == 2:
                    par = self.fit["param"]
                    self.canvas.ax.plot(x, par[0] * SpeHist.s_ped(x, par[1], par[2], par[3]))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[1], par[2], par[4], par[5], 1))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[1], par[2], par[4], par[5], 2))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[1], par[2], par[4], par[5], 3))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[1], par[2], par[4], par[5], 4))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[1], par[2], par[4], par[5], 5))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[1], par[2], par[4], par[5], 6))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[1], par[2], par[4], par[5], 7))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[1], par[2], par[4], par[5], 8))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[1], par[2], par[4], par[5], 9))
            if self.fit["model"] == Fit.GlobalNoise:
                self.canvas.ax.plot(x, SpeHist.global_noise_model(x, *self.fit["param"]))
                if check_status == 2:
                    par = self.fit["param"]
                    self.canvas.ax.plot(x, par[0] * (1 - par[1]) * SpeHist.s_ped(x, par[3], par[4], par[5]))
                    self.canvas.ax.plot(x, par[0] * par[1] * SpeHist.poisson(0, par[3]) * SpeHist.noise_exp(x, par[2], par[4]))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[3], par[4], par[6], par[7], 1, par[1] / par[2]))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[3], par[4], par[6], par[7], 2, par[1] / par[2]))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[3], par[4], par[6], par[7], 3, par[1] / par[2]))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[3], par[4], par[6], par[7], 4, par[1] / par[2]))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[3], par[4], par[6], par[7], 5, par[1] / par[2]))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[3], par[4], par[6], par[7], 6, par[1] / par[2]))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[3], par[4], par[6], par[7], 7, par[1] / par[2]))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[3], par[4], par[6], par[7], 8, par[1] / par[2]))
                    self.canvas.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[3], par[4], par[6], par[7], 9, par[1] / par[2]))
        else:
            pass

    def show_message(self, message: str):
        my_time = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]: \n")
        self.textBrowser.append(my_time + message)

    def show_table_data(self, qmi: QModelIndex):
        dir = self.lineEdit.text()
        file = qmi.data()
        file = os.path.join(dir, file)
        pd_data = pd.read_csv(file)
        pdm = PandasModel(pd_data)
        table = TableDialog(self, pdm)
        table.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = CallUiSPE()
    win.show()
    sys.exit(app.exec_())
