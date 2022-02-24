import numpy as np
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
from CallDialog import FitDialog
import matplotlib.pyplot as plt


class CallUiSPE(Ui_Form, QWidget):
    out_message = pyqtSignal(str)

    def __init__(self):
        super(CallUiSPE, self).__init__()
        self.setupUi(self)
        self.out_message.connect(self.show_message)
        self.pushButton_2.setVisible(False)
        self.textBrowser_2.setVisible(False)
        self.switch_portion(False)
        self.switch_hist_setting(False)
        self.switch_fit_setting(False)
        self.switch_graph_setting(False)
        self.pushButton.clicked.connect(self.add_files)
        self.pushButton_3.clicked.connect(self.remove_file)
        self.pushButton_4.clicked.connect(self.clear_listview)
        self.listView.clicked.connect(self.show_file_info)
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
        self.pushButton_8.clicked.connect(self.draw_hist)
        self.lineEdit_8.setValidator(sci_validator)
        self.lineEdit_8.editingFinished.connect(self.proportion)
        self.comboBox.addItems(["单高斯拟合", "双高斯拟合"])
        self.pushButton_6.clicked.connect(self.set_fit_param)
        self.pushButton_7.clicked.connect(self.refresh)
        self.checkBox.toggled.connect(self.refresh)
        self.checkBox_2.toggled.connect(self.refresh)
        self.checkBox_3.toggled.connect(self.refresh)

        # var
        self.files_list = []
        self.spe = []
        self.hist = []
        self.fit = {"model": None, "param": None}

        # Canvas
        self.canvas = MatPlotCanvas(self, width=5, height=5)
        self.tool_bar = NavigationToolbar(self.canvas, self)
        canvas_size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas_size_policy.setHorizontalStretch(0)
        canvas_size_policy.setVerticalStretch(2)
        self.canvas.setSizePolicy(canvas_size_policy)
        self.gridLayout_6.addWidget(self.tool_bar, 2, 0, 1, 1)
        self.gridLayout_6.addWidget(self.canvas, 3, 0, 1, 1)

    def switch_hist_setting(self, status: bool, clear: bool = False):
        if clear is True and self.lineEdit_6.isEnabled():
            self.lineEdit_6.clear()
            self.lineEdit_7.clear()
        self.lineEdit_6.setEnabled(status)
        self.lineEdit_7.setEnabled(status)
        self.pushButton_8.setEnabled(status)

    def switch_fit_setting(self, status: bool):
        self.comboBox.setEnabled(status)
        self.pushButton_6.setEnabled(status)
        self.pushButton_7.setEnabled(status)

    def switch_portion(self, status: bool, clear: bool = False):
        if clear is True and self.lineEdit_8.isEnabled():
            self.lineEdit_8.clear()
            self.lineEdit_9.clear()
            self.lineEdit_10.clear()
            self.lineEdit_11.clear()
        self.lineEdit_8.setEnabled(status)
        self.lineEdit_9.setEnabled(status)
        self.lineEdit_10.setEnabled(status)
        self.lineEdit_11.setEnabled(status)

    def switch_graph_setting(self, status: bool):
        self.pushButton_5.setEnabled(status)
        self.checkBox.setEnabled(status)
        self.checkBox_2.setEnabled(status)
        self.checkBox_3.setEnabled(status)

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
            self.switch_hist_setting(True)
            if self.checkBox.isChecked():
                self.lineEdit_6.setEnabled(False)
                self.lineEdit_7.setEnabled(False)

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

    def clear_listview(self):
        self.files_list.clear()
        slm = QStringListModel()
        slm.setStringList([])
        self.listView.setModel(slm)
        self.switch_hist_setting(False, True)
        self.switch_graph_setting(False)
        self.switch_portion(False, True)

    def show_file_info(self, index: QModelIndex):
        file = self.files_list[index.row()]
        pd_data = DataSetTool.read_file(file)
        self.lineEdit_2.setText(os.path.basename(file))
        self.lineEdit.setText(os.path.dirname(file))
        self.lineEdit_3.setText(str(len(pd_data)) + " X " + str(len(pd_data.columns)))
        self.lineEdit_4.setText(str(format(os.path.getsize(file) / 1024, '.2f')) + " kB")
        self.fit["model"] = None

    def switch_bin_setting(self):
        print("enter radio")
        if self.radioButton.isChecked():
            self.switch_hist_setting(False)
            self.pushButton_8.setEnabled(True)
        else:
            self.switch_hist_setting(True)

    def draw_hist(self):
        self.canvas.ax.cla()
        self.canvas.ax.grid(True)
        self.spe.clear()
        self.hist.clear()
        scale = float(self.lineEdit_5.text())
        bound = []
        for i in self.listView.selectedIndexes():
            spe = SinglePhotonSpectrum(DataSetTool.read_file(self.files_list[i.row()]), scale)
            self.spe.append(spe)
            bound.append(spe.get_info(spe.get_scale())["min"])
            bound.append(spe.get_info(spe.get_scale())["max"])
        default_bins = np.linspace(np.array(bound).min(), np.array(bound).max(), 301)
        print("default bin: {}".format(default_bins))
        if self.radioButton.isChecked():
            for i in self.spe:
                self.hist.append(SpeHist(i.get_charge(), default_bins, scale))
        else:
            print("custom bin!!!")
            comma2interval = DataSetTool.comma2interval(self.lineEdit_6.text())
            if comma2interval[0]:
                print(comma2interval)
                custom_bin = np.linspace(comma2interval[1], comma2interval[2], int(self.lineEdit_7.text()) + 1)
                for i in self.spe:
                    self.hist.append(SpeHist(i.get_charge(), custom_bin, scale))
            else:
                QMessageBox.warning(None, "警告", "区间设置错误", QMessageBox.Ok)
        for i in self.hist:
            self.canvas.ax.hist(i.get_scatter()[0], i.get_hist()[1], weights=i.get_hist()[0])
        self.canvas.draw()
        self.switch_graph_setting(True)
        if len(self.spe) == 1:
            self.switch_fit_setting(True)
            self.switch_portion(True, True)
        else:
            self.switch_fit_setting(False)
            self.switch_portion(False, True)

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
            dialog = FitDialog(self, Fit.DoubleGauss)
            dialog.out_message.connect(self.fitting)
            dialog.show()
        else:
            QMessageBox.warning(None, "警告", "拟合选项错误", QMessageBox.Ok)

    def fitting(self, dict_data: dict):
        self.fit["model"] = None
        print("Enter fit")
        if dict_data["accept"] is True:
            flag, interval1, interval2 = DataSetTool.comma2interval(dict_data["interval"])
            if dict_data["model"] == Fit.Gauss and len(self.hist) != 0 and flag:
                print("param setting: {}".format(dict_data))
                ppot, pcov = self.hist[0].fit_spe(dict_data["model"], interval1, interval2, float(dict_data["p1"]),
                                                  float(dict_data["p2"]), float(dict_data["p3"]))
                self.fit["param"] = ppot
                self.fit["model"] = Fit.Gauss
                # debug
                # f, a = plt.subplots()
                # xx = np.linspace(-2, 2, 1000)
                # a.plot(xx, SpeHist.model_gauss(xx, *ppot))
                # plt.show()
            elif dict_data["model"] == Fit.DoubleGauss and len(self.hist) != 0 and flag:
                ppot, pcov = self.hist[0].fit_spe(dict_data["model"], interval1, interval2, float(dict_data["p5"]),
                                                  float(dict_data["p0"]), float(dict_data["p1"]), float(dict_data["p2"]),
                                                  float(dict_data["p3"]), float(dict_data["p4"]))
                self.fit["param"] = ppot
                self.fit["model"] = Fit.DoubleGauss
            else:
                print("Fit is wrong")
            print("拟合参数为：\n{}".format(self.fit["param"]))
            self.out_message.emit("拟合参数为：\n{}".format(self.fit["param"]))
        else:
            print("Fit is wrong")

    def collect_param(self):
        print("Enter collection")
        print(self.fit)
        collection = {"hist": False, "scatter": False, "fitting": False}
        if self.checkBox.isEnabled():
            if self.checkBox.isChecked():
                collection["hist"] = True
            print("hist status: {}".format(collection["hist"]))
            if self.checkBox_2.isChecked():
                collection["scatter"] = True
            print("scatter status: {}".format(collection["scatter"]))
            print("fit model: {}".format(self.fit["model"]))
            if self.checkBox_3.isChecked() and self.fit["model"] is not None:
                collection["fitting"] = True
                print("fitting status: {}".format(collection["fitting"]))
            return collection
        else:
            return None

    def refresh(self):
        print("Enter refresh fun")
        self.canvas.ax.cla()
        self.canvas.ax.grid(True)
        collection = self.collect_param()
        print(collection)
        if collection is not None and len(self.hist) != 0:
            print(collection["hist"])
            if collection["hist"] is True:
                for i in self.hist:
                    self.canvas.ax.hist(i.get_scatter()[0], i.get_hist()[1], weights=i.get_hist()[0])
            else:
                for i in self.hist:
                    self.canvas.ax.hist(i.get_scatter()[0], i.get_hist()[1], weights=i.get_hist()[0], histtype="step")
            if collection["scatter"] is True:
                for i in self.hist:
                    self.canvas.ax.scatter(i.get_scatter()[0], i.get_scatter()[1])
            if collection["fitting"] is True and self.fit["model"] is not None:
                xx = self.hist[0].get_scatter()[0]
                if self.fit["model"] == Fit.Gauss:
                    self.canvas.ax.plot(xx, self.hist[0].model_gauss(xx, *self.fit["param"]))
                    # debug
                    # f, a = plt.subplots()
                    # a.plot(xx, self.hist[0].model_gauss(xx, *self.fit["param"]))
                    # plt.show()
                if self.fit["model"] == Fit.DoubleGauss:
                    self.canvas.ax.plot(xx, self.hist[0].model_double_gauss(xx, *self.fit["param"]))
            self.canvas.draw()

    def show_message(self, message: str):
        self.textBrowser.append(message)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    win = CallUiSPE()
    win.show()
    sys.exit(app.exec_())
