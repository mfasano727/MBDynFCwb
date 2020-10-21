
import os
from PySide2 import QtCore, QtWidgets
import FreeCAD as App
import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')

from MBDyn_objects.MBDynObjectFactory.SimulationCreation import createSimulation
from MBDyn_utilities.MBDyn_utils import select_directory

from MBDyn_guitools.External_Ui.dia_sim_config import Ui_dia_sim_config


class SimConfig(QtWidgets.QDialog,  Ui_dia_sim_config):
    def __init__(self, simObj=None):
        """
        Ui interface for editing simulation parameters
        :param simObj: python feature representing the simulation
        """
        super(SimConfig, self).__init__()
        self.mode = 0  # 0 means create new simulation, 1 means edit
        if simObj:
            self.simObj = simObj
            self.mode=1
        self.setupUi()

    def setupUi(self):
        super(SimConfig, self).setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        if self.mode == 0:
            self.setWindowTitle("Create Simulation")
            self.setDefault()
        else:
            self.setWindowTitle("Edit Simulation")
            self.LoadSimParameters()

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
        self.leInitialTime.setText(str(0))
        self.leFinalTime.setText(str(5))
        self.leTimeStep.setText(str(0.01))
        self.leMaxIterations.setText("")
        self.cbDerTol.setChecked(False)
        self.leDerTol.setText("")
        self.leTol.setText("")

        self.cbOutput.setChecked(False)
        output_widget = self.cbOutput.findChildren(QtWidgets.QCheckBox)
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
        sim_parameter["general"]["name"] = self.leSimName.text()
        sim_parameter["general"]["working_dir"] = self.leWorkingDir.text()

        # Get problem data--------
        sim_parameter["problem_data"] = {}
        if 0 < len(self.leInitialTime.text()):
            sim_parameter["problem_data"]["initial_time"] = self.leInitialTime.text()
        if 0 < len(self.leFinalTime.text()):
            sim_parameter["problem_data"]["final_time"] = self.leFinalTime.text()
        if 0 < len(self.leTimeStep.text()):
            sim_parameter["problem_data"]["time_step"] = self.leTimeStep.text()
        if self.cbMaxIterations.isChecked and 0 < len(self.leMaxIterations.text()):
            sim_parameter["problem_data"]["max_iterations"] = self.leMaxIterations.text()
        if self.cbTol.isChecked and 0 < len(self.leTol.text()):
            sim_parameter["problem_data"]["tolerance"] = self.leTol.text()
        if self.cbDerTol.isChecked and 0 < len(self.leDerTol.text()):
            sim_parameter["problem_data"]["derivatives_tolerance"] = self.leDerTol.text()

        if self.cbMethod.isChecked():
            sim_parameter["problem_data"]["method"] = self.getMethod()

        if self.cbOutput.isChecked():
            sim_parameter["problem_data"]["output"] = self.getOutput()

        if self.cbPbCustomParam.isChecked():
            sim_parameter["problem_data"]["custom_parameters"] = self.ptePbCustomParam.toPlainText()

        # Get Control data--------
        sim_parameter["control_data"] = {}
        if self.cbCtrlCustomParam.isChecked():
            sim_parameter["control_data"]["custom_parameters"] = self.pteCtrlCustomParam.toPlainText()
        return sim_parameter

    def getOutput(self):
        """
        function to get the wanted output
        :return: list [str]
        """

        res = []
        for output in self.cbOutput.findChildren(QtWidgets.QCheckBox):
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

        if 0 == self.method.currentIndex():
            res = None
        else:
            res = {"name": self.method.currentText().lower(), "params": []}

            if 2 == self.method.currentIndex():
                # ms
                if 0 < len(self.ms_algebraic_radius.text()):
                    res["params"].append(self.ms_algebraic_radius.text())
                if 0 < len(self.ms_differential_radius.text()):
                    res["params"].append(self.ms_differential_radius.text())
            elif 3 == self.method.currentIndex():
                # hope
                if 0 < len(self.hope_algebraic_radius.text()):
                    res["params"].append(self.hope_algebraic_radius.text())
                if 0 < len(self.hope_differential_radius.text()):
                    res["params"].append(self.hope_differential_radius.text())
            elif 4 == self.method.currentIndex():
                # thirdOrder
                if self.cbAdHoc.isChecked():
                    res["params"].append("ad hoc")
                else:
                    if 0 < len(self.thirdOrder_differential_radius.text()):
                        res["params"].append(self.thirdOrder_differential_radius.text())
            elif 5 == self.method.currentIndex():
                # bdf
                if 0 < len(self.bdf_order.text()):
                    res["params"].append(self.bdf_order.text())
        return res

    def LoadSimParameters(self):
        """
        retrieve all sim parameter from self.simObj
        and fill the dialog box
        :return:
        """
        # This is actually a hand process. Should be automated using an external file

        # set General parameter: Sim Name, working directory,solver, (problem type)--------
        self.leSimName.setText(self.simObj.Label)
        self.leWorkingDir.setText(self.simObj.WorkingDirectory)

        # Get problem data--------
        problem_data = self.simObj.Problem
        control_data = self.simObj.ControlData

        if None != problem_data.initial_time:
            self.leInitialTime.setText(problem_data.initial_time)
        if None != problem_data.final_time:
            self.leFinalTime.setText(problem_data.final_time)
        if None != problem_data.time_step:
            self.leTimeStep.setText(problem_data.time_step)
        if None != problem_data.max_iterations:
            self.leMaxIterations.setText(problem_data.max_iterations)
        if None != problem_data.derivatives_tolerance:
            self.cbDerTol.setChecked(True)
            self.leDerTol.setText(problem_data.derivatives_tolerance)
        if None != problem_data.tolerance:
            self.leTol.setText(problem_data.tolerance)

        if None != problem_data.output and 0 < len(problem_data.output):
            self.cbOutput.setChecked(True)
            output_widget = self.cbOutput.findChildren(QtWidgets.QCheckBox)
            for output in output_widget:
                if output.text() in problem_data.output:
                    output.setChecked(True)


        if None != problem_data.custom_parameters:
            self.cbPbCustomParam.setChecked(True)
            self.ptePbCustomParam.setPlainText(problem_data.custom_parameters)

        if None != control_data.custom_parameters:
            self.cbCtrlCustomParam.setChecked(True)
            self.pteCtrlCustomParam.setPlainText(control_data.custom_parameters)

    def SetWorkingDirectory(self):
        outlocation = select_directory()
        self.leWorkingDir.setText(outlocation)
