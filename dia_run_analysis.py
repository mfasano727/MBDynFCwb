# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dia_run_analysis.ui',
# licensing of 'dia_run_analysis.ui' applies.
#
# Created: Sat Jul 18 14:43:08 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_dia_run_analysis(object):
    def setupUi(self, dia_run_analysis):
        dia_run_analysis.setObjectName("dia_run_analysis")
        dia_run_analysis.resize(311, 254)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dia_run_analysis.sizePolicy().hasHeightForWidth())
        dia_run_analysis.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(dia_run_analysis)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(dia_run_analysis)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.active_solver = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.active_solver.sizePolicy().hasHeightForWidth())
        self.active_solver.setSizePolicy(sizePolicy)
        self.active_solver.setObjectName("active_solver")
        self.horizontalLayout.addWidget(self.active_solver)
        self.use_wsl = QtWidgets.QCheckBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.use_wsl.sizePolicy().hasHeightForWidth())
        self.use_wsl.setSizePolicy(sizePolicy)
        self.use_wsl.setMinimumSize(QtCore.QSize(30, 0))
        self.use_wsl.setObjectName("use_wsl")
        self.horizontalLayout.addWidget(self.use_wsl)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(dia_run_analysis)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.out_filename = QtWidgets.QLineEdit(self.groupBox_2)
        self.out_filename.setObjectName("out_filename")
        self.gridLayout.addWidget(self.out_filename, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.out_location = QtWidgets.QLineEdit(self.groupBox_2)
        self.out_location.setObjectName("out_location")
        self.gridLayout.addWidget(self.out_location, 1, 1, 1, 1)
        self.fp_outfile_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.fp_outfile_2.setObjectName("fp_outfile_2")
        self.gridLayout.addWidget(self.fp_outfile_2, 1, 2, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(45, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(45, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        self.viewStatus = QtWidgets.QPushButton(dia_run_analysis)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewStatus.sizePolicy().hasHeightForWidth())
        self.viewStatus.setSizePolicy(sizePolicy)
        self.viewStatus.setMinimumSize(QtCore.QSize(101, 25))
        self.viewStatus.setObjectName("viewStatus")
        self.gridLayout_2.addWidget(self.viewStatus, 2, 1, 1, 1)
        self.stopSim = QtWidgets.QPushButton(dia_run_analysis)
        self.stopSim.setMinimumSize(QtCore.QSize(291, 25))
        self.stopSim.setObjectName("stopSim")
        self.gridLayout_2.addWidget(self.stopSim, 1, 0, 1, 3)
        self.runSim_2 = QtWidgets.QPushButton(dia_run_analysis)
        self.runSim_2.setMinimumSize(QtCore.QSize(291, 25))
        self.runSim_2.setObjectName("runSim_2")
        self.gridLayout_2.addWidget(self.runSim_2, 0, 0, 1, 3)
        self.verticalLayout_3.addLayout(self.gridLayout_2)

        self.retranslateUi(dia_run_analysis)
        QtCore.QMetaObject.connectSlotsByName(dia_run_analysis)

    def retranslateUi(self, dia_run_analysis):
        dia_run_analysis.setWindowTitle(QtWidgets.QApplication.translate("dia_run_analysis", "Dialog", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("dia_run_analysis", "Solver Settings:", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("dia_run_analysis", "Actual Solver:", None, -1))
        self.use_wsl.setText(QtWidgets.QApplication.translate("dia_run_analysis", "use WSL", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("dia_run_analysis", "Output File:", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("dia_run_analysis", "Name", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("dia_run_analysis", "Path", None, -1))
        self.fp_outfile_2.setText(QtWidgets.QApplication.translate("dia_run_analysis", "Browse...", None, -1))
        self.viewStatus.setText(QtWidgets.QApplication.translate("dia_run_analysis", "View status", None, -1))
        self.stopSim.setText(QtWidgets.QApplication.translate("dia_run_analysis", "Stop Simulation", None, -1))
        self.runSim_2.setText(QtWidgets.QApplication.translate("dia_run_analysis", "Run Simulation", None, -1))

