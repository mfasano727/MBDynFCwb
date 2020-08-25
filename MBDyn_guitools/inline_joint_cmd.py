#!/usr/bin/env python3
# coding: utf-8
#
# revpin_joint_cmd.py

import os
import sys
from math import pi
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


from   MBDyn_guitools.dia_inline_joint import Ui_dia_inline_joint

class inline_joint_cmd(QtWidgets.QDialog, Ui_dia_inline_joint):
    """MBD create inline joint command"""
    def __init__(self):
        super(inline_joint_cmd, self).__init__()
        self.setupUi(self)

    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'inline_icon.svg'),
                'MenuText': "create inline joint",
                'ToolTip': "input inline joint parameters"}
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

        # define conections for dialog widgets
        self.node_1_Box.currentIndexChanged.connect(self.fill_node1_LCS_Box)
        self.node_2_Box.currentIndexChanged.connect(self.fill_node2_LCS_Box)
        self.fill_node1_LCS_Box()
        self.fill_node2_LCS_Box()

        self.line_def_Box.currentIndexChanged.connect(self.choose_line_dir)
        self.choose_line_dir()

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

        # get LCS chasen for each node
        nodeLCS1_str = self.node_1_LCS.currentText()
        nodeLCS2_str = self.node_2_LCS.currentText()

        # get labels for link objects for nodes
        str_lst = nodeobj1.node_name.split("|")
        linkobj1_str = str_lst[0]
        str_lst = nodeobj2.node_name.split("|")
        linkobj2_str = str_lst[0]

        # create joint object
        num_joints =  find_joint_label()
        new_joint = App.ActiveDocument.Joints.newObject("App::FeaturePython","Joint" + str(num_joints))
        MBDyn_objects.MBDynJoints.MBDynInline(new_joint)
        new_joint.ViewObject.Proxy = 0

        new_joint.joint_label = num_joints


        new_joint.node1_label = nodeobj1.node_label
        new_joint.node2_label = nodeobj2.node_label
        App.Console.PrintMessage(" node1: "+ linkobj1_str +" node2pos: "+linkobj2_str)

        # if objects are App::Link use linkednoject otherwise use object itself
        linkobj1 = App.ActiveDocument.getObjectsByLabel(linkobj1_str)[0]
        App.Console.PrintMessage(" node1: ")
        if hasattr(linkobj1, "LinkedObject" ):
            linkedobj1 = linkobj1.LinkedObject
        else:
            linkedobj1 = linkobj1
        linkobj2 = App.ActiveDocument.getObjectsByLabel(linkobj2_str)[0]
        if hasattr(linkobj2, "LinkedObject" ):
            linkedobj2 = linkobj2.LinkedObject
        else:
            linkedobj2 = linkobj2
        App.Console.PrintMessage(" node2: "+ linkedobj1.Label +" node2: "+linkedobj2.Label)

        # get the LCS objects of the linked object
        for subLCSs in linkedobj1.getSubObjects():
            if linkedobj1.getObject(subLCSs[0:-1]).Label == nodeLCS1_str:
                linkedLCS1 = linkedobj1.getObject(subLCSs[0:-1])
        for subLCSs in linkedobj2.getSubObjects():
            App.Console.PrintMessage(" linkobj: " + linkedobj2.getObject(subLCSs[0:-1]).Label)
            if linkedobj2.getObject(subLCSs[0:-1]).Label == nodeLCS2_str:
                linkedLCS2 = linkedobj2.getObject(subLCSs[0:-1])
        App.Console.PrintMessage(" linkobj2: " + linkedLCS2.Label)
        # set position and offset of inline joint
        linkedLCS1_pos = linkedLCS1.Placement.Base
        App.Console.PrintMessage(" linkobj: "+str(linkedLCS1_pos))
        inv_linkobj1_pl = linkobj1.Placement.inverse()
        new_joint.position1 = linkedLCS1_pos - inv_linkobj1_pl.multVec(nodeobj1.position)
        App.Console.PrintMessage(" lcs1pos: "+str(linkedLCS1_pos)+" node1pos: "+str(inv_linkobj1_pl))
        linkedLCS2_pos = linkedLCS2.Placement.Base
        App.Console.PrintMessage(" test")

        inv_linkobj2_pl = linkobj2.Placement.inverse()
        App.Console.PrintMessage(" test")
        new_joint.offset2 = linkedLCS2_pos - inv_linkobj2_pl.multVec(nodeobj2.position)
        App.Console.PrintMessage(" lcs2pos: "+str(linkedLCS2_pos)+" node2pos: "+str(inv_linkobj2_pl))

        # get plasements of LCSs needed to calculate  orientation matrix of inline joint
