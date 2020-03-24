import numpy as np
import math
import FreeCAD as App
import MBDynJoints
from  MBDyn_funcs import *
'''
def writeVect(vector):
   if vector.x == 0 and vector.y == 0 and vector.z == 0:
      return "null"
   else:
      return "{}, {}, {}".format(vector.x, vector.y, vector.z) 

# matrix is a list of 3 FreeCAD vectors
def writeMatrix(matrix_type, matrix):  
    line_end = ""
    matrix_line = ""
    rowcount = 0
    colcount = 0
    if matrix_type == "eye" or matrix_type == "null":
       matrix_line = "{}".format(matrix_type)
    elif matrix_type == "matr":
        
        matrix_line = "{}".format(matrix_type)
        for j in matrix:
            for i in [j.x, j.y, j.z]:
                line_end = line_end + ", " + "{}".format(i)
        matrix_line = matrix_line + line_end
    elif matrix_type == "sym":
        matrix_line = "{}".format(matrix_type)
        for j in matrix:
            rowcount = rowcount +1
            colcount = 0
            for i in [j.x, j.y, j.z]:
                colcount = colcount + 1
                if colcount >= rowcount: 

                    line_end = line_end + ", " + "{}".format(i)
        matrix_line = matrix_line + line_end
    elif matrix_type == "skew":
        matrix_line = "{}".format(matrix_type)
        for j in matrix:
            rowcount = rowcount +1
            colcount = 0 
            for i in [j.x, j.y, j.z]:
                colcount = colcount + 1
                if colcount >= rowcount: 
                    line_end = line_end + ", " + "{}".format(i)
        matrix_line = matrix_line + line_end
    elif matrix_type == "diag":
        matrix_line = "{}".format(matrix_type)
        for j in matrix:
            rowcount = rowcount +1
            colcount = 0
            for i in [j.x, j.y, j.z]:
                colcount = colcount + 1
                App.Console.PrintMessage("row= {}, col= {}".format(rowcount, colcount))
                if colcount == rowcount: 
                    App.Console.PrintMessage("row= {}, col= {}".format(rowcount, colcount))
                    line_end = line_end + ", " + "{}".format(i)
        matrix_line = matrix_line + line_end
    return matrix_line

# Orientationmatrix passed is a list of three FreeCAD vectors even if only 2 are used
def writeOrientationMatrix(description, Orientationmatrix):
#    teststr = "MBDyn {} description".format(description)
#    App.Console.PrintMessage("dscr" + str(description))
    line_end = ""
    matrix_line = ""
    if description == "eye" or description == "null":        
        matrix_line = "{}".format(description)
    elif description == "matr":
        rowcount = 0
        colcount = 0

        matrix_line = "{}".format(description)
        for j in Orientationmatrix:
            for i in [j.x, j.y, j.z]:
                line_end = line_end + ", " + "{}".format(i)
        matrix_line = matrix_line + line_end
     # description xy, xz, yz are for OM with 2 vectors
    elif description == "xy":
        matrix_line = "1, {}, {}, {},  2, {}, {}, {}".format(Orientationmatrix[0][0], Orientationmatrix[0][1], Orientationmatrix[0][2], Orientationmatrix[1][0], Orientationmatrix[1][1], Orientationmatrix[1][2]) 
    elif description == "xz":
        matrix_line = "1, {}, {}, {},  3, {}, {}, {}".format(Orientationmatrix[0][0], Orientationmatrix[0][1], Orientationmatrix[0][2], Orientationmatrix[2][0], Orientationmatrix[2][1], Orientationmatrix[2][2]) 
    elif description == "yz":
        matrix_line = "2, {}, {}, {},  3, {}, {}, {}".format(Orientationmatrix[1][0], Orientationmatrix[1][1], Orientationmatrix[1][2], Orientationmatrix[2][0], Orientationmatrix[2][1], Orientationmatrix[2][2]) 
    else:
        matrix_line = "{}, {}, {},{}".format(description, Orientationmatrix[0][0], Orientationmatrix[0][1], Orientationmatrix[0][2] )
    return matrix_line  

def writeInputFile(name_of_file):
        
    with open(name_of_file, "w") as f:
        if hasattr(App.ActiveDocument, "initial_values"):    
            f.write("begin: data;\n")
            f.write("        problem: initial value;\n")
            f.write("end: data;\n\n")
            
            f.write("begin: initial value;\n")        
            f.write(App.ActiveDocument.initial_values.Proxy.writeInitialValue())
#            if hasattr(App.ActiveDocument, "integration_method"):
#                f.write(App.ActiveDocument.integration_method.Proxy.writeMethod())
            f.write("end: initial value;\n\n")
            
            f.write("begin: control data;\n")
            if len(App.ActiveDocument.Nodes.getSubObjects()) != 0:
                f.write("        strctural nodes: {};\n".format(len(App.ActiveDocument.Nodes.getSubObjects())))
            if len(App.ActiveDocument.Joints.getSubObjects()) != 0:
                f.write("        joints: {};\n".format(len(App.ActiveDocument.Nodes.getSubObjects())))
            if len(App.ActiveDocument.Bodies.getSubObjects()) != 0:
                f.write("        rigid_bodies: {};\n".format(len(App.ActiveDocument.Bodies.getSubObjects())))
            if len(App.ActiveDocument.Forces.getSubObjects()) != 0:
                f.write("        forces: {};\n".format(len(App.ActiveDocument.Forces.getSubObjects())))      
            if hasattr(App.ActiveDocument, "gravity"):
                f.write("        gravity;\n")       
            f.write("end: control data;\n\n")
            
            f.write("begin: nodes;\n")
            for nodeobj in App.ActiveDocument.Nodes.getSubObjects():
                f.write(App.ActiveDocument.getObject(nodeobj[0:-1]).Proxy.writeNode())      # App.ActiveDocument.getObject(nodeobj[0:-1]).Proxy.writeNode()
            f.write("end: nodes;\n\n")
            
            f.write("begin: elements;\n")
            for bodyobj in App.ActiveDocument.Bodies.getSubObjects():
                f.write(App.ActiveDocument.getObject(bodyobj[0:-1]).Proxy.writeBody())
            for jointobj in App.ActiveDocument.Joints.getSubObjects():
                f.write(App.ActiveDocument.getObject(jointobj[0:-1]).Proxy.writeJoint())
            for forceobj in App.ActiveDocument.Forces.getSubObjects():
                f.write(App.ActiveDocument.getObject(forceobj[0:-1]).Proxy.writeForce())
            if hasattr(App.ActiveDocument, "gravity"):
                f.write(App.ActiveDocument.gravity.Proxy.writeGravity())
            f.write("end: elements;\n\n")
        else:
            App.Console.PrintMessage("MBDyn model does not exist")  
'''
class vec:
    
    def __init__(self, x, y, z):
        self.vector = np.array([x, y, z])
        
    def setVector(self, x, y, z):
        self.vector = np.array([x, y, z])
        
    def getVector(self):
        return self.vector
        
    def writeVector(self):
        if np.all(self.vector==0):
            return "null"
        else:
            return "{}, {}, {}".format(self.vector[0], self.vector[1], self.vector[2])
            
            
