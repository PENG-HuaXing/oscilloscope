from UiWaveForm import Ui_Form
from PmtDataSetTool import DataSetTool
from PmtConstant import Extremum, Processing
from CallDialog import ExtremumDialog, TriggerDialog
from PmtWaveForm import WaveForm
from Canvas import MatPlotCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, datetime, os


class CallUiWaveForm(Ui_Form, QWidget):
    text_message = pyqtSignal(str)

    def __init__(self):
        super(CallUiWaveForm, self).__init__()
        self.setupUi(self)
        self.switch_integral_setting(False, False)
        self.switch_other_setting(False, False)
        self.pushButton.clicked.connect(self.load_file)
        self.pushButton_2.clicked.connect(self.list_clear)
        self.comboBox.addItems(["Trapezoid", "Riemann"])
        interval_regex = QRegExpValidator(self)
        reg = QRegExp(r"^([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)\s*,\s*([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)")
        interval_regex.setRegExp(reg)
        self.lineEdit_6.setValidator(interval_regex)
        self.lineEdit_7.setValidator(interval_regex)
        self.lineEdit_8.setValidator(interval_regex)
        self.lineEdit_9.setValidator(interval_regex)
        self.lineEdit_11.setValidator(interval_regex)
        self.lineEdit_12.setValidator(interval_regex)
        self.checkBox.toggled.connect(self.set_ped)
        self.pushButton_3.clicked.connect(self.integral_setting_ok)
        self.pushButton_4.clicked.connect(self.reset_integral_setting)
        self.checkBox_2.toggled.connect(self.active_ext_setting)
        self.checkBox_3.toggled.connect(self.active_trigger_setting)
        self.pushButton_5.clicked.connect(self.set_extremum)
        self.pushButton_6.clicked.connect(self.set_trigger)
        self.pushButton_7.clicked.connect(self.select_save_file)
        self.pushButton_8.clicked.connect(self.run)
        self.pushButton_9.clicked.connect(lambda: self.set_processing_flag(self.pushButton_9))
        self.pushButton_10.clicked.connect(lambda: self.set_processing_flag(self.pushButton_10))
        self.pushButton_11.clicked.connect(lambda: self.set_processing_flag(self.pushButton_11))
        self.listView.clicked.connect(self.draw_wave)
        self.listView.installEventFilter(self)
        self.pushButton_12.setVisible(False)
        self.pushButton_13.setVisible(False)

        # 成员函数
        self.wave_form = None
        self.processing_flag = Processing.Go

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
        self.pushButton_9.setEnabled(enable)
        self.pushButton_10.setEnabled(enable)
        self.pushButton_11.setEnabled(enable)

    def load_file(self):
        dir_name = QFileDialog.getExistingDirectory(self, caption="选择文件夹", directory="/mnt/windows_file/DATA")
        if dir_name == "":
            QMessageBox.warning(self, "警告", "未选择任何文件夹", QMessageBox.Ok)
        else:
            file_list = os.listdir(dir_name)
            base_name = []
            for i in file_list:
                if i.endswith(".csv"):
                    base_name.append(i)
            slm = QStringListModel()
            base_name.sort()
            slm.setStringList(base_name)
            self.listView.setModel(slm)
            self.lineEdit.setText(dir_name)
            self.lineEdit_2.setText(str(len(file_list)))
            self.wave_form = WaveForm.load_from_csv(os.path.join(dir_name, base_name[0]))
            self.lineEdit_3.setText(str(format(self.wave_form.get_time_bound()[0], '.2e')))
            self.lineEdit_4.setText(str(format(self.wave_form.get_time_bound()[1], '.2e')))
            self.lineEdit_5.setText(str(format(self.wave_form.get_delta_time(), '.2e')))
            self.switch_integral_setting(True, False, True)
            self.switch_other_setting(True, False)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)

    def list_clear(self):
        slm = QStringListModel()
        slm.setStringList([])
        self.listView.setModel(slm)
        self.switch_integral_setting(False, False)
        self.switch_other_setting(False, False)
        self.switch_run_setting(False)
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.lineEdit_9.clear()
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

    def reset_integral_setting(self):
        check_status = self.checkBox.isChecked()
        self.switch_integral_setting(True, check_status)

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
            self.label_13.setText("0")

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

    def run(self):
        pass

    def draw_wave(self, index: QModelIndex):
        self.canvas.ax.cla()
        self.canvas.ax.grid(True)
        file = os.path.join(self.lineEdit.text(), index.data())
        print(file)
        self.wave_form = WaveForm.load_from_csv(file)
        self.canvas.ax.plot(self.wave_form.get_time(), self.wave_form.get_ampl())
        if self.checkBox_4.isChecked():
            print("checkBox_4: {}".format(self.checkBox_4.isChecked()))
            x_check, a1, a2 = DataSetTool.comma2interval(self.lineEdit_11.text())
            print(x_check, a1, a2)
            if x_check:
                print(a1,a2)
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













if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CallUiWaveForm()
    win.show()
    sys.exit(app.exec_())