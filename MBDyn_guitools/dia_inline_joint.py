# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dia_inline_joint.ui'
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


class Ui_dia_inline_joint(object):
    def setupUi(self, dia_inline_joint):
        if dia_inline_joint.objectName():
            dia_inline_joint.setObjectName(u"dia_inline_joint")
        dia_inline_joint.resize(400, 300)
        self.buttonBox = QDialogButtonBox(dia_inline_joint)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(60, 250, 231, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.node_1_label = QLabel(dia_inline_joint)
        self.node_1_label.setObjectName(u"node_1_label")
        self.node_1_label.setGeometry(QRect(90, 10, 61, 16))
        font = QFont()
        font.setPointSize(12)
        self.node_1_label.setFont(font)
        self.node_1_Box = QComboBox(dia_inline_joint)
        self.node_1_Box.setObjectName(u"node_1_Box")
        self.node_1_Box.setGeometry(QRect(60, 30, 101, 22))
        self.node_2_Box = QComboBox(dia_inline_joint)
        self.node_2_Box.setObjectName(u"node_2_Box")
        self.node_2_Box.setGeometry(QRect(240, 30, 101, 22))
        self.node_2_label = QLabel(dia_inline_joint)
        self.node_2_label.setObjectName(u"node_2_label")
        self.node_2_label.setGeometry(QRect(270, 10, 61, 16))
        self.node_2_label.setFont(font)
        self.node_1_LCS = QComboBox(dia_inline_joint)
        self.node_1_LCS.setObjectName(u"node_1_LCS")
        self.node_1_LCS.setGeometry(QRect(60, 90, 101, 22))
        self.node_1_LCS_label = QLabel(dia_inline_joint)
        self.node_1_LCS_label.setObjectName(u"node_1_LCS_label")
        self.node_1_LCS_label.setGeometry(QRect(60, 70, 101, 20))
        self.node_1_LCS_label.setFont(font)
        self.node_2_LCS_label = QLabel(dia_inline_joint)
        self.node_2_LCS_label.setObjectName(u"node_2_LCS_label")
        self.node_2_LCS_label.setGeometry(QRect(240, 70, 101, 20))
        self.node_2_LCS_label.setFont(font)
        self.node_2_LCS = QComboBox(dia_inline_joint)
        self.node_2_LCS.setObjectName(u"node_2_LCS")
        self.node_2_LCS.setGeometry(QRect(240, 90, 101, 22))
        self.line_def_Box = QComboBox(dia_inline_joint)
        self.line_def_Box.addItem("")
        self.line_def_Box.addItem("")
        self.line_def_Box.setObjectName(u"line_def_Box")
        self.line_def_Box.setGeometry(QRect(140, 150, 121, 22))
        font1 = QFont()
        font1.setPointSize(10)
        self.line_def_Box.setFont(font1)
        self.line_def_label = QLabel(dia_inline_joint)
        self.line_def_label.setObjectName(u"line_def_label")
        self.line_def_label.setGeometry(QRect(140, 130, 131, 20))
        self.line_def_label.setFont(font1)
        self.LCS_axis_label = QLabel(dia_inline_joint)
        self.LCS_axis_label.setObjectName(u"LCS_axis_label")
        self.LCS_axis_label.setGeometry(QRect(140, 190, 121, 20))
        self.LCS_axis_label.setFont(font1)
        self.node1_axis_Box = QComboBox(dia_inline_joint)
        self.node1_axis_Box.addItem("")
        self.node1_axis_Box.addItem("")
        self.node1_axis_Box.addItem("")
        self.node1_axis_Box.setObjectName(u"node1_axis_Box")
        self.node1_axis_Box.setGeometry(QRect(140, 210, 121, 22))
        self.node1_axis_Box.setFont(font1)

        self.retranslateUi(dia_inline_joint)
        self.buttonBox.accepted.connect(dia_inline_joint.accept)
        self.buttonBox.rejected.connect(dia_inline_joint.reject)

        QMetaObject.connectSlotsByName(dia_inline_joint)
    # setupUi

    def retranslateUi(self, dia_inline_joint):
        dia_inline_joint.setWindowTitle(QCoreApplication.translate("dia_inline_joint", u"inline joint dialog", None))
        self.node_1_label.setText(QCoreApplication.translate("dia_inline_joint", u"Node 1", None))
        self.node_2_label.setText(QCoreApplication.translate("dia_inline_joint", u"Node 2", None))
        self.node_1_LCS_label.setText(QCoreApplication.translate("dia_inline_joint", u"Node 1 LCS pos.", None))
        self.node_2_LCS_label.setText(QCoreApplication.translate("dia_inline_joint", u"Node 2 LCS pos.", None))
        self.line_def_Box.setItemText(0, QCoreApplication.translate("dia_inline_joint", u"line from node LCSs", None))
        self.line_def_Box.setItemText(1, QCoreApplication.translate("dia_inline_joint", u"node 1 LCS axis", None))

        self.line_def_label.setText(QCoreApplication.translate("dia_inline_joint", u"How to define line direction", None))
        self.LCS_axis_label.setText(QCoreApplication.translate("dia_inline_joint", u"node 1 LCS axis", None))
        self.node1_axis_Box.setItemText(0, QCoreApplication.translate("dia_inline_joint", u"X", None))
        self.node1_axis_Box.setItemText(1, QCoreApplication.translate("dia_inline_joint", u"Y", None))
        self.node1_axis_Box.setItemText(2, QCoreApplication.translate("dia_inline_joint", u"Z", None))

    # retranslateUi