class matrix:
    
    def __init__(self, keyword, *args):
        self.matrix_type = keyword
        self.line_end = ""
        for k in args:
                self.line_end = self.line_end + ", " + "{}".format(k)
        
        if keyword == "matr":
            self.matrix = np.array([[args[0], args[1], args[2]],
                                    [args[3], args[4], args[5]],
                                    [args[6], args[7], args[8]]])
            
        elif keyword == "sym":
            self.matrix = np.array([[args[0], args[1], args[2]],
                                    [args[1], args[3], args[4]],
                                    [args[2], args[4], args[5]]])
            
        elif keyword == "skew":
            self.matrix = np.array([[0, -args[2], args[1]],
                                    [args[2], 0, -args[0]],
                                    [-args[1], args[0], 0]])
            
        elif keyword == "diag":
            self.matrix = np.array([[args[0], 0, 0],
                                    [0, args[1], 0],
                                    [0, 0, args[2]]])
            
        elif keyword == "eye":
            self.matrix = np.array([[1, 0, 0],
                                    [0, 1, 0],
                                    [0, 0, 1]])
            
        elif keyword == "null":
            self.matrix = np.array([[0, 0, 0],
                                    [0, 0, 0],
                                    [0, 0, 0]])
            
    def getMatrix(self):
        return self.matrix
    
    def writeMatrix(self):
        if self.matrix_type == "eye" or self.matrix_type == "null":
            matrix_line = "{}".format(self.matrix_type)
        else:
            matrix_line = "{}".format(self.matrix_type) + self.line_end
        return matrix_line
            
