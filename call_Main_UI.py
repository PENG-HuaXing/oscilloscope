from Main_UI import Ui_MainWindow
import call_wave_UI
import call_SPE_UI
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt, QStringListModel, QModelIndex


class Welcome_UI(QMainWindow, Ui_MainWindow):
    call_window = pyqtSignal(str)
    def __init__(self):
        super(Welcome_UI, self).__init__()
        self.setupUi(self)
        self.menu_list=["Waveform Analyse", "SPE"]
        self.next = None
        self.initUI()

    def initUI(self):
        slm = QStringListModel()
        slm.setStringList(self.menu_list)
        # listview
        self.listView.setModel(slm)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listView.clicked.connect(self.get_index)
        # button
        self.pushButton.clicked.connect(self.call_win)

    def get_index(self, index: QModelIndex):
        self.next = self.menu_list[index.row()]

    def call_win(self):
        if self.next is not None:
            self.call_window.emit(self.next)
        else:
            self.call_window.emit("empty")


    def go_to(self):
        if self.next is not None:
            if self.next == "Waveform Analyse":
                return 1
            if self.next == "SPE":
                return 2
        else:
            QMessageBox.warning(None, "warning", "You didn't select any module", QMessageBox.Ok)

def jump_to(win_name:str):
    global ui_wave
    global ui_SPE
    if win_name == "Waveform Analyse":
        ui_wave.show()
    if win_name == "SPE":
        ui_SPE.show()
    if win_name == "empty":
        QMessageBox.warning(None, "warning", "You didn't select any module", QMessageBox.Ok)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_wave = call_wave_UI.wave_analysic()
    ui_SPE = call_SPE_UI.SPE_Ui()
    ui = Welcome_UI()
    ui.call_window.connect(jump_to)
    # ui.pushButton.clicked.connect(ui_SPE.show)
    ui.show()
    # ui.pushButton.connect(ui.go_to)
    sys.exit(app.exec_())

