import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ParaDialog(QDialog):
    para_message = pyqtSignal(list)

    def __init__(self, parent = None, model: str = "Gaus"):
        super(ParaDialog, self).__init__(parent)
        self.setWindowTitle("Parameters Setting")

        self.layout = QGridLayout(self)
        self.model = QLabel(model)
        self.p1 = QLabel("p1")
        self.p2 = QLabel("p2")
        self.p3 = QLabel("p3")
        self.p1_edit = QLineEdit()
        self.p2_edit = QLineEdit()
        self.p3_edit = QLineEdit()
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        self.accepted.connect(self.emit_para)
        buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.model, 0, 0, 1, 1)
        self.formlayout = QFormLayout()
        self.formlayout.addRow(self.p1, self.p1_edit)
        self.formlayout.addRow(self.p2, self.p2_edit)
        self.formlayout.addRow(self.p3, self.p3_edit)
        self.layout.addLayout(self.formlayout, 1, 0, 1, 1)
        self.layout.addWidget(buttons, 2, 0, 1, 1)

    def emit_para(self):
        if self.p1_edit.text() == "" or self.p2_edit.text() == "" or self.p3_edit.text() == "":
            QMessageBox.warning(self, "warning", "parameter can't empty", QMessageBox.Ok)
        else:
            p1 = float(self.p1_edit.text())
            p2 = float(self.p2_edit.text())
            p3 = float(self.p3_edit.text())
            param_list = []
            param_list.append(p1)
            param_list.append(p2)
            param_list.append(p3)
            self.para_message.emit(param_list)


if __name__ == "__main__":
    print("Hello")