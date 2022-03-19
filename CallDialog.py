import pandas as pd
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PmtConstant import Extremum, Fit
import numpy as np
from PmtDataSetTool import DataSetTool


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
        self.data = {"threshold": None, "interval": "0, 0"}
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
        self.data_dict = dict()
        self.data_dict["model"] = Fit.NoFit
        self.data_dict["param"] = []
        self.data_dict["interval"] = ""
        layout = QVBoxLayout(self)
        self.model = model
        if self.model == Fit.Gauss:
            self.formula = QLabel("amp * Gauss(x, q0, sigma0)")
        elif self.model == Fit.Global:
            self.formula = QLabel("amp * {Poisson(0, mu) * Gauss(x, q0, sigma0) + Poisson(1, mu) * Gauss(x, q0 + q1, "
                                  "sigma1)}")
        elif self.model == Fit.GlobalNoise:
            self.formula = QLabel("公式较为复杂，暂时不给予展示")
        else:
            self.formula = QLabel("拟合模型类型错误，清检查代码")
        self.formula.setAlignment(Qt.AlignCenter)

        self.interval = QLabel("拟合区间")
        self.int_edit = QLineEdit()
        self.amp = QLabel("参数amp: ")
        self.w = QLabel("参数w: ")
        self.alpha = QLabel("参数alpha: ")
        self.mu = QLabel("参数mu: ")
        self.q0 = QLabel("参数q0: ")
        self.sigma0 = QLabel("参数sigma0: ")
        self.q1 = QLabel("参数q1: ")
        self.sigma1 = QLabel("参数sigma1: ")
        self.amp_edit = QLineEdit()
        self.w_edit = QLineEdit()
        self.alpha_edit = QLineEdit()
        self.mu_edit = QLineEdit()
        self.q0_edit = QLineEdit()
        self.sigma0_edit = QLineEdit()
        self.q1_edit = QLineEdit()
        self.sigma1_edit = QLineEdit()
        self.fit_button = QPushButton("拟合")
        self.cancel_button = QPushButton("取消")
        form = QFormLayout(self)
        form.addRow(self.interval, self.int_edit)
        form.addRow(self.amp, self.amp_edit)
        form.addRow(self.w, self.w_edit)
        form.addRow(self.alpha, self.alpha_edit)
        form.addRow(self.mu, self.mu_edit)
        form.addRow(self.q0, self.q0_edit)
        form.addRow(self.sigma0, self.sigma0_edit)
        form.addRow(self.q1, self.q1_edit)
        form.addRow(self.sigma1, self.sigma1_edit)

        btn_layout = QHBoxLayout(self)
        btn_layout.addWidget(self.fit_button)
        btn_layout.addWidget(self.cancel_button)
        layout.addWidget(self.formula)
        layout.addLayout(form)
        layout.addLayout(btn_layout)
        # 按键绑定信号发射
        self.fit_button.clicked.connect(self.emit_param)
        self.cancel_button.clicked.connect(self.close)
        # 对输入框设置正则表达筛选器
        interval_reg = QRegExpValidator(self)
        reg = QRegExp(r"^(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)\s*,"
                      r"\s*(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)")
        interval_reg.setRegExp(reg)
        fit_param_validator = QRegExpValidator(self)
        fit_param_reg = QRegExp(r"^(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)\s*,"
                                r"\s*(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)\s*,"
                                r"\s*(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)")
        fit_param_validator.setRegExp(fit_param_reg)
        self.int_edit.setValidator(interval_reg)
        self.amp_edit.setValidator(fit_param_validator)
        self.w_edit.setValidator(fit_param_validator)
        self.alpha_edit.setValidator(fit_param_validator)
        self.mu_edit.setValidator(fit_param_validator)
        self.q0_edit.setValidator(fit_param_validator)
        self.sigma0_edit.setValidator(fit_param_validator)
        self.q1_edit.setValidator(fit_param_validator)
        self.sigma1_edit.setValidator(fit_param_validator)
        # 对不同模型隐藏不同参数
        self.interval.setVisible(False)
        self.int_edit.setVisible(False)
        if self.model == Fit.Global or self.model == Fit.Gauss:
            self.w.setVisible(False)
            self.w_edit.setVisible(False)
            self.alpha.setVisible(False)
            self.alpha_edit.setVisible(False)
            if self.model == Fit.Gauss:
                self.interval.setVisible(True)
                self.int_edit.setVisible(True)
                self.mu.setVisible(False)
                self.mu_edit.setVisible(False)
                self.q1.setVisible(False)
                self.q1_edit.setVisible(False)
                self.sigma1.setVisible(False)
                self.sigma1_edit.setVisible(False)

    def append_param(self, param: list, param_text: str):
        tmp_param = param_text.split(",")
        if len(tmp_param) == 1:
            param.append([float(param_text), -np.inf, np.inf])
        elif len(tmp_param) == 3:
            param.append([float(tmp_param[0]), float(tmp_param[1]), float(tmp_param[2])])
        else:
            QMessageBox.warning(None, "警告", "参数错误", QMessageBox.Ok)

    def emit_param(self):
        self.data_dict["param"].clear()
        if self.model == Fit.Gauss:
            # 拟合模型为高斯函数时
            if self.amp_edit.text() == "" or self.q0_edit.text() == "" or self.sigma0_edit.text() == "" or \
               self.int_edit.text() == 0 or len(self.int_edit.text().split(",")) != 2:
                # 判断参数的输入是否有误
                QMessageBox.warning(None, "警告", "参数未完成", QMessageBox.Ok)
            else:
                # 将lineEdit内的字符转化为[par, bounds1, bounds2]的list形式，并且append到字典
                # data_dict["param"]的list中，形成二维list
                self.data_dict["model"] = Fit.Gauss
                self.data_dict["interval"] = self.int_edit.text()
                self.append_param(self.data_dict["param"], self.amp_edit.text())
                self.append_param(self.data_dict["param"], self.q0_edit.text())
                self.append_param(self.data_dict["param"], self.sigma0_edit.text())
                if len(self.data_dict["param"]) == 3:
                    self.out_message.emit(self.data_dict)
                    print(self.data_dict)
                    self.close()
                else:
                    print("参数错误")
        if self.model == Fit.Global:
            if self.amp_edit.text() == "" or self.mu_edit.text() == "" or self.q0_edit.text() == "" or \
               self.sigma0_edit.text() == "" or self.q1_edit.text() == "" or self.sigma1_edit.text() == "":
                QMessageBox.warning(None, "警告", "参数未完成", QMessageBox.Ok)
            else:
                self.data_dict["model"] = Fit.Global
                self.append_param(self.data_dict["param"], self.amp_edit.text())
                self.append_param(self.data_dict["param"], self.mu_edit.text())
                self.append_param(self.data_dict["param"], self.q0_edit.text())
                self.append_param(self.data_dict["param"], self.sigma0_edit.text())
                self.append_param(self.data_dict["param"], self.q1_edit.text())
                self.append_param(self.data_dict["param"], self.sigma1_edit.text())
                if len(self.data_dict["param"]) == 6:
                    self.out_message.emit(self.data_dict)
                    print(self.data_dict)
                    self.close()
                else:
                    print("参数错误")
        if self.model == Fit.GlobalNoise:
            if self.amp_edit.text() == "" or self.w_edit.text() == "" or self.alpha_edit.text() == "" or \
               self.mu_edit.text() == "" or self.q0_edit.text() == "" or self.sigma0_edit.text() == "" or \
               self.q1_edit.text() == "" or self.sigma1_edit.text() == "":
                QMessageBox.warning(None, "警告", "参数未完成", QMessageBox.Ok)
            else:
                self.data_dict["model"] = Fit.GlobalNoise
                self.append_param(self.data_dict["param"], self.amp_edit.text())
                self.append_param(self.data_dict["param"], self.w_edit.text())
                self.append_param(self.data_dict["param"], self.alpha_edit.text())
                self.append_param(self.data_dict["param"], self.mu_edit.text())
                self.append_param(self.data_dict["param"], self.q0_edit.text())
                self.append_param(self.data_dict["param"], self.sigma0_edit.text())
                self.append_param(self.data_dict["param"], self.q1_edit.text())
                self.append_param(self.data_dict["param"], self.sigma1_edit.text())
                if len(self.data_dict["param"]) == 8:
                    self.out_message.emit(self.data_dict)
                    print(self.data_dict)
                    self.close()
                else:
                    print("参数错误")


