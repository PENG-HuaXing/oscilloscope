from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time

class Test(QWidget):
    def __init__(self):
        super(Test, self).__init__()
        layout = QVBoxLayout(self)
        self.line = QLineEdit()
        self.check = QCheckBox("Check")
        self.check.setTristate(True)
        self.push = QPushButton("Disable")
        self.push2 = QPushButton("Enable")
        self.push3 = QPushButton("Clear")
        self.push4 = QPushButton("Disable Check")
        self.push5 = QPushButton("read line Edit")
        self.push.clicked.connect(self.disable)
        self.push2.clicked.connect(self.enable)
        self.push3.clicked.connect(self.clear)
        self.push4.clicked.connect(self.disable_check)
        self.push5.clicked.connect(self.read)
        # self.check.toggled.connect(self.check_status)
        self.check.stateChanged.connect(self.check_status)
        layout.addWidget(self.line)
        layout.addWidget(self.check)
        layout.addWidget(self.push)
        layout.addWidget(self.push2)
        layout.addWidget(self.push3)
        layout.addWidget(self.push4)
        layout.addWidget(self.push5)

    def check_status(self):
        print("check status: {}".format(self.check.checkState()))
        print("is check: {}".format(self.check.isChecked()))

    def disable_check(self):
        if self.check.isEnabled():
            self.check.setEnabled(False)
        else:
            self.check.setEnabled(True)
        print(self.check.checkState())

    def disable(self):
        self.line.setEnabled(False)

    def enable(self):
        self.line.setEnabled(True)

    def clear(self):
        self.line.clear()

    def read(self):
        print("读取lineEdit内容为： {}".format(self.line.text()))
        print("check 状态: {}".format(self.check.isChecked()))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = Test()
    win.show()
    sys.exit(app.exec_())