class orientationMatrix:
    
    def __init__(self, orient_des, vector1, vector2, vector3):
#        obj.addProperty("App::PropertyInteger","index1","orientationMatrix","index1 of orientation matrix").index1
#        obj.addProperty("App::PropertyVector","vector1","orientationMatrix","vector1 of orientation matrix").vector1
#        obj.addProperty("App::PropertyInteger","index2","orientationMatrix","index2 of orientation matrix").index2
#        obj.addProperty("App::PropertyVector","vector2","orientationMatrix","vector3 of orientation matrix").vector2
#        obj.Proxy = self
         pass
         
         
#        self.index1 = 1
#        self.vector1 = vector1                                                  #object of class vec
        
#        self.index2 = index2
#        self.vector2 = vector2                                                  #object of class vec

        
    def setIndex1(self, index):
        self.index1 = index
        
    def getIndex1(self):
        return self.index1
    
    def setIndex2(self, index):
        self.index2 = index
        
    def getIndex2(self):
        return self.index2
    
    def setVector1(self, vector):
        self.vector1 = vector
        
    def getVector1(self):
        return self.vector1.getVector()
    
    def setVector2(self, vector):
        self.vector2 = vector
        
    def getVector2(self):
        return self.vector2.getVector()
    
    def writeMatrix(self):
        if ((self.index1 == 1) and (self.index2 == 2) and (np.all(self.vector1.getVector() == [1, 0, 0])) and (np.all(self.vector2.getVector() == [0, 1, 0]))):
                matrix_line = "eye"
        else:
            matrix_line = "{}, {}, {}, {}".format(self.index1, self.vector1.writeVector(), self.index2, self.vector2.writeVector())
        return matrix_line
        
        
Null = vec(0, 0, 0)
Eye = matrix("eye")
pi = math.pi


class nodeDof:
    
    def __init__(self, node_label, node_type, dof_number = None, order = None):
        
        self.node_label = node_label
        self.node_type = node_type
        self.dof_number = dof_number
        self.order = order
        
    def setNodeLabel(self, label):
        self.node_label = label
        
    def getNodeLabel(self):
        return self.node_label
    
    def setNodeType(self, node_type):
        self.node_type = node_type
        
    def getNodeType(self):
        return self.node_type
    
    def setDofNumber(self, number):
        self.dof_number = number
        
    def getDofNumber(self):
        return self.dof_number
    
    def setOrder(self, order):
        self.order = order
        
    def writeNodeDof(self):
        if self.dof_number != None:
            if self.order != None:
                line_nodeDof = "{}, {}, {}, {}".format(self.node_label, self.node_type, self.dof_number, self.order)
                
            else: line_nodeDof = "{}, {}, {}".format(self.node_label, self.node_type, self.dof_number)
            
        else:
            line_nodeDof = "{}, {}".format(self.node_label, self.node_type)
            
        return line_nodeDof


class MBDynReference:
    def __init__(self, obj):
        obj.addProperty("App::PropertyInteger","ref_label","MBDynReference","label for reference ").ref_label
        obj.addProperty("App::PropertyString","ref_name","MBDynReference","nane of reference").ref_name
         # refered_label is the label of a reference current reference is refered to.
        obj.addProperty("App::PropertyInteger","refered_label","MBDynReference","reference label of parrent reference").refered_label
         # position and orientation must be in grobal reference 
        obj.addProperty("App::PropertyVector","position","MBDynReference","position of reference ").position
        obj.addProperty("App::PropertyVectorList","orientation","MBDynReference","orientation of reference").orientation
        obj.addProperty("App::PropertyString","orientation_des","MBDynReference","orientation type of reference ").orientation_des
        obj.addProperty("App::PropertyVector","vel","MBDynReference","vlocity of reference").vel
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


        
        
class MBDynOutputData:
    
    def __init__(self, *args):
        
        self.items = list(args)                                                 #list of strings
    
    def addSpecialOutput(self, item):
        self.items.append(item)
        
    def removeSpecialOutput(self, item):
        self.items.remove(item)
        
    def write(self):
        if len(self.items) == 0:
            return None
        l = len(self.items)
        item_string = ''
        for i in range(l-1):
            item_string = item_string + ' ' + self.items[i] + ','
        item_string = item_string + ' ' + self.items[l-1] + ';'
        return '        output:' + item_string   
        

