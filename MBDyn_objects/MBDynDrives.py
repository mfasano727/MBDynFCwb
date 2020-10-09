import numpy as np
import math
import FreeCAD as App
import MBDyn_objects.MBDynJoints
from  MBDyn_utilities.MBDyn_funcs import *

''' Drive callers object will be referenced by other MBDyn objects with a unique integer label
    given the property name drive_label '''
class MBDynconstantDrive:
    '''MBDyn constant drive caller feature python object class'''
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
    '''MBDyn ramp drive caller feature python object class'''
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
        App.Console.PrintMessage("Recompute Python MBDynRampDrive feature\n")

    def onDocumentRestored(self, fp):
        '''restores feature python object when document is read'''
        self.Object = fp

    def writeDrive(self):
        drive_line = "ramp, {}, {}, {}, {}".format(self.Object.slope, self.Object.initial_time, self.Object.final_time, self.Object.initial_value)
        return drive_line


class MBDynTemplateDrive:
    '''MBDyn template drive caller feature python object class'''
    def __init__(self):
        ''' The template drive caller calls as many other drive callers as the type(tpl_type property) calls for.
            the drive callers are referenced by list ofa unique integer labels for each drive caller (drv_calls property)
            if the drive_label is 0 there is no drive caller. References frames are also referred to by the integer label for the
            MBDyn reference object.  This object can handle 3 entity types 'Vec3', 'Vec6' and 'Mat3x3' '''
        obj.addProperty("App::PropertyInteger","drive_label","_MBDynTemplateDrive","type of template drive caller").drive_label
        obj.addProperty("App::PropertyString","drive_name","_MBDynTemplateDrive","name of template drive caller").drive_name
        obj.addProperty("App::PropertyString","tpl_typ","_MBDynTemplateDrive","type of template drive caller").tpl_type
        obj.addProperty("App::PropertyInteger","reference","_MBDynTemplateDrive","reference for drive caller").reference
        obj.addProperty("App::PropertyString","entity_typ","_MBDynTemplateDrive","type of entity for template drive caller").entity_type
        obj.addProperty("App::PropertyVectorList","entity","_MBDynTemplateDrive","entity for template drive caller").entity
        obj.addProperty("App::PropertyIntegerList","drv_calls","_MBDynTemplateDrive","drive callers for template drive caller").drv_calls

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
        App.Console.PrintMessage("Recompute Python MBDynTemplateDrive feature\n")

    def onDocumentRestored(self, fp):
        '''restores feature python object when document is read'''
        self.Object = fp


    def writeDrive(self):
        if self.tpl_type == "null":
            drive_line = "null"

        elif self.tpl_type == "single":
            drive_line = "single, {}, {}".format(self.single_entity.writeVector(), write_drv(self.Object.drv_calls[0]))

        elif self.tpl_type == "component":
            if self.component_type == None:
                drive_line = "component"
                for k in self.Obbject.drv_calls:
                    if k == 0:
                        drive_line = drive_line + ", " + "inactive"
                    else:
                        drive_line = drive_line + ",\n                  " + write_drv(k)

            else:
                drive_line = "component, {}".format(self.component_type)
                for k in self.component_drive_caller:
                    drive_line = drive_line + ",\n                   " + k.writeDrive()

        elif self.tpl_type == "array":
            drive_line = "array, {}".format(self.num_template_drive_callers)
            for k in self.array_drive_caller:
                drive_line = drive_line + ", " + k.writeDrive()

        return drive_line
