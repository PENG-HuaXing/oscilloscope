from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from UiRaiseTime import Ui_Form
from PmtDataSetTool import DataSetTool
from PmtConstant import RaiseTime, Processing, Fit
from PmtWaveForm import WaveForm
from CallDialog import PandasModel, RaiseTimeSetBin, FitDialog
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from Canvas import MatPlotCanvas
from DoubleCanvas import MatPlotDoubleCanvas
import time, os, datetime, hashlib, scipy.optimize
import pandas as pd
import numpy as np


class CallUiRaiseTime(QWidget, Ui_Form):
    text_message = pyqtSignal(str)

    def __init__(self):
        super(CallRaiseTime, self).__init__()
        self.setupUi(self)
        # text browser 输出进程信息
        self.text_message.connect(self.append_message)
        # radio button 分组
        group1 = QButtonGroup(self)
        group2 = QButtonGroup(self)
        group1.addButton(self.radioButton)
        group1.addButton(self.radioButton_2)
        group2.addButton(self.radioButton_3)
        group2.addButton(self.radioButton_4)

        # tableView
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        self.tableView.installEventFilter(self)

        # 控件初始化
        self.switch_filter1(False, True)
        self.switch_file_message(False, True)
        self.switch_raise_time_setting(False, True, False)
        self.switch_save_and_loop(False)
        self.switch_filter2(False, True)
        self.switch_processing(False)
        self.switch_graph_setting(False, True)
        # 加载SPE数据
        self.pushButton_13.clicked.connect(self.add_files)
        # 移除SPE数据
        self.pushButton_14.clicked.connect(self.remove_file)
        # 选择SPE文件
        self.listView.clicked.connect(self.select_file)
        # 筛选信号文件
        self.pushButton_10.clicked.connect(self.filter1)
        # 上升时间设置
        # 初始状态为三次函数拟合模型
        self.radioButton.setChecked(True)
        # 自定义基线计算
        self.checkBox.toggled.connect(self.set_ped)
        self.radioButton_3.toggled.connect(self.custom_ped)
        self.pushButton_11.clicked.connect(self.raise_time_ok)
        self.pushButton_12.clicked.connect(self.raise_time_reset)
        # 设置lineEdit的验证器
        interval_reg = QRegExp(r"^(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)\s*,"
                               r"\s*(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)")
        interval_validator = QRegExpValidator(self)
        interval_validator.setRegExp(interval_reg)
        self.lineEdit_5.setValidator(interval_validator)
        self.lineEdit_8.setValidator(interval_validator)
        self.lineEdit_9.setValidator(interval_validator)
        self.lineEdit_11.setValidator(interval_validator)
        self.lineEdit_12.setValidator(interval_validator)
        self.lineEdit_13.setValidator(interval_validator)
        # 保存文件设置
        self.pushButton_15.clicked.connect(self.select_save_file)
        # 筛选R2
        self.pushButton_2.clicked.connect(self.filter_r2)
        # 载入RaiseTime文件
        self.pushButton_3.clicked.connect(self.select_raise_time_file)
        #
        self.tableView.clicked.connect(self.show_wave)
        # 绘制raise time分布
        self.pushButton_4.clicked.connect(lambda: self.show_raise_time(np.array([])))
        # 设置bins
        self.pushButton_16.clicked.connect(self.set_bins)
        # 创建循环计算线程
        self.my_thread = WorkThread(self.loop)
        # 循环计算结束信号绑定
        self.my_thread.finished.connect(self.work_finish)
        # 开始进行循环计算
        self.pushButton.clicked.connect(self.start_thread)
        # 进程控制
        self.pushButton_5.clicked.connect(lambda: self.set_processing_flag(self.pushButton_5))
        self.pushButton_6.clicked.connect(lambda: self.set_processing_flag(self.pushButton_6))
        self.pushButton_7.clicked.connect(lambda: self.set_processing_flag(self.pushButton_7))
        # 拟合raise time
        self.pushButton_8.clicked.connect(self.set_fit_param)

        # 成员变量
        self.spe_files_list = []
        self.filter1_data = pd.DataFrame()
        self.raise_time_data = pd.DataFrame()
        self.processing_flag = Processing.Go
        self.raise_time_hist = dict()

        # canvas
        self.mpc1 = MatPlotDoubleCanvas(self)
        self.mpc2 = MatPlotCanvas(self)
        self.ntb1 = NavigationToolbar(self.mpc1, self)
        self.ntb2 = NavigationToolbar(self.mpc2, self)
        self.gridLayout_5.addWidget(self.ntb1, 2, 0, 1, 1)
        self.gridLayout_5.addWidget(self.mpc1, 3, 0, 1, 1)
        self.gridLayout_5.addWidget(self.ntb2, 4, 0, 1, 1)
        self.gridLayout_5.addWidget(self.mpc2, 5, 0, 1, 1)

    def switch_filter1(self, widget: bool, clear: bool = False):
        if clear is True:
            self.lineEdit_5.clear()
        self.lineEdit_5.setEnabled(widget)
        self.pushButton_10.setEnabled(widget)

    def switch_file_message(self, widget: bool, clear: bool = True):
        if clear is True:
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_6.clear()
            self.lineEdit_7.clear()
        self.lineEdit_2.setEnabled(widget)
        self.lineEdit_3.setEnabled(widget)
        self.lineEdit_4.setEnabled(widget)
        self.lineEdit_6.setEnabled(widget)
        self.lineEdit_7.setEnabled(widget)

    def switch_raise_time_setting(self, widget: bool, clear: bool = False, visible: bool = False):
        if clear is True:
            self.lineEdit_8.clear()
            self.lineEdit_9.clear()
        self.radioButton_3.setVisible(visible)
        self.radioButton_4.setVisible(visible)
        self.label_10.setVisible(visible)
        self.lineEdit_9.setVisible(visible)
        if visible is False:
            self.lineEdit_9.clear()
        self.radioButton.setEnabled(widget)
        self.radioButton_2.setEnabled(widget)
        self.lineEdit_8.setEnabled(widget)
        self.checkBox.setEnabled(widget)
        self.radioButton_3.setEnabled(widget)
        self.radioButton_4.setEnabled(widget)
        self.lineEdit_9.setEnabled(widget)
        self.pushButton_11.setEnabled(widget)
        self.pushButton_12.setEnabled(widget)

    def switch_save_and_loop(self, widget: bool):
        self.lineEdit_10.setEnabled(widget)
        self.pushButton_15.setEnabled(widget)
        self.pushButton.setEnabled(widget)
        if widget is True:
            self.lineEdit_10.setText("./RaiseTime.csv")
        if widget is False:
            self.lineEdit_10.clear()

    def switch_filter2(self, widget: bool, clear: bool = True):
        self.pushButton_2.setEnabled(widget)
        self.lineEdit_11.setEnabled(widget)
        if clear is True:
            self.lineEdit_11.clear()

    def switch_processing(self, widget: bool):
        self.pushButton_5.setEnabled(widget)
        self.pushButton_6.setEnabled(widget)
        self.pushButton_7.setEnabled(widget)

    def switch_graph_setting(self, widget: bool, clear: bool = False):
        self.pushButton_4.setEnabled(widget)
        self.pushButton_16.setEnabled(widget)
        self.checkBox_2.setEnabled(widget)
        self.checkBox_3.setEnabled(widget)
        self.lineEdit_12.setEnabled(widget)
        self.lineEdit_13.setEnabled(widget)
        if clear is True:
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.lineEdit_12.clear()
            self.lineEdit_13.clear()

    def add_files(self):
        files, filetype = QFileDialog.getOpenFileNames(parent=self, caption="添加文件",
                                                       directory="/run/media/einstein/Elements/CR160_data",
                                                       filter="csvFile (*csv)")
        if len(files) == 0:
            print(len(files))
            QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)
        else:
            self.spe_files_list = self.spe_files_list + files
            base_name = list(map(os.path.basename, self.spe_files_list))
            slm = QStringListModel()
            slm.setStringList(base_name)
            self.listView.setModel(slm)
        self.switch_filter2(False, True)
        slm = QStringListModel()
        slm.setStringList([])
        self.tableView.setModel(slm)
        self.switch_graph_setting(False, True)
        self.lineEdit_14.clear()

    def remove_file(self):
        qmi = self.listView.currentIndex()
        if qmi.row() == -1:
            QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)
        else:
            index = qmi.row()
            self.spe_files_list.pop(index)
            base_name = list(map(os.path.basename, self.spe_files_list))
            slm = QStringListModel()
            slm.setStringList(base_name)
            self.listView.setModel(slm)
            if len(self.spe_files_list) == 0:
                self.switch_filter1(False, True)
            else:
                self.switch_filter1(False, False)
            self.switch_file_message(False, True)
            self.switch_raise_time_setting(False, True, False)
            self.switch_save_and_loop(False)
            self.switch_filter2(False, True)
            self.switch_graph_setting(False, True)
            self.lineEdit.clear()
            slm = QStringListModel()
            slm.setStringList([])
            self.listView_2.setModel(slm)

    def select_file(self, qmi: QModelIndex):
        self.switch_filter1(True)
        self.lineEdit.setText(os.path.dirname(self.spe_files_list[qmi.row()]))

    def filter1(self):
        qmi = self.listView.currentIndex()
        if qmi.row() == -1:
            QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)
        else:
            check, val1, val2 = DataSetTool.comma2interval(self.lineEdit_5.text())
            if check is False:
                QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)
            else:
                spe_data = pd.read_csv(self.spe_files_list[qmi.row()])
                self.filter1_data = spe_data[spe_data["Q"] > val1]
                self.filter1_data = self.filter1_data[self.filter1_data["Q"] < val2]
                if len(self.filter1_data) == 0:
                    QMessageBox.warning(self, "警告", "筛选结果为空", QMessageBox.Ok)
                else:
                    wave = WaveForm.load_from_file(self.filter1_data["File"].iloc[0])
                    self.lineEdit_6.setText(os.path.dirname(self.filter1_data["File"].iloc[0]))
                    self.lineEdit_4.setText(str(len(self.filter1_data)))
                    self.lineEdit_3.setText(format(wave.get_delta_time(), ".3e"))
                    self.lineEdit_2.setText(format(wave.get_time_bound()[0], ".3e"))
                    self.lineEdit_7.setText(format(wave.get_time_bound()[1], ".3e"))
                    base_name = list(map(os.path.basename, self.filter1_data["File"]))
                    base_name.sort()
                    slm = QStringListModel()
                    slm.setStringList(base_name)
                    self.listView_2.setModel(slm)
                    self.switch_file_message(True, False)
                    self.switch_raise_time_setting(True, False, False)
                    self.switch_save_and_loop(False)
                    self.switch_filter2(False, True)

    def set_ped(self):
        if self.checkBox.isChecked():
            self.switch_raise_time_setting(True, False, True)
            self.radioButton_4.setChecked(True)
        else:
            self.switch_raise_time_setting(True, False, False)
            self.lineEdit_9.clear()

    def custom_ped(self):
        if self.radioButton_3.isChecked():
            self.lineEdit_9.setEnabled(False)
        else:
            self.lineEdit_9.setEnabled(True)

    def raise_time_ok(self):
        if self.lineEdit_8.text() == "" or (self.checkBox.isChecked() and self.radioButton_4.isChecked()\
                                            and self.lineEdit_9.text() == ""):
            QMessageBox.warning(self, "警告", "参数设置错误", QMessageBox.Ok)
        else:
            if self.checkBox.isChecked():
                self.switch_raise_time_setting(False, False, True)
            else:
                self.switch_raise_time_setting(False, False, False)
            self.pushButton_12.setEnabled(True)
            self.switch_save_and_loop(True)

    def raise_time_reset(self):
        if self.checkBox.isChecked():
            self.switch_raise_time_setting(True, False, True)
        else:
            self.switch_raise_time_setting(True, False, False)
        self.switch_save_and_loop(False)
        self.switch_filter2(False, True)
        self.switch_graph_setting(False, True)

    def select_save_file(self):
        save_file, file_type = QFileDialog.getSaveFileName(self, "保存文件", "./RaiseTime.csv", "csv文件 (*csv)")
        print("保存文件: {}".format(save_file))
        print("文件格式: {}".format(file_type))
        if DataSetTool.check_file(os.path.dirname(save_file)):
            self.lineEdit_10.setText(save_file)
        else:
            QMessageBox.warning(self, "警告", "文件夹无效", QMessageBox.Ok)

    def collect_param(self):
        param = dict()
        if self.radioButton.isChecked():
            param["fit_model"] = RaiseTime.Cubic
        else:
            param["fit_model"] = RaiseTime.Proportion
        param["signal_interval1"] = DataSetTool.comma2interval(self.lineEdit_8.text())[1]
        param["signal_interval2"] = DataSetTool.comma2interval(self.lineEdit_8.text())[2]
        if self.checkBox.isChecked():
            param["ped"] = RaiseTime.Ped
            if self.radioButton_3.isChecked():
                param["ped_type"] = RaiseTime.Default
            else:
                param["ped_type"] = RaiseTime.Custom
                param["ped_interval1"] = DataSetTool.comma2interval(self.lineEdit_9.text())[1]
                param["ped_interval2"] = DataSetTool.comma2interval(self.lineEdit_9.text())[2]
        else:
            param["ped"] = RaiseTime.NoPed
        param["save_file"] = self.lineEdit_10.text()
        return param

    def loop(self):
        self.raise_time_data = pd.DataFrame()
        save_data = []
        error_file = []
        param = self.collect_param()
        for i in range(len(self.filter1_data)):
            print("文件名称: {}".format(self.filter1_data.iloc[i, 0]))
            self.text_message.emit(self.filter1_data.iloc[i, 0])
            file_name = self.filter1_data.iloc[i, 0]
            wave = WaveForm.load_from_file(file_name)
            # 对基线进行设置
            if param["ped"] == RaiseTime.NoPed:
                ped = 0
            elif param["ped"] == RaiseTime.Ped and param["ped_type"] == RaiseTime.Default:
                ped = self.filter1_data.iloc[i, 2]
            elif param["ped"] == RaiseTime.Ped and param["ped_type"] == RaiseTime.Custom:
                ped = wave.pedestal(param["ped_interval1"], param["ped_interval2"])
            else:
                ped = 0
            min_value, min_index = wave.min_ampl(param["signal_interval1"], param["signal_interval2"])
            # index左移一个单位
            index10 = min_index - 1
            index90 = min_index - 1
            # 获取波形的时幅数据
            t = wave.get_time()
            a = wave.get_ampl()
            while True:
                if a[index10] - ped > 0.1 * (min_value - ped):
                    break
                else:
                    index10 -= 1
            while True:
                if a[index90] - ped > 0.9 * (min_value - ped):
                    break
                else:
                    index90 -= 1
            if np.fabs(index90 - index10) <= 3 or index90 <= 0 or index10 <= 0:
                # 筛去index异常的数据
                continue
            print("index10&90: {}| {}".format(index10, index90))
            # 线性拟合 or 直线拟合
            if param["fit_model"] == RaiseTime.Cubic:
                # 时幅数据在10%处向左移动5个index， 在90%处向右移动5个index
                # 将这些数据作为三次函数拟合的样本点
                lead_edge_t = t[index10 - 5: min_index + 5]
                lead_edge_a = a[index10 - 5: min_index + 5]
                fit_par, residuals, rank, singular_values, rcond = np.polyfit(lead_edge_t, lead_edge_a, 3, full=True)
                # print("拟合参数 a: {} | b: {} | c: {} | d: {} ".format(fit_par[0], fit_par[1], fit_par[2], fit_par[3]))
                # 判断三次函数存在极值点，并且极小值点在样本点的范围内
                if DataSetTool.extreme_cubic_fun(*fit_par) is not None and \
                   (lead_edge_t[0] < DataSetTool.extreme_cubic_fun(*fit_par)[1] < lead_edge_t[-1]):
                    poly_min_value = DataSetTool.extreme_cubic_fun(*fit_par)[3]
                else:
                    # 若三次函数无极值，或者极值不再样本点内，则原始数据的极小值作为极值点
                    poly_min_value = min_value
                # 计算上升前沿10%和90%的阈值
                threshold90 = (poly_min_value - ped) * 0.9 + ped
                threshold10 = (poly_min_value - ped) * 0.1 + ped
                # 计算10%和90%处的根值，时间值
                root90 = np.roots([fit_par[0], fit_par[1], fit_par[2], fit_par[3] - threshold90])
                root10 = np.roots([fit_par[0], fit_par[1], fit_par[2], fit_par[3] - threshold10])
                # 筛选拟合三次函数与90% , 10%分界线焦点的横座标（时间座标）是否在拟合区间内
                root90 = root90[root90 < lead_edge_t[-5]]
                root90 = root90[root90 > lead_edge_t[0]]
                root10 = root10[root10 < lead_edge_t[-1]]
                root10 = root10[root10 > lead_edge_t[0]]
                # print("type root90: {}".format(type(root90[0])))
            else:
                # 直线拟合
                lead_edge_t = t[index10: index90]
                lead_edge_a = a[index10: index90]
                fit_par, residuals, rank, singular_values, rcond = np.polyfit(lead_edge_t, lead_edge_a, 1, full=True)
                poly_min_value = min_value
                threshold90 = (poly_min_value - ped) * 0.9 + ped
                threshold10 = (poly_min_value - ped) * 0.1 + ped
                root90 = np.roots([fit_par[0], fit_par[1] - threshold90])
                root10 = np.roots([fit_par[0], fit_par[1] - threshold10])
            try:
                raise_time = root90[0] - root10[0]
                # 在三次拟合中会出现复数根， 需要筛去复数根
                if isinstance(raise_time, np.complex128):
                    error_file.append(file_name)
                    raise_time = np.nan
            except IndexError:
                # 出现IndexError是因为在上面筛选根的范围过程中，
                # 有可能存在根不在指定范围内，因此root90或者root10
                # 为空list
                error_file.append(file_name)
                raise_time = np.nan
            sst = np.var(lead_edge_a) * len(lead_edge_a)
            try:
                # 存在residual为空的情况
                r2 = 1 - residuals[0] / sst
            except IndexError:
                r2 = np.nan
            # print("R2: {}".format(r2))
            if len(fit_par) == 4:
                # 通过拟合参数判断拟合的模型
                row = [file_name, self.filter1_data.iloc[i, 1], ped, *fit_par, index10 - 5, min_index + 5, raise_time, r2]
            else:
                row = [file_name, self.filter1_data.iloc[i, 1], ped, *fit_par, index10, index90, raise_time, r2]
            save_data.append(row)
            # 进程控制
            while True:
                if self.processing_flag == Processing.Go:
                    break
                if self.processing_flag == Processing.Pause:
                    time.sleep(1)
                    continue
                if self.processing_flag == Processing.Stop:
                    break
            if self.processing_flag == Processing.Stop:
                break
        # 判断拟合模型是三次还是线性，决定输出文件columns列内容
        if param["fit_model"] == RaiseTime.Cubic:
            my_data = pd.DataFrame(save_data,
                                   columns=["File", "Q", "pedestal", "a", "b", "c", "d", "lead_index1", "lead_index2",
                                            "raise_time", "r2"])
        else:
            my_data = pd.DataFrame(save_data, columns=["File", "Q", "pedestal", "a", "b", "lead_index1", "lead_index2",
                                                       "raise_time", "r2"])
        my_data.to_csv(param["save_file"], index=False)
        ######################################################
        # 保存文件信息
        ff = open(param["save_file"].replace(".csv", ".info"), "w")
        ff.write("date: " + datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]") + "\n")
        spe_index = self.listView.selectedIndexes()[0].row()
        ff.write("spe_dir: " + os.path.dirname(self.spe_files_list[spe_index]) + "\n")
        ff.write("spe_file: " + os.path.basename(self.spe_files_list[spe_index]) + "\n")
        ff.write("spe_md5: " + hashlib.md5(open(self.spe_files_list[spe_index], "rb").read()).hexdigest() + "\n")
        ff.write("filter_signal: " + self.lineEdit_5.text() + "\n")
        for key in param:
            if key != "save_file":
                ff.write(key + ": " + str(param[key]) + "\n")
            else:
                ff.write("save_dir: " + os.path.dirname(os.path.realpath(param[key])) + "\n")
                ff.write("save_file: " + os.path.basename(os.path.realpath(param[key])) + "\n")
                ff.write("save_md5: " + hashlib.md5(open(os.path.realpath(param[key]), "rb").read()).hexdigest() + "\n")
        ff.close()
        ######################################################
        self.raise_time_data = my_data
        if len(my_data) != 0:
            file_columns = pd.Series(map(os.path.basename, my_data["File"]))
            r2_columns = self.raise_time_data["r2"].reset_index(drop=True)
            new = pd.concat([file_columns, r2_columns], axis=1)
            new.columns = ["File", "r2"]
            pd_model = PandasModel(new)
            self.tableView.setModel(pd_model)
            self.switch_filter2(True, True)
            self.switch_graph_setting(True, True)
        else:
            QMessageBox.warning(self, "警告", "计算无结果", QMessageBox.Ok)

    def select_raise_time_file(self):
        raise_time_file, file_type = QFileDialog.getOpenFileName(self, "添加文件", "./",
                                                                 "csvFile (*csv)")
        if raise_time_file == "":
            QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)
        elif DataSetTool.check_file(raise_time_file):
            self.raise_time_data = pd.read_csv(raise_time_file)
            self.lineEdit_14.setText(raise_time_file)
            file_columns = pd.Series(map(os.path.basename, self.raise_time_data["File"]))
            r2_columns = self.raise_time_data["r2"].reset_index(drop=True)
            new = pd.concat([file_columns, r2_columns], axis=1)
            new.columns = ["File", "r2"]
            pd_model = PandasModel(new)
            self.tableView.setModel(pd_model)
            self.switch_filter2(True, True)
            self.switch_graph_setting(True, True)
        else:
            QMessageBox.warning(self, "警告", "载入文件无效", QMessageBox.Ok)

    def _get_filter_r2_data(self):
        if self.lineEdit_11.text() == "":
            filter_r2_data = self.raise_time_data
        elif len(self.lineEdit_11.text().split(",")) == 1:
            val = float(self.lineEdit_11.text().split()[0])
            filter_r2_data = self.raise_time_data[self.raise_time_data["r2"] > val]
        else:
            val1 = float(self.lineEdit_11.text().split(",")[0])
            val2 = float(self.lineEdit_11.text().split(",")[1])
            filter_r2_data = self.raise_time_data[self.raise_time_data["r2"] > val1]
            filter_r2_data = filter_r2_data[filter_r2_data["r2"] < val2]
        return filter_r2_data

    def filter_r2(self):
        if self.lineEdit_11.text() == "":
            QMessageBox.warning(self, "警告", "请设置筛选条件", QMessageBox.Ok)
            return None
        elif len(self.lineEdit_11.text().split(",")) == 1:
            val = float(self.lineEdit_11.text().split()[0])
            filter_r2_data = self.raise_time_data[self.raise_time_data["r2"] > val]
        else:
            val1 = float(self.lineEdit_11.text().split(",")[0])
            val2 = float(self.lineEdit_11.text().split(",")[1])
            filter_r2_data = self.raise_time_data[self.raise_time_data["r2"] > val1]
            filter_r2_data = filter_r2_data[filter_r2_data["r2"] < val2]
        if len(filter_r2_data) > 0:
            file_columns = pd.Series(map(os.path.basename, filter_r2_data["File"]))
            r2_columns = filter_r2_data["r2"].reset_index(drop=True)
            new = pd.concat([file_columns, r2_columns], axis=1)
            new.columns = ["File", "r2"]
            pd_model = PandasModel(new)
            # pd_model = PandasModel(filter_r2_data[["File", "r2"]])
            self.tableView.setModel(pd_model)
        else:
            QMessageBox.warning(self, "警告", "筛选结果为0", QMessageBox.Ok)

    def show_wave(self, qmi: QModelIndex):
        # 获取经过或者未经过R2筛选的wave数据
        filter_r2_data = self._get_filter_r2_data()
        data_row = filter_r2_data.iloc[qmi.row()]
        index1 = data_row["lead_index1"]
        index2 = data_row["lead_index2"]
        wave = WaveForm.load_from_file(data_row["File"])
        t = wave.get_time()
        a = wave.get_ampl()
        self.mpc1.ax1.cla()
        self.mpc1.ax1.grid(True)
        self.mpc1.ax2.cla()
        self.mpc1.ax2.grid(True)
        self.mpc1.ax1.plot(t, a)
        self.mpc1.ax2.plot(t[index1 - 20: index2 + 20], a[index1 - 20: index2 + 20])
        if len(data_row) == 9:
            self.mpc1.ax2.plot(t[index1 - 5: index2 + 5],
                               np.polyval([data_row["a"], data_row["b"]], t[index1 - 5: index2 + 5]))
        if len(data_row) == 11:
            self.mpc1.ax2.plot(t[index1 - 5: index2 + 5],
                               np.polyval([data_row["a"], data_row["b"], data_row["c"], data_row["d"]],
                                          t[index1 - 5: index2 + 5]))
        if self.checkBox_2.isChecked():
            check_x, x_val1, x_val2 = DataSetTool.comma2interval(self.lineEdit_12.text())
            print(x_val1, x_val2)
            if check_x:
                self.mpc1.ax1.set_xlim(x_val1, x_val2)
        if self.checkBox_3.isChecked():
            check_y, y_val1, y_val2 = DataSetTool.comma2interval(self.lineEdit_13.text())
            if check_y:
                self.mpc1.ax1.set_ylim(y_val1, y_val2)
        self.mpc1.draw()

    def show_raise_time(self, bins: np.ndarray = np.array([])):
        self.raise_time_hist.clear()
        self.mpc2.ax.cla()
        self.mpc2.ax.grid(True)
        filter_r2_data = self._get_filter_r2_data()
        raise_time = filter_r2_data["raise_time"].to_numpy()
        # 提出nan元素,  否则max和min得出的结果为nan
        raise_time = raise_time[np.logical_not(np.isnan(raise_time))]
        if len(bins) == 0:
            default_bins = np.linspace(raise_time.min(), raise_time.max(), 100)
            content, bins, _ = self.mpc2.ax.hist(raise_time, default_bins)
            self.mpc2.draw()
        else:
            custom_bins = bins
            content, bins, _ = self.mpc2.ax.hist(raise_time, custom_bins)
            self.mpc2.draw()
        self.raise_time_hist["content"] = content
        self.raise_time_hist["bins"] = bins
        self.raise_time_hist["fit"] = Fit.NoFit

    def set_bins(self):
        dialog = RaiseTimeSetBin(self)
        dialog.emit_bins.connect(self.show_raise_time)
        dialog.show()

    def append_message(self, message: str):
        print(datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")+": "+message)
        self.textBrowser.append(datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")+": "+message)

    def set_processing_flag(self, btn: QPushButton):
        if btn is self.pushButton_5:
            self.processing_flag = Processing.Go
            self.text_message.emit("开始")
        if btn is self.pushButton_6:
            self.processing_flag = Processing.Stop
            self.text_message.emit("停止")
        if btn is self.pushButton_7:
            self.processing_flag = Processing.Pause
            self.text_message.emit("暂停")

    def start_thread(self):
        self.switch_processing(True)
        self.my_thread.start()

    def work_finish(self):
        self.switch_filter2(True, True)
        self.switch_graph_setting(True, True)
        self.text_message.emit("完成")
        if len(self.raise_time_data) != 0 and DataSetTool.check_file(self.lineEdit_10.text()):
            self.lineEdit_14.setText(self.lineEdit_10.text())
            file_columns = pd.Series(map(os.path.basename, self.raise_time_data["File"]))
            r2_columns = self.raise_time_data["r2"].reset_index(drop=True)
            new = pd.concat([file_columns, r2_columns], axis=1)
            new.columns = ["File", "r2"]
            pd_model = PandasModel(new)
            self.tableView.setModel(pd_model)
            self.switch_filter2(True, True)
            self.switch_graph_setting(True, True)
        else:
            QMessageBox.warning(self, "警告", "载入文件无效", QMessageBox.Ok)

    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a0 is self.tableView:
            if a1.type() == QEvent.KeyPress:
                current_model_index = self.tableView.currentIndex()
                print("current index data: {}".format(current_model_index.data()))
                print("current index row: {}".format(current_model_index.row()))
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

    def set_fit_param(self):
        fit_dialog = FitDialog(self)
        fit_dialog.out_message.connect(self.fit_and_draw)
        fit_dialog.show()

    @staticmethod
    def gauss(x: float, scale: float = 1, mean: float = 1, sigma: float = 1) -> float:
        return scale / (np.sqrt(2 * np.pi) * sigma) * np.exp(-(x - mean) ** 2 / (2 * sigma ** 2))

    def fit_and_draw(self, initial_par):
        if len(initial_par["param"]) == 3 and len(self.raise_time_hist) != 0:
            print(initial_par)
            par = []
            bound = []
            bins = 1e9 * self.raise_time_hist["bins"]
            content = self.raise_time_hist["content"]
            half_delta_bin = (bins[1] - bins[0]) / 2
            x = bins[: -1] + half_delta_bin
            for i in initial_par["param"]:
                par.append(i[0])
                bound.append((i[1], i[2]))
            fit_par, par_cov = scipy.optimize.curve_fit(CallRaiseTime.gauss, x, content, par, bounds=list(zip(*bound)))
            print("fit param: {}".format(fit_par))
            emit_message = ""
            for i in range(len(fit_par)):
                emit_message = emit_message + "param{0}: {1: .6g}".format(i, fit_par[i]) + "\n"
            self.text_message.emit("\n" + emit_message)
            self.mpc2.ax.cla()
            self.mpc2.ax.hist(x, bins, weights=content)
            self.mpc2.ax.plot(x, CallRaiseTime.gauss(x, *fit_par))
            self.mpc2.ax.grid(True)
            self.mpc2.draw()
        else:
            QMessageBox.warning(self, "警告", "参数错误", QMessageBox.Ok)




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
    ui = CallRaiseTime()
    ui.show()
    sys.exit(app.exec_())