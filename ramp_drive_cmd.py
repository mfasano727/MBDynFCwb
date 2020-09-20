#!/usr/bin/env python3
# coding: utf-8
#
# ref_cmd.py

import os
import sys
import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')
import MBDyn_objects.model_so
from PySide2 import QtCore, QtGui, QtWidgets
import FreeCAD as App
import FreeCADGui as Gui



from   MBDyn_guitools.dia_ramp_drive import Ui_dia_ramp_drive

class ramp_drive_cmd(QtWidgets.QDialog, Ui_dia_ramp_drive):
    """MBD create ramp drive caller command"""
    def __init__(self):
        super(ramp_drive_cmd, self).__init__()
        self.setupUi(self)

    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'rampdriveIcon.svg'),
                'MenuText': "create ramp drive caller command",
                'ToolTip': "input ramp drive caller parameters"}
    def Activated(self):
        """Do something here"""
        self.slope.setText(1.0)
        self.initial_time.setText(1.0)
        self.final_time.setText(2.0)
        self.initial_value.setText(0.0)

        self.show()

        App.Console.PrintMessage(" Activated: " + "\n")

        return

    def IsActive(self):
        if App.ActiveDocument == None:
            return False
        else:
            return True


    def accept(self):
        num_drives = len(App.ActiveDocument.Drive_callers.getSubObjects()) + 1
        new_ramp =App.ActiveDocument.Drive_callers.newObject("App::FeaturePython","ramp" + str(num_drives))
        MBDyn_objects.model_so.MBDynRampDrive(new_ramp)
        new_ramp.ViewObject.Proxy = 0

        new_ramp.slope = float(self.slope.text())
        new_ramp.initial_time = float(self.initial_time.text())
        new_ramp.final_time = float(self.final_time.text())
        new_ramp.initial_value = float(self.initial_value.text())

        self.done(1)

    def reject(self):
        self.done(0)


    def check_valid(self):
         pass
#        teststr = self.sender()
#        if self.valid.validate(teststr.text(),0) != QtGui.QValidator.Acceptable:
#           self.sender.setText("0.0")

Gui.addCommand('ramp_drive_cmd', ramp_drive_cmd())
