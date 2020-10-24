import numpy as np
import math
import FreeCAD as App
import MBDyn_objects.MBDynJoints
from  MBDyn_utilities.MBDyn_funcs import *


class MBDynReference:
    def __init__(self, obj):
        obj.addProperty("App::PropertyInteger","ref_label","MBDynReference","label for reference ").ref_label
        obj.addProperty("App::PropertyString","ref_name","MBDynReference","name of reference").ref_name
         # refered_label is the label of a reference current reference is referred to.
        obj.addProperty("App::PropertyInteger","refered_label","MBDynReference","reference label of parent reference").refered_label
         # position and orientation must be in global reference
        obj.addProperty("App::PropertyVector","position","MBDynReference","position of reference ").position
        obj.addProperty("App::PropertyVectorList","orientation","MBDynReference","orientation of reference").orientation
        obj.addProperty("App::PropertyString","orientation_des","MBDynReference","orientation type of reference ").orientation_des
        obj.addProperty("App::PropertyVector","vel","MBDynReference","velocity of reference").vel
        obj.addProperty("App::PropertyVector","ang_vel","MBDynReference","angular velocity of reference ").ang_vel
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


    def writeStructuralNode(self):
        if self.refLbl == 0:
            line = ("        reference: {}, {},\n"
                "                {},\n"
                "                {},\n"
                "                {},\n"
                "                {};\n").format(self.Object.label, self.Object.ref_name,  writeVect(self.Object.position), writeOrientationMatrix(self.Object.orientation_des,  self.Object.orientation),
                                                                      writeVect(self.Object.vel),  writeVect(self.Object.ang_vel))
            return line


class MBDynIntegrationMethod:

    def __init__(self, obj):  #  differential_radius, algebraic_radius, order
        obj.addProperty("App::PropertyFloat","differential_radius","MBDynIntegrationMethod","differential_radius for method of simulation").differential_radius
        obj.addProperty("App::PropertyFloat","algebraic_radius","MBDynIntegrationMethod","algebraic_radius for method of simulation").algebraic_radius
        obj.addProperty("App::PropertyInteger","order","MBDynIntegrationMethod","order for method of simulation").order
        obj.addProperty("App::PropertyString","Imethod","MBDynIntegrationMethod","method of simulation").Imethod

#        self.differential_radius = differential_radius
#        self.algebraic_radius = algebraic_radius
#        self.order = order
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


    def setDifferentialRadius(self, differential_radius):
        self.differential_radius = differential_radius

    def getDifferentialRadius(self):
        return self.differential_radius

    def setAlgebraicRadius(self, algebraic_radius):
        self.algebraic_radius = algebraic_radius

    def getAlgebraicRadius(self):
        return self.algebraic_radius

    def setOrder(self, order):
        self.order = order

    def getOrder(self, order):
        return self.order

    def writeMethod(self):
        if self.Object.Imethod == "crank nicolson":
            return "crank nicolson"
        elif self.Object.Imethod == "ms":
            if self.Object.algebraic_radius == 0:
                if self.Object.differential_radius == 0:
                    return "ms, {}".format(MBDynConstDrive(self.Object.differential_radius).writeDrive())
                else:
                    return "ms, {}".format(self.Object.differential_radius)
            else:
                if self.Object.differential_radius == 0 and self.Object.algebraic_radius == 0:
                    return "ms, {}, {}".format(MBDynConstDrive(self.Object.differential_radius).writeDrive(), MBDynConstDrive(self.Object.algebraic_radius).writeDrive())
                return "ms, {}, {}".format(selfObject.differential_radius, self.Object.algebraic_radius)

#            m = MBDynModel.ms(float(self.ms_differential_radius.text()), float(self.ms_algebraic_radius.text()))
        elif self.Object.Imethod == "hope":
            if self.Object.algebraic_radius != 0:
                if self.Object.differential_radius != 0:
                    return "hope, {}, {}".format(MBDynConstDrive(self.Object.differential_radius).writeDrive(), MBDynConstDrive(self.Object.differential_radius).writeDrive())
                return "hope, {}, {}".format(self.Object.differential_radius, self.Object.differential_radius)
            else:
                if self.Object.differential_radius == 0:
                    return "hope, {}, {}".format(MBDynConstDrive(self.Object.differential_radius).writeDrive(), MBDynConstDrive(self.Object.algebraic_radius).writeDrive())
                return "hope, {}, {}".format(self.Object.differential_radius, self.Object.algebraic_radius)
        elif self.Object.Imethod == "third order":
            return "third order, {}".format(self.Object.differential_radius)
        elif self.Object.Imethod == "bdf":
            return "bdf, order, {}".format(self.order)
        elif self.Object.Imethod == "implicit euler":
            return "implicit euler"



