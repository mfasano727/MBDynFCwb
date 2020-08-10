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

from   MBDyn_guitools.dia_total_pinjoint import Ui_dia_Totalpinjoint

class total_pinjoint_cmd(QtWidgets.QDialog, Ui_dia_Totalpinjoint):
    """MBD create toal pin joint command"""
    def __init__(self):
        super(total_pinjoint_cmd, self).__init__()
        self.setupUi(self)

    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'TotalPinJointIcon.svg'),
                'MenuText': "create total pin joint",
                'ToolTip': "input total pin joint parameters"}


    def Activated(self):
        """Do something here"""
        self.node1_box.clear()
        if App.ActiveDocument.getObjectsByLabel('Nodes') != None :
            App.Console.PrintMessage(" property3: ")
            for nodeobj in App.ActiveDocument.Nodes.Group:
                App.Console.PrintMessage(" property4: "+ nodeobj.node_name)
                self.node1_box.addItem(nodeobj.node_name)

        # define conections for dialog widgets
        self.node1_box.currentIndexChanged.connect(self.set_node1)
        self.set_node1()
        self.set_fixed()

        self.show()

        App.Console.PrintMessage(" Activated: " + "\n")


    def IsActive(self):
        if App.ActiveDocument == None:
            return False
        else:
            return True


    def accept(self):
        #  get FreeCAD object associated wth nodes chosen.
        for nodeobjs in App.ActiveDocument.Nodes.Group:
            if nodeobjs.node_name  == self.node1_box.currentText():
                nodeobj1 = nodeobjs
                node1_lnk = App.ActiveDocument.getObjectsByLabel(nodeobjs.node_name)[0]
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
            if linkedsub[0:-1] == posLCS1_str:
                posLCS1 = linkedobj1.getObject(linkedsub[0:-1])
            if linkedsub[0:-1] == rotLCS1_str:
                rotLCS1 = linkedobj1.getObject(linkedsub[0:-1])
        # fixed position and rotation LCS
        posLCSf_str = self.fixed_LCS_pos_box.currentText()
        rotLCSf_str = self.fixed_LCS_rot_box.currentText()
        modelobj = App.ActiveDocument.Model
        for modsub in modelobj.getSubObjects():
            if modsub[0:-1] == posLCSf_str:
                posLCSf = modelobj.getObject(modsub[0:-1])
            if modsub[0:-1] == rotLCSf_str:
                rotLCSf = modelobj.getObject(modsub[0:-1])
        App.Console.PrintMessage(" Accept3: " + rotLCSf.Name +"\n")

        # get placements for node 1 position and rotation LCSs
        posLCS1_pl = node1_lnk.Placement.multiply(posLCS1.Placement)
        rotLCS1_pl = node1_lnk.Placement.multiply(rotLCS1.Placement)
        App.Console.PrintMessage(" orient2")
        # make FreeCAD placement matrix from node1 position and orientation matrix
        if nodeobj1.orientation_des == 'euler321':
            rotz = App.Units.parseQuantity("(180/pi)*" + str(nodeobj1.orientation[0][0]))
            roty = App.Units.parseQuantity("(180/pi)*" + str(nodeobj1.orientation[0][1]))
            rotx = App.Units.parseQuantity("(180/pi)*" + str(nodeobj1.orientation[0][2]))
            node1_pl = App.Placement(nodeobj1.position, App.Rotation(rotz, roty, rotx))
            App.Console.PrintMessage(" orient1: " + str(node1_pl))
        node1_pl_inv = node1_pl.inverse()
        App.Console.PrintMessage(" orient2")
        # get placements for fixed position and rotation LCSs
        posLCSf_pl = posLCSf.Placement
        rotLCSf_pl = rotLCSf.Placement

        # create joint object
        num_joints = len(App.ActiveDocument.Joints.getSubObjects()) + 1
        new_joint = App.ActiveDocument.Joints.newObject("App::FeaturePython","Joint" + str(num_joints))
        MBDyn_objects.MBDynJoints.FC_totalpinjoint(new_joint)
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

        # set fixed joint parameters
        new_joint.positionf = posLCSf_pl.Base
        new_joint.pos_orientation_desf = 'xy'
        new_joint.pos_orientationf = [App.Vector(posLCSf_pl.Matrix.A11, posLCSf_pl.Matrix.A21, posLCSf_pl.Matrix.A31),
                                      App.Vector(posLCSf_pl.Matrix.A12, posLCSf_pl.Matrix.A22, posLCSf_pl.Matrix.A32),
                                      App.Vector(0,0,0)]
        new_joint.rot_orientation_desf = 'xy'
        new_joint.rot_orientationf = [App.Vector(rotLCSf_pl.Matrix.A11, rotLCSf_pl.Matrix.A21, rotLCSf_pl.Matrix.A31),
                                      App.Vector(rotLCSf_pl.Matrix.A12, rotLCSf_pl.Matrix.A22, rotLCSf_pl.Matrix.A32),
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
        node1_str = self.node1_box.currentText()
        for linksobj in App.ActiveDocument.getLinksTo():
            if linksobj.Name == node1_str:
                linkedobj = linksobj.getLinkedObject()
                for linkedsub in linkedobj.getSubObjects():
                    if linkedobj.getObject(linkedsub[0:-1]).TypeId == 'PartDesign::CoordinateSystem':
                        self.node1_LCS_pos_box.addItem(linkedsub[0:-1])
                        self.node1_LCS_rot_box.addItem(linkedsub[0:-1])


    def set_fixed(self):
        ''' populates the fixed position and rotation orientation combo boxes'''
        self.fixed_LCS_pos_box.clear()
        self.fixed_LCS_rot_box.clear()
        modelobj = App.ActiveDocument.Model
        for subobj in modelobj.getSubObjects():
            if modelobj.getObject(subobj[0:-1]).TypeId == 'PartDesign::CoordinateSystem':
                self.fixed_LCS_pos_box.addItem(subobj[0:-1])
                self.fixed_LCS_rot_box.addItem(subobj[0:-1])


Gui.addCommand('total_pinjoint_cmd', total_pinjoint_cmd())
