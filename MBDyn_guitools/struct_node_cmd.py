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
from  MBDyn_utilities.MBDyn_funcs import find_node_label
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
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'struct_node_icon.svg'),
                'MenuText': "create structural nodes command",
                'ToolTip': "create structural nodes"}
    def Activated(self):
        """Do something here"""
        # set input field for manual input with default values
        self.pos_x.setText("0") ; self.pos_y.setText("0") ; self.pos_z.setText("0")
        self.vect1_x.setText("1") ; self.vect1_y.setText("0") ; self.vect1_z.setText("0")
        self.vect2_x.setText("0") ; self.vect2_y.setText("1") ; self.vect2_z.setText("0")
        self.vect3_x.setText("0") ; self.vect3_y.setText("0") ; self.vect3_z.setText("1")
        self.vel_x.setText("0") ; self.vel_y.setText("0") ; self.vel_z.setText("0")
        self.ang_vel_x.setText("0") ; self.ang_vel_y.setText("0") ; self.ang_vel_z.setText("0")

        # set connection function for changed orientation matrix type
        self.OM_type.currentIndexChanged.connect(self.set_OM_type)
        self.OM_type.setCurrentIndex(1)
        self.OM_type.setCurrentIndex(0)

        # set connection function for changed input method type
        self.input_method_Box.currentIndexChanged.connect(self.set_input_method)
        self.input_method_Box.setCurrentIndex(1)
        self.input_method_Box.setCurrentIndex(0)

        self.part_Box.clear()
        self.part_Box.addItem('Parent Assemby')
        for modlink in App.ActiveDocument.Model.getSubObjects():
            bodlink = App.ActiveDocument.Model.getObject(modlink[0:-1])
            if hasattr(bodlink, 'LinkedObject'):
                modbod = bodlink.LinkedObject
                self.part_Box.addItem(bodlink.Label)

        # set connection function for changed part selected
        self.part_Box.setCurrentIndex(0)
        self.fill_LCS_Box()
        self.part_Box.currentIndexChanged.connect(self.fill_LCS_Box)


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
        num_nodes = find_node_label()
        # create a new node scripted object
        new_node =App.ActiveDocument.Nodes.newObject("App::FeaturePython","node" + str(num_nodes))
        MBDyn_objects.model_so.MBDynStructuralNode(new_node)
        new_node.ViewObject.Proxy = 0

        new_node.node_label = num_nodes
         # set the reference to be referred to

        new_node.struct_type = self.struct_node_type.currentText()

        if self.input_method_Box.currentIndex() == 0:  # LCS input method
            linkobj_str = self.part_Box.currentText()
            if linkobj_str == 'Parent Assemby':
                linkobj_str = 'Model'
            # if objects are App::Link use linkednoject otherwise use object itself
            linkobj = App.ActiveDocument.getObjectsByLabel(linkobj_str)[0]
            if hasattr(linkobj, "LinkedObject" ):
                linkedobj = linkobj.LinkedObject
            else:
                linkedobj = linkobj
            App.Console.PrintMessage(" accept1: " +  linkedobj.Name + "\n")

            # need to find LCS given its label
            LCStext =  self.LCS_Box.currentText()
            for subobjs in linkedobj.getSubObjects():
                lnkdLCS = linkedobj.getObject(subobjs[0:-1])
                if lnkdLCS.Label == LCStext:
                    linkedLCS = lnkdLCS

            # Placemet of the LCS chosen is the placement of the LCS of the linked part
            # multiplied by the Placement of the pat link in the Assembly
            App.Console.PrintMessage(" accept2: " +  LCStext + "\n")
            linkLCS_pl = linkobj.Placement.multiply(linkedLCS.Placement)
            App.Console.PrintMessage(" accept2: " +  self.LCS_Box.currentText() + "\n")
            App.Console.PrintMessage(" lcsbox " +str(linkLCS_pl) + "\n")
            new_node.node_name = linkobj.Label+"|"+linkedLCS.Label
            new_node.position = linkLCS_pl.Base
            new_node.orientation_des = 'xy'
            new_node.orientation = [App.Vector(linkLCS_pl.Matrix.A11, linkLCS_pl.Matrix.A21, linkLCS_pl.Matrix.A31),
                                    App.Vector(linkLCS_pl.Matrix.A12, linkLCS_pl.Matrix.A22, linkLCS_pl.Matrix.A32),
                                    App.Vector(0,0,0)]


        if self.input_method_Box.currentIndex() == 1:  # Manual input method
            new_node.node_name = "node|"+str(new_node.node_label)
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
        '''Makes only input fields needed for orientation matrix type visible'''
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


    def set_input_method(self):
        '''Makes only widgets needed for input method type visible'''
        index = self.input_method_Box.currentIndex()
        if index == 0:  # make visible only widgets for LCS input method
            self.part_Box.setVisible(True); self.part_label.setVisible(True)
            self.LCS_Box.setVisible(True); self.LCS_label.setVisible(True)
            self.pos_x_label.setVisible(False); self.pos_y_label.setVisible(False); self.pos_z_label.setVisible(False)
            self.pos_x.setVisible(False); self.pos_y.setVisible(False); self.pos_z.setVisible(False)
            self.frame.setVisible(False)
            self.OM_type.setVisible(False); self.OM_type_label.setVisible(False)
            self.OM_label.setVisible(False)
            self.col_x_label.setVisible(False); self.col_y_label.setVisible(False); self.col_z_label.setVisible(False)
            self.row_1_label.setVisible(False); self.row_2_label.setVisible(False); self.row_3_label.setVisible(False)
            self.vect1_x.setVisible(False); self.vect1_y.setVisible(False); self.vect1_z.setVisible(False)
            self.vect2_x.setVisible(False); self.vect2_y.setVisible(False); self.vect2_z.setVisible(False)
            self.vect3_x.setVisible(False); self.vect3_y.setVisible(False); self.vect3_z.setVisible(False)
            self.vel_x.setVisible(False); self.vel_y.setVisible(False); self.vel_z.setVisible(False)
            self.vel_x_label.setVisible(False); self.vel_y_label.setVisible(False); self.vel_z_label.setVisible(False)
            self.ang_vel_x.setVisible(False); self.ang_vel_y.setVisible(False); self.ang_vel_z.setVisible(False)
            self.ang_vel_x_label.setVisible(False); self.ang_vel_y_label.setVisible(False); self.ang_vel_z_label.setVisible(False)

        if index == 1:  # make visible only widgets for manual input method
            self.part_Box.setVisible(False); self.part_label.setVisible(False)
            self.LCS_Box.setVisible(False); self.LCS_label.setVisible(False)
            self.pos_x_label.setVisible(True); self.pos_y_label.setVisible(True); self.pos_z_label.setVisible(True)
            self.pos_x.setVisible(True); self.pos_y.setVisible(True); self.pos_z.setVisible(True)
            self.frame.setVisible(True)
            self.OM_type.setVisible(True); self.OM_type_label.setVisible(True)
            self.OM_label.setVisible(True)
            self.col_x_label.setVisible(True); self.col_y_label.setVisible(True); self.col_z_label.setVisible(True)
            self.row_1_label.setVisible(False); self.row_2_label.setVisible(False); self.row_3_label.setVisible(True)
            self.vect1_x.setVisible(True); self.vect1_y.setVisible(True); self.vect1_z.setVisible(True)
            self.vect2_x.setVisible(True); self.vect2_y.setVisible(True); self.vect2_z.setVisible(True)
            self.vect3_x.setVisible(True); self.vect3_y.setVisible(True); self.vect3_z.setVisible(True)
            self.vel_x.setVisible(True); self.vel_y.setVisible(True); self.vel_z.setVisible(True)
            self.vel_x_label.setVisible(True); self.vel_y_label.setVisible(True); self.vel_z_label.setVisible(True)
            self.ang_vel_x.setVisible(True); self.ang_vel_y.setVisible(True); self.ang_vel_z.setVisible(True)
            self.ang_vel_x_label.setVisible(True); self.ang_vel_y_label.setVisible(True); self.ang_vel_z_label.setVisible(True)


    def fill_LCS_Box(self):
        '''fills LCS_Box combobox with LCSs of selected part'''
        self.LCS_Box.clear()
        linkobj_str = self.part_Box.currentText()
        if linkobj_str == 'Parent Assemby':
            linkobj_str = 'Model'
        # if objects are App::Link use linkednoject otherwise use object itself
        linkobj = App.ActiveDocument.getObject(linkobj_str)

        if hasattr(linkobj, "LinkedObject" ):
            linkedobj = linkobj.LinkedObject
        else:
            linkedobj = linkobj

        for subobjs in linkedobj.getSubObjects():
            if hasattr(linkedobj.getObject(subobjs[0:-1]), 'TypeId'):
                if linkedobj.getObject(subobjs[0:-1]).TypeId == 'PartDesign::CoordinateSystem':
                    self.LCS_Box.addItem(linkedobj.getObject(subobjs[0:-1]).Label)


    def check_valid(self):
        pass
#        teststr = self.sender()
#        if self.valid.validate(teststr.text(),0) != QtGui.QValidator.Acceptable:
#           self.sender.setText("0.0")

Gui.addCommand('struct_node_cmd', struct_node_cmd())
