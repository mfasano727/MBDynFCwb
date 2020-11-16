import FreeCAD as App
from MBDyn_utilities.constants import INPUTFILE_USER_SETTINGS


class Writer():
    _format_spec = "1.3e"
    _zero_threshold = 1e-100

    @classmethod
    def float_to_string(self,value):  #, format_spec='', zero_threshold=1e-15):
        """
        function formating the float value according to a specific format.
        """
        if abs(value) < self._zero_threshold:
            return '{:{format_spec}}'.format(0, format_spec=self._format_spec)
        else:
            return '{:{format_spec}}'.format(value, format_spec=self._format_spec)

    @classmethod
    def set_format(cls, format_spec):
        if format_spec == "":
            format_spec = "1.3e"
        cls._format_spec = format_spec
    
    @classmethod
    def set_zero_threshold(cls, zero_threshold):
        cls._zero_threshold = zero_threshold


def writeVect(vector):
   if vector.x == 0 and vector.y == 0 and vector.z == 0:
      return "null"
   else:
      return "{}, {}, {}".format(Writer().float_to_string(vector.x),
                                 Writer().float_to_string(vector.y),
                                 Writer().float_to_string(vector.z))

# matrix is a list of 3 FreeCAD vectors
def writeMatrix(matrix_type, matrix):
    '''writes matrix to MBDyn input file'''
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
                line_end = line_end + ", " + "{}".format(Writer().float_to_string(i))
        matrix_line = matrix_line + line_end
    elif matrix_type == "sym":
        matrix_line = "{}".format(matrix_type)
        for j in matrix:
            rowcount = rowcount +1
            colcount = 0
            for i in [j.x, j.y, j.z]:
                colcount = colcount + 1
                if colcount >= rowcount:

                    line_end = line_end + ", " + "{}".format(Writer().float_to_string(i))
        matrix_line = matrix_line + line_end
    elif matrix_type == "skew":
        matrix_line = "{}".format(matrix_type)
        for j in matrix:
            rowcount = rowcount +1
            colcount = 0
            for i in [j.x, j.y, j.z]:
                colcount = colcount + 1
                if colcount >= rowcount:
                    line_end = line_end + ", " + "{}".format(Writer().float_to_string(i))
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
                    line_end = line_end + ", " + "{}".format(Writer().float_to_string(i))
        matrix_line = matrix_line + line_end
    return matrix_line

# Orientationmatrix passed is a list of three FreeCAD vectors even if only 2 are used
def writeOrientationMatrix(description, Orientationmatrix):
    '''writes orientation matrix to MBDyn input file'''
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
                line_end = line_end + ", " + "{}".format(Writer().float_to_string(i))
        matrix_line = matrix_line + line_end
     # description xy, xz, yz are for OM with 2 vectors
    elif description == "xy":
        matrix_line = "1, {}, {}, {},  2, {}, {}, {}".format(Writer().float_to_string(Orientationmatrix[0][0]),
                                                             Writer().float_to_string(Orientationmatrix[0][1]),
                                                             Writer().float_to_string(Orientationmatrix[0][2]),
                                                             Writer().float_to_string(Orientationmatrix[1][0]),
                                                             Writer().float_to_string(Orientationmatrix[1][1]),
                                                             Writer().float_to_string(Orientationmatrix[1][2]))
    elif description == "xz":
        matrix_line = "1, {}, {}, {},  3, {}, {}, {}".format(Writer().float_to_string(Orientationmatrix[0][0]), 
                                                             Writer().float_to_string(Orientationmatrix[0][1]),
                                                             Writer().float_to_string(Orientationmatrix[0][2]),
                                                             Writer().float_to_string(Orientationmatrix[2][0]),
                                                             Writer().float_to_string(Orientationmatrix[2][1]),
                                                             Writer().float_to_string(Orientationmatrix[2][2]))
    elif description == "yz":
        matrix_line = "2, {}, {}, {},  3, {}, {}, {}".format(Writer().float_to_string(Orientationmatrix[1][0]),
                                                             Writer().float_to_string(Orientationmatrix[1][1]),
                                                             Writer().float_to_string(Orientationmatrix[1][2]),
                                                             Writer().float_to_string(Orientationmatrix[2][0]),
                                                             Writer().float_to_string(Orientationmatrix[2][1]),
                                                             Writer().float_to_string(Orientationmatrix[2][2]))
    else:
        matrix_line = "{}, {}, {}, {}".format(description,
                                              Writer().float_to_string(Orientationmatrix[0][0]),
                                              Writer().float_to_string(Orientationmatrix[0][1]),
                                              Writer().float_to_string(Orientationmatrix[0][2]))
    return matrix_line

