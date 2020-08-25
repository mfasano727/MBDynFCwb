#!/usr/bin/env python3
# coding: utf-8
#
# prismatic_joint_cmd.py

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



from   MBDyn_guitools.dia_prismatic_joint import Ui_dia_prismatic_joint

class prismatic_joint_cmd(QtWidgets.QDialog, Ui_dia_prismatic_joint):
    """MBD create inline joint command"""
    def __init__(self):
        super(prismatic_joint_cmd, self).__init__()
        self.setupUi(self)

    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'prismatic_icon.svg'),
                'MenuText': "create prismatic joint",
                'ToolTip': "input prismatic joint parameters"}
    def Activated(self):
        """Do something here"""
        self.node_1_Box.clear()
        if App.ActiveDocument.getObject('Nodes') != None :
            for nodeobj in App.ActiveDocument.Nodes.Group:
                self.node_1_Box.addItem(nodeobj.node_name)

        self.node_2_Box.clear()
        if App.ActiveDocument.getObject('Nodes') != None :
            for nodeobj in App.ActiveDocument.Nodes.Group:
                self.node_2_Box.addItem(nodeobj.node_name)

        # set visability for LCS comboboxes to false not needed at this time
        self.node_1_LCS_label.setVisible(False)
        self.node_2_LCS_label.setVisible(False)
        self.node_1_LCS.setVisible(False)
        self.node_2_LCS.setVisible(False)
        # define conections for dialog widgets

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
            if nodeobjs.node_name  == self.node_2_Box.currentText():
                nodeobj2 = nodeobjs
        App.Console.PrintMessage(" node1: "+ nodeobj1.node_name +" node2pos: "+nodeobj2.node_name)
        # check if both nodes are the same
        if nodeobj1.node_label == nodeobj2.node_label:
            mb = QtGui.QMessageBox()
            mb.setText("both nodes can not be the same")
            mb.exec()
            return

        # get labels for link objects for nodes
        str_lst = nodeobj1.node_name.split("|")
        linkobj1_str = str_lst[0]
        str_lst = nodeobj2.node_name.split("|")
        linkobj2_str = str_lst[0]

        # create joint object
        num_joints =  find_joint_label()
        new_joint = App.ActiveDocument.Joints.newObject("App::FeaturePython","Joint" + str(num_joints))
        MBDyn_objects.MBDynJoints.MBDynPrismatic(new_joint)
        new_joint.ViewObject.Proxy = 0

        new_joint.joint_label = num_joints


        new_joint.node1_label = nodeobj1.node_label
        new_joint.node2_label = nodeobj2.node_label
        new_joint.orientation_des1 = "xy"  # relative orientation matrix is identity matrix
        new_joint.orientation1 = [App.Vector(1,0,0), App.Vector(0,1,0), App.Vector(0,0,0)]
        new_joint.orientation_des2 = "xy"  # relative orientation matrix is identity matrix
        new_joint.orientation2 = [App.Vector(1,0,0), App.Vector(0,1,0), App.Vector(0,0,0)]

        self.done(1)

    def reject(self):
        self.done(0)


    """
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



    def fill_node2_LCS_Box(self):
        '''fills LCS_Box combobox with LCSs of selected part of node'''
        self.node_2_LCS.clear()
        node2_text = self.node_2_Box.currentText()
        node2_str = node2_text.split("|")[0]
        linkobj = App.ActiveDocument.getObjectsByLabel(node2_str)[0]
        if hasattr(linkobj, "LinkedObject" ):
            linkedobj = linkobj.getLinkedObject()
        else:
            linkedobj = linkobj
        for linkedsub in linkedobj.getSubObjects():
            linkedsubobj = linkedobj.getObject(linkedsub[0:-1])
            if linkedsubobj.TypeId == 'PartDesign::CoordinateSystem':
                self.node_2_LCS.addItem(linkedsubobj.Label)
    """



    def check_valid(self):
         pass
#        teststr = self.sender()
#        if self.valid.validate(teststr.text(),0) != QtGui.QValidator.Acceptable:
#           self.sender.setText("0.0")

Gui.addCommand('prismatic_joint_cmd', prismatic_joint_cmd())