class MBDynConstDrive:
    
    def __init__(self, const_coef):        
        self.const_coef = const_coef
    
    def setConstCoef(self, const_coef):
        self.const_coef = const_coef
        
    def getConstCoef(self):
        return self.const_coef
    
    def writeDrive(self):
        return "const, {}".format(self.const_coef)

    
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
#        self.label = label
#        self.struct_type = struct_type
#        self.position = position                                                #object of class vec
#        self.orientation = orientation                                          #onject of class orientationMatrix
#        self.orientation_des = orientation_des
#        self.abs_vel = abs_vel                                                  #object of class vec
#        self.abs_ang_vel = abs_ang_vel                                          #object of class vec
#        self.pos_initial_stiffness = pos_initial_stiffness
#        self.vel_initial_stiffness = vel_initial_stiffness
#        self.bool_omega_rotates = bool_omega_rotates                            #yes|no|bool
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
        self.Object = fp
       
    def setLabel(self, label):
        self.label = label
        
    def getLabel(self):
        return self.label
    
    def setStructType(self, struct_type):
        self.struct_type = struct_type
    
    def getStructType(self):
        return self.struct_type
    
    def setPosition(self, position):
        self.position = position
        
    def getPosition(self):
        return self.position
    
    def setOrientation(self, orientation):
        self.orientation = orientation
        
    def getOrientation(self):
        return self.orientation
    
    def setOrientationDescription(self, orientation_des):
        self.orientation_des = orientation_des
        
    def getOrientationDescription(self):
        return self.orientation_des
    
    def setAbsoluteVel(self, abs_vel):
        self.abs_vel = abs_vel
        
    def getAbsoluteVel(self):
        return self.abs_vel
    
    def setAbsoluteAngularVel(self, abs_ang_vel):
        self.abs_ang_vel = abs_ang_vel
        
    def getAbsoluteAngularVel(self):
        return self.abs_ang_vel
    
    def setPositionInitialStiffness(self, pos_initial_stiffness):
        self.pos_initial_stiffness = pos_initial_stiffness
        
    def getPositionInitialStiffness(self):
        return self.pos_initial_stiffness
    
    def setVelocityInitialStiffness(self, vel_initial_stiffness):
        self.vel_initial_stiffness = vel_initial_stiffness
        
    def getVelocityInitialStiffness(self):
        return self.vel_initial_stiffness
    
    def setOmegaRotation(self, bool_omega):
        self.bool_omega_rotates = bool_omega
        
    def getOmegaRotation(self):
        return self.bool_omega_rotates
    
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
#        self.label = label
#        self.node_label = node_label
#        self.mass = mass
#        self.com_offset = com_offset                                             #object of class vec
#        self.inertia_matrix = inertia_matrix                                     #object of class matrix

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
        self.Object = fp


    def setLabel(self, label):
        self.label = label
        
    def getLabel(self):
        return self.label
    
    def setNodeLabel(self, node_label):
        self.node_label = node_label
        
    def getNodeLabel(self):
        return self.node_label
    
    def setMass(self, mass):
        self.mass = mass
        
    def getMass(self, mass):
        return self.mass
    
    def setCOMOffset(self, com_offset):
        self.com_offset = com_offset
        
    def getCOMOffset(self):
        return self.com_offset.getVector()
    
    def setInertiaMatrix(self, matrix):
        self.inertia_matrix = matrix
    
    def getInertiaMatrix(self):
        return self.inertia_matrix.getMatrix()
        
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
        self.Object = fp


    def setGravityAcceleration(self, gravity_acc):
        if isinstance(gravity_acc, int) or isinstance(gravity_acc, float):
            self.gravity_value = gravity_acc
            self.gravity_acc = MBDynTemplateDrive("single", self.gravity_vector, MBDynConstDrive(self.gravity_value))                      
        else:
            self.gravity_acc = MBDynTemplateDrive("single", self.gravity_vector, gravity_acc)
        
    def getGravityAcceleration(self):
        return self.gravity_acc
    
    def setGravityVector(self, vector):
        self.gravity_vector = vector
        self.gravity_acc = MBDynTemplateDrive("single", self.gravity_vector, MBDynConstDrive(self.gravity_value))
    
    def getGravityVector(self):
        return self.gravity_vector.getVector()
    
    def setAbsoluteOrigin(self, abs_origin):
        self.abs_origin = abs_origin
     
    def getAbsoluteOrigin(self):
        return self.abs_origin
    
    def setCGFieldMass(self, cg_field_mass):
        self.cg_field_mass = cg_field_mass
        
    def getCGFieldMass(self):
        return self.cg_field_mass
    
    def setGravityConstant(self, gravity_constant):
        self.gravity_constant = gravity_constant
    
    def getGravityConstant(self):
        return self.gravity_constant
        
    def writeGravity(self):
        if self.Object.field_type == "uniform":
           
            gravity_line = "        gravity: uniform, {}, const, {};\n".format(writeVect(self.Object.gravity_vector), self.Object.gravity_value )
            
        elif self.Object.field_type == "central":
            gravity_line = "        gravity: central, origin, {}, mass, {}, G, {};\n".format(writeVect(self.Object.gravity_origin), self.Object.cg_field_mass, self.Object.gravity_constant)
            
        return gravity_line
        
        
 
  
      



        
                
        
        
        
        
        
        
        
