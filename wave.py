# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wave.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1144, 811)
        self.gridLayout_9 = QtWidgets.QGridLayout(Form)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout.addWidget(self.radioButton, 0, 0, 1, 1)
        self.radioButton_2 = QtWidgets.QRadioButton(Form)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout.addWidget(self.radioButton_2, 0, 1, 1, 1)
        self.radioButton_3 = QtWidgets.QRadioButton(Form)
        self.radioButton_3.setObjectName("radioButton_3")
        self.gridLayout.addWidget(self.radioButton_3, 1, 0, 1, 1)
        self.listView = QtWidgets.QListView(Form)
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 2, 0, 1, 2)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 1, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.groupBox = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(350, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(350, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_4.setObjectName("radioButton_4")
        self.gridLayout_2.addWidget(self.radioButton_4, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 2, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 2)
        self.gridLayout_7.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(350, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(350, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_3.addWidget(self.comboBox, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_3.addWidget(self.lineEdit_3, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 1, 2, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 2, 0, 1, 2)
        self.gridLayout_7.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(350, 0))
        self.tabWidget.setMaximumSize(QtCore.QSize(350, 16777215))
        self.tabWidget.setObjectName("tabWidget")
        self.Trigger = QtWidgets.QWidget()
        self.Trigger.setObjectName("Trigger")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.Trigger)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_8 = QtWidgets.QLabel(self.Trigger)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 0, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.Trigger)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_4.addWidget(self.lineEdit_4, 0, 1, 1, 3)
        self.label_9 = QtWidgets.QLabel(self.Trigger)
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 0, 4, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.Trigger)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout_4.addWidget(self.comboBox_2, 0, 5, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.Trigger)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_4.addWidget(self.checkBox, 1, 0, 1, 2)
        self.checkBox_2 = QtWidgets.QCheckBox(self.Trigger)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_4.addWidget(self.checkBox_2, 1, 2, 1, 1)
        self.checkBox_3 = QtWidgets.QCheckBox(self.Trigger)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout_4.addWidget(self.checkBox_3, 1, 3, 1, 3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_7 = QtWidgets.QPushButton(self.Trigger)
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_3.addWidget(self.pushButton_7)
        self.pushButton_8 = QtWidgets.QPushButton(self.Trigger)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_3.addWidget(self.pushButton_8)
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 2, 0, 1, 5)
        self.tabWidget.addTab(self.Trigger, "")
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_12 = QtWidgets.QLabel(self.widget)
        self.label_12.setObjectName("label_12")
        self.gridLayout_5.addWidget(self.label_12, 0, 0, 1, 1)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout_5.addWidget(self.lineEdit_6, 0, 1, 1, 2)
        self.label_13 = QtWidgets.QLabel(self.widget)
        self.label_13.setObjectName("label_13")
        self.gridLayout_5.addWidget(self.label_13, 0, 3, 1, 2)
        self.comboBox_4 = QtWidgets.QComboBox(self.widget)
        self.comboBox_4.setObjectName("comboBox_4")
        self.gridLayout_5.addWidget(self.comboBox_4, 0, 5, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.widget)
        self.label_10.setObjectName("label_10")
        self.gridLayout_5.addWidget(self.label_10, 1, 0, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_5.addWidget(self.lineEdit_5, 1, 1, 1, 2)
        self.label_11 = QtWidgets.QLabel(self.widget)
        self.label_11.setObjectName("label_11")
        self.gridLayout_5.addWidget(self.label_11, 1, 3, 1, 3)
        self.checkBox_4 = QtWidgets.QCheckBox(self.widget)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout_5.addWidget(self.checkBox_4, 2, 0, 1, 2)
        self.checkBox_5 = QtWidgets.QCheckBox(self.widget)
        self.checkBox_5.setObjectName("checkBox_5")
        self.gridLayout_5.addWidget(self.checkBox_5, 2, 2, 1, 2)
        self.checkBox_6 = QtWidgets.QCheckBox(self.widget)
        self.checkBox_6.setObjectName("checkBox_6")
        self.gridLayout_5.addWidget(self.checkBox_6, 2, 4, 1, 2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_14 = QtWidgets.QPushButton(self.widget)
        self.pushButton_14.setObjectName("pushButton_14")
        self.horizontalLayout_4.addWidget(self.pushButton_14)
        self.pushButton_15 = QtWidgets.QPushButton(self.widget)
        self.pushButton_15.setObjectName("pushButton_15")
        self.horizontalLayout_4.addWidget(self.pushButton_15)
        self.gridLayout_5.addLayout(self.horizontalLayout_4, 3, 0, 1, 4)
        self.tabWidget.addTab(self.widget, "")
        self.gridLayout_7.addWidget(self.tabWidget, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem, 3, 0, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_14 = QtWidgets.QLabel(Form)
        self.label_14.setObjectName("label_14")
        self.gridLayout_6.addWidget(self.label_14, 0, 0, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(Form)
        self.comboBox_3.setObjectName("comboBox_3")
        self.gridLayout_6.addWidget(self.comboBox_3, 0, 1, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(Form)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout_6.addWidget(self.pushButton_9, 0, 2, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(Form)
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout_6.addWidget(self.pushButton_10, 1, 0, 1, 2)
        self.gridLayout_7.addLayout(self.gridLayout_6, 4, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_7, 0, 1, 1, 1)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.textEdit = QtWidgets.QTextEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_8.addWidget(self.textEdit, 1, 0, 1, 4)
        self.pushButton_13 = QtWidgets.QPushButton(Form)
        self.pushButton_13.setObjectName("pushButton_13")
        self.gridLayout_8.addWidget(self.pushButton_13, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem1, 0, 3, 1, 1)
        self.widget1 = QtWidgets.QWidget(Form)
        self.widget1.setObjectName("widget1")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.checkBox_7 = QtWidgets.QCheckBox(self.widget1)
        self.checkBox_7.setObjectName("checkBox_7")
        self.gridLayout_10.addWidget(self.checkBox_7, 0, 0, 1, 1)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_7.sizePolicy().hasHeightForWidth())
        self.lineEdit_7.setSizePolicy(sizePolicy)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout_10.addWidget(self.lineEdit_7, 0, 1, 1, 1)
        self.pushButton_16 = QtWidgets.QPushButton(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_16.sizePolicy().hasHeightForWidth())
        self.pushButton_16.setSizePolicy(sizePolicy)
        self.pushButton_16.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButton_16.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_16.setObjectName("pushButton_16")
        self.gridLayout_10.addWidget(self.pushButton_16, 0, 2, 1, 1)
        self.checkBox_8 = QtWidgets.QCheckBox(self.widget1)
        self.checkBox_8.setObjectName("checkBox_8")
        self.gridLayout_10.addWidget(self.checkBox_8, 0, 3, 1, 1)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_8.sizePolicy().hasHeightForWidth())
        self.lineEdit_8.setSizePolicy(sizePolicy)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.gridLayout_10.addWidget(self.lineEdit_8, 0, 4, 1, 1)
        self.pushButton_17 = QtWidgets.QPushButton(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_17.sizePolicy().hasHeightForWidth())
        self.pushButton_17.setSizePolicy(sizePolicy)
        self.pushButton_17.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButton_17.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_17.setObjectName("pushButton_17")
        self.gridLayout_10.addWidget(self.pushButton_17, 0, 5, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(12, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_10.addItem(spacerItem2, 0, 6, 1, 1)
        self.frame = QtWidgets.QFrame(self.widget1)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_10.addWidget(self.frame, 1, 0, 1, 7)
        self.gridLayout_8.addWidget(self.widget1, 2, 0, 1, 4)
        self.pushButton_12 = QtWidgets.QPushButton(Form)
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout_8.addWidget(self.pushButton_12, 0, 1, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(Form)
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout_8.addWidget(self.pushButton_11, 0, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_8, 0, 2, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.radioButton.setText(_translate("Form", "Absulute Path"))
        self.radioButton_2.setText(_translate("Form", "Relative Path"))
        self.radioButton_3.setText(_translate("Form", "Basename"))
        self.pushButton.setText(_translate("Form", "Load"))
        self.pushButton_2.setText(_translate("Form", "Clear"))
        self.groupBox.setTitle(_translate("Form", "Pedestal Setting"))
        self.radioButton_4.setText(_translate("Form", "Multiple Interval"))
        self.label.setText(_translate("Form", "Interval1"))
        self.label_2.setText(_translate("Form", "s"))
        self.label_3.setText(_translate("Form", "Interval2"))
        self.label_4.setText(_translate("Form", "s"))
        self.pushButton_3.setText(_translate("Form", "OK"))
        self.pushButton_4.setText(_translate("Form", "Reset"))
        self.groupBox_2.setTitle(_translate("Form", "GroupBox"))
        self.label_5.setText(_translate("Form", "Integration Method"))
        self.label_6.setText(_translate("Form", "Interval"))
        self.label_7.setText(_translate("Form", "s"))
        self.pushButton_5.setText(_translate("Form", "OK"))
        self.pushButton_6.setText(_translate("Form", "Reset"))
        self.label_8.setText(_translate("Form", "Interval"))
        self.label_9.setText(_translate("Form", "s"))
        self.checkBox.setText(_translate("Form", "Seq Index"))
        self.checkBox_2.setText(_translate("Form", "Ampl"))
        self.checkBox_3.setText(_translate("Form", "Time"))
        self.pushButton_7.setText(_translate("Form", "OK"))
        self.pushButton_8.setText(_translate("Form", "Reset"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Trigger), _translate("Form", "Extremun Setting"))
        self.label_12.setText(_translate("Form", "Voltage"))
        self.label_13.setText(_translate("Form", "V"))
        self.label_10.setText(_translate("Form", "Interval"))
        self.label_11.setText(_translate("Form", "s"))
        self.checkBox_4.setText(_translate("Form", "Tri Bool"))
        self.checkBox_5.setText(_translate("Form", "Tri Index"))
        self.checkBox_6.setText(_translate("Form", "Tri Time"))
        self.pushButton_14.setText(_translate("Form", "OK"))
        self.pushButton_15.setText(_translate("Form", "Reset"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), _translate("Form", "Trigger Setting"))
        self.label_14.setText(_translate("Form", "Format"))
        self.pushButton_9.setText(_translate("Form", "Save Setting"))
        self.pushButton_10.setText(_translate("Form", "GO"))
        self.pushButton_13.setText(_translate("Form", "Strop"))
        self.checkBox_7.setText(_translate("Form", "x limit"))
        self.pushButton_16.setText(_translate("Form", "OK"))
        self.checkBox_8.setText(_translate("Form", "y limit"))
        self.pushButton_17.setText(_translate("Form", "OK"))
        self.pushButton_12.setText(_translate("Form", "Resume"))
        self.pushButton_11.setText(_translate("Form", "Pause"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())


