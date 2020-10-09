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

from   MBDyn_guitools.dia_total_joint import Ui_dia_Totaljoint

class total_joint_cmd(QtWidgets.QDialog, Ui_dia_Totaljoint):
    """MBD create toal joint command"""
    def __init__(self):
        super(total_joint_cmd, self).__init__()
        self.setupUi(self)

    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'TotalJointIcon.svg'),
                'MenuText': "create total joint",
                'ToolTip': "input total joint parameters"}


    def Activated(self):
        """Do something here"""
        self.node1_box.clear()
        self.node2_box.clear()
        if App.ActiveDocument.getObjectsByLabel('Nodes') != None :
            App.Console.PrintMessage(" property3: ")
            for nodeobj in App.ActiveDocument.Nodes.Group:
                App.Console.PrintMessage(" property4: "+ nodeobj.node_name)
                self.node1_box.addItem(nodeobj.node_name)
                self.node2_box.addItem(nodeobj.node_name)

        # define connections for dialog widgets
        self.node1_box.currentIndexChanged.connect(self.set_node1)
        self.node2_box.currentIndexChanged.connect(self.set_node2)
        self.set_node1()
        self.set_node2()

        self.show()

        App.Console.PrintMessage(" Activated: " + "\n")


    def IsActive(self):
        if App.ActiveDocument == None:
            return False
        else:
            return True


    def accept(self):
        #  get FreeCAD object associated with nodes chosen.
        for nodeobjs in App.ActiveDocument.Nodes.Group:
            if nodeobjs.node_name  == self.node1_box.currentText():
                nodeobj1 = nodeobjs
                node1_lnk = App.ActiveDocument.getObjectsByLabel(nodeobjs.node_name.split("|")[0])[0]
            if nodeobjs.node_name  == self.node2_box.currentText():
                nodeobj2 = nodeobjs
                node2_lnk = App.ActiveDocument.getObjectsByLabel(nodeobjs.node_name.split("|")[0])[0]
        '''
        # check if both nodes are not the same
        if nodeobj1.node_name == nodeobj2.node_name:
            mb = QtGui.QMessageBox()
            mb.setText("both nodes can not be the same")
            mb.exec()
            return
        '''
        # find the position and rotation LCS objects for orientation matraces
        # node 1 position and rotation LCS
        posLCS1_str = self.node1_LCS_pos_box.currentText()
        rotLCS1_str = self.node1_LCS_rot_box.currentText()
        linkedobj1 = node1_lnk.getLinkedObject()
        for linkedsub in linkedobj1.getSubObjects():
            if linkedobj1.getObject(linkedsub[0:-1]).Label == posLCS1_str:
                posLCS1 = linkedobj1.getObject(linkedsub[0:-1])
            if linkedobj1.getObject(linkedsub[0:-1]).Label == rotLCS1_str:
                rotLCS1 = linkedobj1.getObject(linkedsub[0:-1])

        # node 2 position and rotation LCS
        posLCS2_str = self.node2_LCS_pos_box.currentText()
        rotLCS2_str = self.node2_LCS_rot_box.currentText()
        App.Console.PrintMessage(" orient2 "+posLCS2_str)

        linkedobj2 = node2_lnk.getLinkedObject()
        for linkedsub in linkedobj2.getSubObjects():
            App.Console.PrintMessage(" orient2 "+linkedsub)

            if linkedobj2.getObject(linkedsub[0:-1]).Label == posLCS2_str:
                posLCS2 = linkedobj2.getObject(linkedsub[0:-1])
            if linkedobj2.getObject(linkedsub[0:-1]).Label == rotLCS2_str:
                rotLCS2 = linkedobj2.getObject(linkedsub[0:-1])
        App.Console.PrintMessage(" orient3 "+posLCS2_str)

        # get placements for node 1 position and rotation LCSs
        posLCS1_pl = node1_lnk.Placement.multiply(posLCS1.Placement)
        rotLCS1_pl = node1_lnk.Placement.multiply(rotLCS1.Placement)

        App.Console.PrintMessage(" orient4 ")
        # make FreeCAD placement matrix from node1 position and orientation matrix
        if nodeobj1.orientation_des == 'euler321':
            rotz = App.Units.parseQuantity("(180/pi)*" + str(nodeobj1.orientation[0][0]))
            roty = App.Units.parseQuantity("(180/pi)*" + str(nodeobj1.orientation[0][1]))
            rotx = App.Units.parseQuantity("(180/pi)*" + str(nodeobj1.orientation[0][2]))
            node1_pl = App.Placement(nodeobj1.position, App.Rotation(rotz, roty, rotx))
            App.Console.PrintMessage(" orient1: " + str(node1_pl))
        node1_pl_inv = node1_pl.inverse()

        # get placements for node 2 position and rotation LCSs
        posLCS2_pl = node2_lnk.Placement.multiply(posLCS2.Placement)
        rotLCS2_pl = node2_lnk.Placement.multiply(rotLCS2.Placement)
        App.Console.PrintMessage(" orient2")
        # make FreeCAD placement matrix from node1 position and orientation matrix
        if nodeobj2.orientation_des == 'euler321':
            rotz = App.Units.parseQuantity("(180/pi)*" + str(nodeobj2.orientation[0][0]))
            roty = App.Units.parseQuantity("(180/pi)*" + str(nodeobj2.orientation[0][1]))
            rotx = App.Units.parseQuantity("(180/pi)*" + str(nodeobj2.orientation[0][2]))
            node2_pl = App.Placement(nodeobj2.position, App.Rotation(rotz, roty, rotx))
            App.Console.PrintMessage(" orient2: "+str(node2_pl))
        node2_pl_inv = node2_pl.inverse()
        App.Console.PrintMessage(" orient3: "+str(node2_lnk.Placement.multiply(posLCS2_pl)))

        # create joint object
        num_joints = len(App.ActiveDocument.Joints.getSubObjects()) + 1
        new_joint = App.ActiveDocument.Joints.newObject("App::FeaturePython","Joint" + str(num_joints))
        MBDyn_objects.MBDynJoints.FC_totaljoint(new_joint)
        new_joint.ViewObject.Proxy = 0
        new_joint.joint_label = num_joints

        # set node1 joint parameters
        new_joint.node1_label = nodeobj1.node_label
        rel_posLCS1_pl =  node1_pl_inv.multiply(posLCS1_pl)
        rel_rotLCS1_pl =  node1_pl_inv.multiply(rotLCS1_pl)
        App.Console.PrintMessage(" orient4: "+str(rel_rotLCS1_pl))
