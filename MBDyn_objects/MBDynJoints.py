import numpy as np
import math
import FreeCAD as App
import MBDyn_objects.model_so
from  MBDyn_utilities.MBDyn_funcs import writeVect, writeMatrix, writeOrientationMatrix

class MBDynRevoluteHinge:
    def __init__(self, obj):
        obj.addProperty("App::PropertyInteger","joint_label","MBDynRevoluteHinge","label for structural node 1").joint_label
        obj.addProperty("App::PropertyInteger","node1_label","MBDynRevoluteHinge","label for structural node 1").node1_label
        obj.addProperty("App::PropertyVector","position1","MBDynRevoluteHinge","relative position from structural node 1").position1
        obj.addProperty("App::PropertyVectorList","orientation1","MBDynRevoluteHinge","relative orientation from structural node 1").orientation1
        obj.addProperty("App::PropertyString","orientation_des1","MBDynRevoluteHinge","orientation matrix 1 type ").orientation_des1
        obj.addProperty("App::PropertyInteger","node2_label","MBDynRevoluteHinge","label for structural node 1").node2_label
        obj.addProperty("App::PropertyVector","position2","MBDynRevoluteHinge","relative position from structural node 2").position2
        obj.addProperty("App::PropertyVectorList","orientation2","MBDynRevoluteHinge","relative orientation from structural node 2").orientation2
        obj.addProperty("App::PropertyString","orientation_des2","MBDynRevoluteHinge","orientation matrix 2 type ").orientation_des2

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

    def writeJoint(self):
#        writeVect(App.Vector(1,0,0))
#        line = ("        joint: ").format(self.Object.joint_label, self.Object.node1_label)
        
        line = ("        joint: {}, revolute hinge,\n"
                "                {},\n"
                "                {},\n"
                "                hinge, {},\n"
                "                {},\n"
                "                {},\n"
                "                hinge, {};\n").format(self.Object.joint_label, self.Object.node1_label, writeVect(self.Object.position1), 
                                                                      writeOrientationMatrix(self.Object.orientation_des1, self.Object.orientation1),
                                                                      self.Object.node2_label, writeVect(self.Object.position2), 
                                                                      writeOrientationMatrix(self.Object.orientation_des2, self.Object.orientation2))
        
        return line   

class MBDynRevolutePin:
    def __init__(self, obj):
        obj.addProperty("App::PropertyInteger","joint_label","MBDynRevolutePin","label for structural node 1").joint_label
        obj.addProperty("App::PropertyInteger","node1_label","MBDynRevolutePin","label for structural node 1").node1_label
        obj.addProperty("App::PropertyVector","position1","MBDynRevolutePin","relative position from structural node 1").position1
        obj.addProperty("App::PropertyVectorList","orientation1","MBDynRevolutePin","relative orientation from structural node 1").orientation1
        obj.addProperty("App::PropertyString","orientation_des1","MBDynRevolutePin","orientation matrix 1 type ").orientation_des1
        obj.addProperty("App::PropertyVector","positionf","MBDynRevolutePin","fixed positin for pin").positionf
        obj.addProperty("App::PropertyVectorList","orientationf","MBDynRevolutePin","fixed orientation for pin").orientationf
        obj.addProperty("App::PropertyString","orientation_desf","MBDynRevolutePin","orientation matrix type ").orientation_desf

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

    def writeJoint(self):
#        writeVect(App.Vector(1,0,0))
#        line = ("        joint: ").format(self.Object.joint_label, self.Object.node1_label)
        
        line = ("        joint: {}, revolute pin,\n"
                "                {},\n"
                "                {},\n"
                "                hinge, {},\n"
                "                {},\n"
                "                hinge, {};\n").format(self.Object.joint_label, self.Object.node1_label, writeVect(self.Object.position1), 
                                                                      writeOrientationMatrix(self.Object.orientation_des1, self.Object.orientation1),
                                                                      writeVect(self.Object.positionf), 
                                                                      writeOrientationMatrix(self.Object.orientation_desf, self.Object.orientationf))
        
        return line  

