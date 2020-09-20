
import os
import sys
from PySide2 import QtCore, QtGui, QtWidgets
import FreeCADGui as Gui
import FreeCAD as App
import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')
from MBDyn_utilities.MBDyn_funcs import *
from MBDyn_utilities.constants import *
from MBDyn_utilities.Settings_funcs import string_to_list

from MBDynObjectsFactory import createSimulation
from MBDyn_utilities.MBDyn_utils import select_directory

from MBDyn_guitools.dia_sim_config import Ui_dia_sim_config


class SimConfig(QtWidgets.QDialog):
    def __init__(self, simObj=None):
        """
        Ui interface for editing simulation parameters
        :param simObj: python feature representing the simulation
        """

        ui_file = "D:/Garnier/Documents/01_programmation/01_Python/mbdyn_FreeCAD/MBDynFCwb/resources/dia_sim_config.ui"
        a = Gui.PySideUic.loadUi(ui_file)
        self.ui = a

        self.mode = 0  # 0 means create new simulation, 1 means edit
        if simObj:
            self.simObj = simObj
            self.mode=1
        self.setupUi()

    def setupUi(self):

        #Connect
        QtCore.QObject.connect(self.ui.method, QtCore.SIGNAL("currentIndexChanged(int)"), self.ui.methods_stack.setCurrentIndex)
        QtCore.QObject.connect(self.ui.cbMaxIterations, QtCore.SIGNAL("clicked(bool)"), self.ui.leMaxIterations.setEnabled)
        QtCore.QObject.connect(self.ui.cbTol, QtCore.SIGNAL("clicked(bool)"), self.ui.leTol.setEnabled)
        QtCore.QObject.connect(self.ui.cbDerTol, QtCore.SIGNAL("clicked(bool)"), self.ui.leDerTol.setEnabled)
        QtCore.QObject.connect(self.ui.cbMethod, QtCore.SIGNAL("clicked(bool)"), self.ui.method.setEnabled)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QObject.connect(self.ui.bDefault, QtCore.SIGNAL("clicked()"), self.setDefault)
        QtCore.QObject.connect(self.ui.cbMethod, QtCore.SIGNAL("clicked(bool)"), self.ui.methods_stack.setEnabled)
        QtCore.QObject.connect(self.ui.cbAdHoc, QtCore.SIGNAL("clicked(bool)"), self.ui.thirdOrder_algebraic_radius.setDisabled)
        QtCore.QObject.connect(self.ui.bSelectWorkingDir, QtCore.SIGNAL("clicked()"), self.SetWorkingDirectory)

        self.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        if self.mode == 0:
            self.ui.setWindowTitle("Create Simulation")
            self.setDefault()
        else:
            self.ui.setWindowTitle("Edit Simulation")
            self.LoadSimParameters()

    def show(self):
        self.ui.show()

    def accept(self):
        print("Do My Things here")
        sim_parameter = self.getSimParameters()
        if self.mode == 0 :
            # creation of a new simulation
            createSimulation(App.ActiveDocument, sim_parameter)

        else:
            #edit the actual simulation
            self.simObj.Proxy.set_parameters(sim_parameter)

        self.done(1)
        #super(SimConfig, self).accept()

    def setDefault(self):
        self.ui.leInitialTime.setText(str(0))
        self.ui.leFinalTime.setText(str(5))
        self.ui.leTimeStep.setText(str(0.01))
        self.ui.leMaxIterations.setText("")
        self.ui.cbDerTol.setChecked(False)
        self.ui.leDerTol.setText("")
        self.ui.leTol.setText("")

        self.ui.cbOutput.setChecked(False)
        output_widget = self.ui.cbOutput.findChildren(QtWidgets.QCheckBox)
        for output in output_widget:
            output.setChecked(False)


    def getSimParameters(self):
        """
        Function which gather all parameters an return a dict
        :return: sim_parameters = {param1: value, param2: value}
        """
        sim_parameter = {}

        # Get General parameter: Sim Name, working directory,solver, (problem type)--------
        sim_parameter["general"] = {}
        sim_parameter["general"]["name"] = self.ui.leName.text()
        sim_parameter["general"]["working_dir"] = self.ui.leWorkingDir.text()

        # Get problem data--------
        sim_parameter["problem_data"] = {}
        if 0 < len(self.ui.leInitialTime.text()):
            sim_parameter["problem_data"]["initial_time"] = self.ui.leInitialTime.text()
        if 0 < len(self.ui.leFinalTime.text()):
            sim_parameter["problem_data"]["final_time"] = self.ui.leFinalTime.text()
        if 0 < len(self.ui.leTimeStep.text()):
            sim_parameter["problem_data"]["time_step"] = self.ui.leTimeStep.text()
        if self.ui.cbMaxIterations.isChecked and 0 < len(self.ui.leMaxIterations.text()):
            sim_parameter["problem_data"]["max_iterations"] = self.ui.leMaxIterations.text()
        if self.ui.cbTol.isChecked and 0 < len(self.ui.leTol.text()):
            sim_parameter["problem_data"]["tolerance"] = self.ui.leTol.text()
        if self.ui.cbDerTol.isChecked and 0 < len(self.ui.leDerTol.text()):
            sim_parameter["problem_data"]["derivatives_tolerance"] = self.ui.leDerTol.text()

        if self.ui.cbMethod.isChecked():
            sim_parameter["problem_data"]["method"] = self.ui.getMethod()

        if self.ui.cbOutput.isChecked():
            sim_parameter["problem_data"]["output"] = self.ui.getOutput()

        if self.ui.cbPbCustomParam.isChecked():
            sim_parameter["problem_data"]["custom_parameters"] = self.ui.ptePbCustomParam.toPlainText()

        # Get Control data--------
        sim_parameter["control_data"] = {}
        if self.ui.cbCtrlCustomParam.isChecked():
            sim_parameter["control_data"]["custom_parameters"] = self.ui.pteCtrlCustomParam.toPlainText()
        return sim_parameter

    def getOutput(self):
        """
        function to get the wanted output
        :return: list [str]
        """

        res = []
        for output in self.ui.cbOutput.findChildren(QtWidgets.QCheckBox):
            if output.isChecked():
                res.append(output.text())
        if 0 == len(res):
            res = None
        return res

    def getMethod(self):
        """
        function to get the parameter of the selected method
        :return: dic {"name": str, "params": []}
        """

        if 0 == self.ui.method.currentIndex():
            res = None
        else:
            res = {"name": self.ui.method.currentText().lower(), "params": []}

            if 2 == self.ui.method.currentIndex():
                # ms
                if 0 < len(self.ui.ms_algebraic_radius.text()):
                    res["params"].append(self.ui.ms_algebraic_radius.text())
                if 0 < len(self.ui.ms_differential_radius.text()):
                    res["params"].append(self.ui.ms_differential_radius.text())
            elif 3 == self.ui.method.currentIndex():
                # hope
                if 0 < len(self.ui.hope_algebraic_radius.text()):
                    res["params"].append(self.ui.hope_algebraic_radius.text())
                if 0 < len(self.hope_differential_radius.text()):
                    res["params"].append(self.ui.hope_differential_radius.text())
            elif 4 == self.ui.method.currentIndex():
                # thirdOrder
                if self.ui.cbAdHoc.isChecked():
                    res["params"].append("ad hoc")
                else:
                    if 0 < len(self.ui.thirdOrder_differential_radius.text()):
                        res["params"].append(self.ui.thirdOrder_differential_radius.text())
            elif 5 == self.ui.method.currentIndex():
                # bdf
                if 0 < len(self.ui.bdf_order.text()):
                    res["params"].append(self.ui.bdf_order.text())
        return res

    def LoadSimParameters(self):
        """
        retrieve all sim parameter from self.simObj
        and fill the dialog box
        :return:
        """
        # This is actually a hand process. Should be automated using an external file

        # set General parameter: Sim Name, working directory,solver, (problem type)--------
        self.ui.leSimName.setText(self.simObj.Label)
        self.ui.leWorkingDir.setText(self.simObj.WorkingDirectory)

        # Get problem data--------
        problem_data = self.simObj.Problem
        control_data = self.simObj.ControlData

        if None != problem_data.initial_time:
            self.ui.leInitialTime.setText(problem_data.initial_time)
        if None != problem_data.final_time:
            self.ui.leFinalTime.setText(problem_data.final_time)
        if None != problem_data.time_step:
            self.ui.leTimeStep.setText(problem_data.time_step)
        if None != problem_data.max_iterations:
            self.ui.leMaxIterations.setText(problem_data.max_iterations)
        if None != problem_data.derivatives_tolerance:
            self.ui.cbDerTol.setChecked(True)
            self.ui.leDerTol.setText(problem_data.derivatives_tolerance)
        if None != problem_data.tolerance:
            self.ui.leTol.setText(problem_data.tolerance)

        if None != problem_data.output and 0 < len(problem_data.output):
            self.ui.cbOutput.setChecked(True)
            output_widget = self.ui.cbOutput.findChildren(QtWidgets.QCheckBox)
            for output in output_widget:
                if output.text() in problem_data.output:
                    output.setChecked(True)


        if None != problem_data.custom_parameters:
            self.ui.cbPbCustomParam.setChecked(True)
            self.ui.ptePbCustomParam.setPlainText(problem_data.custom_parameters)

        if None != control_data.custom_parameters:
            self.ui.cbCtrlCustomParam.setChecked(True)
            self.ui.pteCtrlCustomParam.setPlainText(control_data.custom_parameters)

    def SetWorkingDirectory(self):
        outlocation = select_directory()
        self.ui.leWorkingDir.setText(outlocation)
