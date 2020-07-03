#!/usr/bin/env python3
# coding: utf-8
#
# body_sel_cmd.py

import os
import sys
import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')

from PySide2 import QtCore, QtGui, QtWidgets
import FreeCADGui as Gui
import FreeCAD as App
import Part
import math, re

from  MBDyn_utilities.MBDyn_funcs import check_solid
import MBDyn_objects.model_so  # MBDyne model with scripted objects
from MBDyn_guitools.dia_body_sel import Ui_dia_body_sel


class body_sel_cmd(QtWidgets.QDialog,  Ui_dia_body_sel):
    """MBD body select command; objects that have solid shape type as rigid bodies."""

    def __init__(self):
        super(body_sel_cmd, self).__init__()
        self.setupUi(self)

    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'rigidbody_icon.svg'),
                'MenuText': "body select",
                'ToolTip': "select body"}
    def Activated(self):
        """Do something here"""
#        ivpDia = IVP_dialog()
#         look for links to solid objects in document and list in combo box
        self.body_list.clear()
        for modlink in App.ActiveDocument.Model.getSubObjects():
            bodlink = App.ActiveDocument.Model.getObject(modlink[0:-1])
            if hasattr(bodlink, 'LinkedObject'):
                modbod = bodlink.LinkedObject
                for modbod_nm in modbod.getSubObjects():
                    modbod_sub = modbod.getObject(modbod_nm[0:-1])
                    if check_solid(modbod_sub):
                        self.body_list.addItem(bodlink.Label)
                '''
                for modbod_nm in modbod.getSubObjects():
                    modbod_sub = modbod.getObject(modbod_nm[0:-1])
                    if check_solid(modbod_sub):
                        App.Console.PrintMessage(" solid:3 " + modbod_sub.Name + "\n")
                        in_list_flag = False
                        for mod_sub_in in modbod_sub.InList:
                            App.Console.PrintMessage(" solid: " + mod_sub_in.Name + "\n")
                            if check_solid(mod_sub_in):
                                App.Console.PrintMessage(" solid2: " + mod_sub_in.Name + "\n")
                                in_list_flag = True
                        if in_list_flag == False:
                            self.body_list.addItem(bodlink.Label)
                '''
        self.show()
        App.Console.PrintMessage(" Activated: " + "\n")

        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional.
        """
        return True
    def accept(self):
        App.Console.PrintMessage(" Accept: " + "\n")
        for linkedparts in App.ActiveDocument.Model.getSubObjects():
            App.Console.PrintMessage(" Accept:2 "+ "\n")
            partlink =  App.ActiveDocument.Model.getObject(linkedparts[0:-1])
            App.Console.PrintMessage(" Accept: " + partlink.Label +"\n")
            if partlink.Label == self.body_list.currentText():
                choose_body = partlink  # part object chosen from combobox

        tempstring = "body_" + self.body_list.currentText()
        App.Console.PrintMessage(" Accept: " + tempstring + "\n")

        # create body element scripted object
        new_body = App.ActiveDocument.Bodies.newObject("App::FeaturePython", tempstring)
        MBDyn_objects.model_so.MBDynRigidBody(new_body)
        new_body.ViewObject.Proxy = 0

        #   create strctural node for ridgid body
        num_nodes = len(App.ActiveDocument.Nodes.getSubObjects()) + 1
        new_node = App.ActiveDocument.Nodes.newObject("App::FeaturePython", self.body_list.currentText()+ "_node_" + str(num_nodes))
        MBDyn_objects.model_so.MBDynStructuralNode(new_node)
        new_node.ViewObject.Proxy = 0
        num_nodes = len(App.ActiveDocument.Nodes.getSubObjects())
        App.Console.PrintMessage(" node1test ")

         # set new node properties
        new_node.node_label = num_nodes
        new_node.struct_type = "dynamic"
        object_chosenbod = choose_body.LinkedObject
        App.Console.PrintMessage(" node2test ")
        for subobjs in object_chosenbod.getSubObjects():
            partsub = object_chosenbod.getObject(subobjs[0:-1])
            App.Console.PrintMessage(" node2test ")
            if hasattr(partsub, 'Shape'):
                App.Console.PrintMessage(" node3test ")
                if partsub.Shape.ShapeType == 'Solid' or  partsub.Shape.ShapeType == 'Compound':
                    chosenbody = partsub
        App.Console.PrintMessage(" node2test "+ str(chosenbody.Shape.CenterOfMass.z))

        new_node.position = choose_body.Placement.multVec(chosenbody.Shape.CenterOfMass)  #  node is at center of mass

         #  orientation matrix is placement rotation in euler angles in radians
        orient = App.Vector(0,0,0)
#        App.Console.PrintMessage(" node2test " +srt(chosenbody[0].Placement.Rotation.toEuler()[0]))
        orient.x = App.Units.parseQuantity("(pi/180)*" + str(choose_body.Placement.Rotation.toEuler()[0])) # App.Units.parseQuantity("(pi/180)*" + srt(chosenbody[0].Placement.Rotation.toEuler()[0]))
        orient.y = App.Units.parseQuantity("(pi/180)*" + str(choose_body.Placement.Rotation.toEuler()[1]))
        orient.z = App.Units.parseQuantity("(pi/180)*" + str(choose_body.Placement.Rotation.toEuler()[2]))
        App.Console.PrintMessage(" node2test " + str(orient))
        new_node.orientation_des = "euler321"
        new_node.orientation = [orient, App.Vector(0.0, 0.0, 0.0), App.Vector(0.0, 0.0, 0.0)]
        new_node.vel = App.Vector(0, 0, 0)
        new_node.ang_vel = App.Vector(0, 0, 0)

        #  set new body properties
        new_body.body_obj_label = self.body_list.currentText()
        new_body.label = len(App.ActiveDocument.Bodies.getSubObjects())
        new_body.node_label = num_nodes
        body_density = 0.01  #  in g/mm**3
        new_body.mass = chosenbody.Shape.Volume * body_density  # volume usually mm**3
        new_body.com_offset = App.Vector(0, 0, 0)
        # calculate moment of inertia with placemrnt matrix = identity
#        placement_mat = chosenbody[0].Placement
#        chosenbody.Placement.Matrix.unity()
        App.Console.PrintMessage(" matrix test ")
        matr_of_inertia = chosenbody.Shape.MatrixOfInertia  # units of IM in FreeCad is L**5  L usally in mm
#        chosenbody.Placement = placement_mat
        # matrix is a list of three FreeCad vector
        new_body.inertia_matrix = [App.Vector(matr_of_inertia.A11, matr_of_inertia.A12, matr_of_inertia.A13)*body_density,
                                   App.Vector(matr_of_inertia.A21, matr_of_inertia.A22, matr_of_inertia.A23)*body_density,
                                   App.Vector(matr_of_inertia.A31, matr_of_inertia.A32, matr_of_inertia.A33)*body_density]
        tol_for_diag = 0.0000001   # if off diaganal elements in MI matrix is less than tol_for_diag make matrix diag
        if matr_of_inertia.A12 < tol_for_diag and matr_of_inertia.A13 < tol_for_diag and matr_of_inertia.A23 < tol_for_diag:
            new_body.matrix_type = "diag"
        else:
            new_body.matrix_type = "sym"
        #  set node name to new_body.body_obj_label + num of nodes on body
        new_node.node_name = new_body.body_obj_label

        self.done(1)

    def reject(self):
        self.done(0)


Gui.addCommand('body_sel_cmd', body_sel_cmd())