class AfterPulseDialog(QDialog):
    def __init__(self, parent=None):
        super(AfterPulseDialog, self).__init__(parent)
        # Dialog初始化
        self.layout = QVBoxLayout(self)
        self.form = QFormLayout()
        self.push0 = QPushButton("选择后脉冲文件")
        self.push0.clicked.connect(self.select_ap_file)
        self.line0 = QLineEdit()
        self.line0.setReadOnly(True)
        self.label1 = QLabel("信号文件数量:")
        int_validator = QIntValidator(self)
        self.line1 = QLineEdit()
        self.line1.setValidator(int_validator)
        self.label2 = QLabel("后脉冲阈值：")
        sci_double_validator = QRegExpValidator(self)
        reg = QRegExp(r"^(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)")
        sci_double_validator.setRegExp(reg)
        self.line2 = QLineEdit()
        self.line2.setValidator(sci_double_validator)
        self.label3 = QLabel("脉冲率")
        self.line3 = QLineEdit()
        self.line3.setReadOnly(True)
        self.form.addRow(self.push0, self.line0)
        self.form.addRow(self.label1, self.line1)
        self.form.addRow(self.label2, self.line2)
        self.form.addRow(self.label3, self.line3)
        self.push_layout = QHBoxLayout()
        self.push1 = QPushButton("计算")
        self.push2 = QPushButton("关闭")
        self.push_layout.addWidget(self.push1)
        self.push_layout.addWidget(self.push2)
        self.layout.addLayout(self.form)
        self.layout.addLayout(self.push_layout)

        self.push1.clicked.connect(self.calculate_apr)
        self.push2.clicked.connect(self.close)

    def select_ap_file(self):
        file, filetype = QFileDialog.getOpenFileName(parent=self, caption="后脉冲文件",
                                                      directory="/mnt/windows_file/DATA/", filter="csvFile (*csv)")
        if file == "":
            QMessageBox.warning(self, "警告", "未选择任何文件", QMessageBox.Ok)
        else:
            self.line0.setText(file)

    def calculate_apr(self):
        try:
            file_num = int(self.line1.text())
            threshold = float(self.line2.text())
            pd_data = pd.read_csv(self.line0.text())
            print(file_num, threshold)
            print(pd_data)
            filter_data = pd_data[pd_data["Q"] < threshold]
            ap_file_no_duplicate = []
            for i in filter_data["File"]:
                if i in ap_file_no_duplicate:
                    pass
                else:
                    ap_file_no_duplicate.append(i)
            self.line3.setText(format(len(ap_file_no_duplicate) / file_num, ".4f"))
        except:
            QMessageBox.warning(self, "警告", "数值设置错误", QMessageBox.Ok)


