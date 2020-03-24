#!/usr/bin/env python3
# coding: utf-8
#
# hinge_joint_cmd.py

import os
import sys
import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')
import model_so
import MBDynJoints
from PySide2 import QtCore, QtGui, QtWidgets
import FreeCAD as App
import FreeCADGui as Gui



from  dia_hinge_joint import Ui_dia_hinge_joint

class hinge_joint_cmd(QtWidgets.QDialog, Ui_dia_hinge_joint):
    """MBD create reference command"""
    def __init__(self):
        super(hinge_joint_cmd, self).__init__()
        self.setupUi(self)

    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'RevoluteHingeIcon.svg'),
                'MenuText': "create revolute hinge joint",
                'ToolTip': "input revolute hinge joint parameters"}
    def Activated(self):
        """Do something here"""
        self.node_1_Box.clear()
        self.node_2_Box.clear()
        if App.ActiveDocument.getObjectsByLabel('Nodes') != None :
            App.Console.PrintMessage(" property3: ")
            for nodeobj in App.ActiveDocument.Nodes.Group:
                App.Console.PrintMessage(" property4: "+ nodeobj.node_name)
                self.node_1_Box.addItem(nodeobj.node_name)
                self.node_2_Box.addItem(nodeobj.node_name)
        self.node1_pos_x.setText("0") ; self.node1_pos_y.setText("0") ; self.node1_pos_z.setText("0")
        self.node1_vect1_x.setText("1") ; self.node1_vect1_y.setText("0") ; self.node1_vect1_z.setText("0")
        self.node1_vect2_x.setText("0") ; self.node1_vect2_y.setText("1") ; self.node1_vect2_z.setText("0")
        self.node1_vect3_x.setText("0") ; self.node1_vect3_y.setText("0") ; self.node1_vect3_z.setText("1")
        

        self.node2_pos_x.setText("0") ; self.node2_pos_y.setText("0") ; self.node2_pos_z.setText("0")
        self.node2_vect1_x.setText("1") ; self.node2_vect1_y.setText("0") ; self.node2_vect1_z.setText("0")
        self.node2_vect2_x.setText("0") ; self.node2_vect2_y.setText("1") ; self.node2_vect2_z.setText("0")
        self.node2_vect3_x.setText("0") ; self.node2_vect3_y.setText("0") ; self.node2_vect3_z.setText("1")
        
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
        for nodeobj in App.ActiveDocument.Nodes.Group:
            App.Console.PrintMessage(" property2: " + nodeobj.node_name)
            
            if nodeobj.node_name  == self.node_1_Box.currentText():
                node_1_lab = nodeobj.node_label
            if nodeobj.node_name  == self.node_2_Box.currentText() and nodeobj.node_name  != self.node_1_Box.currentText():
                App.Console.PrintMessage(" property2: ")
                node_2_lab = nodeobj.node_label
                num_joints = len(App.ActiveDocument.Joints.getSubObjects()) + 1

                new_joint = App.ActiveDocument.Joints.newObject("App::FeaturePython","Joint" + str(num_joints))
                MBDynJoints.MBDynRevoluteHinge(new_joint)
                new_joint.ViewObject.Proxy = 0

                new_joint.joint_label = num_joints
                new_joint.node1_label = node_1_lab
                new_joint.position1 = App.Vector(float(self.node1_pos_x.text()), float(self.node1_pos_y.text()), float(self.node1_pos_z.text()))
                new_joint.orientation1 = [App.Vector(float(self.node1_vect1_x.text()), float(self.node1_vect1_y.text()), float(self.node1_vect1_z.text())), 
                               App.Vector(float(self.node1_vect2_x.text()), float(self.node1_vect2_y.text()), float(self.node1_vect2_z.text())), 
                               App.Vector(float(self.node1_vect3_x.text()), float(self.node1_vect3_y.text()), float(self.node1_vect3_z.text()))]
                new_joint.orientation_des1 = self.node1_OM_type_Box.currentText()

                new_joint.node2_label = node_2_lab
                new_joint.position2 = App.Vector(float(self.node2_pos_x.text()), float(self.node2_pos_y.text()), float(self.node2_pos_z.text()))
                new_joint.orientation2 = [App.Vector(float(self.node2_vect1_x.text()), float(self.node2_vect1_y.text()), float(self.node2_vect1_z.text())), 
                               App.Vector(float(self.node2_vect2_x.text()), float(self.node2_vect2_y.text()), float(self.node2_vect2_z.text())), 
                               App.Vector(float(self.node2_vect3_x.text()), float(self.node2_vect3_y.text()), float(self.node2_vect3_z.text()))]
                new_joint.orientation_des2 = self.node2_OM_type_Box.currentText()

            else:
                App.Console.PrintMessage(" both nodes can not bee the same ")


    def set_OM_type(self):
        index = self.node1_OM_type_Box.currentIndex()
        App.Console.PrintMessage(" property: " +self.node1_OM_type_Box.itemText(index) + "\n")
        if self.node1_OM_type_Box.currentIndex() == 0:  #xy selected  only vectors 1 and 2 are editable
            self.node1_vect1_x.setReadOnly(False); self.node1_vect1_y.setReadOnly(False); self.node1_vect1_z.setReadOnly(False)
            self.node1_vect2_x.setReadOnly(False); self.node1_vect2_y.setReadOnly(False); self.node1_vect2_z.setReadOnly(False)
