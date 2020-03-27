#!/usr/bin/env python3
# coding: utf-8
#
# revpin_joint_cmd.py

import os
import sys
import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')
import MBDyn_objects.model_so
import MBDyn_objects.MBDynJoints
from PySide2 import QtCore, QtGui, QtWidgets
import FreeCAD as App
import FreeCADGui as Gui



from   MBDyn_guitools.dia_revpin_joint import Ui_dia_revpin_joint

class revpin_joint_cmd(QtWidgets.QDialog, Ui_dia_revpin_joint):
    """MBD create reference command"""
    def __init__(self):
        super(revpin_joint_cmd, self).__init__()
        self.setupUi(self)

    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'RevolutePinIcon.svg'),
                'MenuText': "create revolute pin joint",
                'ToolTip': "input revolute pin joint parameters"}
    def Activated(self):
        """Do something here"""
        self.node_1_Box.clear()
        
        if App.ActiveDocument.getObjectsByLabel('Nodes') != None :
            App.Console.PrintMessage(" property3: ")
            for nodeobj in App.ActiveDocument.Nodes.Group:
                App.Console.PrintMessage(" property4: "+ nodeobj.node_name)
                self.node_1_Box.addItem(nodeobj.node_name)

        self.node1_pos_x.setText("0") ; self.node1_pos_y.setText("0") ; self.node1_pos_z.setText("0")
        self.node1_vect1_x.setText("1") ; self.node1_vect1_y.setText("0") ; self.node1_vect1_z.setText("0")
        self.node1_vect2_x.setText("0") ; self.node1_vect2_y.setText("1") ; self.node1_vect2_z.setText("0")
        self.node1_vect3_x.setText("0") ; self.node1_vect3_y.setText("0") ; self.node1_vect3_z.setText("1")
        

        self.fixed_pos_x.setText("0") ; self.fixed_pos_y.setText("0") ; self.fixed_pos_z.setText("0")
        self.fixed_vect1_x.setText("1") ; self.fixed_vect1_y.setText("0") ; self.fixed_vect1_z.setText("0")
        self.fixed_vect2_x.setText("0") ; self.fixed_vect2_y.setText("1") ; self.fixed_vect2_z.setText("0")
        self.fixed_vect3_x.setText("0") ; self.fixed_vect3_y.setText("0") ; self.fixed_vect3_z.setText("1")

        self.node1_OM_type_Box.currentIndexChanged.connect(self.set_node1_OM_type)
        self.fixed_OM_type_Box.currentIndexChanged.connect(self.set_fixed_OM_type)
        self.node1_OM_type_Box.setCurrentIndex(1)
        self.fixed_OM_type_Box.setCurrentIndex(1)
        self.node1_OM_type_Box.setCurrentIndex(0)       
        self.fixed_OM_type_Box.setCurrentIndex(0)
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
        index = self.node1_OM_type_Box.currentIndex()
        App.Console.PrintMessage(" property1: " +self.node1_OM_type_Box.itemText(index) + "\n")

        num_joints = len(App.ActiveDocument.Joints.getSubObjects()) + 1
        new_joint = App.ActiveDocument.Joints.newObject("App::FeaturePython","Joint" + str(num_joints))
        MBDyn_objects.MBDynJoints.MBDynRevolutePin(new_joint)
        new_joint.ViewObject.Proxy = 0

        new_joint.joint_label =  num_joints
        for nodeobj in App.ActiveDocument.Nodes.Group:
            App.Console.PrintMessage(" property2: " + nodeobj.node_name)
            
            if nodeobj.node_name  == self.node_1_Box.currentText():
                App.Console.PrintMessage(" property2: ")
                new_joint.node1_label = nodeobj.node_label
        new_joint.position1 = App.Vector(float(self.node1_pos_x.text()), float(self.node1_pos_y.text()), float(self.node1_pos_z.text()))
        new_joint.orientation1 = [App.Vector(float(self.node1_vect1_x.text()), float(self.node1_vect1_y.text()), float(self.node1_vect1_z.text())), 
                               App.Vector(float(self.node1_vect2_x.text()), float(self.node1_vect2_y.text()), float(self.node1_vect2_z.text())), 
                               App.Vector(float(self.node1_vect3_x.text()), float(self.node1_vect3_y.text()), float(self.node1_vect3_z.text()))]
        new_joint.orientation_des1 = self.node1_OM_type_Box.currentText()
        new_joint.positionf = App.Vector(float(self.fixed_pos_x.text()), float(self.fixed_pos_y.text()), float(self.fixed_pos_z.text()))
        new_joint.orientationf = [App.Vector(float(self.fixed_vect1_x.text()), float(self.fixed_vect1_y.text()), float(self.fixed_vect1_z.text())), 
                               App.Vector(float(self.fixed_vect2_x.text()), float(self.fixed_vect2_y.text()), float(self.fixed_vect2_z.text())), 
                               App.Vector(float(self.fixed_vect3_x.text()), float(self.fixed_vect3_y.text()), float(self.fixed_vect3_z.text()))]
        new_joint.orientation_desf = self.fixed_OM_type_Box.currentText()

        self.done(1)

    def reject(self):
        self.done(0)
    
    def set_node1_OM_type(self):
        index = self.node1_OM_type_Box.currentIndex()
        App.Console.PrintMessage(" property: " +self.node1_OM_type_Box.itemText(index) + "\n")
        if self.node1_OM_type_Box.currentIndex() == 0:  #xy selected  only vectors 1 and 2 are visible
            self.node1_vect1_x.setVisible(True);  self.node1_vect1_y.setVisible(True);  self.node1_vect1_z.setVisible(True)
            self.node1_vect2_x.setVisible(True);  self.node1_vect2_y.setVisible(True);  self.node1_vect2_z.setVisible(True)
            self.node1_vect3_x.setVisible(False); self.node1_vect3_y.setVisible(False); self.node1_vect3_z.setVisible(False)
        elif self.node1_OM_type_Box.currentIndex() == 1:  #xz selected  only vectors 1 and 3 are visible
            self.node1_vect1_x.setVisible(True);  self.node1_vect1_y.setVisible(True);  self.node1_vect1_z.setVisible(True)
            self.node1_vect2_x.setVisible(False); self.node1_vect2_y.setVisible(False); self.node1_vect2_z.setVisible(False)
            self.node1_vect3_x.setVisible(True);  self.node1_vect3_y.setVisible(True);  self.node1_vect3_z.setVisible(True)
        elif self.node1_OM_type_Box.currentIndex() == 2:  #yz selected  only vectors 2 and 3 are visible
            self.node1_vect1_x.setVisible(False); self.node1_vect1_y.setVisible(False); self.node1_vect1_z.setVisible(False)
            self.node1_vect2_x.setVisible(True);  self.node1_vect2_y.setVisible(True);  self.node1_vect2_z.setVisible(True)
            self.node1_vect3_x.setVisible(True);  self.node1_vect3_y.setVisible(True);  self.node1_vect3_z.setVisible(True)
        elif self.node1_OM_type_Box.currentIndex() == 3:  #matr selected  all vectors are visible
            self.node1_vect1_x.setVisible(True);  self.node1_vect1_y.setVisible(True);  self.node1_vect1_z.setVisible(True)
            self.node1_vect2_x.setVisible(True);  self.node1_vect2_y.setVisible(True);  self.node1_vect2_z.setVisible(True)
            self.node1_vect3_x.setVisible(True);  self.node1_vect3_y.setVisible(True);  self.node1_vect3_z.setVisible(True)
        else:  # for euler only  vector 1 is visible
            self.node1_vect1_x.setVisible(True);  self.node1_vect1_y.setVisible(True);  self.node1_vect1_z.setVisible(True)
            self.node1_vect2_x.setVisible(False); self.node1_vect2_y.setVisible(False); self.node1_vect2_z.setVisible(False)
            self.node1_vect3_x.setVisible(False); self.node1_vect3_y.setVisible(False); self.node1_vect3_z.setVisible(False)

    def set_fixed_OM_type(self):
        index = self.fixed_OM_type_Box.currentIndex()
        App.Console.PrintMessage(" property: " +self.fixed_OM_type_Box.itemText(index) + "\n")
        if self.fixed_OM_type_Box.currentIndex() == 0:  #xy selected  only vectors 1 and 2 are visible
            self.fixed_vect1_x.setVisible(True);  self.fixed_vect1_y.setVisible(True);  self.fixed_vect1_z.setVisible(True)
            self.fixed_vect2_x.setVisible(True);  self.fixed_vect2_y.setVisible(True);  self.fixed_vect2_z.setVisible(True)
            self.fixed_vect3_x.setVisible(False); self.fixed_vect3_y.setVisible(False); self.fixed_vect3_z.setVisible(False)
        elif self.fixed_OM_type_Box.currentIndex() == 1:  #xz selected  only vectors 1 and 3 are visible
            self.fixed_vect1_x.setVisible(True);  self.fixed_vect1_y.setVisible(True);  self.fixed_vect1_z.setVisible(True)
            self.fixed_vect2_x.setVisible(False); self.fixed_vect2_y.setVisible(False); self.fixed_vect2_z.setVisible(False)
            self.fixed_vect3_x.setVisible(True);  self.fixed_vect3_y.setVisible(True);  self.fixed_vect3_z.setVisible(True)
        elif self.fixed_OM_type_Box.currentIndex() == 2:  #yz selected  only vectors 2 and 3 are visible
            self.fixed_vect1_x.setVisible(False); self.fixed_vect1_y.setVisible(False); self.fixed_vect1_z.setVisible(False)
            self.fixed_vect2_x.setVisible(True);  self.fixed_vect2_y.setVisible(True);  self.fixed_vect2_z.setVisible(True)
            self.fixed_vect3_x.setVisible(True);  self.fixed_vect3_y.setVisible(True);  self.fixed_vect3_z.setVisible(True)
        elif self.fixed_OM_type_Box.currentIndex() == 3:  #matr selected  all vectors are visible
            self.fixed_vect1_x.setVisible(True);  self.fixed_vect1_y.setVisible(True);  self.fixed_vect1_z.setVisible(True)
            self.fixed_vect2_x.setVisible(True);  self.fixed_vect2_y.setVisible(True);  self.fixed_vect2_z.setVisible(True)
            self.fixed_vect3_x.setVisible(True);  self.fixed_vect3_y.setVisible(True);  self.fixed_vect3_z.setVisible(True)
        else:  # for euler only  vector 1 is visible
            self.fixed_vect1_x.setVisible(True);  self.fixed_vect1_y.setVisible(True);  self.fixed_vect1_z.setVisible(True)
            self.fixed_vect2_x.setVisible(False); self.fixed_vect2_y.setVisible(False); self.fixed_vect2_z.setVisible(False)
            self.fixed_vect3_x.setVisible(False); self.fixed_vect3_y.setVisible(False); self.fixed_vect3_z.setVisible(False)

   
    def check_valid(self):
         pass
#        teststr = self.sender()
#        if self.valid.validate(teststr.text(),0) != QtGui.QValidator.Acceptable:
#           self.sender.setText("0.0")

Gui.addCommand('revpin_joint_cmd', revpin_joint_cmd())