# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dia_postproc.ui',
# licensing of 'dia_postproc.ui' applies.
#
# Created: Sat Sep 19 09:25:45 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_dia_postporc(object):
    def setupUi(self, dia_postporc):
        dia_postporc.setObjectName("dia_postporc")
        dia_postporc.resize(400, 200)
        self.buttonBox = QtWidgets.QDialogButtonBox(dia_postporc)
        self.buttonBox.setGeometry(QtCore.QRect(100, 100, 211, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.sel_out_path = QtWidgets.QPushButton(dia_postporc)
        self.sel_out_path.setGeometry(QtCore.QRect(310, 50, 80, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sel_out_path.setFont(font)
        self.sel_out_path.setObjectName("sel_out_path")
        self.output_path = QtWidgets.QLineEdit(dia_postporc)
        self.output_path.setGeometry(QtCore.QRect(10, 50, 301, 20))
        self.output_path.setReadOnly(True)
        self.output_path.setObjectName("output_path")
        self.sel_output_path = QtWidgets.QLabel(dia_postporc)
        self.sel_output_path.setGeometry(QtCore.QRect(160, 30, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sel_output_path.setFont(font)
        self.sel_output_path.setObjectName("sel_output_path")
        self.iScaleFactor = QtWidgets.QSpinBox(dia_postporc)
        self.iScaleFactor.setGeometry(QtCore.QRect(130, 80, 42, 22))
        self.iScaleFactor.setMinimum(1)
        self.iScaleFactor.setProperty("value", 2)
        self.iScaleFactor.setObjectName("iScaleFactor")
        self.label = QtWidgets.QLabel(dia_postporc)
        self.label.setGeometry(QtCore.QRect(46, 80, 71, 20))
        self.label.setObjectName("label")

        self.retranslateUi(dia_postporc)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), dia_postporc.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), dia_postporc.reject)
        QtCore.QMetaObject.connectSlotsByName(dia_postporc)

    def retranslateUi(self, dia_postporc):
        dia_postporc.setWindowTitle(QtWidgets.QApplication.translate("dia_postporc", "Dialog", None, -1))
        self.sel_out_path.setText(QtWidgets.QApplication.translate("dia_postporc", "select output...", None, -1))
        self.sel_output_path.setText(QtWidgets.QApplication.translate("dia_postporc", "select an output file", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("dia_postporc", "Scale Factor", None, -1))

