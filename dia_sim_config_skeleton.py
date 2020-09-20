# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dia_sim_config_skeleton.ui',
# licensing of 'dia_sim_config_skeleton.ui' applies.
#
# Created: Thu Sep 10 23:48:10 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_dia_sim_config(object):
    def setupUi(self, dia_sim_config):
        dia_sim_config.setObjectName("dia_sim_config")
        dia_sim_config.resize(447, 646)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dia_sim_config.sizePolicy().hasHeightForWidth())
        dia_sim_config.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(dia_sim_config)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(dia_sim_config)
        self.frame.setObjectName("frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.frame)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_3.addWidget(self.buttonBox, 1, 2, 1, 1)
        self.bDefault = QtWidgets.QPushButton(self.frame)
        self.bDefault.setObjectName("bDefault")
        self.gridLayout_3.addWidget(self.bDefault, 1, 1, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.frame)
        self.tabWidget.setObjectName("tabWidget")
        self.ProblemTab = QtWidgets.QWidget()
        self.ProblemTab.setObjectName("ProblemTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.ProblemTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ProblemTabLayout = QtWidgets.QFormLayout()
        self.ProblemTabLayout.setObjectName("ProblemTabLayout")
        self.verticalLayout_2.addLayout(self.ProblemTabLayout)
        self.tabWidget.addTab(self.ProblemTab, "")
        self.ControlDataTab = QtWidgets.QWidget()
        self.ControlDataTab.setObjectName("ControlDataTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.ControlDataTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ControlDataTabLayout = QtWidgets.QFormLayout()
        self.ControlDataTabLayout.setContentsMargins(-1, -1, -1, 0)
        self.ControlDataTabLayout.setSpacing(6)
        self.ControlDataTabLayout.setObjectName("ControlDataTabLayout")
        self.verticalLayout.addLayout(self.ControlDataTabLayout)
        self.tabWidget.addTab(self.ControlDataTab, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 3)
        self.verticalLayout_3.addWidget(self.frame)

        self.retranslateUi(dia_sim_config)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), dia_sim_config.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), dia_sim_config.reject)
        QtCore.QObject.connect(self.bDefault, QtCore.SIGNAL("clicked()"), dia_sim_config.setDefault)
        QtCore.QMetaObject.connectSlotsByName(dia_sim_config)

    def retranslateUi(self, dia_sim_config):
        dia_sim_config.setWindowTitle(QtWidgets.QApplication.translate("dia_sim_config", "Dialog", None, -1))
        self.bDefault.setText(QtWidgets.QApplication.translate("dia_sim_config", "Default", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ProblemTab), QtWidgets.QApplication.translate("dia_sim_config", "Problem", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ControlDataTab), QtWidgets.QApplication.translate("dia_sim_config", "Control Data", None, -1))