class MBDynStructuralNode:

    def __init__(self, obj):
        obj.addProperty("App::PropertyString","node_name","MBDynStructuralNodes","name of structural node ").node_name
        obj.addProperty("App::PropertyInteger","node_label","MBDynStructuralNodes","label for structural node ").node_label
        obj.addProperty("App::PropertyString","struct_type","MBDynStructuralNodes","type of structural node ").struct_type
        obj.addProperty("App::PropertyVector","position","MBDynStructuralNodes","position of structural node ").position
        obj.addProperty("App::PropertyVectorList","orientation","MBDynStructuralNodes","orientation of structural node ").orientation
        obj.addProperty("App::PropertyString","orientation_des","MBDynStructuralNodes","type of orientation matrix ").orientation_des
        obj.addProperty("App::PropertyVector","vel","MBDynStructuralNodes","velosity of structural node ").vel
        obj.addProperty("App::PropertyVector","ang_vel","MBDynStructuralNodes","Angular velosity of structural node ").ang_vel
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


    def writeNode(self):
        teststr =( "write node " + self.Object.orientation_des)
        App.Console.PrintMessage(teststr)
        line = ("        structural: {}, {},\n"
                "                {},\n"
                "                {},\n"
                "                {},\n"
                "                {};\n").format(self.Object.node_label, self.Object.struct_type, writeVect(self.Object.position),
                                                                      writeOrientationMatrix(self.Object.orientation_des, self.Object.orientation),
                                                                      writeVect(self.Object.vel), writeVect(self.Object.ang_vel))
        return line

class MBDynRigidBody:

    def __init__(self, obj):
        obj.addProperty("App::PropertyString","body_obj_label","MBDynRigidBody","label of FreeCad object for rigid body").body_obj_label
        obj.addProperty("App::PropertyInteger","label","MBDynRigidBody","label for rigid body").label
        obj.addProperty("App::PropertyInteger","node_label","MBDynRigidBody","node_label for rigid body").node_label
        obj.addProperty("App::PropertyFloat","mass","MBDynRigidBody","mass for rigid body").mass
        obj.addProperty("App::PropertyVector","com_offset","MBDynRigidBody","com_offset for rigid body").com_offset
        obj.addProperty("App::PropertyString","matrix_type","MBDynRigidBody","type of moment of inertia matrix  for rigid body").matrix_type
        obj.addProperty("App::PropertyVectorList","inertia_matrix","MBDynRigidBody","inertia_matrix for rigid body").inertia_matrix
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

    def writeBody(self):
        line = ("        body: {}, {},\n"
                "                {},\n"
                "                {},\n"
                "                {};\n").format(self.Object.label, self.Object.node_label, self.Object.mass, writeVect(self.Object.com_offset), writeMatrix(self.Object.matrix_type, self.Object.inertia_matrix))
        return line


class MBDynGravity:

    def __init__(self, obj):

        obj.addProperty("App::PropertyString","field_type","Base","grvity field type").field_type
        obj.addProperty("App::PropertyVector","gravity_vector","Unifom gravity","grvity vector").gravity_vector                                          #object of class vec
        obj.addProperty("App::PropertyFloat","gravity_value","Unifom gravity","grvity acc.").gravity_value

        obj.addProperty("App::PropertyVector","gravity_origin","Central gravity","central grvity origin").gravity_origin
        obj.addProperty("App::PropertyFloat","cg_field_mass","Central gravity","central grvity mass").cg_field_mass
        obj.addProperty("App::PropertyFloat","gravity_constant","Central gravity","central grvity const.").gravity_constant

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

    def writeGravity(self):
        if self.Object.field_type == "uniform":

            gravity_line = "        gravity: uniform, {}, const, {};\n".format(writeVect(self.Object.gravity_vector), self.Object.gravity_value )

        elif self.Object.field_type == "central":
            gravity_line = "        gravity: central, origin, {}, mass, {}, G, {};\n".format(writeVect(self.Object.gravity_origin), self.Object.cg_field_mass, self.Object.gravity_constant)

        return gravity_line



