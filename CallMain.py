import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from UiMain import Ui_MainWindow
import CallUiWaveForm as UiW
import CallUiSPE as UiSPE
import CallUiAfertPulse as UiAP
import CallUiQDC as UiQDC
import CallUiRaiseTime as UiRT


class CallUiMain(QMainWindow, Ui_MainWindow):
    call_window = pyqtSignal(int)

    def __init__(self):
        super(CallUiMain, self).__init__()
        self.setupUi(self)
        self.menu_list = ["波形分析模块", "单光电子谱分析模块", "后脉冲分析模块", "QDC分析模块", "上升时间分析模块"]
        slm = QStringListModel()
        slm.setStringList(self.menu_list)
        self.listView.setModel(slm)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listView.clicked.connect(self.get_index)
        self.pushButton.clicked.connect(self.call_win)

        # var
        self.next = -1

    def get_index(self, index: QModelIndex):
        self.next = index.row()

    def call_win(self):
        self.call_window.emit(self.next)


def jump_to(win_index: int):
    global wave_form_ui
    global SPE_ui
    global after_pulse_ui
    global qdc_ui
    global raise_time_ui
    if win_index == 0:
        wave_form_ui.show()
    if win_index == 1:
        SPE_ui.show()
    if win_index == 2:
        after_pulse_ui.show()
    if win_index == 3:
        qdc_ui.show()
    if win_index == 4:
        raise_time_ui.show()
    if win_index == -1:
        QMessageBox.warning(None, "warning", "You didn't select any module", QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_ui = CallUiMain()
    wave_form_ui = UiW.CallUiWaveForm()
    SPE_ui = UiSPE.CallUiSPE()
    after_pulse_ui = UiAP.CallUiAfterPulse()
    qdc_ui = UiQDC.CallUiQDC()
    raise_time_ui = UiRT.CallUiRaiseTime()
    main_ui.call_window.connect(jump_to)
    main_ui.show()
    sys.exit(app.exec_())

