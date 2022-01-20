from wave import Ui_Form
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtCore import pyqtSignal, Qt


class wave_analysic(QWidget, Ui_Form):
    def __init__(self):
        super(wave_analysic, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = wave_analysic()
    ui.show()
    sys.exit(app.exec_())
