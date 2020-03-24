# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dia_body_sel.ui'
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


class Ui_dia_body_sel(object):
    def setupUi(self, dia_body_sel):
        if dia_body_sel.objectName():
            dia_body_sel.setObjectName(u"dia_body_sel")
        dia_body_sel.resize(400, 300)
        self.buttonBox = QDialogButtonBox(dia_body_sel)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.body_list = QComboBox(dia_body_sel)
        self.body_list.setObjectName(u"body_list")
        self.body_list.setGeometry(QRect(160, 100, 181, 101))
        self.body_list_label = QLabel(dia_body_sel)
        self.body_list_label.setObjectName(u"body_list_label")
        self.body_list_label.setGeometry(QRect(160, 70, 161, 20))
        font = QFont()
        font.setPointSize(12)
        self.body_list_label.setFont(font)

        self.retranslateUi(dia_body_sel)
        self.buttonBox.accepted.connect(dia_body_sel.accept)
        self.buttonBox.rejected.connect(dia_body_sel.reject)

        QMetaObject.connectSlotsByName(dia_body_sel)
    # setupUi

    def retranslateUi(self, dia_body_sel):
        dia_body_sel.setWindowTitle(QCoreApplication.translate("dia_body_sel", u"Dialog", None))
        self.body_list_label.setText(QCoreApplication.translate("dia_body_sel", u"choose a body from list", None))
    # retranslateUi

