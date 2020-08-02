import numpy as np
import math
import FreeCAD as App
import MBDyn_objects.model_so
from  MBDyn_utilities.MBDyn_funcs import write_drv
from  MBDyn_utilities.MBDyn_funcs import writeVect, writeMatrix, writeOrientationMatrix

class MBDynRevoluteHinge:
    def __init__(self, obj):
        obj.addProperty("App::PropertyInteger", "joint_label", "MBDynRevoluteHinge", "label for revolute hinge joint").joint_label
        obj.addProperty("App::PropertyInteger", "node1_label", "MBDynRevoluteHinge", "label for structural node 1").node1_label
        obj.addProperty("App::PropertyVector", "position1", "MBDynRevoluteHinge", "relative position from structural node 1").position1
        obj.addProperty("App::PropertyVectorList", "orientation1", "MBDynRevoluteHinge", "relative orientation from structural node 1").orientation1
        obj.addProperty("App::PropertyString", "orientation_des1", "MBDynRevoluteHinge", "orientation matrix 1 type ").orientation_des1
        obj.addProperty("App::PropertyInteger", "node2_label", "MBDynRevoluteHinge", "label for structural node 2").node2_label
        obj.addProperty("App::PropertyVector", "position2", "MBDynRevoluteHinge", "relative position from structural node 2").position2
        obj.addProperty("App::PropertyVectorList", "orientation2", "MBDynRevoluteHinge", "relative orientation from structural node 2").orientation2
        obj.addProperty("App::PropertyString", "orientation_des2", "MBDynRevoluteHinge", "orientation matrix 2 type ").orientation_des2

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
        obj.addProperty("App::PropertyInteger","joint_label","MBDynRevolutePin","label for revolute pin joint").joint_label
        obj.addProperty("App::PropertyInteger","node1_label","MBDynRevolutePin","label for structural node 1").node1_label
        obj.addProperty("App::PropertyVector","position1","MBDynRevolutePin","relative position from structural node 1").position1
        obj.addProperty("App::PropertyVectorList","orientation1","MBDynRevolutePin","relative orientation from structural node 1").orientation1
        obj.addProperty("App::PropertyString","orientation_des1","MBDynRevolutePin","orientation matrix 1 type ").orientation_des1
        obj.addProperty("App::PropertyVector","positionf","MBDynRevolutePin","fixed positin for pin").positionf
        obj.addProperty("App::PropertyVectorList","orientationf","MBDynRevolutePin","fixed orientation for pin").orientationf
        obj.addProperty("App::PropertyString","orientation_desf","MBDynRevolutePin","orientation matrix pin type ").orientation_desf

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

        if joint_type == 'fixed':  #Clamp
            self.position_constraint = [True, True, True]
            self.orientation_constraint = [True, True, True]

        elif joint_type == 'pointOnLine':  #inline
            self.position_constraint = [True, True, False]  # assuming local axis 3 is used
            self.orientation_constraint = [False, False, False]

        elif joint_type == 'pointOnPlane':  #inplane
            self.position_constraint = [False, False, True]
            self.orientation_constraint = [False, False, False]

        elif joint_type == 'sphereOnSphere' or joint_type == 'pointOnPoint':  # spherical Hinge
            self.position_constraint = [True, True, True]
            self.orientation_constraint = [False, False, False]

        elif joint_type == 'axisCoincident':  # lockrotation check
            self.position_constraint = [True, True, False]
            self.orientation_constraint = [True, True, False]

        elif joint_type == 'circularEdge':  # revolute hinge
            self.position_constraint = [True, True, True]
            self.orientation_constraint = [True, True, False]

        elif joint_type == 'axisParallel' or joint_type == 'planeParallel' or joint_type == 'axisPlaneNormal':  # Revolute rotation
            self.position_constraint = [False, False, False]
            self.orientation_constraint = [True, True, False]  # assuming local axis 3 is the common axis/perpendicular to both planes

        elif joint_type == 'planeCoincident':  # planeCoincident
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