class MBDynAbstractForce:
    
    def __init__(self, label, dof, force_magnitude):
        
        self.label = label
        self.dof = dof
        self.force_magnitude = force_magnitude
        
    def setLabel(self, label):
        self.label = label
        
    def getLabel(self):
        return self.label
        
    def setDof(self, dof):
        self.dof = dof
        
    def getDof(self):
        return self.dof
    
    def setForceMagnitude(self, force_mag):
        self.force_magnitude = force_mag
        
    def getForceMagnitude(self):
        return self.force_magnitude
    
    def writeForce(self):
        line_force = "        force: {}, abstract, {}, {};\n\n".format(self.label, self.dof.writeNodeDof(), self.force_magnitude)
        return line_force
    
    
class MBDynAbstractReactionForce:
    
    def __init__(self, label, dof1, dof2, force_magnitude):
        
        self.label = label
        self.dof1 = dof1
        self.dof2 = dof2
        self.force_magnitude = force_magnitude
        
    def setLabel(self, label):
        self.label = label
        
    def getLabel(self):
        return self.label
    
    def setDof1(self, dof):
        self.dof1 = dof
        
    def getDof1(self):
        return self.dof1
    
    def setDof2(self, dof):
        self.dof2 = dof
        
    def getDof2(self):
        return self.dof2
    
    def setForceMagnitude(self, force_mag):
        self.force_magnitude = force_mag
        
    def getForceMagnitude(self):
        return self.force_magnitude
    
    def writeForce(self):
        line_force = "        force: {}, abstract internal, {}, {}, {};\n\n".format(self.label, self.dof1.writeNodeDof(), self.dof2.writeNodeDof(), self.force_magnitude)
        return line_force
    
    
class MBDynStructuralForce:
    
    def __init__(self, label, force_type, node_label, relative_arm, force_value, moment_value = None, force_orientation = None, moment_orientation = None):
        
        self.label = label
        self.force_type = force_type                                            #absolute|follower|total
        self.node_label = node_label
        self.relative_arm = relative_arm
        self.force_value = force_value
        self.moment_value = moment_value
        self.force_orientation = force_orientation
        self.moment_orientation = moment_orientation
        
        
    def setLabel(self, label):
        self.label = label
        
    def getLabel(self):
        return self.label
        
    def setForceType(self, force_type):
        self.force_type = force_type
    
    def getForceType(self):
        return self.force_type
    
    def setNodeLabel(self, node_label):
        self.node_label = node_label
        
    def getNodeLabel(self):
        return self.node_label
    
    def setRelativeArm(self, relative_arm):
        self.relative_arm = relative_arm
        
    def getRelativeArm(self):
        return self.relative_arm
    
    def setForceValue(self, force_value):
        self.force_value = force_value
        
    def getForceValue(self):
        return self.force_value
    
    def setMomentValue(self, moment_value):
        self.moment_value = moment_value
        
    def getMomentValue(self):
        return self.moment_value
        
    def setForceOrientation(self, force_orientation):
        self.force_orientation = force_orientation
        
    def getForceOrientation(self):
        return self.force_orientation
    
    def setMomentOrientation(self, moment_orientation):
        self.moment_orientation = moment_orientation
        
    def getMomentOrientation(self):
        return self.moment_orientation
    
    def writeForce(self):
        if self.force_type == "absolute" or self.force_type == "follower":
            line_force = ("        force: {}, {},\n"
                          "                {},\n"
                          "                position, {},\n"
                          "                {};\n\n").format(self.label, self.force_type, self.node_label, self.relative_arm.writeVector(), self.force_value.writeDrive())
        
        else:
            line_force = ("        force: {}, {},\n"
                          "                {},\n"
                          "                position, {},\n"
                          "                force orientation, {},\n"
                          "                moment orientation, {},\n"
                          "                force, {},\n"
                          "                moment, {};\n\n").format(self.label, self.force_type, self.node_label,
                                                                  self.relative_arm.writeVector(), self.force_orientation.writeMatrix(), self.moment_orientation.writeMatrix(),
                                                                  self.force_value.writeDrive(), self.moment_value.writeDrive())
        return line_force
            
        
    
    

