import FreeCAD as App
import FreeCADGui as Gui

import os

import MBDyn_locator

from MBDyn_objects.MBDynObjectFactory.LayoutCreation import createTree

MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')


class CommandTreeLayout:
    """Layout creation, Should only be use once per document"""
    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'MBDyn_Tree_cmd.svg'),
                'MenuText': "Create Tree Layout",

                'ToolTip': "Create the MBDyn tree Layout"}

    def IsActive(self):
        # Has the Custom toolbar is not composed of "command object" the IsActive mthedo have to be triggered manually
        if hasattr(Gui,"mbdynAnimationToolBar"):
            Gui.mbdynAnimationToolBar.IsActive()

        if App.ActiveDocument is None:
            return False
        elif hasattr(App.ActiveDocument, "MBDyn_Workbench"):
             return False
        else:
            return True

    def Activated(self):
        createTree()

Gui.addCommand('CommandTreeLayout', CommandTreeLayout())