class FC_totaljoint():
    def __init__(self, obj):
        super(FC_totaljoint, self).__init__()
        obj.addProperty("App::PropertyInteger", "joint_label", "FC_totaljoint", "label for total joint").joint_label
        obj.addProperty("App::PropertyInteger", "node1_label", "FC_totaljoint", "label for structural node 1").node1_label
        obj.addProperty("App::PropertyVector", "position1", "FC_totaljoint", "relative position from structural node 1").position1
        obj.addProperty("App::PropertyVectorList", "pos_orientation1", "FC_totaljoint", "relative orientation from structural node 1").pos_orientation1
        obj.addProperty("App::PropertyString", "pos_orientation_des1", "FC_totaljoint", "orientation matrix 1 type ").pos_orientation_des1
        obj.addProperty("App::PropertyVectorList", "rot_orientation1", "FC_totaljoint", "relative orientation from structural node 1").rot_orientation1
        obj.addProperty("App::PropertyString", "rot_orientation_des1", "FC_totaljoint", "orientation matrix 1 type ").rot_orientation_des1
        obj.addProperty("App::PropertyInteger", "node2_label", "FC_totaljoint", "label for structural node 1").node2_label
        obj.addProperty("App::PropertyVector", "position2", "FC_totaljoint", "relative position from structural node 2").position2
        obj.addProperty("App::PropertyVectorList", "pos_orientation2", "FC_totaljoint", "relative orientation from structural node 2").pos_orientation2
        obj.addProperty("App::PropertyString", "pos_orientation_des2", "FC_totaljoint", "orientation matrix 2 type ").pos_orientation_des2
        obj.addProperty("App::PropertyVectorList", "rot_orientation2", "FC_totaljoint", "relative orientation from structural node 2").rot_orientation1
        obj.addProperty("App::PropertyString", "rot_orientation_des2", "FC_totaljoint", "orientation matrix 2 type ").rot_orientation_des2
        obj.addProperty("App::PropertyBoolList", "pos_constraint", "FC_totaljoint", " position constrants ").pos_constraint
        obj.addProperty("App::PropertyBoolList", "rot_constraint", "FC_totaljoint", "rotation contrants").rot_constraint
        obj.addProperty("App::PropertyBoolList", "vel_constraint", "FC_totaljoint", "velocity constrants").vel_constraint
        obj.addProperty("App::PropertyBoolList", "angvel_constraint", "FC_totaljoint", "angular velocity contraint").angvel_constraint

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
        App.Console.PrintMessage("write:")

        pconst = ""
        rconst = ""
        for count in range(0,3):
            if self.Object.pos_constraint[count] == False and self.Object.vel_constraint[count] == True:
                pconst = pconst + " velocity,"
            elif self.Object.pos_constraint[count] == False and self.Object.vel_constraint[count] == False:
                pconst = pconst + " inactive,"
            else:
                 pconst = pconst + " active,"
            if self.Object.rot_constraint[count] == False and self.Object.angvel_constraint[count] == True:
                rconst = rconst + " angular velocity,"
            elif self.Object.rot_constraint[count] == False and self.Object.angvel_constraint[count] == False:
                rconst = rconst + " inactive,"
            else:
                 rconst = rconst + " active,"

        line = ("        joint: {}, total joint,\n"
                   "                {},\n"
                   "                        position, {},\n"
                   "                        position orientation, {},\n"
                   "                        rotation orientation, {},\n"
                   "                {},\n"
                   "                        position, {},\n"
                   "                        position orientation, {},\n"
                   "                        rotation orientation, {},\n"
                   "                position constraint, {} null,\n"
                   "                orientation constraint, {} null;\n").format(self.Object.joint_label, self.Object.node1_label, writeVect(self.Object.position1),
                                                                                 writeOrientationMatrix(self.Object.pos_orientation_des1, self.Object.pos_orientation1),
                                                                                 writeOrientationMatrix(self.Object.rot_orientation_des1, self.Object.rot_orientation1),
                                                                                 self.Object.node2_label, writeVect(self.Object.position2),
                                                                                 writeOrientationMatrix(self.Object.pos_orientation_des2, self.Object.pos_orientation2),
                                                                                 writeOrientationMatrix(self.Object.rot_orientation_des2, self.Object.rot_orientation2),
                                                                                 pconst, rconst)
        return line


