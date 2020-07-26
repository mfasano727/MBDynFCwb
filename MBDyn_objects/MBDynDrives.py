import numpy as np
import math
import FreeCAD as App
import MBDyn_objects.MBDynJoints
from  MBDyn_utilities.MBDyn_funcs import *


class MBDynconstantDrive:
    '''MBDyn constant drive caller feature pyhton object class'''
    def __init__(self, obj):
        obj.addProperty("App::PropertyFloat","const_coef","MBDynconstantDrive","initial time for ramp drive").const_coef

        obj.Proxy = self
        self.Object = obj

    def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
                Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
                to return a tuple of all serializable objects or None.'''
        return None

    def __setstate__(self,state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
                Since no data were serialized nothing needs to be done here.'''
        return None

    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        App.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        App.Console.PrintMessage("Recompute Python MBDynInitialValue feature\n")

    def onDocumentRestored(self, fp):
        '''restores feature python object when document is read'''
        self.Object = fp

    def writeDrive(self):
        return "const, {}".format(self.Object.const_coef)


class MBDynRampDrive:
    '''MBDyn ramp drive caller feature pyhton object class'''
    def __init__(self, obj):
        obj.addProperty("App::PropertyInteger","drive_label","_MBDynRampDrive","label for ramp drive").drive_label
        obj.addProperty("App::PropertyString","drive_name","_MBDynRampDrive","name for ramp drive").drive_name
        obj.addProperty("App::PropertyFloat","initial_time","_MBDynRampDrive","initial time for ramp drive").initial_time
        obj.addProperty("App::PropertyFloat","final_time","_MBDynRampDrive","final time for ramp drive").final_time
        obj.addProperty("App::PropertyFloat","initial_value","_MBDynRampDrive","initial value for ramp drive").initial_value
        obj.addProperty("App::PropertyFloat","slope","_MBDynRampDrive","slope for ramp drive").slope

        obj.Proxy = self
        self.Object = obj

    def __getstate__(self):
        '''When saving the document this object gets stored using Python's json module.\
                Since we have some un-serializable parts here -- the Coin stuff -- we must define this method\
                to return a tuple of all serializable objects or None.'''
        return None

    def __setstate__(self,state):
        '''When restoring the serialized object from document we have the chance to set some internals here.\
                Since no data were serialized nothing needs to be done here.'''
        return None

    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        App.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        App.Console.PrintMessage("Recompute Python MBDynInitialValue feature\n")

    def onDocumentRestored(self, fp):
        '''restores feature python object when document is read'''
        self.Object = fp

    def writeDrive(self):
        drive_line = "ramp, {}, {}, {}, {}".format(self.Object.slope, self.Object.initial_time, self.Object.final_time, self.Object.initial_value)
        return drive_line


class MBDynTemplateDrive:

    def __init__(self, tpl_type, *args):
        self.tpl_type = tpl_type
        self.reference = None
        self.args = list(args)

        if tpl_type == "single":
            self.single_entity = args[0]
            self.single_drive_caller = args[1]

        elif tpl_type == "component":
            self.component_drive_caller = list(args)
            self.component_type = None

        elif tpl_type == "array":
            self.num_template_drive_callers = args[0]
            self.array_drive_caller = list(args[1:])

    def setReference(self, reference):
        self.reference = reference

    def getReference(self):
        return self.reference

    def setSingleEntity(self, single_entity):
        self.single_entity  = single_entity

    def getSingleEntity(self):
        return self.single_entity

    def setSingleDriveCaller(self, single_drive_caller):
        self.single_drive_caller = single_drive_caller

    def getSingleDriveCaller(self):
        return self.single_drive_caller

    def setComponentDriveCaller(self, component_drive_caller):
        self.component_drive_caller = component_drive_caller

    def getComponentDriveCaller(self):
        return self.component_drive_caller

    def setComponentType(self, component_type):
        self.component_type = component_type

    def getComponentType(self):
        return self.component_type

    def setNumTemplateDriveCallers(self, num_template_drive_callers):
        self.num_template_drive_callers = num_template_drive_callers

    def getNumTemplateDriveCallers(self):
        return self.num_template_drive_callers

    def setArrayDriveCaller(self, array_drive_caller):
        self.array_drive_caller = array_drive_caller

    def getArrayDriveCaller(self):
        return self.array_drive_caller

    def writeDrive(self):
        if self.tpl_type == "null":
            drive_line = "null"

        elif self.tpl_type == "single":
            drive_line = "single, {}, {}".format(self.single_entity.writeVector(), self.single_drive_caller.writeDrive())

        elif self.tpl_type == "component":
            if self.component_type == None:
                drive_line = "component"
                for k in self.component_drive_caller:
                    if k == "inactive":
                        drive_line = drive_line + ", " + "inactive"
                    else:
                        drive_line = drive_line + ",\n                  " + k.writeDrive()

            else:
                drive_line = "component, {}".format(self.component_type)
                for k in self.component_drive_caller:
                    drive_line = drive_line + ",\n                   " + k.writeDrive()

        elif self.tpl_type == "array":
            drive_line = "array, {}".format(self.num_template_drive_callers)
            for k in self.array_drive_caller:
                drive_line = drive_line + ", " + k.writeDrive()

        return drive_line
