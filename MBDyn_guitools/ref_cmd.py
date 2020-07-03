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



from   MBDyn_guitools.dia_ref import Ui_ref_dialog

class ref_cmd(QtWidgets.QDialog, Ui_ref_dialog):
    """MBD create reference command"""
    def __init__(self):
        super(ref_cmd, self).__init__()
        self.setupUi(self)

    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'reference.svg'),
                'MenuText': "create reference command",
                'ToolTip': "input reference parameters"}
    def Activated(self):
        """Do something here"""
        self.parent_ref_box.clear()
        self.parent_ref_box.addItem("none")
        if App.ActiveDocument.getObjectsByLabel('References') != None :
            for refobj in App.ActiveDocument.References.Group:
                self.parent_ref_box.addItem(refobj.ref_name)

        self.pos_x.setText("0") ; self.pos_y.setText("0") ; self.pos_z.setText("0")
        self.vect1_x.setText("1") ; self.vect1_y.setText("0") ; self.vect1_z.setText("0")
        self.vect2_x.setText("0") ; self.vect2_y.setText("1") ; self.vect2_z.setText("0")
        self.vect3_x.setText("0") ; self.vect3_y.setText("0") ; self.vect3_z.setText("1")
        self.vel_x.setText("0") ; self.vel_y.setText("0") ; self.vel_z.setText("0")
        self.ang_vel_x.setText("0") ; self.ang_vel_y.setText("0") ; self.ang_vel_z.setText("0")

        self.OM_type.currentIndexChanged.connect(self.set_OM_type)
        self.OM_type.setCurrentIndex(1)
        self.OM_type.setCurrentIndex(0)
#        self.valid = QtGui.QDoubleValidator()
#        self.pos_x.setValidator(self.valid)
#        self.pos_x.textEdited.connect(self.check_valid())
#        self.pos_x.textEdited.emit(self.pos_x.text())
        self.show()

        App.Console.PrintMessage(" Activated: " + "\n")

        return

    def IsActive(self):
        if App.ActiveDocument == None:
            return False
        else:
            return True


    def accept(self):
        index = self.OM_type.currentIndex()
        App.Console.PrintMessage(" property1: " +self.OM_type.itemText(index) + "\n")
#        testgroup  = App.ActiveDocument.getObjectsByLabel('references')
#        new_ref = App.ActiveDocument.addObject("App::FeaturePython","reference2")
        new_ref =App.ActiveDocument.References.newObject("App::FeaturePython","reference" + str(self.parent_ref_box.count()))
        MBDyn_objects.model_so.MBDynReference(new_ref)
        new_ref.ViewObject.Proxy = 0

        new_ref.ref_label = self.parent_ref_box.count()
        new_ref.ref_name = "reference" + str(self.parent_ref_box.count())
        # set the reference to be refered to
        if self.parent_ref_box.currentIndex() == 0:
            new_ref.refered_label = 0
        else:
            for refobj in App.ActiveDocument.References.Group:
                if refobj.ref_name  == self.parent_ref_box.currentText():
                    new_ref.refered_label = refobj.ref_label
        new_ref.position = App.Vector(float(self.pos_x.text()), float(self.pos_y.text()), float(self.pos_z.text()))
        new_ref.orientation = [App.Vector(float(self.vect1_x.text()), float(self.vect1_y.text()), float(self.vect1_z.text())),
                               App.Vector(float(self.vect2_x.text()), float(self.vect2_y.text()), float(self.vect2_z.text())),
                               App.Vector(float(self.vect3_x.text()), float(self.vect3_y.text()), float(self.vect3_z.text()))]
        new_ref.orientation_des = self.OM_type.currentText()
        new_ref.vel = App.Vector(float(self.vel_x.text()), float(self.vel_y.text()), float(self.vel_z.text()))
        new_ref.ang_vel = App.Vector(float(self.ang_vel_x.text()), float(self.ang_vel_y.text()), float(self.ang_vel_z.text()))

        self.done(1)

    def reject(self):
        self.done(0)


    def set_OM_type(self):
        index = self.OM_type.currentIndex()
        App.Console.PrintMessage(" property: " +self.OM_type.itemText(index) + "\n")
        if self.OM_type.currentIndex() == 0:  #xy selected  only vectors 1 and 2 are visible
            self.vect1_x.setVisible(True);  self.vect1_y.setVisible(True);  self.vect1_z.setVisible(True)
            self.vect2_x.setVisible(True);  self.vect2_y.setVisible(True);  self.vect2_z.setVisible(True)
            self.vect3_x.setVisible(False); self.vect3_y.setVisible(False); self.vect3_z.setVisible(False)
        elif self.OM_type.currentIndex() == 1:  #xz selected  only vectors 1 and 3 are visible
            self.vect1_x.setVisible(True);  self.vect1_y.setVisible(True);  self.vect1_z.setVisible(True)
            self.vect2_x.setVisible(False); self.vect2_y.setVisible(False); self.vect2_z.setVisible(False)
            self.vect3_x.setVisible(True);  self.vect3_y.setVisible(True);  self.vect3_z.setVisible(True)
        elif self.OM_type.currentIndex() == 2:  #yz selected  only vectors 2 and 3 are visible
            self.vect1_x.setVisible(False); self.vect1_y.setVisible(False); self.vect1_z.setVisible(False)
            self.vect2_x.setVisible(True);  self.vect2_y.setVisible(True);  self.vect2_z.setVisible(True)
            self.vect3_x.setVisible(True);  self.vect3_y.setVisible(True);  self.vect3_z.setVisible(True)
        elif self.OM_type.currentIndex() == 3:  #matr selected  all vectors are visible
            self.vect1_x.setVisible(True);  self.vect1_y.setVisible(True);  self.vect1_z.setVisible(True)
            self.vect2_x.setVisible(True);  self.vect2_y.setVisible(True);  self.vect2_z.setVisible(True)
            self.vect3_x.setVisible(True);  self.vect3_y.setVisible(True);  self.vect3_z.setVisible(True)
        else:  # for euler only  vector 1 is visible
            self.vect1_x.setVisible(True);  self.vect1_y.setVisible(True);  self.vect1_z.setVisible(True)
            self.vect2_x.setVisible(False); self.vect2_y.setVisible(False); self.vect2_z.setVisible(False)
            self.vect3_x.setVisible(False); self.vect3_y.setVisible(False); self.vect3_z.setVisible(False)

    def check_valid(self):
         pass
#        teststr = self.sender()
#        if self.valid.validate(teststr.text(),0) != QtGui.QValidator.Acceptable:
#           self.sender.setText("0.0")

Gui.addCommand('ref_cmd', ref_cmd())