class FC_totalpinjoint():
    def __init__(self, obj):
        super(FC_totalpinjoint, self).__init__()
        obj.addProperty("App::PropertyInteger", "joint_label", "FC_totalpinjoint", "label for structural node 1").joint_label
        obj.addProperty("App::PropertyInteger", "node1_label", "FC_totalpinjoint", "label for structural node 1").node1_label
        obj.addProperty("App::PropertyVector", "position1", "FC_totalpinjoint", "relative position from structural node 1").position1
        obj.addProperty("App::PropertyVectorList", "pos_orientation1", "FC_totalpinjoint", "relative orientation from structural node 1").pos_orientation1
        obj.addProperty("App::PropertyString", "pos_orientation_des1", "FC_totalpinjoint", "orientation matrix 1 type ").pos_orientation_des1
        obj.addProperty("App::PropertyVectorList", "rot_orientation1", "FC_totalpinjoint", "relative orientation from structural node 1").rot_orientation1
        obj.addProperty("App::PropertyString", "rot_orientation_des1", "FC_totalpinjoint", "orientation matrix 1 type ").rot_orientation_des1
        obj.addProperty("App::PropertyVector", "positionf", "FC_totalpinjoint", "position of fixed").positionf
        obj.addProperty("App::PropertyVectorList", "pos_orientationf", "FC_totalpinjoint", "position orientation of fixed").pos_orientationf
        obj.addProperty("App::PropertyString", "pos_orientation_desf", "FC_totalpinjoint", "position orientation matrix fixed type ").pos_orientation_desf
        obj.addProperty("App::PropertyVectorList", "rot_orientationf", "FC_totalpinjoint", "rotation orientation of fixed").rot_orientationf
        obj.addProperty("App::PropertyString", "rot_orientation_desf", "FC_totalpinjoint", "rotation orientation matrix fixed type ").rot_orientation_desf
        obj.addProperty("App::PropertyBoolList", "pos_constraint", "FC_totalpinjoint", "r position constrants").pos_constraint
        obj.addProperty("App::PropertyBoolList", "rot_constraint", "FC_totalpinjoint", "rotation contrants").rot_constraint
        obj.addProperty("App::PropertyBoolList", "vel_constraint", "FC_totalpinjoint", "velocity constrants").vel_constraint
        obj.addProperty("App::PropertyBoolList", "angvel_constraint", "FC_totalpinjoint", "angular velocity contraint").angvel_constraint

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

        pconst = ""
        rconst = ""
        for count in range(0,3):
            if self.Object.pos_constraint[count] == False and self.Object.vel_constraint[count] == True:
                pconst = pconst + " velocity,"
            elif self.Object.pos_constraint[count] == False and self.Object.vel_constraint[count] == False:
                pconst = pconst + " inactive,"
            else:
                 pconst = pconst + " active,"
            if self.Object.rot_constraint[count] == False and self.Object.angvel_constraint[count] == True:
                rconst = rconst + " angular velocity,"
            elif self.Object.rot_constraint[count] == False and self.Object.angvel_constraint[count] == False:
                rconst = rconst + " inactive,"
            else:
                 rconst = rconst + " active,"

        App.Console.PrintMessage("write pin: "+rconst)
        line = ("        joint: {}, total pin joint,\n"
                "                {},\n"
                "                        position, {},\n"
                "                        position orientation, {},\n"
                "                        rotation orientation, {},\n"
                "                    position, {},\n"
                "                    position orientation, {},\n"
                "                    rotation orientation, {},\n"
                "                position constraint, {} null,\n"
                "                orientation constraint, {} null;\n").format(self.Object.joint_label, self.Object.node1_label, writeVect(self.Object.position1),
                                                                                 writeOrientationMatrix(self.Object.pos_orientation_des1, self.Object.pos_orientation1),
                                                                                 writeOrientationMatrix(self.Object.rot_orientation_des1, self.Object.rot_orientation1),
                                                                                 writeVect(self.Object.positionf),
                                                                                 writeOrientationMatrix(self.Object.pos_orientation_desf, self.Object.pos_orientationf),
                                                                                 writeOrientationMatrix(self.Object.rot_orientation_desf, self.Object.rot_orientationf),
                                                                                 pconst, rconst)
        return line

