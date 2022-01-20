import sys
from SPE import Ui_Form
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import pyqtSignal


class SPE_Ui(QWidget, Ui_Form):
    def __init__(self):
        super(SPE_Ui, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = SPE_Ui()
    ui.show()
    sys.exit(app.exec_())