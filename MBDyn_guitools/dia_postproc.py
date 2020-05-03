# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dia_postproc.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_dia_postporc(object):
    def setupUi(self, dia_postporc):
        if dia_postporc.objectName():
            dia_postporc.setObjectName(u"dia_postporc")
        dia_postporc.resize(400, 200)
        self.buttonBox = QDialogButtonBox(dia_postporc)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(100, 100, 211, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.sel_out_path = QPushButton(dia_postporc)
        self.sel_out_path.setObjectName(u"sel_out_path")
        self.sel_out_path.setGeometry(QRect(310, 50, 80, 21))
        font = QFont()
        font.setPointSize(10)
        self.sel_out_path.setFont(font)
        self.output_path = QLineEdit(dia_postporc)
        self.output_path.setObjectName(u"output_path")
        self.output_path.setGeometry(QRect(10, 50, 301, 20))
        self.output_path.setReadOnly(True)
        self.sel_output_path = QLabel(dia_postporc)
        self.sel_output_path.setObjectName(u"sel_output_path")
        self.sel_output_path.setGeometry(QRect(160, 30, 171, 21))
        font1 = QFont()
        font1.setPointSize(12)
        self.sel_output_path.setFont(font1)

        self.retranslateUi(dia_postporc)
        self.buttonBox.accepted.connect(dia_postporc.accept)
        self.buttonBox.rejected.connect(dia_postporc.reject)

        QMetaObject.connectSlotsByName(dia_postporc)
    # setupUi

    def retranslateUi(self, dia_postporc):
        dia_postporc.setWindowTitle(QCoreApplication.translate("dia_postporc", u"Dialog", None))
        self.sel_out_path.setText(QCoreApplication.translate("dia_postporc", u"select output...", None))
        self.sel_output_path.setText(QCoreApplication.translate("dia_postporc", u"select an output file", None))
    # retranslateUi