#        new_joint.position1 = linkLCS1_pos - node1_pl_inv.multVec(nodeobj1.position)
        new_joint.position1 = rel_posLCS1_pl.Base
        new_joint.pos_orientation_des1 = 'xy'
        new_joint.pos_orientation1 = [App.Vector(rel_posLCS1_pl.Matrix.A11, rel_posLCS1_pl.Matrix.A21, rel_posLCS1_pl.Matrix.A31),
                                      App.Vector(rel_posLCS1_pl.Matrix.A12, rel_posLCS1_pl.Matrix.A22, rel_posLCS1_pl.Matrix.A32),
                                      App.Vector(0,0,0)]
        new_joint.rot_orientation_des1 = 'xy'
        new_joint.rot_orientation1 = [App.Vector(rel_rotLCS1_pl.Matrix.A11, rel_rotLCS1_pl.Matrix.A21, rel_rotLCS1_pl.Matrix.A31),
                                      App.Vector(rel_rotLCS1_pl.Matrix.A12, rel_rotLCS1_pl.Matrix.A22, rel_rotLCS1_pl.Matrix.A32),
                                      App.Vector(0,0,0)]

        # set node2 joint parameters
        new_joint.node2_label = nodeobj2.node_label
        rel_posLCS2_pl =  node2_pl_inv.multiply(posLCS2_pl)
        rel_rotLCS2_pl =  node2_pl_inv.multiply(rotLCS2_pl)
        new_joint.position2 = rel_posLCS2_pl.Base
        new_joint.pos_orientation_des2 = 'xy'
        new_joint.pos_orientation2 = [App.Vector(rel_posLCS2_pl.Matrix.A11, rel_posLCS2_pl.Matrix.A21, rel_posLCS2_pl.Matrix.A31),
                                      App.Vector(rel_posLCS2_pl.Matrix.A12, rel_posLCS2_pl.Matrix.A22, rel_posLCS2_pl.Matrix.A32),
                                      App.Vector(0,0,0)]
        new_joint.rot_orientation_des2 = 'xy'
        new_joint.rot_orientation2 = [App.Vector(rel_rotLCS2_pl.Matrix.A11, rel_rotLCS2_pl.Matrix.A21, rel_rotLCS2_pl.Matrix.A31),
                                      App.Vector(rel_rotLCS2_pl.Matrix.A12, rel_rotLCS2_pl.Matrix.A22, rel_rotLCS2_pl.Matrix.A32),
                                      App.Vector(0,0,0)]

        # set position and rotation constraints from check boxes.
        new_joint.pos_constraint = [self.posx_checkBox.isChecked(), self.posy_checkBox.isChecked(), self.posz_checkBox.isChecked()]
        new_joint.rot_constraint = [self.rotx_checkBox.isChecked(), self.roty_checkBox.isChecked(), self.rotz_checkBox.isChecked()]
        new_joint.vel_constraint = [self.velx_checkBox.isChecked(), self.vely_checkBox.isChecked(), self.velz_checkBox.isChecked()]
        new_joint.angvel_constraint = [self.angvelx_checkBox.isChecked(), self.angvely_checkBox.isChecked(), self.angvelz_checkBox.isChecked()]

        self.done(1)


    def set_node1(self):
        ''' populates the node 1 position and rotation orientation combo boxes'''
        self.node1_LCS_pos_box.clear()
        self.node1_LCS_rot_box.clear()
        node1_str = self.node1_box.currentText().split("|")[0]
        for linksobj in App.ActiveDocument.getLinksTo():
            if linksobj.Name == node1_str:
                linkedobj = linksobj.getLinkedObject()
                for linkedsub in linkedobj.getSubObjects():
                    if linkedobj.getObject(linkedsub[0:-1]).TypeId == 'PartDesign::CoordinateSystem':
                        self.node1_LCS_pos_box.addItem(linkedobj.getObject(linkedsub[0:-1]).Label)
                        self.node1_LCS_rot_box.addItem(linkedobj.getObject(linkedsub[0:-1]).Label)


    def set_node2(self):
        ''' populates the node 2 position and rotation orientation combo boxes'''
        self.node2_LCS_pos_box.clear()
        self.node2_LCS_rot_box.clear()
        node2_str = self.node2_box.currentText().split("|")[0]
        for linksobj in App.ActiveDocument.getLinksTo():
            if linksobj.Name == node2_str:
                linkedobj = linksobj.getLinkedObject()
                for linkedsub in linkedobj.getSubObjects():
                    if linkedobj.getObject(linkedsub[0:-1]).TypeId == 'PartDesign::CoordinateSystem':
                        self.node2_LCS_pos_box.addItem(linkedobj.getObject(linkedsub[0:-1]).Label)
                        self.node2_LCS_rot_box.addItem(linkedobj.getObject(linkedsub[0:-1]).Label)


Gui.addCommand('total_joint_cmd', total_joint_cmd())