class MBDynStructuralInternalForce:
    
    def __init__(self, label, force_type, node1_label, relative_arm1, node2_label, relative_arm2, force_value, moment_value = None,
                 force_orientation1 = None, moment_orientation1 = None, force_orientation2 = None, moment_orientation2 = None):
        
        self.label = label
        self.force_type = force_type
        self.node1_label = node1_label
        self.relative_arm1 = relative_arm1
        self.node2_label = node2_label
        self.relative_arm2 = relative_arm2
        self.force_value = force_value
        self.moment_value = moment_value
        self.force_orientation1 = force_orientation1
        self.moment_orientation1 = moment_orientation1
        self.force_orientation2 = force_orientation2
        self.moment_orientation2 = moment_orientation2
        
    
    
    def setLabel(self, label):
        self.label = label
        
    def getLabel(self):
        return self.label
    
    def setForceType(self, force_type):
        self.force_type = force_type
    
    def getForceType(self):
        return self.force_type
    
    def setNode1Label(self, node_label):
        self.node1_label = node_label
        
    def getNode1Label(self):
        return self.node1_label
    
    def setRelativeArm1(self, relative_arm):
        self.relative_arm1 = relative_arm
        
    def getRelativeArm1(self):
        return self.relative_arm1
    
    def setNode2Label(self, node_label):
        self.node2_label = node_label
        
    def getNode2Label(self):
        return self.node2_label
    
    def setRelativeArm2(self, relative_arm):
        self.relative_arm2 = relative_arm
        
    def getRelativeArm2(self):
        return self.relative_arm2
    
    def setForceValue(self, force_value):
        self.force_value = force_value
        
    def getForceValue(self):
        return self.force_value
    
    def setMomentValue(self, moment_value):
        self.moment_value = moment_value
        
    def getMomentValue(self):
        return self.moment_value
    
    def setForceOrientation1(self, force_orientation):
        self.force_orientation1 = force_orientation
        
    def getForceOrientation1(self):
        return self.force_orientation1
    
    def setMomentOrientation1(self, moment_orientation):
        self.moment_orientation1 = moment_orientation
        
    def getMomentOrientation1(self):
        return self.moment_orientation1
    
    def setForceOrientation2(self, force_orientation):
        self.force_orientation2 = force_orientation
        
    def getForceOrientation2(self):
        return self.force_orientation2
    
    def setMomentOrientation2(self, moment_orientation):
        self.moment_orientation = moment_orientation
        
    def getMomentOrientation2(self):
        return self.moment_orientation2
    
    def writeForce(self):
        if self.force_type == "absolute" or self.force_type == "follower":
            line_force = ("        force: {}, {} internal,\n"
                          "                {}, position, {},\n"
                          "                {}, position, {},\n"
                          "                {};\n\n").format(self.label, self.force_type,
                                                           self.node1_label, self.relative_arm1.writeVector(),
                                                           self.node2_label, self.relative_arm2.writeVector(),
                                                           self.force_value.writeDrive())
            
        else:
            line_force = ("        force: {}, total internal,\n",
                          "                {},\n"
                          "                position, {},\n"
                          "                force orientation, {},\n"
                          "                moment orientation, {},\n"
                          "                {},\n"
                          "                position, {},\n"
                          "                force orientation, {},\n"
                          "                moment orientation, {},\n"
                          "                force, {},\n"
                          "                moment, {};\n\n"
                          ).format(self.label, self.node1_label, self.node1_label, self.relative_arm1.writeVector(), self.force_orientation1.writeMatrix(),
                                  self.moment_orientation1.writeMatrix(), self.node2_label, self.relative_arm1.writeVector(), self.force_orientation2.writeMatrix(),
                                  self.moment_orientation2.writeMatrix(), self.force_value.writeVector(), self.moment_value.writeVector())
            
        return line_force
    
    
    

