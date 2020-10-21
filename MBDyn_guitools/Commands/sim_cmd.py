import os

import FreeCAD as App
import FreeCADGui as Gui

import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')

from MBDyn_guitools.External_Ui.sim_config import SimConfig
#from MBDyn_guitools.sim_config_test import SimConfig

class CommandAddSimulation:
    """Command to create a new simlation"""

    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'MBDyn_AddSim_cmd.svg'),
                'MenuText': "New Simulation",
                'ToolTip': "Add a new simulation to the model"}

    def IsActive(self):
        if App.ActiveDocument is None:
            return False
        elif hasattr(App.ActiveDocument, "MBDyn_Workbench"):
            return True
        else:
            return False

    def Activated(self):
        #Call the Gui to fill initial values and solver parameters
        self.ui = SimConfig() #mbdyn_configure2()
        self.ui.show() #exec_() exec lock the main gui


Gui.addCommand('CommandAddSimulation', CommandAddSimulation())
