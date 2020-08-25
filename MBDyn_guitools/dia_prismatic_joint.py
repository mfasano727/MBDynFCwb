# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dia_prismatic_joint.ui'
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


class Ui_dia_prismatic_joint(object):
    def setupUi(self, dia_prismatic_joint):
        if dia_prismatic_joint.objectName():
            dia_prismatic_joint.setObjectName(u"dia_prismatic_joint")
        dia_prismatic_joint.resize(400, 300)
        self.buttonBox = QDialogButtonBox(dia_prismatic_joint)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(60, 250, 231, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.node_1_label = QLabel(dia_prismatic_joint)
        self.node_1_label.setObjectName(u"node_1_label")
        self.node_1_label.setGeometry(QRect(90, 60, 61, 16))
        font = QFont()
        font.setPointSize(12)
        self.node_1_label.setFont(font)
        self.node_1_Box = QComboBox(dia_prismatic_joint)
        self.node_1_Box.setObjectName(u"node_1_Box")
        self.node_1_Box.setGeometry(QRect(60, 80, 101, 22))
        self.node_2_Box = QComboBox(dia_prismatic_joint)
        self.node_2_Box.setObjectName(u"node_2_Box")
        self.node_2_Box.setGeometry(QRect(240, 80, 101, 22))
        self.node_2_label = QLabel(dia_prismatic_joint)
        self.node_2_label.setObjectName(u"node_2_label")
        self.node_2_label.setGeometry(QRect(270, 60, 61, 16))
        self.node_2_label.setFont(font)
        self.node_1_LCS = QComboBox(dia_prismatic_joint)
        self.node_1_LCS.setObjectName(u"node_1_LCS")
        self.node_1_LCS.setGeometry(QRect(60, 150, 101, 22))
        self.node_1_LCS_label = QLabel(dia_prismatic_joint)
        self.node_1_LCS_label.setObjectName(u"node_1_LCS_label")
        self.node_1_LCS_label.setGeometry(QRect(60, 130, 101, 20))
        self.node_1_LCS_label.setFont(font)
        self.node_2_LCS_label = QLabel(dia_prismatic_joint)
        self.node_2_LCS_label.setObjectName(u"node_2_LCS_label")
        self.node_2_LCS_label.setGeometry(QRect(240, 130, 101, 20))
        self.node_2_LCS_label.setFont(font)
        self.node_2_LCS = QComboBox(dia_prismatic_joint)
        self.node_2_LCS.setObjectName(u"node_2_LCS")
        self.node_2_LCS.setGeometry(QRect(240, 150, 101, 22))

        self.retranslateUi(dia_prismatic_joint)
        self.buttonBox.accepted.connect(dia_prismatic_joint.accept)
        self.buttonBox.rejected.connect(dia_prismatic_joint.reject)

        QMetaObject.connectSlotsByName(dia_prismatic_joint)
    # setupUi

    def retranslateUi(self, dia_prismatic_joint):
        dia_prismatic_joint.setWindowTitle(QCoreApplication.translate("dia_prismatic_joint", u"Dialog", None))
        self.node_1_label.setText(QCoreApplication.translate("dia_prismatic_joint", u"Node 1", None))
        self.node_2_label.setText(QCoreApplication.translate("dia_prismatic_joint", u"Node 2", None))
        self.node_1_LCS_label.setText(QCoreApplication.translate("dia_prismatic_joint", u"Node 1 LCS", None))
        self.node_2_LCS_label.setText(QCoreApplication.translate("dia_prismatic_joint", u"Node 2 LCS", None))
    # retranslateUi