def write_drv(drv_lab):
    ''' finds the drive caller refered to by drv_lab and executes the write_drive of that drive
        caller.  it will return the string returned by the write_drive function. '''
    for drvs in App.ActiveDocument.Drive_callers.Group:
        App.Console.PrintMessage("MBDyn drive"+str(drvs.drive_label)+" "+str(drv_lab))
        if drvs.drive_label == drv_lab:
            return drvs.Proxy.writeDrive()
    return ""


def writeInputFile(sim_obj, name_of_file):
    ''' writes MBDyn input file
    :param sim_obj: Simulation object to write
    :param name_of_file: Name of the text file
    '''
    #set the formet_spec and zero_threshold for float
    format_spec = App.ParamGet(INPUTFILE_USER_SETTINGS).GetString("FORMAT_SPEC","1.7e")
    zero_threshold = float(App.ParamGet(INPUTFILE_USER_SETTINGS).GetString("ZERO_THRESHOLD","1e-15"))
    Writer.set_format(format_spec)
    Writer.set_zero_threshold(zero_threshold)
    doc = sim_obj.Document
    with open(name_of_file, "w") as f:
        if True: #hasattr(doc, "initial_values"):
            f.write("begin: data;\n")
            f.write("        problem: {};\n".format(sim_obj.Problem.type))
            f.write("end: data;\n\n")

            f.write(sim_obj.Proxy.write_problem())

            f.write("begin: control data;\n")
            f.write(sim_obj.Proxy.write_control_data_param())
            if len(doc.Nodes.getSubObjects()) != 0:
                f.write("    structural nodes: {};\n".format(len(doc.Nodes.getSubObjects())))
            if len(doc.Joints.getSubObjects()) != 0:
                f.write("    joints: {};\n".format(len(doc.Joints.getSubObjects())))
            if len(doc.Bodies.getSubObjects()) != 0:
                f.write("    rigid bodies: {};\n".format(len(doc.Bodies.getSubObjects())))
            if len(doc.Loads.getSubObjects()) != 0:
                offset = 0
                if hasattr(doc, "GravityField"): offset = -1
                f.write("    forces: {};\n".format(len(doc.Loads.getSubObjects()) + offset))
            if hasattr(doc, "GravityField"):
                f.write("    gravity;\n")
            f.write("end: control data;\n\n")

            f.write("begin: nodes;\n")
            for nodeobj in doc.Nodes.getSubObjects():
                f.write(doc.getObject(nodeobj[0:-1]).Proxy.writeNode())      # App.ActiveDocument.getObject(nodeobj[0:-1]).Proxy.writeNode()
            f.write("end: nodes;\n\n")

            f.write("begin: elements;\n")
            for bodyobj in doc.Bodies.getSubObjects():
                f.write(doc.getObject(bodyobj[0:-1]).Proxy.writeBody())
            f.write("\n")
            for jointobj in doc.Joints.getSubObjects():
                f.write(doc.getObject(jointobj[0:-1]).Proxy.writeJoint())
            f.write("\n")
            #for forceobj in doc.Forces.getSubObjects():
            #    f.write(doc.getObject(forceobj[0:-1]).Proxy.writeForce())
            f.write("\n")
            if hasattr(doc, "GravityField"):
                f.write(doc.GravityField.Proxy.write())
            f.write("end: elements;\n\n")
        else:
            App.Console.PrintMessage("MBDyn model does not exist")

