import sys, os
from Canvas import MatPlotCanvas
from ParaDialog import ParaDialog
from AnalysisSPESpectrumData import AnalysisSPESpectrumData
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from SPE import Ui_Form
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QAbstractItemView, QVBoxLayout, QCheckBox, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal, QStringListModel, QModelIndex
import numpy as np
from scipy.optimize import curve_fit


class SPE_Ui(QWidget, Ui_Form):
    message = pyqtSignal(str)

    def __init__(self):
        super(SPE_Ui, self).__init__()
        self.setupUi(self)
        self.radioButton_2.setChecked(True)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.pushButton.clicked.connect(self.add_SPE_file)
        self.pushButton_2.clicked.connect(self.clear_file_list)
        self.pushButton_3.clicked.connect(self.remove_file_from_list)
        self.pushButton_4.clicked.connect(self.select_files)
        self.listView.doubleClicked.connect(self.select_single_file)
        self.radioButton_3.setChecked(True)
        self.radioButton_4.setText("Custom")
        self._widget_switch(False)
        self.pushButton_13.setEnabled(True)
        self.radioButton_4.toggled.connect(self.costum_setting)
        self.pushButton_6.clicked.connect(self.get_histo_setting)
        self.pushButton_7.clicked.connect(self.reset_setting)
        self.widget.setHidden(True)
        self.pushButton_13.clicked.connect(self.graph_SPE)
        self.pushButton_12.clicked.connect(self.get_info)
        self.comboBox.currentIndexChanged.connect(self.set_fitting_model)
        self.radioButton_5.setChecked(True)
        self.radioButton_5.toggled.connect(self.switch_fit)
        self.pushButton_10.setText("Parameter Setting")
        self.comboBox.addItems(["Gaus", "Exp"])
        self.comboBox.setCurrentIndex(-1)
        self.lineEdit_5.setEnabled(True)
        self.pushButton_10.setText("Parameter Setting")
        self.pushButton_10.clicked.connect(self.call_fitting_dialog)

        # Canvas
        self.mpc = MatPlotCanvas(self)
        self.mpc.ax.grid(True)
        self.mpc_tb = NavigationToolbar(self.mpc, self)
        self.gridLayout_7.addWidget(self.mpc, 2, 0, 1, 1)
        self.gridLayout_7.addWidget(self.mpc_tb, 3, 0, 1, 1)

        self.histogram_check_box = QCheckBox("Histogram")
        self.histogram_check_box.setChecked(True)
        self.scatter_cehck_box = QCheckBox("Scatter")
        self.fitting_check_box = QCheckBox("Fitting")
        self.button1 = QPushButton("backup")
        self.button2 = QPushButton("backup")

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.histogram_check_box)
        h_layout.addWidget(self.scatter_cehck_box)
        h_layout.addWidget(self.fitting_check_box)
        h_layout.addWidget(self.button1)
        h_layout.addWidget(self.button2)
        self.gridLayout_7.addLayout(h_layout, 1, 0, 1, 1)

        self.scatter_cehck_box.stateChanged.connect(self.switch_scatter)
        # var
        self.file_list = []
        self.selected_files = []
        self.bin_interval = []
        self.bin_num = None
        self.scale = None
        self.fitting_model = None
        self.gaus_para = []
        self.fit_interval = []
        self.hist_data = []
        self.hist_object = []
        self.scatter_data = []
        self.scatter_object = []

    def switch_fit(self):
        if self.radioButton_5.isChecked():
            self.comboBox.clear()
            self.comboBox.addItems(["Gaus", "Exp"])
            self.comboBox.setCurrentIndex(-1)
            self.lineEdit_5.setEnabled(True)
            self.pushButton_10.clicked.disconnect(self.global_fitting)
            self.pushButton_10.clicked.connect(self.call_fitting_dialog)
        else:
            print("switch")
            self.comboBox.clear()
            self.comboBox.addItems(["Global Fitting"])
            self.lineEdit_5.setEnabled(False)
            print("change buttons text")
            self.pushButton_10.clicked.disconnect(self.call_fitting_dialog)
            self.pushButton_10.clicked.connect(self.global_fitting)

    def _widget_switch(self, switch: bool = True):
        self.lineEdit.setEnabled(switch)
        self.lineEdit_3.setEnabled(switch)
        self.lineEdit_4.setEnabled(switch)
        self.pushButton_6.setEnabled(switch)
        self.pushButton_7.setEnabled(switch)
        self.pushButton_13.setEnabled(switch)

    def add_SPE_file(self):
        files, filetype = QFileDialog.getOpenFileNames(self, "Select Files", os.getcwd(), "csv File (*csv *root)")
        self.file_list = self.file_list + files
        slm = QStringListModel()
        if self.radioButton.isChecked():
            slm.setStringList(self.file_list)
        if self.radioButton_2.isChecked():
            slm.setStringList(list(map(os.path.basename, self.file_list)))
        self.listView.setModel(slm)

    def clear_file_list(self):
        self.file_list.clear()
        slm = QStringListModel()
        slm.setStringList([])
        self.listView.setModel(slm)

    def remove_file_from_list(self):
        for i in self.listView.selectedIndexes():
            for j in self.file_list:
                if j.endswith(i.data()):
                    self.file_list.remove(j)
        slm = QStringListModel()
        if self.radioButton.isChecked():
            slm.setStringList(self.file_list)
        if self.radioButton_2.isChecked():
            slm.setStringList(list(map(os.path.basename, self.file_list)))
        self.listView.setModel(slm)

    def select_files(self):
        self.selected_files.clear()
        for i in self.listView.selectedIndexes():
            for j in self.file_list:
                if j.endswith(i.data()):
                    self.selected_files.append(j)
        for k in self.selected_files:
            print("selected file: {}".format(k))

    def select_single_file(self, model_index: QModelIndex):
        self.selected_files.clear()
        self.selected_files.append(self.file_list[model_index.row()])
        for k in self.selected_files:
            print("selected file: {}".format(k))

    def costum_setting(self):
        if self.radioButton_4.isChecked():
            self._widget_switch(True)
        else:
            self.bin_interval.clear()
            self.bin_num = None
            self.scale = None
            self._widget_switch(False)
            self.pushButton_13.setEnabled(True)

    def get_histo_setting(self):
        interval = self.lineEdit.text()
        self.bin_interval.clear()
        self.bin_interval.append(float(interval.split(",")[0]))
        self.bin_interval.append(float(interval.split(",")[1]))
        self.bin_num = int(self.lineEdit_3.text())
        if self.lineEdit_4.text() == "":
            pass
        else:
            self.scale = float(self.lineEdit_4.text())
        self._widget_switch(False)
        self.pushButton_7.setEnabled(True)
        self.pushButton_13.setEnabled(True)

    def reset_setting(self):
        self._widget_switch(True)

    def graph_SPE(self):
        self.hist_data.clear()
        self.scatter_data.clear()
        self.hist_object.clear()
        self.scatter_object.clear()
        bounder = []
        self.mpc.ax.cla()
        if self.radioButton_4.isChecked():
            print("interval: {}".format(self.bin_interval))
            print("num: {}".format(self.bin_num))
            bins = np.linspace(self.bin_interval[0], self.bin_interval[1], self.bin_num)
            print("bins: {}".format(bins))
            print("select_file: {}".format(self.selected_files))
            for i in self.selected_files:
                print("iter: {}".format(i))
                analysis = AnalysisSPESpectrumData.load_from_file(i)
                if self.scale is None:
                    hist_object = self.mpc.ax.hist(analysis.get_column("Q").to_numpy(), bins, histtype="step")
                    scatter_x = hist_object[1][1:]-(hist_object[1][1]-hist_object[1][0]) / 2
                    scatter_y = hist_object[0]
                    scatter_object = self.mpc.ax.scatter(scatter_x, scatter_y)
                else:
                    print("scale: {}".format(self.scale))
                    hist_object = self.mpc.ax.hist(self.scale * analysis.get_column("Q").to_numpy(), bins, histtype="step")
                    scatter_x = hist_object[1][1:] - (hist_object[1][1] - hist_object[1][0]) / 2
                    scatter_y = hist_object[0]
                    scatter_object = self.mpc.ax.scatter(scatter_x, scatter_y)
                self.hist_object.append(hist_object)
                self.scatter_data.append((scatter_x, scatter_y))
                self.scatter_object.append(scatter_object)
            if self.scatter_cehck_box.isChecked():
                for i in self.scatter_object:
                    i.set_visible(True)
            else:
                for i in self.scatter_object:
                    i.set_visible(False)
            self.mpc.draw()
        else:
            for i in self.selected_files:
                analysis = AnalysisSPESpectrumData.load_from_file(i)
                bounder.append(analysis.get_column("Q").max())
                bounder.append(analysis.get_column("Q").min())
            bins = np.linspace(np.array(bounder).min(), np.array(bounder).max(), 300)
            print("bounder: {}".format(bounder))
            print("bins: {}".format(bins))
            for i in self.selected_files:
                analysis = AnalysisSPESpectrumData.load_from_file(i)
                print("Q columns: {}".format(analysis.get_column("Q").to_numpy()))
                hist_object = self.mpc.ax.hist(analysis.get_column("Q").to_numpy(), bins, histtype="step")
                scatter_x = hist_object[1][1:] - (hist_object[1][1] - hist_object[1][0]) / 2
                scatter_y = hist_object[0]
                scatter_object = self.mpc.ax.scatter(scatter_x, scatter_y)
                self.hist_object.append(hist_object)
                self.scatter_object.append(scatter_object)
                self.scatter_data.append((scatter_x, scatter_y))
            if self.scatter_cehck_box.isChecked():
                for i in self.scatter_object:
                    i.set_visible(True)
            else:
                for i in self.scatter_object:
                    i.set_visible(False)
            self.mpc.draw()

    def get_info(self):
        print(len(self.selected_files))
        if len(self.selected_files) == 0:
            QMessageBox.warning(self, "warning", "No file was selected", QMessageBox.Ok)
        else:
            anaSPE = AnalysisSPESpectrumData.load_from_file(self.selected_files[0])
            info = anaSPE.get_info()
            print(info)
            print(self.selected_files)
            self.label_12.setText(self.selected_files[0].split(".")[1])
            self.label_13.setText(str(info["columns_index"]))
            self.label_14.setText(str(info["shape"]))

    def set_fitting_model(self):
        self.fitting_model = self.comboBox.currentText()

    def call_fitting_dialog(self):
        self.fit_interval.clear()
        if self.lineEdit_5.text != "":
            interval = self.lineEdit_5.text()
            self.fit_interval.append(float(interval.split(",")[0]))
            self.fit_interval.append(float(interval.split(",")[1]))
        else:
            QMessageBox.warning(self, "warning", "No fit interval was set!!", QMessageBox.Ok)
        dialog = ParaDialog(self, self.fitting_model)
        dialog.para_message.connect(self.get_parameters)
        dialog.para_message.connect(self.fit_gaus)
        dialog.show()

    def get_parameters(self, para: list):
        self.gaus_para = para

    def _model_gaus(self, x: float, p_scale: float=1, p_mean: float=1, p_sigma: float=1) -> float:
        return p_scale / (np.sqrt(2 * np.pi) * p_sigma) * np.exp(-(x - p_mean)**2 / (2 * p_sigma**2))

    def fit_gaus(self):
        x_data = self.scatter_data[0][0]
        y_data = self.scatter_data[0][1]
        delta_data = x_data[1]-x_data[0]
        start_index = int((self.fit_interval[0]-x_data[0])/delta_data)
        end_index = int((self.fit_interval[1]-x_data[0])/delta_data) + 1
        x_data_in_interval = x_data[start_index: end_index]
        y_data_in_interval = y_data[start_index: end_index]
        popt, pcov = curve_fit(self._model_gaus, x_data_in_interval, y_data_in_interval, self.gaus_para)
        self.mpc.ax.cla()
        self.mpc.ax.scatter(x_data, y_data)
        fit_x = np.linspace(self.fit_interval[0], self.fit_interval[1], 100)
        self.mpc.ax.plot(fit_x, self._model_gaus(fit_x, *popt), color='red')
        self.mpc.draw()
        print("fit gaus")


    def global_fitting(self):
        print("Global Fitting")

    def switch_scatter(self):
        print("Get into")















if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = SPE_Ui()
    ui.show()
    sys.exit(app.exec_())