#!/usr/bin/env python3
# coding: utf-8
#
# struct_node_cmd.py

import os
import sys
import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')
import MBDyn_objects.model_so
from PySide2 import QtCore, QtGui, QtWidgets
import FreeCAD as App
import FreeCADGui as Gui



from  MBDyn_guitools.dia_struct_node import Ui_struct_node_dialog

class struct_node_cmd(QtWidgets.QDialog, Ui_struct_node_dialog):
    """MBD create structural node command"""
    def __init__(self):
        super(struct_node_cmd, self).__init__()
        self.setupUi(self)

    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'Struct_node_icon.svg'),
                'MenuText': "create structural nodes command",
                'ToolTip': "create structural nodess"}
    def Activated(self):
        """Do something here"""
       
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
        num_nodes = len(App.ActiveDocument.Nodes.getSubObjects())+ 1
        # create a new node scripted object
        new_node =App.ActiveDocument.Nodes.newObject("App::FeaturePython","node" + str(num_nodes))
        MBDyn_objects.model_so.MBDynStructuralNode(new_node)
        new_node.ViewObject.Proxy = 0

        new_node.node_label = num_nodes
         # set the reference to be refered to

        new_node.struct_type = self.struct_node_type.currentText()
        new_node.position = App.Vector(float(self.pos_x.text()), float(self.pos_y.text()), float(self.pos_z.text()))
        new_node.orientation = [App.Vector(float(self.vect1_x.text()), float(self.vect1_y.text()), float(self.vect1_z.text())), 
                                App.Vector(float(self.vect2_x.text()), float(self.vect2_y.text()), float(self.vect2_z.text())), 
                                App.Vector(float(self.vect3_x.text()), float(self.vect3_y.text()), float(self.vect3_z.text()))]
        new_node.orientation_des = str(self.OM_type.currentText())
#        App.Console.PrintMessage(" property2: " + str(new_node.orientation[1].x)  + "\n")
        new_node.vel = App.Vector(float(self.vel_x.text()), float(self.vel_y.text()), float(self.vel_z.text()))
        new_node.ang_vel = App.Vector(float(self.ang_vel_x.text()), float(self.ang_vel_y.text()), float(self.ang_vel_z.text()))

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

Gui.addCommand('struct_node_cmd', struct_node_cmd())