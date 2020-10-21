import os

from PySide2 import QtWidgets

import FreeCAD as App
import FreeCADGui as Gui

import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')
from MBDyn_guitools.External_Ui.MBDynFreeCAD import mbdyn_launchGui

from MBDyn_utilities.MBDyn_utils import get_active_simulation

class mbdyn_launch_cmd:
    def GetResources(self):
        tooltip = """Open the launcher.
        One analysis must be active."""
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'WrtMBDynIcon.svg'),
                'MenuText': "MBD launcher",
                'ToolTip': tooltip}

    def IsActive(self):
        active_document = App.activeDocument()
        active_sim = get_active_simulation(active_document)
        if active_sim is not None:
            return True
        return False

    def Activated(self):
        """Do something here"""
        #        App.Console.PrintMessage( Gui.activeWorkbench().iv.initial_time)
        active_document = App.activeDocument()
        # The Global import can fail !
        # if the gui is defined in the same file there is no need to add it here!
        #from MBDyn_guitools.MBDynFreeCAD import mbdyn_launchGui
        self.ui = mbdyn_launchGui() # put the ui in a self.xx variable allow to keep track of it after the end of the function

        # Check if the document is saved
        if not active_document.FileName:
            mb = QtWidgets.QMessageBox()
            mb.setIcon(mb.Icon.Warning)
            mb.setText("Please save the model before continue")
            mb.setWindowTitle("Warning")
            mb.exec_()
            return

        self.ui.getWorkbenchSettings()
        if not self.ui.default_solver:
            mb = QtWidgets.QMessageBox()
            mb.setIcon(mb.Icon.Warning)
            mb.setText("""
No default solver selected!
Please update preferences:
    Edit
        - Preferences...
            - MBDyn""")
            mb.setWindowTitle("Warning")
            mb.exec_()
        else:
            self.ui.updateView()
            self.ui.show()


Gui.addCommand('mbdyn_launchGui', mbdyn_launch_cmd())