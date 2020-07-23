#!/usr/bin/env python3
# coding: utf-8
#
# revpin_joint_cmd.py

import os
import sys
import platform
import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')
from MBDyn_utilities.Settings_funcs import string_to_list, list_to_string

from PySide2 import QtCore, QtGui, QtWidgets
import FreeCAD as App

from MBDyn_guitools.wb_settings_widgets.ui_solver_settings import Ui_solver_settings
from MBDyn_utilities.constants import *


class wdgt_solver_settings(QtWidgets.QWidget, Ui_solver_settings):
    """MBD Workbench settings command"""
    def __init__(self):
        super(wdgt_solver_settings, self).__init__()
        self.setupUi()
        self.binaries_list = []
        self.default_solver = ""
        self.binaries = []

    def setupUi(self):
        super(wdgt_solver_settings, self).setupUi(self)

        pixmap = QtGui.QPixmap(os.path.join(MBDwb_icons_path,"plus.svg"))
        btnIcon = QtGui.QIcon(pixmap)
        self.addBinaryPathButton.setIcon(btnIcon)
        self.addBinaryPathButton.setIconSize(QtCore.QSize(18,18))

        pixmap = QtGui.QPixmap(os.path.join(MBDwb_icons_path,"cross.svg"))
        btnIcon = QtGui.QIcon(pixmap)
        self.rmvBinaryPathButton.setIcon(btnIcon)
        self.rmvBinaryPathButton.setIconSize(QtCore.QSize(18,18))

        # rmv and add Buttons are disable at the begining
        self.addBinaryPathButton.setEnabled(False)
        self.rmvBinaryPathButton.setEnabled(False)
        
        # define conections for dialog widgets
        self.defaultSolverComboBox.activated.connect(self.setDefaultSolver)
        self.mbdynBinariesPath.cellDoubleClicked.connect(self.editActivePath)
        self.addBinaryPathButton.clicked.connect(self.addBinaryPath)
        self.selectBinaryPathButton.clicked.connect(self.selectBinaryPath)
        self.rmvBinaryPathButton.clicked.connect(self.rmvBinaryPath)
        self.activeBinaryName.editingFinished.connect(self.checkActiveBinary)
        self.activeBinaryPath.editingFinished.connect(self.checkActiveBinary)

    def saveSettings(self):
        """Save solver settings"""
        App.Console.PrintMessage("Saving MBDyn Solver settings...")

        # Add default solver
        if not self.default_solver:
            mb = QtWidgets.QMessageBox()
            mb.setIcon(mb.Icon.Warning)
            mb.setText("No default solver selected!")
            mb.setWindowTitle("Warning")
            mb.exec_()
        App.ParamGet(SOLVERS_USER_SETTINGS).SetString("DEFAULT_SOLVER", self.default_solver)

        # Remove old binaries        
        binaries_list = string_to_list(App.ParamGet(SOLVERS_USER_SETTINGS).GetString("BINARIES_LIST",""), SEP)
        for binary_name in binaries_list:
            if binary_name not in self.binaries_list:
                App.ParamGet(SOLVERS_USER_SETTINGS).RemString(binary_name)

        # Add binary names + path
        for index, binary_name in enumerate(self.binaries_list):
            binary_path = self.binaries[index]
            App.ParamGet(SOLVERS_USER_SETTINGS).SetString(binary_name, binary_path)

        # Save binaries name list
        App.ParamGet(SOLVERS_USER_SETTINGS).SetString("BINARIES_LIST", list_to_string(self.binaries_list,SEP))

        # save WSL cmd
        App.ParamGet(SOLVERS_USER_SETTINGS).SetBool("USE_WSL", self.useWSL.isChecked())
        
        App.Console.PrintMessage("... MBDyn Solver settings saved." + "\n")

    def loadSettings(self):
        """Load solver settings"""
        App.Console.PrintMessage("Loading MBDyn Solver settings...")
        #get Actual settings
        self.getSolverSettings()
        self.useWSL.setChecked(App.ParamGet(SOLVERS_USER_SETTINGS).GetBool("USE_WSL", False))
        self.updateView()

        App.Console.PrintMessage("... MBDyn Solver settings loaded." + "\n")

    def getSolverSettings(self):
        self.default_solver = App.ParamGet(SOLVERS_USER_SETTINGS).GetString("DEFAULT_SOLVER","")
        self.binaries_list = string_to_list(App.ParamGet(SOLVERS_USER_SETTINGS).GetString("BINARIES_LIST",""), SEP)

        for binary_name in self.binaries_list:
            self.binaries.append(App.ParamGet(SOLVERS_USER_SETTINGS).GetString(binary_name,""))

    def updateView(self):
        # Fill combobox Data
        self.defaultSolverComboBox.clear()
        self.defaultSolverComboBox.addItem("--Select--")
        self.defaultSolverComboBox.addItems(self.binaries_list)
        #set default item
        if self.default_solver in self.binaries_list:
            self.defaultSolverComboBox.setCurrentIndex(self.binaries_list.index(self.default_solver) + 1)
        else:
            self.defaultSolverComboBox.selectedIndex = 0

        # Fill Table Data
        self.mbdynBinariesPath.clearContents()
        self.mbdynBinariesPath.setRowCount(0)
        self.mbdynBinariesPath.setColumnCount(2)
        for i, binary_name in enumerate(self.binaries_list):
            rowPosition = self.mbdynBinariesPath.rowCount()
            self.mbdynBinariesPath.insertRow(rowPosition)
            self.mbdynBinariesPath.setItem(rowPosition,0,
                                           QtWidgets.QTableWidgetItem(binary_name))  # Add name
            self.mbdynBinariesPath.setItem(rowPosition,1,
                                           QtWidgets.QTableWidgetItem(self.binaries[i]))  # Add Path

    def setDefaultSolver(self, row):
        App.Console.PrintMessage("SetDefaultSolver" + "\n")
        binary_name = self.defaultSolverComboBox.currentText()
        if not binary_name == "--Select--": 
            self.default_solver = binary_name
        else:
            self.defaultSolverComboBox.setCurrentIndex(self.binaries_list.index(self.default_solver) + 1)

    def editActivePath(self):
        App.Console.PrintMessage("EditActivePath" + "\n")
        row = self.mbdynBinariesPath.currentRow()
        self.activeBinaryName.setText(self.mbdynBinariesPath.item(row, 0).text())
        self.activeBinaryPath.setText(self.mbdynBinariesPath.item(row, 1).text())
        self.activeBinaryName.editingFinished.emit()

    def selectBinaryPath(self):
        App.Console.PrintMessage("Select BinaryPath" + "\n")
        
        #setting default directory
        starting_directory = ""
        if platform.system() == 'Windows':
            starting_directory = os.environ['LOCALAPPDATA']
        else: #linux and Mac
            starting_directory = "/home"

        mbdyn_binary_path = QtWidgets.QFileDialog.getOpenFileName(self,"get MBDyn binary file", dir=starting_directory)[0]
        App.Console.PrintMessage("was" + mbdyn_binary_path)
        self.activeBinaryPath.setText(mbdyn_binary_path)
        self.activeBinaryPath.editingFinished.emit()

    def rmvBinaryPath(self):
        App.Console.PrintMessage("Remove BinaryPath" + "\n")
        binary_name = self.activeBinaryName.text()
        index = self.binaries_list.index(binary_name)

        self.binaries_list.pop(index)
        self.binaries.pop(index)

        if self.default_solver == binary_name:
            self.default_solver = ""
            self.defaultSolverComboBox.selectedIndex = 0

        self.updateView()
        self.checkActiveBinary()

    def addBinaryPath(self):
        App.Console.PrintMessage("Add BinaryPath" + "\n")
        binary_name = self.activeBinaryName.text()
        bynary_path = self.activeBinaryPath.text().replace("\\", "/")

        if not binary_name in self.binaries_list:
            self.binaries_list.append(binary_name)
            self.binaries.append(bynary_path)
        else:
            index = self.binaries_list.index(binary_name)
            self.binaries[index] = bynary_path
        self.updateView()

    def checkActiveBinary(self):
        App.Console.PrintMessage("Check BinaryPath" + "\n")
        self.addBinaryPathButton.setEnabled(False)
        self.rmvBinaryPathButton.setEnabled(False)
        if self.activeBinaryName.text():
            if os.path.isfile(self.activeBinaryPath.text()):
                self.addBinaryPathButton.setEnabled(True)
        if self.activeBinaryName.text() in self.binaries_list:
            self.rmvBinaryPathButton.setEnabled(True)
        
        
