import FreeCAD as App
import FreeCADGui as Gui
from six import string_types
import os

from PySide2 import QtCore, QtWidgets

import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')

from MBDyn_viewproviders.view_base_container import ViewProviderBaseContainer


class ViewProviderSimulation(ViewProviderBaseContainer):
    def __init__(self, vobj):
        super(ViewProviderSimulation,self).__init__(vobj)

    def getIcon(self):
        # https://forum.freecadweb.org/viewtopic.php?f=18&t=44009
        if not hasattr(self.Object, "Proxy"):
            App.Console.PrintMessage("{}, has no Proxy.\n".format(self.Object.Name))
            return ""
        if not hasattr(self.Object.Proxy, "Type"):
            App.Console.PrintMessage(
                "{}: Proxy does has not have attribte Type.\n"
                .format(self.Object.Name)
            )
            return ""
        if (
            isinstance(self.Object.Proxy.Type, string_types)
            and self.Object.Proxy.Type.startswith("MBDyn::")
        ):
            if not App.ActiveDocument.MBDyn_Workbench.Proxy.getActiveSimulation() == self.Object:
                icon_path = "{}/{}.svg".format(MBDwb_icons_path, self.Object.Proxy.Type.replace("MBDyn::", "MBDyn_"))
                App.Console.PrintLog("{} --> {}\n".format(self.Object.Name, icon_path))
            else:
                icon_path = "{}/{}Active.svg".format(MBDwb_icons_path, self.Object.Proxy.Type.replace("MBDyn::", "MBDyn_"))
                App.Console.PrintLog("{} --> {}\n".format(self.Object.Name, icon_path))

            return icon_path

        else:
            App.Console.PrintError("No icon returned for {}\n".format(self.Object.Name))
            App.Console.PrintMessage("{}\n".format(self.Object.Proxy.Type))
            return ""

    def doubleClicked(self, vobj):
        self.setActive()
        # Do nothing to avoid renaming of the container
        return True

    def setActive(self):
        App.ActiveDocument.MBDyn_Workbench.Proxy.setActiveSimulation(self.Object)
        self.ViewObject.signalChangeIcon()

    def setupContextMenu(self,vobj,menu):
        # Activate Action
        action1 = QtWidgets.QAction("Activate", menu)
        QtCore.QObject.connect(action1,
                               QtCore.SIGNAL("triggered()"),
                               self.setActive)
        # Edit action
        action2 = QtWidgets.QAction("Edit..", menu)
        QtCore.QObject.connect(action2,
                               QtCore.SIGNAL("triggered()"),
                               self.setActive)
        #Analyze Action
        action3 = QtWidgets.QAction("Analyze", menu)
        QtCore.QObject.connect(action3,
                               QtCore.SIGNAL("triggered()"),
                               self.setActive)
        menu.addAction(action1)
        menu.addAction(action2)
        menu.addAction(action3)

