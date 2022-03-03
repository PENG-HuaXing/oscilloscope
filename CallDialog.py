from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PmtConstant import Extremum
from PmtConstant import Fit


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
        reg = QRegExp(r"^(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)\s*,"
                      r"\s*(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)")
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
        reg = QRegExp(r"^(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)\s*,"
                      r"\s*(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)")
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


class FitDialog(QDialog):
    out_message = pyqtSignal(dict)

    def __init__(self, parent=None, model=Fit.Gauss):
        super(FitDialog, self).__init__(parent)
        self.data_dict = {"accept": False, "p0": None, "p1": None, "p2": None, "p3": None, "p4": None, "p5": None,
                          "interval": None, "model": None}
        layout = QVBoxLayout(self)
        self.model = model
        if self.model == Fit.Gauss:
            self.formula = QLabel("p1 * Gauss(x, p2, p3)")
        else:
            self.formula = QLabel("P5 * {Poisson(0, p0) * Gauss(x, p1, p2) + Poisson(1, p0) * Gauss(x, p3, p4)}")

            self.formula.setAlignment(Qt.AlignCenter)

        self.interval = QLabel("拟合区间")
        self.int_edit = QLineEdit()
        self.p0 = QLabel("参数p0: ")
        self.p1 = QLabel("参数p1: ")
        self.p2 = QLabel("参数p2: ")
        self.p3 = QLabel("参数p3: ")
        self.p4 = QLabel("参数p4: ")
        self.p5 = QLabel("参数p5: ")
        self.p0_edit = QLineEdit()
        self.p1_edit = QLineEdit()
        self.p2_edit = QLineEdit()
        self.p3_edit = QLineEdit()
        self.p4_edit = QLineEdit()
        self.p5_edit = QLineEdit()
        self.fit_button = QPushButton("拟合")
        self.cancel_button = QPushButton("取消")
        form = QFormLayout(self)
        form.addRow(self.interval, self.int_edit)
        if self.model == Fit.Gauss:
            form.addRow(self.p1, self.p1_edit)
            form.addRow(self.p2, self.p2_edit)
            form.addRow(self.p3, self.p3_edit)
        else:
            form.addRow(self.p0, self.p0_edit)
            form.addRow(self.p1, self.p1_edit)
            form.addRow(self.p2, self.p2_edit)
            form.addRow(self.p3, self.p3_edit)
            form.addRow(self.p4, self.p4_edit)
            form.addRow(self.p5, self.p5_edit)

        btn_layout = QHBoxLayout(self)
        btn_layout.addWidget(self.fit_button)
        btn_layout.addWidget(self.cancel_button)
        layout.addWidget(self.formula)
        layout.addLayout(form)
        layout.addLayout(btn_layout)
        self.fit_button.clicked.connect(self.emit_param)
        self.cancel_button.clicked.connect(self.close)
        interval_reg = QRegExpValidator(self)
        reg = QRegExp(r"^(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)\s*,"
                      r"\s*(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)")
        interval_reg.setRegExp(reg)
        sci_validator = QRegExpValidator(self)
        sci_reg = QRegExp(r"^(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)")
        sci_validator.setRegExp(sci_reg)
        self.int_edit.setValidator(interval_reg)
        self.p1_edit.setValidator(sci_validator)
        self.p2_edit.setValidator(sci_validator)
        self.p3_edit.setValidator(sci_validator)

    def emit_param(self):
        if self.model == Fit.Gauss:
            if self.p1_edit.text() == "" or self.p2_edit.text() == "" or self.p3_edit.text() == "" or \
               self.int_edit.text() == "":
                QMessageBox.warning(None, "警告", "参数未完成", QMessageBox.Ok)
            else:
                self.data_dict["accept"] = True
                self.data_dict["p1"] = self.p1_edit.text()
                self.data_dict["p2"] = self.p2_edit.text()
                self.data_dict["p3"] = self.p3_edit.text()
                self.data_dict["interval"] = self.int_edit.text()
                self.data_dict["model"] = Fit.Gauss
                self.out_message.emit(self.data_dict)
                print(self.data_dict)
                self.close()
        else:
            if self.p0_edit.text() == "" or self.p1_edit.text() == "" or self.p2_edit.text() == "" or \
               self.p3_edit.text() == "" or self.p4_edit.text() == "" or self.p5_edit.text() == "" or \
               self.int_edit.text() == "":
                QMessageBox.warning(None, "警告", "参数未完成", QMessageBox.Ok)
            else:
                self.data_dict["accept"] = True
                self.data_dict["p0"] = self.p0_edit.text()
                self.data_dict["p1"] = self.p1_edit.text()
                self.data_dict["p2"] = self.p2_edit.text()
                self.data_dict["p3"] = self.p3_edit.text()
                self.data_dict["p4"] = self.p4_edit.text()
                self.data_dict["p5"] = self.p5_edit.text()
                self.data_dict["interval"] = self.int_edit.text()
                self.data_dict["model"] = Fit.DoubleGauss
                self.out_message.emit(self.data_dict)
                print(self.data_dict)
                self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = FitDialog(model=Fit.DoubleGauss)
    ui.show()
    sys.exit(app.exec_())