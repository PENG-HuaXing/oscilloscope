import os
import sys

import pandas as pd

from AfterPlus import AfterPulse
from Date_set import DataSet
from Waveform import Waveform
from AP import Ui_Form
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from Canvas import MatPlotCanvas
from PyQt5.QtCore import pyqtSignal, QStringListModel, QModelIndex, QThread, Qt, QEvent
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QFileDialog, QAbstractItemView
from PyQt5 import QtGui
from PyQt5.QtGui import QKeyEvent

class CallAfterPulse(QWidget, Ui_Form):
    message = pyqtSignal(str)
    key_press = pyqtSignal(int)

    def __init__(self):
        super(CallAfterPulse, self).__init__()
        self.setupUi(self)
        self.message.connect(self.out_message)
        self.pushButton_9.clicked.connect(self.select_files)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listView_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listView.doubleClicked.connect(self.select_analysis_file)
        self.listView_2.clicked.connect(self.show_wave)
        self.listView_2.installEventFilter(self)
        # self.listView_2.indexesMoved.connect(self.show_wave)
        self.comboBox.addItems(["<", ">"])
        self.comboBox.setCurrentIndex(-1)
        self.comboBox.currentIndexChanged.connect(self.get_Q_trigger_flag)
        self.pushButton_4.clicked.connect(self.get_Q_trigger_value)
        self.pushButton_6.clicked.connect(self.get_AP_setting_param)
        self.pushButton.clicked.connect(self.filter_file)
        self.pushButton_7.clicked.connect(self.set_save_file)
        self.pushButton_8.clicked.connect(self.start_thread)

        # Canvas
        self.mpc1 = MatPlotCanvas(self)
        self.mpc_tb1 = NavigationToolbar(self.mpc1, self)
        self.mpc2 = MatPlotCanvas(self)
        self.mpc_tb2 = NavigationToolbar(self.mpc2, self)
        self.verticalLayout_3.addWidget(self.mpc_tb1)
        self.verticalLayout_3.addWidget(self.mpc1)
        self.verticalLayout_3.addWidget(self.mpc_tb2)
        self.verticalLayout_3.addWidget(self.mpc2)

        # Thread
        self.thread = WorkThread(self.loop)
        self.thread.finished.connect(self.show_scatter)


        # value
        self.SPE_files = []
        self.analysis_file = None
        self.Q_trigger_flag_index = None
        self.Q_trigger_value = None
        self.AP_setting_param = []
        self.class_AP = None
        self.filter_files = []
        self.save_file = ""

    def out_message(self, message: str):
        self.textEdit.append(message)

    def select_files(self):
        self.SPE_files, _ = QFileDialog.getOpenFileNames(self, "Select SPE File", "/run/media/einstein/Elements/CR160_data/", "Data File (*.csv *.root *.pickle)")
        if len(self.SPE_files) == 0:
            QMessageBox.warning(self, "warning", "No File Selected", QMessageBox.Ok)
            self.label_2.setText("File Path:")
        else:
            self.label_2.setText("File Path: " + os.path.dirname(self.SPE_files[0]))
            self.SPE_files.sort()
            slm = QStringListModel()
            base_name_file = list(map(os.path.basename, self.SPE_files))
            slm.setStringList(base_name_file)
            self.listView.setModel(slm)
        self.message.emit("set SPE_files: {}".format(self.SPE_files))
        print("set SPE_files: {}".format(self.SPE_files))

    def select_analysis_file(self, index: QModelIndex):
        self.analysis_file = self.SPE_files[index.row()]
        self.message.emit("analysis file: {}".format(self.analysis_file))
        print("analysis file: {}".format(self.analysis_file))

    def get_Q_trigger_flag(self, index: int):
        self.Q_trigger_flag_index = index

    def get_Q_trigger_value(self):
        self.Q_trigger_value = float(self.lineEdit_3.text())
        self.message.emit("Q trigger flag: {}".format(self.Q_trigger_flag_index))
        self.message.emit("Q trigger value: {}".format(self.Q_trigger_value))
        print("Q trigger flag: {}".format(self.Q_trigger_flag_index))
        print("Q trigger value: {}".format(self.Q_trigger_value))

    def filter_file(self):
        self.class_AP = AfterPulse(self.analysis_file, self.Q_trigger_value)
        if self.Q_trigger_flag_index == 0:
            self.class_AP.filter_under_Q()
        else:
            self.class_AP.filter_over_Q()
        self.filter_files = list(self.class_AP.get_filter_data()["File"])
        print(self.filter_files)
        self.filter_files.sort()
        print("sort: {}".format(self.analysis_file))
        self.message.emit("filter complete!!")
        if len(self.filter_files) == 0:
            QMessageBox.warning(self, "Filter warning", "There is no file", QMessageBox.Ok)
        else:
            print("after sort: {}".format(self.filter_files))
            slm = QStringListModel()
            slm.setStringList(list(map(os.path.basename, self.filter_files)))
            self.listView_2.setModel(slm)

    def get_AP_setting_param(self):
        self.AP_setting_param.append(float(self.lineEdit_4.text()))
        self.AP_setting_param.append(float(self.lineEdit_5.text()))
        self.AP_setting_param.append(float(self.lineEdit_6.text()))
        self.message.emit("AP trigger: {}\nAP region: {}\nAP window: {}".format(self.AP_setting_param[0],
                                                                                self.AP_setting_param[1],
                                                                                self.AP_setting_param[2]))
        print("AP trigger: {}\nAP region: {}\nAP window: {}".format(self.AP_setting_param[0],
                                                                    self.AP_setting_param[1],
                                                                    self.AP_setting_param[2]))

    def set_save_file(self):
        self.save_file, _ = QFileDialog.getSaveFileName(self, "Save File", "./save.csv")

    def loop(self):
        self.class_AP.set_after_pulse_trigger(self.AP_setting_param[0])
        self.message.emit("save file: {}".format(self.save_file))
        self.class_AP.loop_and_save(self.save_file, self.AP_setting_param[1], self.AP_setting_param[2])

    def show_wave(self, index: QModelIndex):
        print(self.listView_2.currentIndex().row())
        self.mpc1.ax.cla()
        t, a = DataSet.read_csv(self.filter_files[index.row()])
        self.mpc1.ax.plot(t, a)
        self.mpc1.draw()

    def show_scatter(self):
        try:
            open(self.save_file, "r")
            state = True
        except FileNotFoundError:
            state = False
        if state:
            data = pd.read_csv(self.save_file)
            t = data["Time"].to_numpy()
            a = data["Q"].to_numpy()
            self.mpc2.ax.cla()
            self.mpc2.ax.scatter(t, a)
            self.mpc2.draw()
        else:
            print("No File")

    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a0 == self.listView_2:
            if a1.type() == QEvent.KeyPress:
                if a1.key() == Qt.Key_Up or a1.key() == Qt.Key_Down:
                    print("Up or Down: {}".format(self.listView_2.currentIndex().row()))
                    self.mpc1.ax.cla()
                    t, a = DataSet.read_csv(self.filter_files[self.listView_2.currentIndex().row()])
                    self.mpc1.ax.plot(t, a)
                    self.mpc1.draw()

        return QWidget.eventFilter(self, a0, a1)

    def start_thread(self):
        self.thread.start()


class WorkThread(QThread):
    def __init__(self, fun, *args):
        super(WorkThread, self).__init__()
        self.fun = fun
        self.args = args

    def run(self) -> None:
        self.fun(*self.args)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = CallAfterPulse()
    ui.show()
    sys.exit(app.exec_())
