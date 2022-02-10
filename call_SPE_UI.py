import sys, os
from SPE import Ui_Form
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QAbstractItemView
from PyQt5.QtCore import pyqtSignal, QStringListModel, QModelIndex


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
        self.radioButton_4.toggled.connect(self.costum_setting)

        # var
        self.file_list = []
        self.selected_files = []
        self.bin_interval = []
        self.bin_num = None
        self.scale = None

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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = SPE_Ui()
    ui.show()
    sys.exit(app.exec_())