class MBDynStructuralCouple:
    
    def __init__(self, label, force_type, node_label, relative_arm, couple_value):
        
        self.label = label
        self.force_type = force_type
        self.node_label = node_label
        self.relative_arm = relative_arm
        self.couple_value = couple_value
        
    def setLabel(self, label):
        self.label = label
        
    def getLabel(self):
        return self.label
        
    def setForceType(self, force_type):
        self.force_type = force_type
    
    def getForceType(self):
        return self.force_type
    
    def setNodeLabel(self, node_label):
        self.node_label = node_label
        
    def getNodeLabel(self):
        return self.node_label
    
    def setRelativeArm(self, relative_arm):
        self.relative_arm = relative_arm
        
    def getRelativeArm(self):
        return self.relative_arm.getVector()
    
    def setCoupleValue(self, couple_value):
        self.couple_value = couple_value
        
    def getCoupleValue(self):
        return self.couple_value
    
    def writeForce(self):
        line_force = ("        couple: {}, {},\n"
                      "                {},\n"
                      "                position, {},\n"
                      "                {};\n\n"
                      ).format(self.label, self.force_type, self.node_label, self.relative_arm.writeVector(), self.couple_value.writeDrive())
        
        return line_force
    

class StructuralInternalCouple:
    
    def __init__(self, label, force_type, node1_label, relative_arm1, node2_label, relative_arm2, couple_value):
        
        self.label = label
        self.force_type = force_type
        self.node1_label = node1_label
        self.relative_arm1 = relative_arm1
        self.node2_label = node2_label
        self.relative_arm2 = relative_arm2
        self.couple_value = couple_value
        
    def setLabel(self, label):
        self.label = label
        
    def getLabel(self):
        return self.label
        
    def setForceType(self, force_type):
        self.force_type = force_type
    
    def getForceType(self):
        return self.force_type
    
    def setNode1Label(self, node_label):
        self.node1_label = node_label
        
    def getNode1Label(self):
        return self.node1_label
    
    def setRelativeArm1(self, relative_arm):
        self.relative_arm1 = relative_arm
        
    def getRelativeArm1(self):
        return self.relative_arm1.getVector()
    
    def setNode2Label(self, node_label):
        self.node2_label = node_label
        
    def getNode2Label(self):
        return self.node2_label
    
    def setRelativeArm2(self, relative_arm):
        self.relative_arm2 = relative_arm
        
    def getRelativeArm2(self):
        return self.relative_arm2.getVector()
    
    def setCoupleValue(self, couple_value):
        self.couple_value = couple_value
        
    def getCoupleValue(self):
        return self.couple_value
    
    def writeForce(self):
        line_force = ("        couple: {}, {},\n"
                      "                {},\n"
                      "                position, {},\n"
                      "                {},\n"
                      "                position, {},\n"
                      "                {};\n\n").format(self.label, self.force_type, self.node1_label, self.relative_arm1.writeVector(),
                                                        self.node2_label, self.relative_arm2.writeVector(), self.couple_value.writeDrive())
        
        return line_force




class MBDynData:
    
    def __init__(self, problem_type = "initial value"):
        self.problem_type = problem_type
        
    def writeData(self):
        return "        problem : {};".format(self.problem_type)
    
    
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
        
