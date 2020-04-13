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



from   MBDyn_guitools.dia_revpin_joint_AS4_2 import Ui_dia_revpin_joint

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

        
        self.link_const_Box.clear()
        for linksobj in App.ActiveDocument.getLinksTo():
            constname = linksobj.Name + linksobj.AttachedBy+ " to " + linksobj.AttachedTo
            self.link_const_Box.addItem(constname)

        self.Choose_z_axis_Box.clear()
        strlist = str(self.link_const_Box.currentText()).split(' to ')
        for strlcs in strlist:
            strlcsx = strlcs + " x"
            self.Choose_z_axis_Box.addItem(strlcsx)
            strlcsx = strlcs + " y"
            self.Choose_z_axis_Box.addItem(strlcsx)
            strlcsx = strlcs + " z"
            self.Choose_z_axis_Box.addItem(strlcsx)

        self.link_const_Box.currentIndexChanged.connect(self.set_choose_z) 
        self.choose_z_axis_1.toggled.connect(self.set_z_method) 

        self.choose_z_axis_1.setChecked(True)
        self.choose_z_axis_2.setChecked(True)

        self.show()

        App.Console.PrintMessage(" Activated: " + "\n")
        
        return

    def IsActive(self):
        if App.ActiveDocument == None:
            return False
        else:
            return True


    def accept(self): 