class RaiseTimeSetBin(QDialog):
    emit_bins = pyqtSignal(np.ndarray)

    def __init__(self, parent=None):
        super(RaiseTimeSetBin, self).__init__(parent)
        layout = QVBoxLayout(self)
        label1 = QLabel("bin区间")
        self.edit1 = QLineEdit()
        label2 = QLabel("bin数量")
        # 设置正则表达筛选器
        interval_validator = QRegExpValidator(self)
        reg = QRegExp(r"^(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)\s*,"
                      r"\s*(([\+-]?\d+(\.{0}|\.\d+))[Ee]{1}([\+-]?\d+)|[\+-]?\d+\.?\d*)")
        interval_validator.setRegExp(reg)
        self.edit1.setValidator(interval_validator)
        self.spin = QSpinBox()
        self.spin.setRange(0, 2147483647)
        button1 = QPushButton("绘制")
        button2 = QPushButton("取消")
        formal = QFormLayout()
        formal.addRow(label1, self.edit1)
        formal.addRow(label2, self.spin)
        hlayout = QHBoxLayout()
        hlayout.addWidget(button1)
        hlayout.addWidget(button2)
        layout.addLayout(formal)
        layout.addLayout(hlayout)
        button2.clicked.connect(self.close)
        button1.clicked.connect(self.emit_data)

    def emit_data(self):
        check, val1, val2 = DataSetTool.comma2interval(self.edit1.text())
        if check:
            bin = np.linspace(val1, val2, self.spin.value())
            # print("set bins: {}".format(bin))
            self.emit_bins.emit(bin)
            self.close()
        else:
            QMessageBox.warning(self, "警告", "参数错误", QMessageBox.Ok)


class PandasModel(QAbstractTableModel):
    """A model to interface a Qt view with pandas dataframe """

    def __init__(self, dataframe: pd.DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = dataframe

    def rowCount(self, parent=QModelIndex()) -> int:
        """ Override method from QAbstractTableModel

        Return row count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe)

        return 0

    def columnCount(self, parent=QModelIndex()) -> int:
        """Override method from QAbstractTableModel

        Return column count of the pandas DataFrame
        """
        if parent == QModelIndex():
            return len(self._dataframe.columns)
        return 0

    def data(self, index: QModelIndex, role=Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return data cell from the pandas DataFrame
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        """Override method from QAbstractTableModel

        Return dataframe index as vertical header data and columns as horizontal header data.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == Qt.Vertical:
                return str(self._dataframe.index[section])

        return None


class TableDialog(QDialog):
    def __init__(self, parent = None, pdm: PandasModel = PandasModel(pd.DataFrame())):
        super(TableDialog, self).__init__(parent)
        self.resize(800, 500)
        layout = QHBoxLayout(self)
        view = QTableView()
        view.setModel(pdm)
        view.setAlternatingRowColors(True)
        view.setSelectionBehavior(QTableView.SelectRows)
        view.resizeColumnsToContents()
        layout.addWidget(view)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = RaiseTimeSetBin()
    ui.show()
    sys.exit(app.exec_())
    #========pandas转table方法====================
    # df = pd.read_csv("./example/1353V.csv")
    # view = QTableView()
    # view.resize(800, 500)
    # view.horizontalHeader().setStretchLastSection(True)
    # view.setAlternatingRowColors(True)
    # view.setSelectionBehavior(QTableView.SelectRows)
    # model = PandasModel(df)
    # view.setModel(model)
    # view.show()
    # app.exec()
    #=============================================