#        linkedLCS1_pl = linkedLCS1.Placement
#        linkedLCS2_pl = linkedLCS2.Placement
        linkobj1_pl = linkobj1.Placement
        linkLCS1_pl = linkobj1_pl.multiply(linkedLCS1.Placement)
        linkobj2_pl = linkobj2.Placement
        linkLCS2_pl = linkobj2_pl.multiply(linkedLCS2.Placement)
        linkLCS1_mat = linkLCS1_pl.Matrix
        App.Console.PrintMessage(" linkLCS1_mat: "+str(linkLCS1_mat))

        # make FreeCAD placement matrix from node1 position and orientation matrix
        node1_pl = calc_placement(nodeobj1.position, nodeobj1.orientation, nodeobj1.orientation_des)
        App.Console.PrintMessage(" linkLCS: "+str(linkLCS2_pl)+" node1_pl "+str(node1_pl.Matrix))

        if self.line_def_Box.currentIndex() == 0:   # z-axis is line from node1 LCS to node2 LCS
            #  find the orientation matrix for node 1.  Z axis is in direction from position 1( LCS1) to offset(lCS2)
            line_vec = linkLCS1_pl.Base - linkLCS2_pl.Base
            App.Console.PrintMessage(" line: z"+str(line_vec))
            # find an axis not in line with line_vec for an other part of the orientation matrix
            # columns of placement matrix are orientation axies
            if line_vec.getAngle(App.Vector(linkLCS1_mat.A11,linkLCS1_mat.A21,linkLCS1_mat.A31)) > pi/6 and line_vec.getAngle(App.Vector(linkLCS1_mat.A11,linkLCS1_mat.A21,linkLCS1_mat.A31)) < pi*.7:
                x_vec = line_vec.cross(App.Vector(linkLCS1_mat.A11,linkLCS1_mat.A21,linkLCS1_mat.A31))
            elif line_vec.getAngle(App.Vector(linkLCS1_mat.A12,linkLCS1_mat.A22,linkLCS1_mat.A32)) > pi/6 and line_vec.getAngle(App.Vector(linkLCS1_mat.A12,linkLCS1_mat.A22,linkLCS1_mat.A32)) < pi*.7:
                x_vec = line_vec.cross(App.Vector(linkLCS1_mat.A12,linkLCS1_mat.A22,linkLCS1_mat.A32))
            App.Console.PrintMessage(" line: x"+str(x_vec))
            x_vec_rel_node1 = node1_pl.inverse().Rotation.multVec(x_vec) # x vector relative node 1
            App.Console.PrintMessage(" node_inv:"+str( node1_pl.inverse().Matrix))
            line_vec_rel_node1 = node1_pl.inverse().Rotation.multVec(line_vec) # line vector relative node 1
            new_joint.orientation_des1 = "xz"
            new_joint.orientation1 = [x_vec_rel_node1.normalize(), App.Vector(0,0,0), line_vec_rel_node1.normalize()]
            App.Console.PrintMessage(" line2: x "+str(x_vec)+"  z "+str(line_vec))
            App.Console.PrintMessage(" line2_rel: x "+str(x_vec_rel_node1)+"  z "+str(line_vec_rel_node1))
        else: # z-axis will be chosen axis of node 1 LCS
            new_joint.orientation_des1 = "xz"
            if self.node1_axis_Box.currentText() == "X":
                App.Console.PrintMessage(" line3: x "+str(App.Vector(linkLCS1_mat.A13,linkLCS1_mat.A23,linkLCS1_mat.A33).normalize()))
                App.Console.PrintMessage(" yvec: "+str(App.Vector(linkLCS1_mat.A12,linkLCS1_mat.A22,linkLCS1_mat.A32).normalize()))
                linkLCS1_mat_roty = linkLCS1_mat.rotateY(-pi/2.0)
                line_vec = App.Vector(linkLCS1_mat.A13,linkLCS1_mat.A23,linkLCS1_mat.A33).normalize()
                x_vec = App.Vector(linkLCS1_mat.A11,linkLCS1_mat.A21,linkLCS1_mat.A31).normalize()
                App.Console.PrintMessage(" line4: x "+str(x_vec)+" line4 z "+str(line_vec))
            if self.node1_axis_Box.currentText() == "Y":
                linkLCS1_mat_roty = linkLCS1_mat.rotateX(pi/2.0)
                line_vec = App.Vector(linkLCS1_mat.A13,linkLCS1_mat.A23,linkLCS1_mat.A33).normalize()
                x_vec = App.Vector(linkLCS1_mat.A11,linkLCS1_mat.A21,linkLCS1_mat.A31).normalize()
            if self.node1_axis_Box.currentText() == "Z":
                line_vec = App.Vector(linkLCS1_mat.A13,linkLCS1_mat.A23,linkLCS1_mat.A33).normalize()
                x_vec = App.Vector(linkLCS1_mat.A11,linkLCS1_mat.A21,linkLCS1_mat.A31).normalize()
            x_vec_rel_node1 = node1_pl.inverse().Rotation.multVec(x_vec) # x vector relative node 1
            line_vec_rel_node1 = node1_pl.inverse().Rotation.multVec(line_vec) # line vector relative node 1
            new_joint.orientation1 = [x_vec_rel_node1.normalize(), App.Vector(0,0,0), line_vec_rel_node1.normalize()]

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


    def choose_line_dir(self):
        if self.line_def_Box.currentIndex() == 0:
            self.node1_axis_Box.setVisible(False)
            self.LCS_axis_label.setVisible(False)
        else:
            self.node1_axis_Box.setVisible(True)
            self.LCS_axis_label.setVisible(True)


    def check_valid(self):
         pass
#        teststr = self.sender()
#        if self.valid.validate(teststr.text(),0) != QtGui.QValidator.Acceptable:
#           self.sender.setText("0.0")

Gui.addCommand('inline_joint_cmd', inline_joint_cmd())
