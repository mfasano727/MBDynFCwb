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
import time

# import MBDyn_objects.model_so  # MBDyne model with scripted objects
from  MBDyn_utilities.MBDyn_funcs import calc_placement, check_solid
from MBDyn_guitools.dia_postproc import Ui_dia_postporc

class postproc_cmd(QtWidgets.QDialog,  Ui_dia_postporc):
    """MBD post process command; reads output and animates FreeCad model."""
    def __init__(self):
        super(postproc_cmd, self).__init__()        
        self.setupUi(self)
#        self.timer = QtCore.QTimer()  # qt timer will be used
    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'postproc_icon.svg'),
                'MenuText': "post process",
                'ToolTip': "post process"}
    def Activated(self):
        """Do something here"""
        self.output_path.clear()
        self.sel_out_path.clicked.connect(self.get_file)
        self.show()
        App.Console.PrintMessage(" Activated now: " + "\n")
        
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True
    def accept(self):
        App.Console.PrintMessage(" Accept1: " + "\n")
        
        filepath = self.output_path.text()
        dirlist = os.path.split(filepath)
        outpath = dirlist[0]
        outfile = dirlist[1][0:-4]
        
        outfile_mov = outfile + ".mov"
        outfile_jnt = outfile + ".jnt"
        outfile_ine = outfile + ".ine"
        outfile_out = outfile + ".out"
        path_outfile_mov = os.path.join(outpath, outfile_mov)
        path_outfile_out = os.path.join(outpath, outfile_out)
        path_outfile_jnt = os.path.join(outpath, outfile_jnt)
        App.Console.PrintMessage("filename: Accept " + path_outfile_mov)
        
        num_nodes = len(App.ActiveDocument.Nodes.Group)
        num_bodies = len(App.ActiveDocument.Bodies.Group)
        num_joints = len(App.ActiveDocument.Joints.Group)
        App.Console.PrintMessage("filename: Accept2 " )
        node_list = [] # keep a list of nodes for bodies
        bods = {} # bods is a dictionary with node label key and FreeCAD object  as the value
        bods_cm = {}  # bods is a dictionary with node label key and center of mass vector of linked object  as the value 
        bods_exp ={} # holds objects expressions temporarily 
        for body_obj in App.ActiveDocument.Bodies.Group:
            body_ob = App.ActiveDocument.getObjectsByLabel(body_obj.body_obj_label)
            node_list.append(body_obj.node_label)
            bods[body_obj.node_label] = body_ob[0]
            modbod = bods[body_obj.node_label].LinkedObject
            for modbod_nm in modbod.getSubObjects():  # find linked object subobject that is solid.
                App.Console.PrintMessage("filename: Accept4 " + modbod_nm)
                modbod_sub = modbod.getObject(modbod_nm[0:-1])
                if check_solid(modbod_sub):
                    App.Console.PrintMessage("filename: Accept3 " + modbod_sub.Name)
                    bods_cm[body_obj.node_label] = App.Placement(modbod_sub.Shape.CenterOfMass, App.Rotation(0,0,0))
            App.Console.PrintMessage("filename: Accept5 " + str(bods_cm[body_obj.node_label]))
        
        # set up to open and read MBDyn output files
#        nodes_lst = []  # list of nodes in MBDyn mov file
        node_pos = App.Vector(0,0,0)
        node_orient = App.Vector(0,0,0)
        node_vel = App.Vector(0,0,0)
        node_angvel = App.Vector(0,0,0) 
        node_pl = {}  # a dictionary of placements to hold for each node
        bod_ee = {}  # hold ExpressionEngine for links temporarily for animation.
        for node_l in node_list:
            node_pl[node_l] = App.Placement(node_pos, App.Rotation(0,0,0))
            bod_ee[node_l] = bods[node_l].ExpressionEngine.copy()
        # set up timer for animation.
#        timer = QtCore.QTimer()
#        timer.timeout.connect(self.update)

        timestep = App.ActiveDocument.initial_values.time_step * 2
        timeout_flag = False

        

        movfile = open(path_outfile_mov, 'r')
        outfile = open(path_outfile_out, 'r')
        outline = outfile.readline()  # read 3 line header of .out file
        outline = outfile.readline()
        outline = outfile.readline()
        movline = movfile.readline()
        App.Console.PrintMessage("filename: Accept2 " + str(timestep))
        
        while movline != '':
            timestart = time.perf_counter()  # start time before reading each node block.
            outline = outfile.readline()
            outline_list = outline.split(' ')
            
            for i  in range(num_nodes):  #  read block to get motion info for each node at each step
                
                line_list = movline.split(' ')
                node = int(line_list[7])
                node_pos.x = float(line_list[8]); node_pos.y = float(line_list[9]); node_pos.z = float(line_list[10])
                node_orient.z = float(line_list[11]); node_orient.y = float(line_list[12]); node_orient.x = float(line_list[13])
#                node_vel.x = float(line_list[14]); node_vel.y = float(line_list[15]); node_vel.z = float(line_list[16])
#                node_angvel.x = float(line_list[17]); node_angvel.y = float(line_list[18]); node_angvel.z = float(line_list[19])
                node_pl[node] =  App.Placement(node_pos, App.Rotation(node_orient.x,node_orient.y,node_orient.z)) #calc_placement(node_pos, node_orient) 
                movline = movfile.readline()

            # this is where the parts get placed with the lines read from MBDyn mov file.
            timeend = time.perf_counter()
            while (timeend - timestart) <= timestep:  #wait for time step to elapse
                 timeend = time.perf_counter()
            for node_l in node_list:
                bods[node_l].Placement = node_pl[node_l].multiply(bods_cm[node_l].inverse())
            Gui.updateGui()   

        App.Console.PrintMessage("end animation")
        movfile.close()
        outfile.close()
        
        self.done(1)

    def reject(self):
        self.done(0)

    def get_file(self):        
        outfilename = QtWidgets.QFileDialog.getOpenFileName(self,"get MBDyn output file","","MBDyn_output (*.mov *.jnt *.ine *.out)")[0]  #tr("MBDyn_output (*.mov *.jnt *.ine *.out)"
#        outlocation = QDir.toNativeSeparators(outlocation)
        
#        outfilename = "C:\\Users\\Matt\\Documents\\freecad\\pend new\\New folder\\input_AS4_7.mov"
        if os.sep=='\\':
            outfilename=outfilename.replace('/', '\\')

        self.output_path.setText(outfilename)
   

Gui.addCommand('postproc_cmd', postproc_cmd())