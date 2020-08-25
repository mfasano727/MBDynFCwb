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
from  MBDyn_utilities.MBDyn_funcs import find_joint_label
from  MBDyn_utilities.place_funcs import calc_placement
from PySide2 import QtCore, QtGui, QtWidgets
import FreeCAD as App
import FreeCADGui as Gui



from   MBDyn_guitools.dia_clamp_joint import Ui_dia_clamp_joint

class clamp_joint_cmd(QtWidgets.QDialog, Ui_dia_clamp_joint):
    """MBD create inline joint command"""
    def __init__(self):
        super(clamp_joint_cmd, self).__init__()
        self.setupUi(self)

    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'clamp_icon.svg'),
                'MenuText': "create clamp joint",
                'ToolTip': "input clamp joint parameters"}
    def Activated(self):
        """Do something here"""
        self.node_1_Box.clear()
        if App.ActiveDocument.getObject('Nodes') != None :
            for nodeobj in App.ActiveDocument.Nodes.Group:
                self.node_1_Box.addItem(nodeobj.node_name)

        # define conections for dialog widgets
        self.node_1_Box.currentIndexChanged.connect(self.fill_node1_LCS_Box)
        self.fill_node1_LCS_Box()


        self.show()

        App.Console.PrintMessage(" Activated: " + "\n")

        return

    def IsActive(self):
        if App.ActiveDocument == None:
            return False
        else:
            return True


    def accept(self):

        #  get node objects chosen
        for nodeobjs in App.ActiveDocument.Nodes.Group:
            App.Console.PrintMessage(" node1:")
            if nodeobjs.node_name  == self.node_1_Box.currentText():
                nodeobj1 = nodeobjs

        # get LCS chasen for each node
        nodeLCS1_str = self.node_1_LCS.currentText()

        # get labels for link objects for nodes
        str_lst = nodeobj1.node_name.split("|")
        linkobj1_str = str_lst[0]

        # create joint object
        num_joints =  find_joint_label()
        new_joint = App.ActiveDocument.Joints.newObject("App::FeaturePython","Joint" + str(num_joints))
        MBDyn_objects.MBDynJoints.MBDynClamp(new_joint)
        new_joint.ViewObject.Proxy = 0

        new_joint.joint_label = num_joints


        new_joint.node1_label = nodeobj1.node_label

        # if objects are App::Link use linkednoject otherwise use object itself
        linkobj1 = App.ActiveDocument.getObjectsByLabel(linkobj1_str)[0]
        if hasattr(linkobj1, "LinkedObject" ):
            linkedobj1 = linkobj1.LinkedObject
        else:
            linkedobj1 = linkobj1


        # get the LCS objects of the linked object
        for subLCSs in linkedobj1.getSubObjects():
            if linkedobj1.getObject(subLCSs[0:-1]).Label == nodeLCS1_str:
                linkedLCS1 = linkedobj1.getObject(subLCSs[0:-1])

        App.Console.PrintMessage(" linkobj2: " + linkedLCS1.Label)
        # set position of joint
        linkedLCS1_pos = linkedLCS1.Placement.Base
        inv_linkobj1_pl = linkobj1.Placement.inverse()
        new_joint.position1 = linkedLCS1_pos - inv_linkobj1_pl.multVec(nodeobj1.position)


        linkobj1_pl = linkobj1.Placement
        linkLCS1_pl = linkobj1_pl.multiply(linkedLCS1.Placement)


        new_joint.orientation_des1 = "xz"
        mat = inv_linkobj1_pl.multiply(linkLCS1_pl).Matrix
        new_joint.orientation1 = [App.Vector(mat.A11,mat.A21,mat.A31).normalize(), App.Vector(0,0,0), App.Vector(mat.A13,mat.A23,mat.A33).normalize()]

        self.done(1)

    def reject(self):
        self.done(0)



    def fill_node1_LCS_Box(self):
        '''fills LCS_Box combobox with LCSs of selected part of node'''

        self.node_1_LCS.clear()
        node1_text = self.node_1_Box.currentText()
        node1_str = node1_text.split("|")[0]
        linkobj = App.ActiveDocument.getObjectsByLabel(node1_str)[0]
        if hasattr(linkobj, "LinkedObject" ):
            linkedobj = linkobj.getLinkedObject()
        else:
            linkedobj = linkobj
        for linkedsub in linkedobj.getSubObjects():
            linkedsubobj = linkedobj.getObject(linkedsub[0:-1])
            if linkedsubobj.TypeId == 'PartDesign::CoordinateSystem':
                self.node_1_LCS.addItem(linkedsubobj.Label)


    def check_valid(self):
         pass
#        teststr = self.sender()
#        if self.valid.validate(teststr.text(),0) != QtGui.QValidator.Acceptable:
#           self.sender.setText("0.0")

Gui.addCommand('clamp_joint_cmd', clamp_joint_cmd())
