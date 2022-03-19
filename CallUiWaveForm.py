import time, sys, datetime, os, hashlib
from UiWaveForm import Ui_Form
from PmtDataSetTool import DataSetTool
from PmtConstant import Extremum, Processing, Active, Wave
from CallDialog import ExtremumDialog, TriggerDialog, PandasModel, TableDialog
from PmtWaveForm import WaveForm
from Canvas import MatPlotCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd


class CallUiWaveForm(Ui_Form, QWidget):
    text_message = pyqtSignal(str)

    def __init__(self):
        super(CallUiWaveForm, self).__init__()
        self.setupUi(self)
        self.text_message.connect(self.out_message)
        # 初始状态
        self.switch_integral_setting(False, False)
        self.switch_other_setting(False, False)
        self.switch_run_setting(False)
        self.switch_process(False)
        # 载入文件， 清空文件
        self.pushButton.clicked.connect(self.load_file)
        self.pushButton_2.clicked.connect(self.list_clear)
        self.comboBox.addItems(["Trapezoid", "Riemann"])
        interval_regex = QRegExpValidator(self)
        reg = QRegExp(r"^(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)\s*,"
                      r"\s*(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)")
        interval_regex.setRegExp(reg)
        self.lineEdit_6.setValidator(interval_regex)
        self.lineEdit_7.setValidator(interval_regex)
        self.lineEdit_8.setValidator(interval_regex)
        self.lineEdit_9.setValidator(interval_regex)
        self.lineEdit_11.setValidator(interval_regex)
        self.lineEdit_12.setValidator(interval_regex)
        # 计算基线checkbox
        self.checkBox.toggled.connect(self.set_ped)
        self.pushButton_3.clicked.connect(self.integral_setting_ok)
        self.pushButton_4.clicked.connect(self.reset_integral_setting)
        # 极值记录checkbox
        self.checkBox_2.toggled.connect(self.active_ext_setting)
        # 触发记录checkbox
        self.checkBox_3.toggled.connect(self.active_trigger_setting)
        # 极值参数设置
        self.pushButton_5.clicked.connect(self.set_extremum)
        # 触发参数设置
        self.pushButton_6.clicked.connect(self.set_trigger)
        # 设置保存数据文件
        self.pushButton_7.clicked.connect(self.select_save_file)
        # 开始循环
        self.pushButton_8.clicked.connect(self.start_thread)
        self.pushButton_9.clicked.connect(lambda: self.set_processing_flag(self.pushButton_9))
        self.pushButton_10.clicked.connect(lambda: self.set_processing_flag(self.pushButton_10))
        self.pushButton_11.clicked.connect(lambda: self.set_processing_flag(self.pushButton_11))
        self.listView.clicked.connect(self.draw_wave)
        self.listView.installEventFilter(self)
        self.listView.doubleClicked.connect(self.show_table_data)

        # 成员变量
        self.wave_form = None
        self.processing_flag = Processing.Go
        self.data_file_list = []

        # 线程
        self.my_thread = WorkThread(self.run)
        self.my_thread.finished.connect(self.work_finish)

        # Canvas
        self.canvas = MatPlotCanvas(self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.verticalLayout_4.addWidget(self.toolbar)
        self.verticalLayout_4.addWidget(self.canvas)
        canvas_size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas_size_policy.setHorizontalStretch(0)
        canvas_size_policy.setVerticalStretch(2)
        self.canvas.setSizePolicy(canvas_size_policy)

    def switch_integral_setting(self, group: bool, visible: bool, widget: bool = True):
        self.groupBox.setEnabled(group)
        self.comboBox.setEnabled(widget)
        self.lineEdit_6.setEnabled(widget)
        self.checkBox.setEnabled(widget)
        self.lineEdit_7.setEnabled(widget)
        self.pushButton_3.setEnabled(widget)
        self.pushButton_4.setEnabled(widget)
        self.line.setVisible(visible)
        self.label_8.setVisible(visible)
        self.lineEdit_7.setVisible(visible)

    def switch_other_setting(self, group: bool, visible: bool):
        self.groupBox_2.setEnabled(group)
        self.label_9.setVisible(visible)
        self.label_10.setVisible(visible)
        self.label_12.setVisible(visible)
        self.label_13.setVisible(visible)
        self.label_14.setVisible(visible)
        self.lineEdit_8.setVisible(visible)
        self.lineEdit_9.setVisible(visible)

    def switch_run_setting(self, enable: bool):
        self.lineEdit_10.setEnabled(enable)
        self.pushButton_7.setEnabled(enable)
        self.pushButton_8.setEnabled(enable)

    def switch_process(self, enable: bool):
        self.pushButton_9.setEnabled(enable)
        self.pushButton_10.setEnabled(enable)
        self.pushButton_11.setEnabled(enable)

    def load_file(self):
        self.data_file_list.clear()
        dir_name = QFileDialog.getExistingDirectory(self, caption="选择文件夹", directory="/mnt/windows_file/DATA")
        if dir_name == "":
            QMessageBox.warning(self, "警告", "未选择任何文件夹", QMessageBox.Ok)
        else:
            file_list = os.listdir(dir_name)
            base_name = []
            for i in file_list:
                if i.endswith(".csv") or i.endswith("trc"):
                    base_name.append(i)
            base_name.sort()
            for i in base_name:
                self.data_file_list.append(os.path.join(dir_name, i))
            slm = QStringListModel()
            slm.setStringList(base_name)
            self.listView.setModel(slm)
            self.lineEdit.setText(dir_name)
            self.lineEdit_2.setText(str(len(file_list)))
            self.wave_form = WaveForm.load_from_file(self.data_file_list[0])
            self.lineEdit_3.setText(str(format(self.wave_form.get_time_bound()[0], '.2e')))
            self.lineEdit_4.setText(str(format(self.wave_form.get_time_bound()[1], '.2e')))
            self.lineEdit_5.setText(str(format(self.wave_form.get_delta_time(), '.2e')))
            # 加载文件成功， 积分设置控件状态
            self.switch_integral_setting(True, False, True)
            self.checkBox.setChecked(False)
            # 加载文件成功， 其他设置控件状态
            self.switch_other_setting(True, False)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)

    def list_clear(self):
        self.data_file_list.clear()
        slm = QStringListModel()
        slm.setStringList([])
        self.listView.setModel(slm)
        # 清空文件后控件状态
        self.switch_integral_setting(False, False)
        self.switch_other_setting(False, False)
        self.switch_run_setting(False)
        self.switch_process(False)
        # 清空参数输入框的内容
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.lineEdit_9.clear()
        # 清空保存文件框的内容
        self.lineEdit_10.clear()
        # 清楚文件信息框的内容
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()

    def set_ped(self, status: bool):
        self.switch_integral_setting(True, status, True)
        self.lineEdit_7.clear()

    def integral_setting_ok(self):
        check_status = self.checkBox.isChecked()
        if check_status is False and self.lineEdit_6 == "":
            QMessageBox.warning(self, "警告", "区间设置未完成", QMessageBox.Ok)
        elif check_status is True and (self.lineEdit_6.text() == "" or self.lineEdit_7.text() == ""):
            QMessageBox.warning(self, "警告", "区间设置未完成", QMessageBox.Ok)
        else:
            self.switch_integral_setting(True, check_status, False)
            self.switch_run_setting(True)
            self.pushButton_4.setEnabled(True)
            self.comboBox.setEnabled(True)
            self.checkBox.setEnabled(True)
            self.switch_run_setting(True)
            self.lineEdit_10.setText("./spe.csv")

    def reset_integral_setting(self):
        check_status = self.checkBox.isChecked()
        self.switch_integral_setting(True, check_status)
        self.switch_run_setting(False)
        self.lineEdit_10.clear()

    def active_ext_setting(self, status: bool):
        self.pushButton_5.setEnabled(status)
        if status is False:
            self.label_9.setVisible(False)
            self.label_10.setVisible(False)
            self.lineEdit_8.setVisible(False)
            self.lineEdit_8.clear()

    def active_trigger_setting(self, status: bool):
        self.pushButton_6.setEnabled(status)
        if status is False:
            self.label_13.setVisible(False)
            self.label_14.setVisible(False)
            self.label_12.setVisible(False)
            self.lineEdit_9.setVisible(False)
            self.lineEdit_9.clear()

    def set_extremum(self):
        dialog = ExtremumDialog(self)
        dialog.out_message.connect(self.setting_ext)
        dialog.show()

    def set_trigger(self):
        dialog = TriggerDialog(self)
        dialog.out_message.connect(self.setting_tri)
        dialog.show()

    def setting_ext(self, data_dict: dict):
        if data_dict["ext_flag"] == Extremum.Max:
            self.label_9.setText("极大值")
        elif data_dict["ext_flag"] == Extremum.Min:
            self.label_9.setText("极小值")
        else:
            self.label_9.setText("错误")
        self.lineEdit_8.setText(data_dict["interval"])
        self.label_9.setVisible(True)
        self.label_10.setVisible(True)
        self.lineEdit_8.setVisible(True)

    def setting_tri(self, data_dict: dict):
        self.label_13.setText(str(data_dict["threshold"]))
        self.lineEdit_9.setText(data_dict["interval"])
        self.label_13.setVisible(True)
        self.label_14.setVisible(True)
        self.label_12.setVisible(True)
        self.lineEdit_9.setVisible(True)

    def select_save_file(self):
        save_file, file_type = QFileDialog.getSaveFileName(self, "保存文件", "./spe.csv", "csv文件 (*csv)")
        print("保存文件: {}".format(save_file))
        print("文件格式: {}".format(file_type))
        if DataSetTool.check_file(os.path.dirname(save_file)):
            self.lineEdit_10.setText(save_file)
        else:
            QMessageBox.warning(self, "警告", "文件夹无效", QMessageBox.Ok)

    def collect_param(self) -> dict:
        # param = {"int_flag": Wave.Trapezoid, "int_interval": None, "ped_flag": Active.NoPed, "ped_interval": None,
        #          "ext_flag": Active.NoExt, "ext_interval": None, "tri_flag": Active.NoTri, "tri_threshold": None,
        #          "tri_interval": None}
        param = dict()
        # 基线参数获取
        if self.checkBox.isChecked():
            param["ped_flag"] = Active.Ped
            # self.lineEdit_7.setEnabled(True)
            param["ped_interval"] = DataSetTool.comma2interval(self.lineEdit_7.text())
            # self.lineEdit_7.setEnabled(False)
        else:
            param["ped_flag"] = Active.NoPed
        # 积分参数获取
        if self.comboBox.currentIndex() == 1:
            param["int_flag"] = Wave.Riemann
        else:
            param["int_flag"] = Wave.Trapezoid
        # self.lineEdit_6.setEnabled(True)
        param["int_interval"] = DataSetTool.comma2interval(self.lineEdit_6.text())
        # self.lineEdit_6.setEnabled(False)
        # 获取极值参数
        if self.checkBox_2.isChecked():
            if self.label_9.text() == "极大值":
                param["ext_flag"] = Active.ExtMax
            else:
                param["ext_flag"] = Active.ExtMin
                param["ext_interval"] = DataSetTool.comma2interval(self.lineEdit_8.text())
        else:
            param["ext_flag"] = Active.NoExt
        # 获取触发参数
        if self.checkBox_3.isChecked():
            param["tri_flag"] = Active.Tri
            param["tri_threshold"] = float(self.label_13.text())
            param["tri_interval"] = DataSetTool.comma2interval(self.lineEdit_9.text())
        else:
            param["tri_flag"] = Active.NoTri
        return param

    def run(self):
        print("Enter Run")
        param = self.collect_param()
        data = []
        ped = 0
        print(param)
        for i in self.data_file_list:
            row = []
            row.append(i)
            wave = WaveForm.load_from_file(i)
            if param["ped_flag"] == Active.Ped:
                ped = wave.pedestal(param["ped_interval"][1], param["ped_interval"][2], param["int_flag"])
            int_value = wave.integrate(param["int_interval"][1], param["int_interval"][2], ped, param["int_flag"])
            row.append(int_value)
            row.append(ped)
            if param["ext_flag"] == Active.ExtMin:
                ext_value, ext_index = wave.min_ampl(param["ext_interval"][1], param["ext_interval"][2])
                row.append(ext_value)
            if param["ext_flag"] == Active.ExtMax:
                ext_value, ext_index = wave.max_ampl(param["ext_interval"][1], param["ext_interval"][2])
                row.append(ext_value)
            if param["tri_flag"] == Active.Tri:
                tri_value = wave.trigger(param["tri_threshold"], param["tri_interval"][1], param["tri_interval"][2])
                row.append(tri_value)
            data.append(row)
            self.text_message.emit(i)
            print(i)
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
        col = ["File", "Q", "Pedestal"]
        if param["ext_flag"] != Active.NoExt:
            col.append("Extremum")
        if param["tri_flag"] == Active.Tri:
            col.append("Trigger")
        save_file = self.lineEdit_10.text()
        pd_data = pd.DataFrame(data, columns=col)
        if DataSetTool.check_file(os.path.dirname(save_file)):
            pd_data.to_csv(save_file, index=False)
        #################################################
        # 保存文件信息
        ff = open(save_file.replace(".csv", ".info"), "w")
        ff.write("date: " + datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]") + "\n")
        ff.write("wave_data_dir: " + self.lineEdit.text() + "\n")
        ff.write("wave_data_num: " + self.lineEdit_2.text() + "\n")
        for i in range(3):
            tmp_file = self.data_file_list[i]
            ff.write("file{}[md5]: {}[{}]\n".format(i, tmp_file, hashlib.md5(open(tmp_file, "rb").read()).hexdigest()))
        for key in param:
            if str(key).endswith("interval"):
                ff.write(key + ": {}, {}\n".format(param[key][1], param[key][2]))
            else:
                ff.write(key + ": " + str(param[key]) + "\n")
        ff.write("spe_dir: " + os.path.dirname(os.path.realpath(save_file)) + "\n")
        ff.write("spe_file: " + os.path.basename(os.path.realpath(save_file)) + "\n")
        ff.write("spe_md5: " + hashlib.md5(open(os.path.realpath(save_file), "rb").read()).hexdigest() + "\n")
        ff.close()
        #################################################

    def draw_wave(self, index: QModelIndex):
        self.canvas.ax.cla()
        self.canvas.ax.grid(True)
        file = os.path.join(self.lineEdit.text(), index.data())
        print(file)
        self.wave_form = WaveForm.load_from_file(file)
        self.canvas.ax.plot(self.wave_form.get_time(), self.wave_form.get_ampl())
        if self.checkBox_4.isChecked():
            print("checkBox_4: {}".format(self.checkBox_4.isChecked()))
            x_check, a1, a2 = DataSetTool.comma2interval(self.lineEdit_11.text())
            print(x_check, a1, a2)
            if x_check:
                print(a1, a2)
                self.canvas.ax.set_xlim(a1, a2)
        if self.checkBox_5.isChecked():
            y_check, b1, b2 = DataSetTool.comma2interval(self.lineEdit_12.text())
            if y_check:
                self.canvas.ax.set_ylim(b1, b2)
        self.canvas.draw()

    def set_processing_flag(self, btn: QPushButton):
        if btn is self.pushButton_9:
            self.processing_flag = Processing.Go
        if btn is self.pushButton_10:
            self.processing_flag = Processing.Pause
        if btn is self.pushButton_11:
            self.processing_flag = Processing.Stop
        print(self.processing_flag)

    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a0 is self.listView:
            if a1.type() == QEvent.KeyPress:
                current_model_index = self.listView.currentIndex()
                print(current_model_index.data())
                if a1.key() == Qt.Key_Up:
                    up_model_index = current_model_index.siblingAtRow(current_model_index.row() - 1)
                    print("Up: {}".format(up_model_index.data()))
                    if up_model_index.data() is None:
                        self.draw_wave(current_model_index)
                    else:
                        self.draw_wave(up_model_index)
                if a1.key() == Qt.Key_Down:
                    down_model_index = current_model_index.siblingAtRow(current_model_index.row() + 1)
                    print("Down: {}".format(down_model_index.data()))
                    if down_model_index.data() is None:
                        self.draw_wave(current_model_index)
                    else:
                        self.draw_wave(down_model_index)
        return QWidget.eventFilter(self, a0, a1)

    def out_message(self, message: str):
        self.textBrowser.append(datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")+": "+message)

    def work_finish(self):
        self.lineEdit_10.setReadOnly(False)
        self.switch_process(False)
        self.pushButton_7.setEnabled(True)
        self.pushButton_8.setEnabled(True)
        self.text_message.emit("完成")

    def start_thread(self):
        self.switch_process(True)
        self.lineEdit_10.setReadOnly(True)
        self.pushButton_7.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        self.my_thread.start()

    def show_table_data(self, qmi: QModelIndex):
        dir = self.lineEdit.text()
        file = qmi.data()
        file = os.path.join(dir, file)
        if file.endswith(".csv") and DataSetTool.check_file(file):
            pd_data = pd.read_csv(file, header=4)
            model = PandasModel(pd_data)
            table = TableDialog(self, model)
            table.show()

        if file.endswith(".trc") and DataSetTool.check_file(file):
            wave = WaveForm.load_from_file(file)
            t = list(wave.get_time())
            a = list(wave.get_ampl())
            table = [t, a]
            table = list(map(list, zip(*table)))
            pd_data = pd.DataFrame(table, columns=["Time", "Ampl"])
            model = PandasModel(pd_data)
            table = TableDialog(self, model)
            table.show()


class WorkThread(QThread):
    def __init__(self, fun, *args):
        super(WorkThread, self).__init__()
        self.fun = fun
        self.args = args

    def run(self) -> None:
        self.fun(*self.args)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CallUiWaveForm()
    win.show()
    sys.exit(app.exec_())