#        self.initial_time = initial_time                                        #Non-negetive number
#        self.final_time = final_time                                            #Positive number
#        self.time_step = time_step                                              #Positive number
#        self.max_iterations = max_iterations                                    #Positive integer
#        self.tolerance = tolerance                                              #Positive number
#        self.derivatives_tolerance = derivatives_tolerance                      #Positive number
#        self.method = method                                                    #Object of a subclass of MBDynIntegrationMethod
#        self.output = output                                                    #Object of class MBDynOutputData
#        self.output_meter = output_meter                                        #drivecaller
        
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
        self.Object = fp


    def setInitialTime(self, initial_time):
        self.initial_time = initial_time
            
    def getInitialTime(self):
        return self.initial_time
    
    def setFinalTime(self, final_time):
        self.final_time = final_time
            
    def getFinalTime(self):
        return self.final_time
    
    def setTimeStep(self, time_step):
        self.time_step = time_step
            
    def getTimeStep(self):
        return self.time_step
    
    def setMaxIterations(self, max_iterations):
        self.max_iterations = max_iterations
            
    def getMaxIterations(self):
        return self.max_iterations
    
    
    def setTolerance(self, tolerance):
        self.tolerance = tolerance
        
    def getTolerance(self):
        return self.tolerance
    
    def setDerivativesTolerance(self, derivatives_tolerance):
        self.derivatives_tolerance = derivatives_tolerance
        
    def getDerivativesTolerance(self):
        self.derivatives_tolerance
        
    def setMethod(self, method):
        self.method = method
        
    def getMethod(self):
        return self.method.writeMethodType()
        
    def setOutput(self, output):
        self.output = output
        
    def getOutput(self):
        return self.output.write()
    
    def setOutputMeter(self, when):
        self.output_meter = when
        
    def getOutputMeter(self):
        return self.output_meter
    
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
        
    
class MBDynNodes:
    
    def __init__(self):
        self.nodes = []                                                         #list of objects of class MBDynStructuralNode
        
    def addNode(self, *node):
        self.nodes.extend(node)
        
    def removeNode(self, node):
        self.nodes.remove(node)
        
    def writeNodes(self):
        inputline = ""
        for k in self.nodes:
            inputline = inputline + k.writeStructuralNode()
        return inputline
       
class MBDynElements:
    
    def __init__(self):
        self.bodies = []
        self.joints = []
        self.forces = []
        self.gravity = []
        
    def addBody(self, *body_objects):
        self.bodies.extend(body_objects)
        
    def removeBody(self, body_object):
        self.bodies.remove(body_object)
        
    def addJoint(self, *joint_objects):
        self.joints.extend(joint_objects)
        
    def removeJoint(self, joint_object):
        self.joints.remove(joint_object)
        
    def addForce(self, *force_objects):
        self.forces.extend(force_objects)
        
    def removeForce(self, force_object):
        self.forces.remove(force_object)
        
    def addGravity(self, gravity_object):
        self.gravity.append(gravity_object)
        
    def removeGravity(self, gravity_object):
        self.gravity.remove(gravity_object)
        
    def writeElements(self):
        element_line = ""
        
        for k in self.bodies:
            element_line = element_line + k.writeRigidBody()
        
        for k in self.joints:
            element_line = element_line + k.writeJoint()
            
        for k in self.forces:
            element_line = element_line + k.writeForce()
            
        for k in self.gravity:
            element_line = element_line + k.writeGravity()
        
        return element_line
            
            
class MBDynModel:
    
    def __init__(self, initial_value = None, control_data = None, nodes = None, elements = None):
        
        self.initial_value = initial_value
        self.control_data = control_data
        self.nodes = nodes
        self.elements = elements

    def setInitialValue(self, iv):
        self.initial_value = iv

    def setControlData(self, cd):
        self.control_data = cd

    def setNodes(self, nodes):
        self.nodes = nodes

    def setElements(self, elements):
        self.elements = elements
        
    def writeInputFile(self, name_of_file):
       
        with open(name_of_file, "w") as f:
            
            f.write("begin: data;\n")
            f.write("        problem: initial value;\n")
            f.write("end: data;\n\n")
            
            f.write("begin: initial value;\n")
            f.write(self.initial_value.writeInitialValue())
            f.write("end: initial value;\n\n")
            
            f.write("begin: control data;\n")
            f.write(self.control_data.writeControlData())
            f.write("end: control data;\n\n")
            
            f.write("begin: nodes;\n")
            f.write(self.nodes.writeNodes())
            f.write("end: nodes;\n\n")
            
            f.write("begin: elements;\n")
            f.write(self.elements.writeElements())
            f.write("end: elements;\n\n")


