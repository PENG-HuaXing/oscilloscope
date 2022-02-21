from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PmtConstant import Extremum


class ExtremumDialog(QDialog):
    out_message = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(ExtremumDialog, self).__init__(parent)
        # 传递参数
        self.data = {"ext_flag": None, "interval": "0e0, 0e0"}
        # Ui初始化
        self.setWindowTitle("极值设置")
        total_layout = QVBoxLayout(self)
        self.label1 = QLabel("极值：")
        self.com = QComboBox()
        self.com.addItems(["极大值", "极小值"])
        self.label2 = QLabel("区间：")
        self.interval = QLineEdit()
        interval_reg = QRegExpValidator(self)
        reg = QRegExp(r"^([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)\s*,\s*([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)")
        interval_reg.setRegExp(reg)
        self.interval.setValidator(interval_reg)
        form_layout = QFormLayout(self)
        form_layout.addRow(self.label1, self.com)
        form_layout.addRow(self.label2, self.interval)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                                   Qt.Horizontal, self)
        buttons.accepted.connect(self.accept_param)
        buttons.rejected.connect(self.reject_param)
        total_layout.addLayout(form_layout)
        total_layout.addWidget(buttons)

    def accept_param(self):
        index = self.com.currentIndex()
        if self.interval.text() == "":
            QMessageBox.warning(self, "警告", "区间数值不正确", QMessageBox.Ok)
        elif len(self.interval.text().split(",")) != 2:
            QMessageBox.warning(self, "警告", "区间数值不正确", QMessageBox.Ok)
        else:
            if index == 0:
                self.data["ext_flag"] = Extremum.Max
            if index == 1:
                self.data["ext_flag"] = Extremum.Min
            self.data["interval"] = self.interval.text()
            self.out_message.emit(self.data)
        print(self.data)
        self.close()

    def reject_param(self):
        print(self.data)
        self.close()


class TriggerDialog(QDialog):
    out_message = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(TriggerDialog, self).__init__(parent)
        self.data = {"threshold": None, "interval": "0e0, 0e0"}
        self.setWindowTitle("触发阈值设置")
        self.layout = QVBoxLayout(self)
        self.label1 = QLabel("触发阈值(V)：")
        self.edit = QLineEdit()
        double_validator = QDoubleValidator(self)
        self.edit.setValidator(double_validator)
        self.label2 = QLabel("区间(s)：")
        self.interval = QLineEdit()
        interval_reg = QRegExpValidator(self)
        reg = QRegExp(r"^([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)\s*,\s*([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)")
        interval_reg.setRegExp(reg)
        self.interval.setValidator(interval_reg)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                                   Qt.Horizontal, self)
        buttons.accepted.connect(self.accept_param)
        buttons.rejected.connect(self.reject_param)
        form_layout = QFormLayout(self)
        form_layout.addRow(self.label1, self.edit)
        form_layout.addRow(self.label2, self.interval)
        self.layout.addLayout(form_layout)
        self.layout.addWidget(buttons)

    def accept_param(self):
        if self.edit.text() == "" or self.interval.text() == "":
            QMessageBox.warning(self, "警告", "区间数值不正确", QMessageBox.Ok)
        elif len(self.interval.text().split(",")) != 2:
            QMessageBox.warning(self, "警告", "区间数值不正确", QMessageBox.Ok)
        else:
            self.data["threshold"] = float(self.edit.text())
            self.data["interval"] = self.interval.text()
            print(self.data)
            self.out_message.emit(self.data)
        self.close()

    def reject_param(self):
        print(self.data)
        self.close()






if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = TriggerDialog()
    ui.show()
    sys.exit(app.exec_())