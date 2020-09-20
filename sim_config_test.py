import os
import sys
from PySide2 import QtCore, QtGui, QtWidgets


import FreeCADGui as Gui
import FreeCAD as App
import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')

from MBDyn_utilities.constants import *



from MBDyn_guitools.dia_sim_config_skeleton import Ui_dia_sim_config
from .sim_parameter_widgets.ui_sim_param_string import Ui_dia_sim_param_string
from .sim_parameter_widgets.ui_sim_param_integration_method import Ui_dia_sim_param_integration_method


SIMULATION_PARAMETERS = {"Problem":[], "ControlData":[]}
SIMULATION_PARAMETERS["Problem"].append({"label": "InitialTime", "MBDynsyntax": "initial time", "desc": "Initial time for simulation",
                                         "default": 0.0, "Active": True, "Type": "String"})
SIMULATION_PARAMETERS["Problem"].append({"label": "FinalTime", "MBDynsyntax": "final time", "desc": "Final time for simulation",
                                         "default": 0.0, "Active": True, "Type": "String"})
SIMULATION_PARAMETERS["Problem"].append({"label": "TimeStep", "MBDynsyntax": "time step", "desc": "time step for simulation",
                                         "default": 0.0, "Active": True, "Type": "String"})

SIMULATION_PARAMETERS["Problem"].append({"label": "MaxIterations", "MBDynsyntax": "Max Iteration", "desc":"max_iterations for simulation",
                                         "default": 0.0, "Active": True, "Type": "String"})
SIMULATION_PARAMETERS["Problem"].append({"label": "Tolerance", "MBDynsyntax": "Tolerance", "desc":"Tolerance for simulation",
                                         "default": 0.0, "Active": True, "Type": "String"})
SIMULATION_PARAMETERS["Problem"].append({"label": "DerivativesTolerance", "MBDynsyntax": "Der. Tolerance", "desc": "derivatives_tolerance for simulation",
                                         "default": 0.0, "Active": False, "Type": "String"})

PROBLEM_OUTPUT = [("none", False, False), ("iterations", False, False), ("residual", False, False),
                  ("solution", False, False), ("jacobian matrix", False, False), ("messages", False, False),
                  ("counter", False, False), ("bailout", False, False), ("matrix condition number", False, False),
                  ("solver condition number", False, False),("cpu time", False, False)]


# FIND a WAY TO ADD Integration method and complex parameters !
#obj.addProperty("App::PropertyFloat", "DifferentialRadius", "IntegrationMethod",
#                "differential_radius for method of integration").DifferentialRadius
#obj.addProperty("App::PropertyFloat", "AlgebraicRadius", "IntegrationMethod",
#                "algebraic_radius for method of integration").AlgebraicRadius
#obj.addProperty("App::PropertyInteger", "Order", "IntegrationMethod", "order for method of integration").Order
#obj.addProperty("App::PropertyString", "Imethod", "IntegrationMethod", "method of integration").Imethod

INTEGRATION_METHOD = {}

class SimConfig(QtWidgets.QDialog,  Ui_dia_sim_config):
    def __init__(self, simObj=None):
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
            self.createUi()
        else:
            self.setWindowTitle("Edit Simulation")

    def setDefault(self):
        pass

    def accept(self):
        print("Do My Things here")


    def createUi(self):
        """Create the UI layout base on the SIMULATION_PARAMETERS dict
        """
        # Load Problem tab
        for param in SIMULATION_PARAMETERS["Problem"]:
            self.t = create_parameter_widget(param)
            self.t = SimParamString(param, self.ProblemTab, self.ProblemTabLayout)
        SimParamIntegrationMethod(param, self.ProblemTab, self.ProblemTabLayout)
        # Load ControlData tab
        for param in SIMULATION_PARAMETERS["ControlData"]:
            self.t = SimParamString(param, self.ControlDataTab, self.ControlDataTabLayout)


    def loadUi(self):
        """Create the UI layout base on the SIMULATION_PARAMETERS dict
        and the parameter already present in the existing sim
        """


## Classes for all widgets specific to the simulation parameters
#def create_parameter_widget(param, simObj=None):
#    if simObj:
#        #if the simObj is not None, get its parameters
#
#    else:
#


class SimParamString(QtWidgets.QWidget, Ui_dia_sim_param_string):
    def __init__(self, parameter, parent, layout):
        super(SimParamString, self).__init__(parent)
        self.setupUi(parameter)

        layout.addRow(self.cbParameterStatus, self.leParameterText)

        QtCore.QObject.connect(self.cbParameterStatus, QtCore.SIGNAL("clicked(bool)"), self.leParameterText.setEnabled)

    def setupUi(self, parameter):
        super(SimParamString, self).setupUi(self)
        self.cbParameterStatus.setText(parameter["MBDynsyntax"])

        if parameter["Active"] == True:
            self.leParameterText.setText(str(parameter["default"]))
        else:
            self.cbParameterStatus.setChecked(False)
            self.leParameterText.setEnabled(False)

    def getParameter(self):
        if self.cbParameterStatus.isChecked():
            return True, self.leParameterText.getText()
        else:
            return False, ""


class SimParamIntegrationMethod(QtWidgets.QWidget, Ui_dia_sim_param_integration_method):
    def __init__(self, parameter, parent, layout):
        super(SimParamIntegrationMethod, self).__init__(parent)
        self.setupUi(parameter)
        print("hello from here")

        layout.addRow(self.groupBox_2)


    def setupUi(self, parameter):
        super(SimParamIntegrationMethod, self).setupUi(self)