class MBDynInline():
    """inline joint class."""

    def __init__(self, obj):

        obj.addProperty("App::PropertyInteger", "joint_label", "MBDynInline", "label for joint").joint_label
        obj.addProperty("App::PropertyInteger", "node1_label", "MBDynInline", "label for structural node 1").node1_label
        obj.addProperty("App::PropertyVector", "position1", "MBDynInline", "relative position from structural node 1").position1
        obj.addProperty("App::PropertyVectorList", "orientation1", "MBDynInline", "relative orientation from structural node 1").orientation1
        obj.addProperty("App::PropertyString", "orientation_des1", "MBDynInline", "orientation matrix 1 type ").orientation_des1
        obj.addProperty("App::PropertyInteger", "node2_label", "MBDynInline", "label for structural node 2").node2_label
        obj.addProperty("App::PropertyVector", "offset2", "MBDynInline", "relative offset node 2").offset2

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

        line = ("        joint: {}, in line,\n"
                "                {},\n"
                "                {},\n"
                "                {},\n"
                "                {},\n"
                "                {};\n").format(self.Object.joint_label, self.Object.node1_label, writeVect(self.Object.position1),
                                                                      writeOrientationMatrix(self.Object.orientation_des1, self.Object.orientation1),
                                                                      self.Object.node2_label, writeVect(self.Object.offset2))

        return line



class MBDynPrismatic():
    """inline joint class."""

    def __init__(self, obj):

        obj.addProperty("App::PropertyInteger", "joint_label", "MBDynPrismatic", "label for joint").joint_label
        obj.addProperty("App::PropertyInteger", "node1_label", "MBDynPrismatic", "label for structural node 1").node1_label
        obj.addProperty("App::PropertyVectorList", "orientation1", "MBDynPrismatic", "relative orientation from structural node 1").orientation1
        obj.addProperty("App::PropertyString", "orientation_des1", "MBDynPrismatic", "orientation matrix 1 type ").orientation_des1
        obj.addProperty("App::PropertyInteger", "node2_label", "MBDynPrismatic", "label for structural node 2").node2_label
        obj.addProperty("App::PropertyVectorList", "orientation2", "MBDynPrismatic", "relative orientation from structural node 2").orientation2
        obj.addProperty("App::PropertyString", "orientation_des2", "MBDynPrismatic", "orientation matrix 2 type ").orientation_des2

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

        line = ("        joint: {}, prismatic,\n"
                "                {},\n"
                "                {},\n"
                "                {},\n"
                "                {};\n").format(self.Object.joint_label, self.Object.node1_label,
                                                                      writeOrientationMatrix(self.Object.orientation_des1, self.Object.orientation1),
                                                                      self.Object.node2_label,
                                                                      writeOrientationMatrix(self.Object.orientation_des2, self.Object.orientation2))
        return line



class MBDynAxialrotion:
    def __init__(self, obj):
        obj.addProperty("App::PropertyInteger", "joint_label", "MBDynAxialrotation", "label for revolute hinge joint").joint_label
        obj.addProperty("App::PropertyInteger", "node1_label", "MBDynAxialrotation", "label for structural node 1").node1_label
        obj.addProperty("App::PropertyVector", "position1", "MBDynAxialrotation", "relative position from structural node 1").position1
        obj.addProperty("App::PropertyVectorList", "orientation1", "MBDynAxialrotation", "relative orientation from structural node 1").orientation1
        obj.addProperty("App::PropertyString", "orientation_des1", "MBDynAxialrotation", "orientation matrix 1 type ").orientation_des1
        obj.addProperty("App::PropertyInteger", "node2_label", "MBDynAxialrotation", "label for structural node 2").node2_label
        obj.addProperty("App::PropertyVector", "position2", "MBDynAxialrotation", "relative position from structural node 2").position2
        obj.addProperty("App::PropertyVectorList", "orientation2", "MBDynAxialrotation", "relative orientation from structural node 2").orientation2
        obj.addProperty("App::PropertyString", "orientation_des2", "MBDynAxialrotation", "orientation matrix 2 type ").orientation_des2

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

        line = ("        joint: {}, axial rotation,\n"
                "                {},\n"
                "                {},\n"
                "                {},\n"
                "                {},\n"
                "                {},\n"
                "                {};\n").format(self.Object.joint_label, self.Object.node1_label, writeVect(self.Object.position1),
                                                                      writeOrientationMatrix(self.Object.orientation_des1, self.Object.orientation1),
                                                                      self.Object.node2_label, writeVect(self.Object.position2),
                                                                      writeOrientationMatrix(self.Object.orientation_des2, self.Object.orientation2))
        return line
