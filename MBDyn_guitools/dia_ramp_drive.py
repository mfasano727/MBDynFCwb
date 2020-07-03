# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dia_ramp_drive.ui'
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


class Ui_dia_ramp_drive(object):
    def setupUi(self, dia_ramp_drive):
        if dia_ramp_drive.objectName():
            dia_ramp_drive.setObjectName(u"dia_ramp_drive")
        dia_ramp_drive.resize(400, 300)
        self.buttonBox = QDialogButtonBox(dia_ramp_drive)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(90, 260, 221, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.slope_lab = QLabel(dia_ramp_drive)
        self.slope_lab.setObjectName(u"slope_lab")
        self.slope_lab.setGeometry(QRect(200, 30, 35, 16))
        font = QFont()
        font.setPointSize(10)
        self.slope_lab.setFont(font)
        self.slope = QLineEdit(dia_ramp_drive)
        self.slope.setObjectName(u"slope")
        self.slope.setGeometry(QRect(160, 50, 113, 20))
        self.initial_time = QLineEdit(dia_ramp_drive)
        self.initial_time.setObjectName(u"initial_time")
        self.initial_time.setGeometry(QRect(160, 100, 113, 20))
        self.initial_time_lab = QLabel(dia_ramp_drive)
        self.initial_time_lab.setObjectName(u"initial_time_lab")
        self.initial_time_lab.setGeometry(QRect(190, 80, 71, 20))
        self.initial_time_lab.setFont(font)
        self.final_time_lab = QLabel(dia_ramp_drive)
        self.final_time_lab.setObjectName(u"final_time_lab")
        self.final_time_lab.setGeometry(QRect(190, 130, 71, 20))
        self.final_time_lab.setFont(font)
        self.final_time = QLineEdit(dia_ramp_drive)
        self.final_time.setObjectName(u"final_time")
        self.final_time.setGeometry(QRect(160, 150, 113, 20))
        self.initial_value_lab = QLabel(dia_ramp_drive)
        self.initial_value_lab.setObjectName(u"initial_value_lab")
        self.initial_value_lab.setGeometry(QRect(190, 190, 71, 20))
        self.initial_value_lab.setFont(font)
        self.initial_value = QLineEdit(dia_ramp_drive)
        self.initial_value.setObjectName(u"initial_value")
        self.initial_value.setGeometry(QRect(160, 210, 113, 20))

        self.retranslateUi(dia_ramp_drive)
        self.buttonBox.accepted.connect(dia_ramp_drive.accept)
        self.buttonBox.rejected.connect(dia_ramp_drive.reject)

        QMetaObject.connectSlotsByName(dia_ramp_drive)
    # setupUi

    def retranslateUi(self, dia_ramp_drive):
        dia_ramp_drive.setWindowTitle(QCoreApplication.translate("dia_ramp_drive", u"Dialog", None))
        self.slope_lab.setText(QCoreApplication.translate("dia_ramp_drive", u"slope", None))
        self.initial_time_lab.setText(QCoreApplication.translate("dia_ramp_drive", u"initial time", None))
        self.final_time_lab.setText(QCoreApplication.translate("dia_ramp_drive", u"final time", None))
        self.initial_value_lab.setText(QCoreApplication.translate("dia_ramp_drive", u"initial value", None))
    # retranslateUi

