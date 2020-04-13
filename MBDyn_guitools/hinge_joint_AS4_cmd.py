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



from   MBDyn_guitools.dia_hinge_joint_AS4 import Ui_dia_hinge_joint

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
        if App.ActiveDocument.getObjectsByLabel('Nodes') != None :
            App.Console.PrintMessage(" property3: ")
            for nodeobj in App.ActiveDocument.Nodes.Group:
                App.Console.PrintMessage(" property4: "+ nodeobj.node_name)
                self.node_1_Box.addItem(nodeobj.node_name)

        self.node_2_Box.clear()
        if App.ActiveDocument.getObjectsByLabel('Nodes') != None :
            for nodeobj in App.ActiveDocument.Nodes.Group:
                self.node_2_Box.addItem(nodeobj.node_name)

        # define conections for dialog widgets
        self.link_const_Box.currentIndexChanged.connect(self.set_choose_z) 
        self.choose_z_axis_1.toggled.connect(self.set_z_method) 
        self.node_1_Box.currentIndexChanged.connect(self.set_nodes) 
        self.node_2_Box.currentIndexChanged.connect(self.set_nodes)

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
            linkobj2_str = "Model"
        else:
            linkobj2_str = strlist2[0]
        linkLCS2_str = strlist2[1]

        #  match node with the link constraint chosen.
        for nodeobjs in App.ActiveDocument.Nodes.Group:
            if nodeobjs.node_name  == self.node_1_Box.currentText():
                if nodeobjs.node_name[0:-2] == linkobj1_str:
                    nodeobj1 = nodeobjs
                elif nodeobjs.node_name[0:-2] == linkobj2_str:
                    nodeobj2 = nodeobjs
            if nodeobjs.node_name  == self.node_2_Box.currentText():
                if nodeobjs.node_name[0:-2] == linkobj1_str:
                    nodeobj1 = nodeobjs
                elif nodeobjs.node_name[0:-2] == linkobj2_str:
                    nodeobj2 = nodeobjs
       
        # check if both nodes are not the same
        if nodeobj1.node_name == nodeobj2.node_name:
            mb = QtGui.QMessageBox()
            mb.setText("The document has been modified.")
            mb.exec()
            return

        # create joint object
        num_joints = len(App.ActiveDocument.Joints.getSubObjects()) + 1
        new_joint = App.ActiveDocument.Joints.newObject("App::FeaturePython","Joint" + str(num_joints))
        MBDyn_objects.MBDynJoints.MBDynRevoluteHinge(new_joint)
        new_joint.ViewObject.Proxy = 0
        new_joint.joint_label = num_joints
        
        new_joint.node1_label = nodeobj1.node_label
        new_joint.node2_label = nodeobj2.node_label

        # if objects are App::Link use linkednoject otherwise use object itself
        linkobj1 = App.ActiveDocument.getObject(linkobj1_str)
        if hasattr(linkobj1, "LinkedObject" ):
            linkedobj1 = linkobj1.LinkedObject
        else:
            linkedobj1 = linkobj1
        linkobj2 = App.ActiveDocument.getObject(linkobj2_str)
        if hasattr(linkobj2, "LinkedObject" ):
            linkedobj2 = linkobj2.LinkedObject
        else:
            linkedobj2 = linkobj2


        linkLCS1_pos = linkedobj1.getObject(linkLCS1_str).Placement.Base   
#        linkLCS1_pos = linkobj1.Placement.multVec(linkedobj1.getObject(linkLCS1_str).Placement.Base)
        inv_linkobj1_pl = linkobj1.Placement.inverse()
        new_joint.position1 = linkLCS1_pos - inv_linkobj1_pl.multVec(nodeobj1.position)   
        App.Console.PrintMessage(" lcs1pos: "+str(linkLCS1_pos)+" node1pos: "+str(inv_linkobj1_pl))
        # if object is App::Link use linkednoject otherwise use objcect itself
        App.Console.PrintMessage(" property4: ")
        linkLCS2_pos = linkedobj2.getObject(linkLCS2_str).Placement.Base