#            self.vect3_x.cear(); self.vect3_y.cear(); self.vect3_z.cear()
            self.node1_vect3_x.setReadOnly(True); self.node1_vect3_y.setReadOnly(True); self.node1_vect3_z.setReadOnly(True)
        elif self.node1_OM_type_Box.currentIndex() == 1:  #xz selected  only vectors 1 and 3 are editable
            self.node1_vect1_x.setReadOnly(False); self.node1_vect1_y.setReadOnly(False); self.node1_vect1_z.setReadOnly(False)
#            self.vect2_x.cear(); self.vect2_y.cear(); self.vect2_z.cear()
            self.node1_vect2_x.setReadOnly(True); self.node1_vect2_y.setReadOnly(True); self.node1_vect2_z.setReadOnly(True)
            self.node1_vect3_x.setReadOnly(False); self.node1_vect3_y.setReadOnly(False); self.node1_vect3_z.setReadOnly(False)
        elif self.node1_OM_type_Box.currentIndex() == 2:  #yz selected  only vectors 2 and 3 are editable
#            self.vect1_x.cear(); self.vect1_y.cear(); self.vect1_z.cear()
            self.node1_vect1_x.setReadOnly(True); self.node1_vect1_y.setReadOnly(True); self.node1_vect1_z.setReadOnly(True)
            self.node1_vect2_x.setReadOnly(False); self.node1_vect2_y.setReadOnly(False); self.node1_vect2_z.setReadOnly(False)
            self.node1_vect3_x.setReadOnly(False); self.node1_vect3_y.setReadOnly(False); self.node1_vect3_z.setReadOnly(False)
        elif self.node1_OM_type_Box.currentIndex() == 3:  #MATRIX selected  all vectors are editable
            self.node1_vect1_x.setReadOnly(False); self.node1_vect1_y.setReadOnly(False); self.node1_vect1_z.setReadOnly(False)
            self.node1_vect2_x.setReadOnly(False); self.node1_vect2_y.setReadOnly(False); self.node1_vect2_z.setReadOnly(False)
            self.node1_vect3_x.setReadOnly(False); self.node1_vect3_y.setReadOnly(False); self.node1_vect3_z.setReadOnly(False)
        else:  # for euler only  vector 1 is editable
            self.node1_vect1_x.setReadOnly(False); self.node1_vect1_y.setReadOnly(False); self.node1_vect1_z.setReadOnly(False)
#            self.vect2_x.cear(); self.vect2_y.cear(); self.vect2_z.cear()
            self.node1_vect2_x.setReadOnly(True); self.node1_vect2_y.setReadOnly(True); self.node1_vect2_z.setReadOnly(True)
 #           self.vect3_x.cear(); self.vect3_y.cear(); self.vect3_z.cear()
            self.node1_vect3_x.setReadOnly(True); self.node1_vect3_y.setReadOnly(True); self.node1_vect3_z.setReadOnly(True)
    
    def check_valid(self):
         pass
#        teststr = self.sender()
#        if self.valid.validate(teststr.text(),0) != QtGui.QValidator.Acceptable:
#           self.sender.setText("0.0")

Gui.addCommand('hinge_joint_cmd', hinge_joint_cmd())