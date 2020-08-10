import FreeCAD as App
import FreeCADGui as Gui

import os

import MBDyn_locator

from MBDynObjectsFactory import createSimulation
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')


class CommandAddSimulation:
    """Command to create a new simlation"""
    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'MBDyn_AddSim_cmd.svg'),
                'MenuText': "New Simulation",
                'ToolTip': "Add e new simulation to the model"}

    def IsActive(self):
        if App.ActiveDocument is None:
            return False
        elif hasattr(App.ActiveDocument, "MBDyn_Workbench"):
            return True
        else:
            return False

    def Activated(self):
        #Call the Gui to fill initial values and solver parameters
        createSimulation()

Gui.addCommand('CommandAddSimulation', CommandAddSimulation())
