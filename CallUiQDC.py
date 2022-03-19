import time, sys, datetime, os
import numpy as np
from UiQDC import Ui_Form
from PmtDataSetTool import DataSetTool
from PmtConstant import Fit
from PmtSpeHist import SpeHist
from CallDialog import FitDialog, PandasModel, TableDialog
from Canvas import MatPlotCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd


class CallUiQDC(QWidget, Ui_Form):
    out_message = pyqtSignal(str)

    def __init__(self):
        super(CallUiQDC, self).__init__()
        self.setupUi(self)
        # 控件初始状态
        self.switch_hist_setting(False, True)
        self.switch_fit_setting(False)
        self.switch_portion_setting(False, True)
        self.switch_graph_setting()
        # text Browser展示信息
        self.out_message.connect(self.append_message)
        # 对table widget的一些初始化设置
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # 加载文件动作
        self.pushButton.clicked.connect(self.add_files)
        # 删除文件动作
        self.pushButton_2.clicked.connect(self.remove_file)
        # 右键请求
        self.tableWidget.customContextMenuRequested.connect(self.set_channel)
        # 选择行动作
        self.tableWidget.clicked.connect(self.select_row)
        # 打开原始数据动作
        self.tableWidget.doubleClicked.connect(self.show_table_data)
        # radio状态
        self.radioButton.setChecked(True)
        self.radioButton.toggled.connect(self.custom_hist_setting)
        # 绘制谱图
        self.pushButton_3.clicked.connect(self.draw_hist)
        # 拟合设置
        self.comboBox.addItems(["高斯拟合", "全局拟合", "全局拟合(含噪声)"])
        self.pushButton_4.clicked.connect(self.set_fit_param)
        # 拟合绘制曲线
        self.pushButton_5.clicked.connect(self.refresh)
        # 设置拟合曲线checkbox三种状态
        self.checkBox_4.setTristate(True)
        # 绘图区的checkBox
        self.checkBox.toggled.connect(self.refresh)
        self.checkBox_2.toggled.connect(self.refresh)
        self.checkBox_3.toggled.connect(self.refresh)
        self.checkBox_4.stateChanged.connect(self.refresh)
        # 事例数比例计算
        self.lineEdit_4.editingFinished.connect(self.proportion)
        # Canvas
        self.mpc = MatPlotCanvas(self, 5, 10)
        self.ntb = NavigationToolbar(self.mpc, self)
        self.gridLayout_5.addWidget(self.ntb, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.mpc, 2, 0, 1, 1)

        # 成员变量
        self.tab_list = []
        self.hist_list = []
        self.fit = {"model": Fit.NoFit, "param": None}

    def switch_hist_setting(self, widget: bool, zero: bool = False):
        self.radioButton.setEnabled(widget)
        self.radioButton_2.setEnabled(widget)
        if zero is True:
            self.spinBox.setValue(0)
            self.spinBox_2.setValue(0)
        if self.radioButton.isChecked():
            self.spinBox.setEnabled(False)
            self.spinBox_2.setEnabled(False)
        else:
            self.spinBox.setEnabled(widget)
            self.spinBox_2.setEnabled(widget)
        self.pushButton_3.setEnabled(widget)

    def switch_fit_setting(self, widget: bool):
        self.comboBox.setEnabled(widget)
        self.pushButton_4.setEnabled(widget)
        self.pushButton_5.setEnabled(widget)

    def switch_portion_setting(self, widget: bool, clear: bool = False):
        if clear is True:
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            self.lineEdit_6.clear()
            self.lineEdit_7.clear()
        self.lineEdit_4.setEnabled(widget)
        self.lineEdit_5.setEnabled(widget)
        self.lineEdit_6.setEnabled(widget)
        self.lineEdit_7.setEnabled(widget)

    def switch_graph_setting(self, c1: bool = False, c2: bool = False, c3: bool = False, c4: bool = False,
                             check: bool = False):
        if check is False:
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)
        self.checkBox.setEnabled(c1)
        self.checkBox_2.setEnabled(c2)
        self.checkBox_3.setEnabled(c3)
        self.checkBox_4.setEnabled(c4)

    def add_files(self):
        file_names, file_type = QFileDialog.getOpenFileNames(parent=self, caption="添加文件",
                                                             directory="/run/media/einstein/Elements/CR160_SPE/2022.01.17/", filter="txtFile (*txt)")
        if len(file_names) == 0:
            QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)
        else:
            self.tab_list = self.tab_list + file_names
            self.tableWidget.setRowCount(len(self.tab_list))
            print("Hello")
            base_names = list(map(os.path.basename, self.tab_list))
            for i in range(len(base_names)):
                new_item = QTableWidgetItem(base_names[i])
                self.tableWidget.setItem(i, 0, new_item)
                self.tableWidget.setItem(i, 1, QTableWidgetItem("0"))

    def remove_file(self):
        model_index = self.tableWidget.selectionModel().selection().indexes()
        if len(model_index) == 0:
            QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)
        else:
            row = model_index[0].row()
            self.tab_list.pop(row)
            self.tableWidget.removeRow(row)
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            if self.tableWidget.rowCount() != 0:
                self.switch_hist_setting(False)
            else:
                self.switch_hist_setting(False, True)
            self.switch_portion_setting(False, True)
            self.switch_fit_setting(False)
            self.switch_graph_setting(False, False, False, False, False)
            # 拟合flag调整到非拟合状态
            self.fit["model"] = Fit.NoFit

    def set_channel(self, pos):
        select_list = self.tableWidget.selectionModel().selection().indexes()
        if len(select_list) != 0:
            menu = QMenu()
            row = select_list[0].row()
            pd_data = pd.read_table(self.tab_list[row])
            for i in range(len(pd_data.columns)):
                menu.addAction("channel: {}".format(i))
            global_pos = self.tableWidget.mapToGlobal(pos)
            action = menu.exec_(global_pos)
            if action is None:
                return None
            else:
                set_channel = str(int(action.text().split(":")[1]))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(set_channel))
                self.lineEdit_2.setText(set_channel)
        else:
            QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)

    def select_row(self, index: QModelIndex):
        file = self.tab_list[index.row()]
        self.lineEdit.setText(os.path.dirname(file))
        self.lineEdit_2.setText(self.tableWidget.selectionModel().selection().indexes()[1].data())
        self.lineEdit_3.setText(str(pd.read_table(file).shape[0]))
        self.spinBox.setRange(0, int(self.lineEdit_3.text()))
        self.spinBox_2.setRange(0, int(self.lineEdit_3.text()))
        self.switch_hist_setting(True)
        self.switch_portion_setting(False, True)
        self.switch_fit_setting(False)
        self.switch_graph_setting()
        # 拟合flag调整到非拟合状态
        self.fit["model"] = Fit.NoFit

    def custom_hist_setting(self):
        if self.radioButton.isChecked():
            self.spinBox.setEnabled(False)
            self.spinBox_2.setEnabled(False)
        else:
            self.spinBox.setEnabled(True)
            self.spinBox_2.setEnabled(True)

    def draw_hist(self):
        self.hist_list.clear()
        self.mpc.initial(x_label="25fC/Channel", y_label="count", title="single photon spectra [QDC]")
        # 获取所选择的QModelIndex
        model_index_list = self.tableWidget.selectionModel().selection().indexes()
        selected_file_and_channel = [[], []]
        qdc_hist_content = []
        if len(model_index_list) != 0:
            # 通过QModelIndex的row()从self变量中找到对应文件的路径
            # 并将文件路径添加到selected_file_and_channel中
            for i in range(0, len(model_index_list), 2):
                selected_file_and_channel[0].append(self.tab_list[model_index_list[i].row()])
                selected_file_and_channel[1].append(int(model_index_list[i + 1].data()))
            # 读取selected_file_and_channel中的qdc文件，将读取到的hist_content添加到
            # qdc_hist_content中
            for i in range(len(selected_file_and_channel[0])):
                qdc_hist_content.append(DataSetTool.read_qdc(selected_file_and_channel[0][i],
                                                             selected_file_and_channel[1][i]))
            if self.radioButton.isChecked():
                # 默认bins
                bounds = []
                for i in qdc_hist_content:
                    bounds.append(i.min())
                    bounds.append(i.max())
                bins = DataSetTool.qdc_bins(int(np.array(bounds).min()), int(np.array(bounds).max()))
                for i in qdc_hist_content:
                    # 遍历qdc_hist_content实例化SpeHist类
                    self.hist_list.append(SpeHist(i, bins))
            else:
                #自定义bin
                if self.spinBox.value() >= self.spinBox_2.value():
                    QMessageBox.warning(self, "警告", "参数设置错误", QMessageBox.Ok)
                    return None
                else:
                    bins = DataSetTool.qdc_bins(self.spinBox.value(), self.spinBox_2.value())
                    print(bins)
                    for i in qdc_hist_content:
                        self.hist_list.append(SpeHist(i, bins))
            # 设置其他控件的状态
            if len(model_index_list) == 2:
                self.switch_fit_setting(True)
                self.switch_portion_setting(True)
                self.switch_graph_setting(True, False, True, True)
                self.checkBox.setChecked(True)
            else:
                self.switch_fit_setting(False)
                self.switch_portion_setting(False, True)
                self.switch_graph_setting(True, True, False, False)
            for i in self.hist_list:
                if self.checkBox.isChecked():
                    self.mpc.ax.hist(i.get_scatter()[0], i.get_hist()[1], weights=i.get_hist()[0])
                else:
                    self.mpc.ax.hist(i.get_scatter()[0], i.get_hist()[1], weights=i.get_hist()[0], histtype="step")
            print("draw!!")
            self.mpc.draw()
            # 拟合flag调整到非拟合状态
            self.fit["model"] = Fit.NoFit
        else:
            QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)

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
        print("fit model: {}".format(dict_data["model"]))
        if dict_data["model"] == Fit.Gauss:
            flag, interval1, interval2 = DataSetTool.comma2interval(dict_data["interval"])
            print(flag, interval1, interval2)
        if dict_data["model"] == Fit.Gauss and len(self.hist_list) == 1 and flag:
            print("param setting: {}".format(dict_data))
            fit_par, fit_cov = self.hist_list[0].fit_spe(dict_data["model"], interval1, interval2, *dict_data["param"])
            self.fit["param"] = fit_par
            self.fit["model"] = Fit.Gauss
        elif dict_data["model"] == Fit.Global and len(self.hist_list) == 1:
            fit_par, fit_cov = self.hist_list[0].fit_spe(dict_data["model"], 1, 1, *dict_data["param"])
            self.fit["param"] = fit_par
            self.fit["model"] = Fit.Global
        elif dict_data["model"] == Fit.GlobalNoise and len(self.hist_list) == 1:
            fit_par, fit_cov = self.hist_list[0].fit_spe(dict_data["model"], 1, 1, *dict_data["param"])
            self.fit["param"] = fit_par
            self.fit["model"] = Fit.GlobalNoise
        else:
            print("Fit is wrong")
        print("拟合参数为：\n{}".format(self.fit["param"]))
        if self.fit["model"] != Fit.NoFit:
            # 开启直方图控件， 关闭归一化控件， 开启散点控件， 开启fit控件
            self.switch_graph_setting(True, False, True, True)
        # 拟合参数格式化输出
        emit_message = "=" * 6 + "拟合结果为" + "=" * 6 + "\n"
        print("emit message")
        print("len: {}".format(len(self.fit["param"])))
        print("param: {}".format(self.fit["param"]))
        for i in range(len(self.fit["param"])):
            emit_message = emit_message + "param{0}: {1: .6g}".format(i, self.fit["param"][i]) + "\n"
        print(emit_message)
        self.out_message.emit(emit_message)

    def append_message(self, message: str):
        date_message = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]: \n")
        self.textBrowser.append(date_message + message)

    def collect_param(self):
        collection = {"hist": False, "normal": False, "scatter": False, "fitting": 0}
        if self.checkBox.isEnabled() and self.checkBox.isChecked():
            collection["hist"] = True
        if self.checkBox_2.isEnabled() and self.checkBox_2.isChecked():
            collection["normal"] = True
        if self.checkBox_3.isEnabled() and self.checkBox_3.isChecked():
            collection["scatter"] = True
        if self.checkBox_4.isEnabled() and self.checkBox_4.isChecked():
            collection["fitting"] = True
        return collection

    def refresh(self):
        self.mpc.initial(x_label="25fC/Channel", y_label="count", title="single photon spectra [QDC]")
        collection = self.collect_param()
        if len(self.hist_list) != 0:
            if collection["hist"] is True:
                for i in self.hist_list:
                    if collection["normal"] is True:
                        self.mpc.ax.hist(i.get_scatter()[0], i.get_hist()[1],
                                         weights=(i.get_hist()[0] / i.get_hist()[0].sum()))
                    else:
                        self.mpc.ax.hist(i.get_scatter()[0], i.get_hist()[1], weights=i.get_hist()[0])
            else:
                for i in self.hist_list:
                    if collection["normal"] is False:
                        self.mpc.ax.hist(i.get_scatter()[0], i.get_hist()[1], weights=i.get_hist()[0],
                                         histtype="step")
                    else:
                        self.mpc.ax.hist(i.get_scatter()[0], i.get_hist()[1],
                                         weights=(i.get_hist()[0] / i.get_hist()[0].sum()), histtype="step")
            if collection["scatter"] is True:
                for i in self.hist_list:
                    self.mpc.ax.scatter(i.get_scatter()[0], i.get_scatter()[1])
            if collection["fitting"] != 0 and self.fit["model"] != Fit.NoFit:
                print("checkbox4 status: {}".format(self.checkBox_4.checkState()))
                self.draw_fit(self.checkBox_4.checkState())
            self.mpc.draw()

    def draw_fit(self, check_status: int = 0):
        if self.fit["model"] != Fit.NoFit:
            x = self.hist_list[0].get_scatter()[0]
            if self.fit["model"] == Fit.Gauss and (check_status == 1 or check_status == 2):
                self.mpc.ax.plot(x, SpeHist.gauss(x, *self.fit["param"]))
            if self.fit["model"] == Fit.Global:
                self.mpc.ax.plot(x, SpeHist.global_model(x, *self.fit["param"]))
                if check_status == 2:
                    par = self.fit["param"]
                    print("enter!!")
                    self.mpc.ax.plot(x, par[0] * SpeHist.s_ped(x, par[1], par[2], par[3]))
                    self.mpc.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[1], par[2], par[4], par[5], 1))
                    self.mpc.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[1], par[2], par[4], par[5], 2))
                    self.mpc.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[1], par[2], par[4], par[5], 3))
                    self.mpc.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[1], par[2], par[4], par[5], 4))
                    self.mpc.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[1], par[2], par[4], par[5], 5))
            if self.fit["model"] == Fit.GlobalNoise:
                self.mpc.ax.plot(x, SpeHist.global_noise_model(x, *self.fit["param"]))
                if check_status == 2:
                    par = self.fit["param"]
                    self.mpc.ax.plot(x, par[0] * (1 - par[1]) * SpeHist.s_ped(x, par[3], par[4], par[5]))
                    self.mpc.ax.plot(x, par[0] * par[1] * SpeHist.poisson(0, par[3]) * SpeHist.noise_exp(x, par[2], par[4]))
                    self.mpc.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[3], par[4], par[6], par[7], 1, par[1] / par[2]))
                    self.mpc.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[3], par[4], par[6], par[7], 2, par[1] / par[2]))
                    self.mpc.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[3], par[4], par[6], par[7], 3, par[1] / par[2]))
                    self.mpc.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[3], par[4], par[6], par[7], 4, par[1] / par[2]))
                    self.mpc.ax.plot(x, par[0] * SpeHist.n_gauss(x, par[3], par[4], par[6], par[7], 5, par[1] / par[2]))
        else:
            pass

    def proportion(self):
        threshold = float(self.lineEdit_4.text())
        content, bins = self.hist_list[0].get_hist()
        part1_indexes = np.where(bins < threshold)[0]
        part2_indexes = np.where(bins >= threshold)[0]
        part1 = content[part1_indexes].sum()
        print("len: {}".format(len(content)))
        print("part2: {}".format(part2_indexes[: -1]))
        # print("content: {}".format(content[396]))
        part2 = content[part2_indexes[: -1]].sum()
        print("part2: {}".format(part2))
        total = part1 + part2
        self.lineEdit_5.setText(str(total))
        self.lineEdit_6.setText(str(format(part1 / total, ".5f")))
        self.lineEdit_7.setText(str(format(part2 / total, ".5f")))

    def show_table_data(self, qmi: QModelIndex):
        file = self.tab_list[qmi.row()]
        if DataSetTool.check_file(file):
            pd_data = pd.read_table(file)
            col = []
            for i in range(len(pd_data.columns)):
                col.append("channel {}".format(i))
            pd_data.columns = col
            pdm = PandasModel(pd_data)
            table = TableDialog(self, pdm)
            table.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = CallUiQDC()
    ui.show()
    sys.exit(app.exec_())