class MBDynTotalJoint:
    
    def __init__(self, label, joint_type, node1_label, relative_offset_1, rel_pos_orientation1, rel_rot_orientation1,
                  node2_label, relative_offset_2, rel_pos_orientation2, rel_rot_orientation2):
        
        self.label = label
        self.node1_label = node1_label
        self.relative_offset_1 = relative_offset_1
        self.rel_pos_orientation1 = rel_pos_orientation1
        self.rel_rot_orientation1 = rel_rot_orientation1
        
        self.node2_label = node2_label
        self.relative_offset_2 = relative_offset_2
        self.rel_pos_orientation2 = rel_pos_orientation2
        self.rel_rot_orientation2 = rel_rot_orientation2
        
        if joint_type == 'fixed':                                                                                                   #Clamp
            self.position_constraint = [True, True, True]
            self.orientation_constraint = [True, True, True]
            
        elif joint_type == 'pointOnLine':                                                                                           #inline
            self.position_constraint = [True, True, False]                                                                          #assuming local axis 3 is used
            self.orientation_constraint = [False, False, False]
            
        elif joint_type == 'pointOnPlane':                                                                                          #inplane
            self.position_constraint = [False, False, True]         
            self.orientation_constraint = [False, False, False]
            
        elif joint_type == 'sphereOnSphere' or joint_type == 'pointOnPoint':                                                        #spherical Hinge
            self.position_constraint = [True, True, True]
            self.orientation_constraint = [False, False, False]
            
        elif joint_type == 'axisCoincident':                                    ##lockrotation check
            self.position_constraint = [True, True, False]
            self.orientation_constraint = [True, True, False]
            
        elif joint_type == 'circularEdge':                                                                                          #revolute hinge
            self.position_constraint = [True, True, True]
            self.orientation_constraint = [True, True, False]
            
        elif joint_type == 'axisParallel' or joint_type == 'planeParallel' or joint_type == 'axisPlaneNormal':                      #Revolute rotation
            self.position_constraint = [False, False, False]
            self.orientation_constraint = [True, True, False]                                                                       #assuming local axis 3 is the common axis/perpendicular to both planes
        
        elif joint_type == 'planeCoincident':                                                                                       #planeCoincident
            self.position_constraint = [False, False, True]
            self.orientation_constraint = [True, True, False]
            
        elif joint_type == 'planeAngular':                                                                                          #planeAngular
            self.position_constraint = [False, False, False]
            self.orientation_constraint = [True, True, True]
            
        elif joint_type == 'axisPlaneParallel':                                                                                     #axisPlaneParallel
            self.position_constraint = [False, False, False]
            self.orientation_constraint = [False, True, False]                                                                      #assuming local axis 3 is perpendicular to axis and parallel to plane
        
        self.ps = ""
        self.rc = ""
        for k in self.position_constraint:
            if k == True:
                self.ps = self.ps+"active, "
            else:
                self.ps = self.ps+"inactive, "
                
        for k in self.orientation_constraint:
            if k == True:
                self.rc = self.rc+"active, "
            else:
                self.rc = self.rc+"inactive, "
                
    def setLabel(self, label):
        self.label = label
        
    def getLabel(self):
        return self.label
        
    def setNode1Label(self, label):
        self.node1_label = label
        
    def getNode1Label(self):
        return self.node1_label
    
    def setNode2Label(self, label):
        self.node2_label = label
        
    def getNode2Label(self):
        return self.node2_label
    
    def setRelativeOffset1(self, relative_offset_1):
        self.relative_offset_1 = relative_offset_1
        
    def getRelativeOffset1(self):
        return self.relative_offset_1.getVector()
    
    def setRelativeOffset2(self, relative_offset_2):
        self.relative_offset_2 = relative_offset_2
        
    def getRelativeOffset2(self):
        return self.relative_offset_2.getVector()
    
    def setPositionOrientation1(self, rel_pos_orientation1):
        self.rel_pos_orientation1 = rel_pos_orientation1
        
    def getPositionOrientation1(self):
        return self.rel_pos_orientation1.getMatrix()
    
    def setPositionOrientation2(self, rel_pos_orientation2):
        self.rel_pos_orientation2 = rel_pos_orientation2
        
    def getPositionOrientation2(self):
        return self.rel_pos_orientation2.getMatrix()
    
    def setRotationOrientation1(self, rel_rot_orientation1):
        self.rel_rot_orientation1 = rel_rot_orientation1
        
    def getRotationOrientation1(self):
        return self.rel_rot_orientation1.getMatrix()
    
    def setRotationOrientation2(self, rel_rot_orientation2):
        self.rel_rot_orientation2 = rel_rot_orientation2
        
    def getRotationOrientation2(self):
        return self.rel_rot_orientation2.getMatrix()
        
        
    def writeJoint(self):
        line_00 = ("        joint: {}, total joint,\n"
                   "                {},\n"
                   "                        position, {},\n"
                   "                        position orientation, {},\n"
                   "                        rotation orientation, {},\n"
                   "                {},\n"
                   "                        position, {},\n"
                   "                        position orientation, {},\n"
                   "                        rotation orientation, {},\n"
                   "                position constraint, {}null,\n"
                   "                orientation constraint, {}null;\n\n").format(self.label, self.node1_label, self.relative_offset_1.writeVector(),
                                                                                 self.rel_pos_orientation1.writeMatrix(), self.rel_rot_orientation1.writeMatrix(),
                                                                                 self.node2_label, self.relative_offset_2.writeVector(),
                                                                                 self.rel_pos_orientation2.writeMatrix(), self.rel_rot_orientation2.writeMatrix(),
                                                                                 self.ps, self.rc)
        
        return line_00