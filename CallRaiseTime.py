from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from UiRaiseTime import Ui_Form
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from Canvas import MatPlotCanvas
from DoubleCanvas import MatPlotDoubleCanvas
import time, os, datetime
import pandas as pd
import numpy as np


class CallRaiseTime(QWidget, Ui_Form):
    text_message = pyqtSignal(str)

    def __init__(self):
        super(CallRaiseTime, self).__init__()
        self.setupUi(self)
        # 控件初始化
        self.switch_filter1(False, True)
        self.switch_file_message(False, True)
        self.switch_raise_time_setting(False, True, False)
        self.switch_save_and_loop(False)
        self.switch_filter2(False, True)
        self.switch_processing(False)
        self.switch_graph_setting(False, True)
        

        # canvas
        # self.mpc1 = MatPlotCanvas(self)
        # self.mpc2 = MatPlotDoubleCanvas(self)
        # self.ntb1 = NavigationToolbar(self.mpc1, self)
        # self.ntb2 = NavigationToolbar(self.mpc2, self)
        # self.gridLayout_5.addWidget(self.ntb1, 2, 0, 1, 1)
        # self.gridLayout_5.addWidget(self.mpc1, 3, 0, 1, 1)
        # self.gridLayout_5.addWidget(self.ntb2, 4, 0, 1, 1)
        # self.gridLayout_5.addWidget(self.mpc2, 5, 0, 1, 1)

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
        self.lineEdit_3.setEnable(widget)
        self.lineEdit_4.setEnable(widget)
        self.lineEdit_6.setEnable(widget)
        self.lineEdit_7.setEnable(widget)

    def switch_raise_time_setting(self, widget: bool, clear: bool = False, visible: bool = False):
        if clear is True:
            self.lineEdit_8.clear()
            self.lineEdit_9.clear()
        if visible is False:
            self.checkBox.setChecked(False)
            self.radioButton_3.setVisible(False)
            self.radioButton_4.setVisible(False)
            self.label_10.setVisible(False)
            self.lineEdit_9.setVisible(False)
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
        self.pushButton_15.setEnable(widget)
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
        self.checkBox_2.setEnabled(widget)
        self.checkBox_3.setEnabled(widget)
        self.lineEdit_12.setEnabled(widget)
        self.lineEdit_13.setEnabled(widget)
        if clear is True:
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.lineEdit_12.clear()
            self.lineEdit_13.clear()





if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = CallRaiseTime()
    ui.show()
    sys.exit(app.exec_())
        