#        index = self.node1_OM_type_Box.currentIndex()
#        App.Console.PrintMessage(" property1: " +self.node1_OM_type_Box.itemText(index) + "\n")

        num_joints = len(App.ActiveDocument.Joints.getSubObjects()) + 1
        new_joint = App.ActiveDocument.Joints.newObject("App::FeaturePython","Joint" + str(num_joints))
        MBDyn_objects.MBDynJoints.MBDynRevolutePin(new_joint)
        new_joint.ViewObject.Proxy = 0
        new_joint.joint_label =  num_joints

        # finnd the node chosen in combobox
        for nodeobjs in App.ActiveDocument.Nodes.Group:
            App.Console.PrintMessage(" property2: " + nodeobjs.node_name)
            if nodeobjs.node_name  == self.node_1_Box.currentText():
                nodeobj = nodeobjs
                App.Console.PrintMessage(" property2: ")
                new_joint.node1_label = nodeobj.node_label


        # parse the string from the link contraint combobox
        # the form is node1 object # LCS Attaced to node 1 object at pivot ' to ' fixed object maybe 'parent Assembly' # LCS of fixwd oject at pivot
        strlist =  str(self.link_const_Box.currentText()).split(' to ')
        strlist1 = strlist[0].split('#')
        strlist2 = strlist[1].split('#')
        App.Console.PrintMessage(" links "+strlist[0])
        # parse first half of string node1 prart  (first part is link and second is LCS)
        if strlist1[0] == "Parent Assembly":  #Parrent Assembly is the App::Part object named model.
            linkobj1_str = "Model"
        else:
            linkobj1_str = strlist1[0]  
        linkLCS1_str = strlist1[1]
        # parse second half of string fixed prart  (first part is link and second is LCS)
        if strlist2[0] == "Parent Assembly":   #Parrent Assembly is the App::Part object named model.
            linkobjfix_str = "Model"
        else:
            linkobjfix_str = strlist2[0]
        linkLCSfix_str = strlist2[1]

        # if object is App::Link use linkednoject otherwise use object itself
        linkobj1 = App.ActiveDocument.getObject(linkobj1_str)
        if hasattr(linkobj1, "LinkedObject" ):
            linkedobj1 = linkobj1.LinkedObject
        else:
            linkedobj1 = linkobj1
        linkLCS1_pos = linkobj1.Placement.multVec(linkedobj1.getObject(linkLCS1_str).Placement.Base)
        inv_linkobj1_pl = linkobj1.Placement.inverse()
        new_joint.position1 = linkLCS1_pos - inv_linkobj1_pl.multVec(nodeobj.position)   

        # if object is App::Link use linkednoject otherwise use objcect itself
        linkobjfix = App.ActiveDocument.getObject(linkobjfix_str)
        if hasattr(linkobjfix, "LinkedObject" ):
            linkedobjfix = linkobjfix.LinkedObject
        else:
            linkedobjfix = linkobjfix
        App.Console.PrintMessage(" property3: ")
        new_joint.positionf = linkobjfix.Placement.multVec(linkedobjfix.getObject(linkLCSfix_str).Placement.Base)

        linkobj1_pl = linkobj1.Placement
        linkLCS1_pl =  linkobj1_pl.multiply(linkedobj1.getObject(linkLCS1_str).Placement)
        linkLCSfix_pl = linkedobjfix.getObject(linkLCSfix_str).Placement

        # make FreeCAD placement matrix from node position and orientation matrix
        if nodeobj.orientation_des == 'euler123':            
            rotz = App.Units.parseQuantity("(180/pi)*" + str(nodeobj.orientation[0][0]))
            roty = App.Units.parseQuantity("(180/pi)*" + str(nodeobj.orientation[0][1]))
            rotx = App.Units.parseQuantity("(180/pi)*" + str(nodeobj.orientation[0][2]))
            node1_pl = App.Placement(nodeobj.position, App.Rotation(rotz, roty, rotx))
            App.Console.PrintMessage(" orient1: "+str(node1_pl))


        if self.choose_z_axis_2.isChecked():
            if str(strlist[0] + " x") ==  self.Choose_z_axis_Box.currentText():
                linkLCS1_Z_rot = App.Rotation(0,90,0).multiply(linkLCS1_pl.Rotation)
                linkLCS1_rot_rel = linkLCS1_Z_rot.multiply(node1_pl.Rotation.inverted())       
            elif str(strlist[0] + " y") ==  self.Choose_z_axis_Box.currentText():
                linkLCS1_Z_rot = App.Rotation(0,0,90).multiply(linkLCS1_pl.Rotation)
                linkLCS1_rot_rel = linkLCS1_Z_rot.multiply(node1_pl.Rotation.inverted())
            elif str(strlist[0] + " z") ==  self.Choose_z_axis_Box.currentText(): 
                linkLCS1_Z_rot = linkLCS1_pl.Rotation
                linkLCS1_rot_rel = linkLCS1_Z_rot.multiply(node1_pl.Rotation.inverted())

            orient = App.Vector(0,0,0)
            App.Console.PrintMessage(" orient2: " + str(linkLCS1_rot_rel.toEuler()))
            new_joint.orientation_des1 = "euler123"
            orient.z = App.Units.parseQuantity("(pi/180)*" + str(linkLCS1_rot_rel.toEuler()[0] )) # convert angle to radians
            orient.y = App.Units.parseQuantity("(pi/180)*" + str(linkLCS1_rot_rel.toEuler()[1] ))
            orient.x = App.Units.parseQuantity("(pi/180)*" + str(linkLCS1_rot_rel.toEuler()[2] ))
            new_joint.orientation1 = [orient, App.Vector(0,0,0), App.Vector(0,0,0)]

            new_joint.orientation_desf = "euler123"
            orient.z = App.Units.parseQuantity("(pi/180)*" + str(linkLCS1_Z_rot.toEuler()[0] )) # convert angle to radians
            orient.y = App.Units.parseQuantity("(pi/180)*" + str(linkLCS1_Z_rot.toEuler()[1] ))
            orient.x = App.Units.parseQuantity("(pi/180)*" + str(linkLCS1_Z_rot.toEuler()[2] ))
            new_joint.orientationf = [orient, App.Vector(0,0,0), App.Vector(0,0,0)]

        else:
        
            joint_z_axis = App.Vector(float(self.z_axis_set_x.text()), float(self.z_axis_set_y.text()), float(self.z_axis_set_z.text()))
        
             
            new_joint.orientation1 = [App.Vector(float(self.node1_vect1_x.text()), float(self.node1_vect1_y.text()), float(self.node1_vect1_z.text())), 
                               App.Vector(float(self.node1_vect2_x.text()), float(self.node1_vect2_y.text()), float(self.node1_vect2_z.text())), 
                               joint_z_axis]
        

        '''
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
        '''
        self.done(1)

    def reject(self):
        self.done(0)
    
    def set_choose_z(self):
        self.Choose_z_axis_Box.clear()
        strlist = str(self.link_const_Box.currentText()).split(' to ')
        for strlcs in strlist:
            strlcsx = strlcs + " x"
            self.Choose_z_axis_Box.addItem(strlcsx)
            strlcsx = strlcs + " y"
            self.Choose_z_axis_Box.addItem(strlcsx)
            strlcsx = strlcs + " z"
            self.Choose_z_axis_Box.addItem(strlcsx)

    def set_z_method(self):
        App.Console.PrintMessage(" method ")
        if self.choose_z_axis_2.isChecked():
            App.Console.PrintMessage(" method 2")
            self.z_axis_set_x_lab.setVisible(False); self.z_axis_set_y_lab.setVisible(False); self.z_axis_set_z_lab.setVisible(False)
            self.z_axis_set_x.setVisible(False); self.z_axis_set_y.setVisible(False); self.z_axis_set_z.setVisible(False)
            self.Choose_z_axis_Box.setVisible(True)
            self.choose_z_axis_lab.setVisible(True)
        else: 
            self.z_axis_set_x_lab.setVisible(True); self.z_axis_set_y_lab.setVisible(True); self.z_axis_set_z_lab.setVisible(True)
            self.z_axis_set_x.setVisible(True); self.z_axis_set_y.setVisible(True); self.z_axis_set_z.setVisible(True)
            self.Choose_z_axis_Box.setVisible(False)
            self.choose_z_axis_lab.setVisible(False)


    def check_valid(self):
         pass
#        teststr = self.sender()
#        if self.valid.validate(teststr.text(),0) != QtGui.QValidator.Acceptable:
#           self.sender.setText("0.0")

Gui.addCommand('revpin_joint_cmd', revpin_joint_cmd())