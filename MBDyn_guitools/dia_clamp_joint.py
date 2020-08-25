# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dia_clamp_joint.ui'
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


class Ui_dia_clamp_joint(object):
    def setupUi(self, dia_clamp_joint):
        if dia_clamp_joint.objectName():
            dia_clamp_joint.setObjectName(u"dia_clamp_joint")
        dia_clamp_joint.resize(291, 300)
        self.buttonBox = QDialogButtonBox(dia_clamp_joint)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(50, 240, 181, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.node_1_label = QLabel(dia_clamp_joint)
        self.node_1_label.setObjectName(u"node_1_label")
        self.node_1_label.setGeometry(QRect(120, 10, 61, 16))
        font = QFont()
        font.setPointSize(12)
        self.node_1_label.setFont(font)
        self.node_1_Box = QComboBox(dia_clamp_joint)
        self.node_1_Box.setObjectName(u"node_1_Box")
        self.node_1_Box.setGeometry(QRect(90, 30, 101, 22))
        self.node_1_LCS = QComboBox(dia_clamp_joint)
        self.node_1_LCS.setObjectName(u"node_1_LCS")
        self.node_1_LCS.setGeometry(QRect(90, 90, 101, 22))
        self.node_1_LCS_label = QLabel(dia_clamp_joint)
        self.node_1_LCS_label.setObjectName(u"node_1_LCS_label")
        self.node_1_LCS_label.setGeometry(QRect(100, 70, 101, 20))
        self.node_1_LCS_label.setFont(font)

        self.retranslateUi(dia_clamp_joint)
        self.buttonBox.accepted.connect(dia_clamp_joint.accept)
        self.buttonBox.rejected.connect(dia_clamp_joint.reject)

        QMetaObject.connectSlotsByName(dia_clamp_joint)
    # setupUi

    def retranslateUi(self, dia_clamp_joint):
        dia_clamp_joint.setWindowTitle(QCoreApplication.translate("dia_clamp_joint", u"clamp joint dialog", None))
        self.node_1_label.setText(QCoreApplication.translate("dia_clamp_joint", u"Node 1", None))
        self.node_1_LCS_label.setText(QCoreApplication.translate("dia_clamp_joint", u"Node 1 LCS", None))
    # retranslateUi

