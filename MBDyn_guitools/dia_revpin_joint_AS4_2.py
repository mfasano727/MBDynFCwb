# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dia_revpin_joint_AS4_2.ui'
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


class Ui_dia_revpin_joint(object):
    def setupUi(self, dia_revpin_joint):
        if dia_revpin_joint.objectName():
            dia_revpin_joint.setObjectName(u"dia_revpin_joint")
        dia_revpin_joint.resize(600, 400)
        font = QFont()
        font.setPointSize(10)
        dia_revpin_joint.setFont(font)
        self.buttonBox = QDialogButtonBox(dia_revpin_joint)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(40, 370, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.node_1_Box = QComboBox(dia_revpin_joint)
        self.node_1_Box.setObjectName(u"node_1_Box")
        self.node_1_Box.setGeometry(QRect(140, 20, 101, 22))
        self.node_1_Box.setFont(font)
        self.node_1_label = QLabel(dia_revpin_joint)
        self.node_1_label.setObjectName(u"node_1_label")
        self.node_1_label.setGeometry(QRect(170, 0, 91, 21))
        font1 = QFont()
        font1.setPointSize(12)
        self.node_1_label.setFont(font1)
        self.z_axis_set_x_lab = QLabel(dia_revpin_joint)
        self.z_axis_set_x_lab.setObjectName(u"z_axis_set_x_lab")
        self.z_axis_set_x_lab.setGeometry(QRect(190, 170, 81, 21))
        font2 = QFont()
        font2.setPointSize(11)
        self.z_axis_set_x_lab.setFont(font2)
        self.z_axis_set_z_lab = QLabel(dia_revpin_joint)
        self.z_axis_set_z_lab.setObjectName(u"z_axis_set_z_lab")
        self.z_axis_set_z_lab.setGeometry(QRect(370, 170, 81, 21))
        self.z_axis_set_z_lab.setFont(font2)
        self.z_axis_set_y = QLineEdit(dia_revpin_joint)
        self.z_axis_set_y.setObjectName(u"z_axis_set_y")
        self.z_axis_set_y.setGeometry(QRect(280, 190, 81, 20))
        self.z_axis_set_y.setFont(font)
        self.z_axis_set_x = QLineEdit(dia_revpin_joint)
        self.z_axis_set_x.setObjectName(u"z_axis_set_x")
        self.z_axis_set_x.setGeometry(QRect(190, 190, 81, 20))
        self.z_axis_set_x.setFont(font)
        self.z_axis_set_z = QLineEdit(dia_revpin_joint)
        self.z_axis_set_z.setObjectName(u"z_axis_set_z")
        self.z_axis_set_z.setGeometry(QRect(370, 190, 81, 20))
        self.z_axis_set_z.setFont(font)
        self.z_axis_set_y_lab = QLabel(dia_revpin_joint)
        self.z_axis_set_y_lab.setObjectName(u"z_axis_set_y_lab")
        self.z_axis_set_y_lab.setGeometry(QRect(280, 170, 81, 21))
        self.z_axis_set_y_lab.setFont(font2)
        self.link_const_Box = QComboBox(dia_revpin_joint)
        self.link_const_Box.setObjectName(u"link_const_Box")
        self.link_const_Box.setGeometry(QRect(260, 20, 291, 22))
        self.link_const_lab = QLabel(dia_revpin_joint)
        self.link_const_lab.setObjectName(u"link_const_lab")
        self.link_const_lab.setGeometry(QRect(380, 0, 81, 16))
        self.link_const_lab.setFont(font1)
        self.choose_z_axis_1 = QRadioButton(dia_revpin_joint)
        self.choose_z_axis_1.setObjectName(u"choose_z_axis_1")
        self.choose_z_axis_1.setGeometry(QRect(220, 70, 101, 16))
        self.choose_z_axis_2 = QRadioButton(dia_revpin_joint)
        self.choose_z_axis_2.setObjectName(u"choose_z_axis_2")
        self.choose_z_axis_2.setGeometry(QRect(340, 70, 141, 16))
        self.Choose_z_axis_Box = QComboBox(dia_revpin_joint)
        self.Choose_z_axis_Box.setObjectName(u"Choose_z_axis_Box")
        self.Choose_z_axis_Box.setGeometry(QRect(220, 130, 201, 22))
        self.choose_z_axis_lab = QLabel(dia_revpin_joint)
        self.choose_z_axis_lab.setObjectName(u"choose_z_axis_lab")
        self.choose_z_axis_lab.setGeometry(QRect(260, 110, 111, 20))

        self.retranslateUi(dia_revpin_joint)
        self.buttonBox.accepted.connect(dia_revpin_joint.accept)
        self.buttonBox.rejected.connect(dia_revpin_joint.reject)

        QMetaObject.connectSlotsByName(dia_revpin_joint)
    # setupUi

    def retranslateUi(self, dia_revpin_joint):
        dia_revpin_joint.setWindowTitle(QCoreApplication.translate("dia_revpin_joint", u"revlute pin joint", None))
        self.node_1_label.setText(QCoreApplication.translate("dia_revpin_joint", u"node", None))
        self.z_axis_set_x_lab.setText(QCoreApplication.translate("dia_revpin_joint", u"z_axis set x", None))
        self.z_axis_set_z_lab.setText(QCoreApplication.translate("dia_revpin_joint", u"z_axis set z", None))
        self.z_axis_set_y_lab.setText(QCoreApplication.translate("dia_revpin_joint", u"z_axis set y", None))
        self.link_const_lab.setText(QCoreApplication.translate("dia_revpin_joint", u"Link constraint", None))
        self.choose_z_axis_1.setText(QCoreApplication.translate("dia_revpin_joint", u"input rotation axis", None))
        self.choose_z_axis_2.setText(QCoreApplication.translate("dia_revpin_joint", u"choose LCS axis for rotation", None))
        self.choose_z_axis_lab.setText(QCoreApplication.translate("dia_revpin_joint", u"Choose Z axis from LCS", None))
    # retranslateUi

