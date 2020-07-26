# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dia_axial_rot_joint_As4.ui'
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


class Ui_dia_axial_rot_joint(object):
    def setupUi(self, dia_axial_rot_joint):
        if dia_axial_rot_joint.objectName():
            dia_axial_rot_joint.setObjectName(u"dia_axial_rot_joint")
        dia_axial_rot_joint.resize(600, 400)
        self.buttonBox = QDialogButtonBox(dia_axial_rot_joint)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(40, 370, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.node_1_Box = QComboBox(dia_axial_rot_joint)
        self.node_1_Box.setObjectName(u"node_1_Box")
        self.node_1_Box.setGeometry(QRect(90, 20, 101, 22))
        font = QFont()
        font.setPointSize(10)
        self.node_1_Box.setFont(font)
        self.node_1_label = QLabel(dia_axial_rot_joint)
        self.node_1_label.setObjectName(u"node_1_label")
        self.node_1_label.setGeometry(QRect(90, 0, 91, 21))
        font1 = QFont()
        font1.setPointSize(12)
        self.node_1_label.setFont(font1)
        self.node_2_Box = QComboBox(dia_axial_rot_joint)
        self.node_2_Box.setObjectName(u"node_2_Box")
        self.node_2_Box.setGeometry(QRect(380, 30, 121, 22))
        self.node_2_Box.setFont(font)
        self.node_2_label = QLabel(dia_axial_rot_joint)
        self.node_2_label.setObjectName(u"node_2_label")
        self.node_2_label.setGeometry(QRect(380, 10, 91, 21))
        self.node_2_label.setFont(font1)
        self.z_axis_set_x_lab = QLabel(dia_axial_rot_joint)
        self.z_axis_set_x_lab.setObjectName(u"z_axis_set_x_lab")
        self.z_axis_set_x_lab.setGeometry(QRect(170, 250, 81, 21))
        font2 = QFont()
        font2.setPointSize(11)
        self.z_axis_set_x_lab.setFont(font2)
        self.z_axis_set_y_lab = QLabel(dia_axial_rot_joint)
        self.z_axis_set_y_lab.setObjectName(u"z_axis_set_y_lab")
        self.z_axis_set_y_lab.setGeometry(QRect(260, 250, 81, 21))
        self.z_axis_set_y_lab.setFont(font2)
        self.z_axis_set_x = QLineEdit(dia_axial_rot_joint)
        self.z_axis_set_x.setObjectName(u"z_axis_set_x")
        self.z_axis_set_x.setGeometry(QRect(170, 270, 81, 20))
        self.z_axis_set_x.setFont(font)
        self.z_axis_set_z_lab = QLabel(dia_axial_rot_joint)
        self.z_axis_set_z_lab.setObjectName(u"z_axis_set_z_lab")
        self.z_axis_set_z_lab.setGeometry(QRect(350, 250, 81, 21))
        self.z_axis_set_z_lab.setFont(font2)
        self.z_axis_set_z = QLineEdit(dia_axial_rot_joint)
        self.z_axis_set_z.setObjectName(u"z_axis_set_z")
        self.z_axis_set_z.setGeometry(QRect(350, 270, 81, 20))
        self.z_axis_set_z.setFont(font)
        self.z_axis_set_y = QLineEdit(dia_axial_rot_joint)
        self.z_axis_set_y.setObjectName(u"z_axis_set_y")
        self.z_axis_set_y.setGeometry(QRect(260, 270, 81, 20))
        self.z_axis_set_y.setFont(font)
        self.choose_z_axis_1 = QRadioButton(dia_axial_rot_joint)
        self.choose_z_axis_1.setObjectName(u"choose_z_axis_1")
        self.choose_z_axis_1.setGeometry(QRect(180, 140, 101, 16))
        self.choose_z_axis_2 = QRadioButton(dia_axial_rot_joint)
        self.choose_z_axis_2.setObjectName(u"choose_z_axis_2")
        self.choose_z_axis_2.setGeometry(QRect(300, 140, 141, 16))
        self.Choose_z_axis_Box = QComboBox(dia_axial_rot_joint)
        self.Choose_z_axis_Box.setObjectName(u"Choose_z_axis_Box")
        self.Choose_z_axis_Box.setGeometry(QRect(180, 200, 201, 22))
        self.choose_z_axis_lab = QLabel(dia_axial_rot_joint)
        self.choose_z_axis_lab.setObjectName(u"choose_z_axis_lab")
        self.choose_z_axis_lab.setGeometry(QRect(220, 180, 111, 20))
        self.choose_z_axis_lab.setFont(font)
        self.link_const_lab = QLabel(dia_axial_rot_joint)
        self.link_const_lab.setObjectName(u"link_const_lab")
        self.link_const_lab.setGeometry(QRect(250, 70, 81, 16))
        self.link_const_lab.setFont(font1)
        self.link_const_Box = QComboBox(dia_axial_rot_joint)
        self.link_const_Box.setObjectName(u"link_const_Box")
        self.link_const_Box.setGeometry(QRect(130, 90, 291, 22))
        self.drive_Box = QComboBox(dia_axial_rot_joint)
        self.drive_Box.setObjectName(u"drive_Box")
        self.drive_Box.setGeometry(QRect(230, 330, 141, 22))
        self.drive_Box.setFont(font)
        self.drive_label = QLabel(dia_axial_rot_joint)
        self.drive_label.setObjectName(u"drive_label")
        self.drive_label.setGeometry(QRect(260, 310, 101, 16))
        self.drive_label.setFont(font)

        self.retranslateUi(dia_axial_rot_joint)
        self.buttonBox.accepted.connect(dia_axial_rot_joint.accept)
        self.buttonBox.rejected.connect(dia_axial_rot_joint.reject)

        QMetaObject.connectSlotsByName(dia_axial_rot_joint)
    # setupUi

    def retranslateUi(self, dia_axial_rot_joint):
        dia_axial_rot_joint.setWindowTitle(QCoreApplication.translate("dia_axial_rot_joint", u"axial rotation joint", None))
        self.node_1_label.setText(QCoreApplication.translate("dia_axial_rot_joint", u"node 1", None))
        self.node_2_label.setText(QCoreApplication.translate("dia_axial_rot_joint", u"node 2", None))
        self.z_axis_set_x_lab.setText(QCoreApplication.translate("dia_axial_rot_joint", u"z_axis set x", None))
        self.z_axis_set_y_lab.setText(QCoreApplication.translate("dia_axial_rot_joint", u"z_axis set y", None))
        self.z_axis_set_z_lab.setText(QCoreApplication.translate("dia_axial_rot_joint", u"z_axis set z", None))
        self.choose_z_axis_1.setText(QCoreApplication.translate("dia_axial_rot_joint", u"input rotation axis", None))
        self.choose_z_axis_2.setText(QCoreApplication.translate("dia_axial_rot_joint", u"choose LCS axis for rotation", None))
        self.choose_z_axis_lab.setText(QCoreApplication.translate("dia_axial_rot_joint", u"Choose Z axis from LCS", None))
        self.link_const_lab.setText(QCoreApplication.translate("dia_axial_rot_joint", u"Link constraint", None))
        self.drive_label.setText(QCoreApplication.translate("dia_axial_rot_joint", u"choose drive caller", None))
    # retranslateUi