def check_solid(sol_obj):
    '''checks if FreeCAD odject is solid'''
    if hasattr(sol_obj, 'Shape'):
        App.Console.PrintMessage(" checksolid: " + sol_obj.Name + "\n")
        if sol_obj.Shape.ShapeType == 'Solid' or sol_obj.Shape.ShapeType == 'Compound':
            return True
        else:
            return False
    else:
        return False


def calc_placement(pos, orient, orient_des):
    '''calculate FreeCAD placement from MBDyn position and orientation matrix'''
    tu = App.Units.parseQuantity
    m = App.Matrix()
    x_vec = App.Vector(0,0,0)
    y_vec = App.Vector(0,0,0)
    z_vec = App.Vector(0,0,0)
    if orient_des == 'xy' or orient_des == 'xz' or orient_des == 'yz':
        if orient_des == 'xy':
            x_vec = orient[0]
            x_vec.normalize()  # just to be sure; it's important to have the matrix normalized
            z_vec = x_vec.cross(orient[1])
            Z_vec.normalize()
            y_vec = z_vec.cross(x_vec)
            y_vec.normalize()
        elif orient_des == 'xz':
            z_vec = orient[2]
            z_vec.normalize()  # just to be sure; it's important to have the matrix normalized
            y_vec = z_vec.cross(orient[0])
            y_vec.normalize()
            x_vec = y_vec.cross(z_vec)
            x_vec.normalize()
        elif orient_des == 'yz':
            y_vec = orient[1]
            y_vec.normalize()  # just to be sure; it's important to have the matrix normalized
            x_vec = y_vec.cross(orient[2])
            x_vec.normalize()
            z_vec = x_vec.cross(y_vec)
            z_vec.normalize()
        # make matrix
        m.A = list(x_vec)+[0.0]+list(y_vec)+[0.0]+list(z_vec)+[0.0]+[0.0]*3+[1.0]
        m.transpose() # local axes vectors are columns of matrix, but we put them in as rwos, because it is convenient, and then transpose it.
        # make placement out of matrix,

    elif orient_des == 'euler123' or orient_des == 'euler321':  # euler angles
        eulers = orient[0]
        m_roll = App.Matrix(); m_pitch = App.Matrix(); m_yaw = App.Matrix()
        m_roll.unity(); m_pitch.unity(); m_yaw.unity();
        if orient_des == 'euler123':
            m_roll.rotate(eulers.x)
            m_pitch.rotate(eulers.y)
            m_yaw.rotate(eulers.z)
            m = m_roll.multiply(m_pitch)
            m = m.multiply(m_yaw)
        if orient_des == 'euler321':
            m_roll.rotate(eulers.z)
            m_pitch.rotate(eulers.y)
            m_yaw.rotate(eulers.x)
            m = m_yaw.multiply(m_pitch)
            m = m.multiply(m_roll)

    pla = App.Placement(m)
    Rot = pla.Rotation
    return App.Placement(pos, Rot)

def find_joint_label():
    maxjointnum = 0
    for jnt in App.ActiveDocument.Joints.Group:
        if maxjointnum < jnt.joint_label:
            maxjointnum = jnt.joint_label
    return maxjointnum + 1

def find_node_label():
    maxnodenum = 0
    App.Console.PrintMessage(" find node: ") # + str(maxnodeum) + "\n")
    for nod in App.ActiveDocument.Nodes.Group:
        if maxnodenum < nod.node_label:
            maxnodenum = nod.node_label
    return maxnodenum + 1

def find_body_label():
    maxbodynum = 0
    for bod in App.ActiveDocument.Bodies.Group:
        if maxbodynum < bod.label:
            maxbodynum = bod.label
    return maxbodynum + 1

def find_drive_label():
    maxdrivenum = 0
    App.Console.PrintMessage(" find drive: ")
    for drive in App.ActiveDocument.Drive_callers.Group:
        if maxdrivenum < drive.label:
            maxdrivenum = drive.label
    return maxdrivenum + 1