#        linkLCS2_pos = linkobj2.Placement.multVec(linkedobj2.getObject(linkLCS2_str).Placement.Base)
        inv_linkobj2_pl = linkobj2.Placement.inverse()
        new_joint.position2 = linkLCS2_pos - inv_linkobj2_pl.multVec(nodeobj2.position)
        App.Console.PrintMessage(" lcs2pos: "+str(linkLCS2_pos)+" node2pos: "+str(inv_linkobj2_pl))
        linkobj1_pl = linkobj1.Placement
        linkLCS1_pl = linkobj1_pl.multiply(linkedobj1.getObject(linkLCS1_str).Placement)
        linkobj2_pl = linkobj2.Placement
        linkLCS2_pl = linkobj1_pl.multiply(linkedobj2.getObject(linkLCS2_str).Placement)

        # make FreeCAD placement matrix from node1 position and orientation matrix
        if nodeobj1.orientation_des == 'euler123':            
            rotz = App.Units.parseQuantity("(180/pi)*" + str(nodeobj1.orientation[0][0]))
            roty = App.Units.parseQuantity("(180/pi)*" + str(nodeobj1.orientation[0][1]))
            rotx = App.Units.parseQuantity("(180/pi)*" + str(nodeobj1.orientation[0][2]))
            node1_pl = App.Placement(nodeobj1.position, App.Rotation(rotz, roty, rotx))
            App.Console.PrintMessage(" orient1: "+str(node1_pl))

        # make FreeCAD placement matrix from node1 position and orientation matrix
        if nodeobj2.orientation_des == 'euler123':            
            rotz = App.Units.parseQuantity("(180/pi)*" + str(nodeobj2.orientation[0][0]))
            roty = App.Units.parseQuantity("(180/pi)*" + str(nodeobj2.orientation[0][1]))
            rotx = App.Units.parseQuantity("(180/pi)*" + str(nodeobj2.orientation[0][2]))
            node2_pl = App.Placement(nodeobj2.position, App.Rotation(rotz, roty, rotx))
            App.Console.PrintMessage(" orient2: "+str(node2_pl))

        # find orientation where z is axis of rotation and relative to nodes orientation
        if self.choose_z_axis_2.isChecked():
            if str(strlist[0] + " x") ==  self.Choose_z_axis_Box.currentText():
                linkLCS1_Z_rot = App.Rotation(0,90,0).multiply(linkLCS1_pl.Rotation)
                linkLCS1_rot_rel = linkLCS1_Z_rot.multiply(node1_pl.Rotation.inverted())
                linkLCS2_rot_rel = linkLCS1_Z_rot.multiply(node2_pl.Rotation.inverted())
            elif str(strlist[0] + " y") ==  self.Choose_z_axis_Box.currentText():
                linkLCS1_Z_rot = App.Rotation(0,0,90).multiply(linkLCS1_pl.Rotation)
                linkLCS1_rot_rel = linkLCS1_Z_rot.multiply(node1_pl.Rotation.inverted())
                linkLCS2_rot_rel = linkLCS1_Z_rot.multiply(node2_pl.Rotation.inverted())
            elif str(strlist[0] + " z") ==  self.Choose_z_axis_Box.currentText(): 
                linkLCS1_Z_rot = linkLCS1_pl.Rotation
                linkLCS1_rot_rel = linkLCS1_Z_rot.multiply(node1_pl.Rotation.inverted())
                linkLCS2_rot_rel = linkLCS1_Z_rot.multiply(node2_pl.Rotation.inverted())

            orient = App.Vector(0,0,0)
            App.Console.PrintMessage(" orient3: " + str(linkLCS1_rot_rel.toEuler()))
            new_joint.orientation_des1 = "euler123"
            orient.z = App.Units.parseQuantity("(pi/180)*" + str(linkLCS1_rot_rel.toEuler()[0] )) # convert angle to radians
            orient.y = App.Units.parseQuantity("(pi/180)*" + str(linkLCS1_rot_rel.toEuler()[1] ))
            orient.x = App.Units.parseQuantity("(pi/180)*" + str(linkLCS1_rot_rel.toEuler()[2] ))
            new_joint.orientation1 = [orient, App.Vector(0,0,0), App.Vector(0,0,0)]

            new_joint.orientation_des2 = "euler123"
            orient.z = App.Units.parseQuantity("(pi/180)*" + str(linkLCS2_rot_rel.toEuler()[0] )) # convert angle to radians
            orient.y = App.Units.parseQuantity("(pi/180)*" + str(linkLCS2_rot_rel.toEuler()[1] ))
            orient.x = App.Units.parseQuantity("(pi/180)*" + str(linkLCS2_rot_rel.toEuler()[2] ))
            new_joint.orientation2 = [orient, App.Vector(0,0,0), App.Vector(0,0,0)]
 
        else:        
            joint_z_axis = App.Vector(float(self.z_axis_set_x.text()), float(self.z_axis_set_y.text()), float(self.z_axis_set_z.text()))             
            new_joint.orientation1 = [App.Vector(float(self.node1_vect1_x.text()), float(self.node1_vect1_y.text()), float(self.node1_vect1_z.text())), 
                               App.Vector(float(self.node1_vect2_x.text()), float(self.node1_vect2_y.text()), float(self.node1_vect2_z.text())), 
                               joint_z_axis]
        

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

    def set_nodes(self):
        self.link_const_Box.clear()
        node1_str = self.node_1_Box.currentText()
        node2_str = self.node_2_Box.currentText()
        for linksobj in App.ActiveDocument.getLinksTo():
            constname = linksobj.Name + linksobj.AttachedBy+ " to " + linksobj.AttachedTo
            linkobj_atch = linksobj.AttachedTo.split("#")[0]
            if linksobj.Name == node1_str[0:-2] or linksobj.Name == node2_str[0:-2]:
                if linkobj_atch == node1_str[0:-2] or linkobj_atch == node2_str[0:-2]:
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

    def check_valid(self):
         pass
#        teststr = self.sender()
#        if self.valid.validate(teststr.text(),0) != QtGui.QValidator.Acceptable:
#           self.sender.setText("0.0")

Gui.addCommand('hinge_joint_cmd', hinge_joint_cmd())