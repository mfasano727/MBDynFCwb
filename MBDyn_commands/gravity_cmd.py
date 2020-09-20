import os

from PySide2 import QtCore, QtGui, QtWidgets

import FreeCAD as App
import FreeCADGui as Gui

import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')

from MBDyn_guitools.gravity_field import GravityField

class CommandAddGravity:
    """Command to create a new gravity field"""

    def GetResources(self):
        return {'Pixmap': "", #os.path.join(MBDwb_icons_path, 'MBDyn_AddSim_cmd.svg'),
                'MenuText': "Add Gravity",
                'ToolTip': "Add a gravity field to the model"}

    def IsActive(self):
        if App.ActiveDocument is None:
            return False
        elif hasattr(App.ActiveDocument, "MBDyn_Workbench"):
            return True
        else:
            return False

    def Activated(self):
        #Call the Gui
        gravObj = None
        if hasattr(App.ActiveDocument, "GravityField"):
            gravObj = getattr(App.ActiveDocument, "GravityField")
        self.ui = GravityField(gravObj)
        self.ui.show()


Gui.addCommand('CommandAddGravity', CommandAddGravity())