class MBDynInitialValue:

    def __init__(self, obj):

        obj.addProperty("App::PropertyFloat","initial_time","MBDynInitialValue","initial time for simulation").initial_time
        obj.addProperty("App::PropertyFloat","final_time","MBDynInitialValue","final time for simulation").final_time
        obj.addProperty("App::PropertyFloat","time_step","MBDynInitialValue","time step for simulation").time_step
        obj.addProperty("App::PropertyInteger","max_iterations","MBDynInitialValue","max_iterations for simulation").max_iterations
        obj.addProperty("App::PropertyFloat","tolerance","MBDynInitialValue","tolerance for simulation").tolerance
        obj.addProperty("App::PropertyFloat","derivatives_tolerance","MBDynInitialValue","derivatives_tolerance for simulation").derivatives_tolerance
        self.Object = obj
        obj.Proxy = self

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

    def writeInitialValue(self):
        App.Console.PrintMessage("  write  inttial")
        line_iv = ""

        if self.Object.initial_time != None:
            line1 = "        initial time: {};\n".format(self.Object.initial_time)
            line_iv = line_iv + line1
        if self.Object.final_time != None:
            line2 = "        final time: {};\n".format(self.Object.final_time)
            line_iv = line_iv + line2
        if self.Object.time_step != None:
            line3 = "        time step: {};\n".format(self.Object.time_step)
            line_iv = line_iv + line3
        if self.Object.tolerance != None:
            line4 = "        tolerance: {};\n".format(self.Object.tolerance)
            line_iv = line_iv + line4
        if self.Object.max_iterations != None:
            line5 = "        max iterations: {};\n".format(self.Object.max_iterations)
            line_iv = line_iv + line5

        if self.Object.derivatives_tolerance != None:
            line7 = "        derivatives tolerance: {};\n".format(self.Object.derivatives_tolerance)
            line_iv = line_iv + line7
        '''
        if self.Object.output != None:
            line8 = self.Object.output.write()
            line_iv = line_iv + line8

        if self.Object.output_meter != None:
            line9 = "        output meter: {};\n".format(self.Object.output_meter.writeDrive())
            line_iv = line_iv + line9
        '''
        return line_iv


class MBDynControlData:

    def __init__(self, obj):
        obj.addProperty("App::PropertyInteger","structural_nodes","MBDynControlData","total number of nodes").structural_nodes
        obj.addProperty("App::PropertyInteger","rigid_bodies","MBDynControlData","total number of rigid_bodies").rigid_bodies
        obj.addProperty("App::PropertyInteger","joints","MBDynControlData","total number of joints").joints
        obj.addProperty("App::PropertyInteger","forces","MBDynControlData","total number of forces").forces
        obj.addProperty("App::PropertyBool","forces","MBDynControlData","total number of forces").forces
        obj.Proxy = self
#        self.structural_nodes = len(nodes.nodes)                                             #int
#        self.rigid_bodies = len(elements.bodies)                                             #int
#        self.joints = len(elements.joints)                                                   #int
#        self.forces = len(elements.forces)                                                   #int
#        self.gravity = len(elements.gravity)                                                 #Yes|No
        self.use = []
        self.default_output = []
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


    def setStucturalNodes(self, integer):
        if ((float(integer).is_integer()) & integer > 0):
            self.structural_nodes = integer
        else: print("Invalid number of structural nodes")

    def getStructuralNodes(self):
        return self.structural_nodes

    def setRigidBodies(self, integer):
        if ((float(integer).is_integer()) & integer > 0):
            self.rigid_bodies = integer
        else: print("Invalid number of rigid bodies")

    def getRigidBodies(self):
        return self.rigid_bodies

    def setJoints(self, integer):
        if ((float(integer).is_integer()) & integer > 0):
            self.joints = integer
        else: print("Invalid number of joints")

    def getJoints(self):
        return self.joints

    def setForces(self, integer):
        if ((float(integer).is_integer()) & integer > 0):
            self.forces = integer
        else: print("Invalid number of forces")

    def getForces(self):
        return self.forces

    def setUse(self, *args):
        self.use = list(args)

    def getUse(self):
        return self.use

    def setDefaultOutput(self, *args):
        self.default_output = args

    def getDefaultOutput(self):
        return self.default_output

    def writeControlData(self):
        cd_line = ""
        if self.Object.structural_nodes != 0:
            line1 = "        structural nodes: {};\n".format(self.Object.structural_nodes)
            cd_line = cd_line + line1
        if self.Object.rigid_bodies != 0:
            line2 = "        rigid bodies: {};\n".format(self.Object.rigid_bodies)
            cd_line = cd_line + line2
        if self.Object.forces != 0:
             line3 = "        forces: {};\n".format(self.Object.forces)
             cd_line = cd_line + line3
        if self.Object.joints != 0:
            line4 = "        joints: {};\n".format(self.Object.joints)
            cd_line = cd_line + line4
        if self.Object.gravity != 0:
            line5 = "        gravity;\n"
            cd_line = cd_line + line5

        if len(self.use) != 0:
            line6 = "        use: "
            for k in self.use:
                line6 = line6 + k +", "
            line6 = line6 + "in assembly;\n"
            cd_line = cd_line + line6

        if len(self.default_output) != 0:
            l = len(self.default_output)
            line7 = "        default output: "
            for i in range(l-1):
                line7 = line7 + self.default_output[i] + ", "
            line7 = line7 + self.default_output[l-1] + ";\n"
            cd_line = cd_line + line7

        return cd_line
