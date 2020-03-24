import FreeCAD as App
import MBDynJoints
import model_so

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
                f.write("        structural nodes: {};\n".format(len(App.ActiveDocument.Nodes.getSubObjects())))
            if len(App.ActiveDocument.Joints.getSubObjects()) != 0:
                f.write("        joints: {};\n".format(len(App.ActiveDocument.Nodes.getSubObjects())))
            if len(App.ActiveDocument.Bodies.getSubObjects()) != 0:
                f.write("        rigid bodies: {};\n".format(len(App.ActiveDocument.Bodies.getSubObjects())))
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
                App.Console.PrintMessage("joint test")
                f.write(App.ActiveDocument.getObject(jointobj[0:-1]).Proxy.writeJoint())
            for forceobj in App.ActiveDocument.Forces.getSubObjects():
                f.write(App.ActiveDocument.getObject(forceobj[0:-1]).Proxy.writeForce())
            if hasattr(App.ActiveDocument, "gravity"):
                f.write(App.ActiveDocument.gravity.Proxy.writeGravity())
            f.write("end: elements;\n\n")
        else:
            App.Console.PrintMessage("MBDyn model does not exist")  
