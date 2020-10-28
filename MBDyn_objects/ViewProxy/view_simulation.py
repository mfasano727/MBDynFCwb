import FreeCAD as App
from six import string_types
import os

from PySide2 import QtCore, QtWidgets

import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')

from MBDyn_objects.ViewProxy.view_base_container import ViewProviderBaseContainer

from MBDyn_guitools.External_Ui.sim_config import SimConfig
from MBDyn_guitools.External_Ui.MBDynFreeCAD import mbdyn_launchGui

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
        # Return true to tell freecad we handled the doubleClicked function
        return True

    def setActive(self):
        doc = self.ViewObject.Object.Document
        print(doc)
        print(App.ActiveDocument)
        doc.MBDyn_Workbench.Proxy.setActiveSimulation(self.Object)
        self.ViewObject.signalChangeIcon()
        doc.recompute()

    def edit(self):
        self.ui = SimConfig(self.Object)
        self.ui.show()
        self.ViewObject.Object.Document.recompute()

    def analyze(self):
        self.setActive()
        active_document = App.activeDocument()
        self.ui = mbdyn_launchGui()  # put the ui in a self.xx variable allow to keep track of it after the end of
        # the function

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

    def setupContextMenu(self,vobj,menu):
        # Activate Action
        actionActivate = QtWidgets.QAction("Activate", menu)
        QtCore.QObject.connect(actionActivate,
                               QtCore.SIGNAL("triggered()"),
                               self.setActive)
        # Edit action
        actionEdit = QtWidgets.QAction("Edit..", menu)
        QtCore.QObject.connect(actionEdit,
                               QtCore.SIGNAL("triggered()"),
                               self.edit)
        #Analyze Action
        actionAnalyze = QtWidgets.QAction("Analyze", menu)
        QtCore.QObject.connect(actionAnalyze,
                               QtCore.SIGNAL("triggered()"),
                               self.analyze)
        menu.addAction(actionActivate)
        menu.addAction(actionEdit)
        menu.addAction(actionAnalyze)

