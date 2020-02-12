import numpy as np
import math

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
    
    def __init__(self, index1, vector1, index2, vector2):
        self.index1 = index1
        self.vector1 = vector1                                                  #object of class vec
        
        self.index2 = index2
        self.vector2 = vector2                                                  #object of class vec
        
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




class MBDynIntegrationMethod:
    
    def __init__(self, differential_radius, algebraic_radius, order):
        self.differential_radius = differential_radius                          
        self.algebraic_radius = algebraic_radius
        self.order = order


class crankNicolson(MBDynIntegrationMethod):
    
    def __init__(self):
        super().__init__(1, 1, 2)
        
    def writeMethod(self):
        return "crank nicolson"
    
class ms(MBDynIntegrationMethod):
    
    def __init__(self, differential_radius, algebraic_radius = None,):
        super().__init__(differential_radius, algebraic_radius, None)
        
    def setDifferentialRadius(self, differential_radius):
        self.differential_radius = differential_radius
        
    def getDifferentialRadius(self):
        return self.differential_radius
    
    def setAlgebraicRadius(self, algebraic_radius):
        self.algebraic_radius = algebraic_radius
        
    def getAlgebraicRadius(self):
        return self.algebraic_radius
    
    def writeMethod(self):
        if self.algebraic_radius == None:
            if isinstance(self.differential_radius, float):
                return "ms, {}".format(MBDynConstDrive(self.differential_radius).writeDrive())
            else:
                return "ms, {}".format(self.differential_radius.writeDrive())
        else:
            if isinstance(self.differential_radius, float) and isinstance(self.algebraic_radius, float):
                return "ms, {}, {}".format(MBDynConstDrive(self.differential_radius).writeDrive(), MBDynConstDrive(self.algebraic_radius).writeDrive())
            return "ms, {}, {}".format(self.differential_radius.writeDrive(), self.algebraic_radius.writeDrive())
    

    
class hope(MBDynIntegrationMethod):
    
    def __init__(self, differential_radius, algebraic_radius = None):
        super().__init__(differential_radius, algebraic_radius, None)
        
    def setDifferentialRadius(self, differential_radius):
        self.differential_radius = differential_radius
        
    def getDifferentialRadius(self):
        return self.differential_radius
    
    def setAlgebraicRadius(self, algebraic_radius):
        self.algebraic_radius = algebraic_radius
        
    def getAlgebraicRadius(self):
        return self.algebraic_radius
    
    def writeMethod(self):
        if self.algebraic_radius != None:
            if isinstance(self.differential_radius, float):
                return "hope, {}, {}".format(MBDynConstDrive(self.differential_radius).writeDrive(), MBDynConstDrive(self.differential_radius).writeDrive())
            return "hope, {}, {}".format(self.differential_radius.writeDrive(), self.differential_radius.writeDrive())
        else:
            if isinstance(self.differential_radius, float):
                return "hope, {}, {}".format(MBDynConstDrive(self.differential_radius).writeDrive(), MBDynConstDrive(self.algebraic_radius).writeDrive())
            return "hope, {}, {}".format(self.differential_radius.writeDrive(), self.algebraic_radius.writeDrive())
        

class thirdOrder(MBDynIntegrationMethod):
    
    def __init__(self, differential_radius):
        super().__init__(differential_radius, None, None)
        
    def setDifferentialRadius(self, differential_radius):
        self.differential_radius = differential_radius
        
    def getDifferentialRadius(self):
        return self.differential_radius
    
    def writeMethod(self):
        return "third order, {}".format(self.differential_radius)
        
class bdf(MBDynIntegrationMethod):
    
    def __init__(self, order = 2):
        if ((order == 1) or (order == 2)):
            super().__init__(None, None, order)
        else: print("Order can either be 1 or 2.")
        
    def setOrder(self, order):
        self.order = order
        
    def getOrder(self, order):
        return order
    
    def writeMethod(self):
        return "bdf, order, {}".format(self.order)
    
class implicitEuler(MBDynIntegrationMethod):
    
    def __init__(self):
        
        super().__init__(None, None, None)
        
    def writeMethod(self):
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
        


class MBDynArrayDrive:
    
    def __init__(self, num_drives, *drive_callers):
        
        self.num_drives = num_drives
        self.drive_callers = list(drive_callers)
        
    def setNumberOfDrives(self, num_drives):
        self.num_drives = num_drives
        
    def getNumberOfDrives(self):
        return self.num_drives
    
    def addDriveCaller(self, *drive_caller):
        self.drive_callers.extend(drive_caller)
        
    def removeDriveCaller(self, drive_caller):
        self.drive_callers.remove(drive_caller)
        
    def writeDrive(self):
        drive_line = "array"
        for k in self.drive_callers:
            drive_line = drive_line + ", " + k.writeDrive()
            
        return drive_line
    
    
class MBDynClosestNextDrive:
    
    def __init_(self, initial_time, final_time, increment):
        
        self.initial_time = initial_time
        self.final_time = final_time
        self.increment = increment
        
    def setInitialTime(self, initial_time):
        self.initial_time = initial_time
        
    def getInitialTime(self):
        return self.initial_time
    
    def setFinalTime(self, final_time):
        self.final_time = final_time
        
    def getFinalTime(self):
        return self.final_time
    
    def setIncrement(self, increment):
        self.increment = increment
        
    def getIncrement(self, increment):
        return self.increment
    
    def writeDrive(self):
        drive_line = "closest next, {}, {}, {}".format(self.initial_time, self.final_time, self.increment.writeDrive())
        return drive_line
    
    
class MBDynConstDrive:
    
    def __init__(self, const_coef):
        
        self.const_coef = const_coef
    
    def setConstCoef(self, const_coef):
        self.const_coef = const_coef
        
    def getConstCoef(self):
        return self.const_coef
    
    def writeDrive(self):
        return "const, {}".format(self.const_coef)
    
    
class MBDynCosineDrive:
    
    def __init__(self, initial_time, angular_velocity, amplitude, number_of_cycles, initial_value):
        
        self.initial_time = initial_time
        self.angular_velocity = angular_velocity
        self.amplitude = amplitude
        self.number_of_cycles = number_of_cycles
        self.initial_value = initial_value
     
    def setInitialTime(self, initial_time):
        self.initial_time = initial_time
        
    def getInitialTime(self):
        return self.initial_time
    
    def setAngularVelocity(self, angular_velocity):
        self.angular_velocity = angular_velocity
        
    def getAngularVelocity(self):
        return self.angular_velocity
    
    def setAmplitude(self, amplitude):
        self.amplitude = amplitude
        
    def getAmplitude(self):
        return self.amplitude
    
    def setNumberOfCycles(self, number):
        self.number_of_cycles = number
        
    def getNumberOfCycles(self):
        return self.number_of_cycles
    
    def setInitialValue(self, initial_value):
        self.initial_value = initial_value
        
    def getInitialValue(self):
        return self.initial_value
    
    def writeDrive(self):
        drive_line = "cosine, {}, {}, {}, {}, {}".format(self.initial_time, self.angular_velocity, self.amplitude, 
                                                         self.number_of_cycles, self.initial_value)
        return drive_line
    

class MBDynCubicDrive:
    
    def __init__(self, const_coef, linear_coef, parabolic_coef, cubic_coef):
        
        self.const_coef = const_coef
        self.linear_coef = linear_coef
        self.parabolic_coef = parabolic_coef
        self.cubic_coef = cubic_coef
        
    def setConstCoef(self, const_coef):
        self.const_coef = const_coef
        
    def getConstCoef(self):
        return self.const_coef
    
    def setLinearCoef(self, linear_coef):
        self.linear_coef = linear_coef
        
    def getLinearCoef(self):
        return self.linear_coef
    
    def setParabolicCoef(self, parabolic_coef):
        self.parabolic_coef = parabolic_coef
        
    def getParabolicCoef(self):
        return self.parabolic_coef
    
    def setCubicCoef(self, cubic_coeff):
        self.cubic_coef = cubic_coeff
        
    def getCubicCoef(self):
        return self.cubic_coef
    
    def writeDrive(self):
        drive_line = "cubic, {}, {}, {}, {}".format(self.const_coef, self.linear_coef, self.parabolic_coef, self.cubic_coef)
        return drive_line



class MBDynDirectDrive:
    
    def __init__(self):
        
        self.drive_caller = "direct"
        
    def writeDrive(self):
        drive_line = "direct"
        return drive_line
        

class MBDynDofDrive:
    
    def __init__(self, driving_dof, func_drive):
        
        self.driving_dof = driving_dof
        self.func_drive = func_drive
        
    def setDofDrive(self, driving_dof):
        self.driving_dof = driving_dof
        
    def getDofDrive(self):
        return self.driving_dof
    
    def setFuncDrive(self, func_drive):
        self.func_drive = func_drive
        
    def getFuncDrive(self):
        return self.func_drives
    
    
class MBDynDoubleRampDrive:
    
    def __init__(self, a_slope, a_initial_time, a_final_time, d_slope, d_initial_time, d_final_time, initial_value):
        
        self.a_slope = a_slope
        self.a_initial_time = a_initial_time
        self.a_final_time = a_final_time
        self.d_slope = d_slope
        self.d_initial_time = d_initial_time
        self.d_final_time = d_final_time
        self.initial_value = initial_value
        
    def setaSlope(self, slope):
        self.a_slope = slope
        
    def getaSlope(self):
        return self.a_slope
    
    def setaInitialTime(self, initial_time):
        self.a_initial_time = initial_time
        
    def getaInitialTime(self):
        return self.a_initial_time
    
    def setaFinalTime(self, final_time):
        self.a_final_time = final_time
        
    def getaFinalTime(self):
        return self.a_final_time
    
    def setdSlope(self, slope):
        self.d_slope = slope
        
    def getdSlope(self):
        return self.d_slope
    
    def getdInitialTime(self):
        return self.d_initial_time
    
    def setdFinalTime(self, final_time):
        self.d_final_time = final_time
        
    def getdFinalTime(self):
        return self.d_final_time
       
    def setInitialValue(self, initial_value):
        self.initial_value = initial_value
        
    def getInitialValue(self):
        return self.initial_value
    
    def writeDrive(self):
        drive_line = "double ramp, {}, {}, {}, {}, {}, {}, {}".format(self.a_slope, self.a_initial_time, self.a_final_time,
                                                                      self.d_slope, self.d_initial_time, self.d_final_time, self.initial_value)
        return drive_line
    
    
class MBDynDoubleStepDrive:
    
    def __init__(self, initial_time, final_time, step_value, initial_value):
        
        self.initial_time = initial_time
        self.final_time = final_time
        self.step_value = step_value
        self.initial_value = initial_value
        
    def setInitialTime(self, initial_time):
        self.initial_time = initial_time
        
    def getInitialTime(self):
        return self.initial_time
    
    def setFinalTime(self, final_time):
        self.final_time = final_time
        
    def getFinalTime(self):
        return self.final_time
    
    def setStepValue(self, step_value):
        self.step_value = step_value
        
    def getStepValue(self):
        return self.step_value
    
    def setInitialValue(self, initial_value):
        self.initial_value = initial_value
        
    def getInitialValue(self):
        return self.initial_value
    
    def writeDrive(self):
        drive_line = "double step".format(self.initial_time, self.final_time, self.step_value, self.initial_value)
        return drive_line
    
    
class MBDynDriveDrive:
    
    def __init__(self, drive_caller1, drive_caller2):
        
        self.drive_caller1 = drive_caller1
        self.drive_caller2 = drive_caller2
        
    def setDriveCaller1(self, drive_caller):
        self.drive_caller1 = drive_caller
        
    def getDriveCaller1(self):
        return self.drive_caller1
        
    def setDriveCaller2(self, drive_caller):
        self.drive_caller2 = drive_caller
        
    def getDriveCaller2(self):
        return self.drive_caller2
    
    def writeDrive(self):
        drive_line = "drive, {}, {}".format(self.drive_caller1.writeDrive(), self.drive_caller2.writeDrive())
        return drive_line
    
    
class MBDynElementDrive:
    
    def __init_(self, label, typ, name, index, func_drive):
        
        self.label = label
        self.type = typ
        self.name = name
        self.index = index
        self.func_drive
        
    def setLabel(self, label):
        self.label = label
        
    def getLabel(self):
        return self.label
    
    def setType(self, typ):
        self.type = typ
        
    def getType(self):
        return self.type
    
    def setName(self, name):
        self.name = name
        
    def getName(self):
        return self.name
    
    def setIndex(self, index):
        self.index = index
        
    def getIndex(self):
        return self.index
    
    def setFuncDrive(self, func_drive):
        self.func_drive = func_drive
        
    def getFuncDrive(self):
        return self.func_drive
    
    
    
class MBDynExponentialDrive:
    
    def __init__(self, amplitude, time_constant, initial_time, initial_value):
        
        self.amplitude = amplitude
        self.time_constant = time_constant
        self.initial_time = initial_time
        self.initial_value = initial_value
        
    def setAmplitude(self, amplitude):
        self.amplitude = amplitude
        
    def getAmplitude(self):
        return self.amplitude
    
    def setTimeConstant(self, time_constant):
        self.time_constant = time_constant
        
    def getTimeConstant(self):
        return self.time_constant
    
    def setInitialTime(self, initial_time):
        self.initial_time = initial_time
        
    def getInitialTime(self):
        return self.initial_time
    
    def setInitialValue(self, initial_value):
        self.initial_value = initial_value
        
    def getInitialValue(self):
        return self.initial_value
    
    def writeDrive(self):
        drive_line = "exponential, {}, {}, {}, {}".format(self.amplitude, self.time_constant, self.initial_time, self.initial_value)
        return drive_line
    
    
    
class MBDynFileDrive:
    
    def __init__(self, drive_label, column_number, user_defined):
        
        self.drive_label = drive_label
        self.column_number = column_number
        self.user_defined = user_defined
        
    def setDriveLabel(self, label):
        self.drive_label = label
        
    def getDriveLabel(self):
        return self.drive_label
    
    def setColumnNumber(self, number):
        self.column_number = number
        
    def setUserDefined(self, user_defined):
        self.user_defined = user_defined
        
    def getUserDefined(self):
        return self.user_defined
    

class MBDynFourierSeriesDrive:
    
    def __init__(self, initial_time, angular_velocity, no_of_terms, lst, no_of_cycles, initial_value):
        
        self.initial_time = initial_time
        self.angular_velocity = angular_velocity
        self.no_of_terms = no_of_terms
        self.list_of_terms = list(lst)
        self.no_of_cycles = no_of_cycles
        self.initial_value = initial_value
        
    def setInitialValue(self, initial_value):
        self.initial_value = initial_value
        
    def getInitialValue(self):
        return self.initial_value
    
    def setAngularVelocity(self, angular_velocity):
        self.angular_velocity = angular_velocity
        
    def getAngularVelocity(self):
        return self.angular_velocity
    
    def setNumberOfTerms(self, number):
        self.no_of_terms = number
        
    def getNumberOfTerms(self):
        return self.no_of_terms
    
    def addTerm(self, term):
        self.list_of_terms.append(term)
        
    def removeTerm(self, term):
        self.list_of_terms.remove(term)
        
    def getListOfTerms(self):
        return self.list_of_terms
    
    def setNumberOfCycles(self, number):
        self.no_of_cycles = number
        
    def getNumberOfCycles(self):
        return self.no_of_cycles
    
    def setInitialTime(self, initial_time):
        self.initial_time = initial_time
        
    def getInitialTime(self):
        return self.initial_time
    
    
class MBDynFrequencySweepDrive:
    
    def __init__(self, initial_time, angular_velocity_drive, amplitude_drive, initial_value, final_time, final_value):
        
        self.initial_time = initial_time
        self.angular_velocity_drive = angular_velocity_drive
        self.amplitude_drive = amplitude_drive
        self.initial_value = initial_value
        self.final_time = final_time
        self.final_value = final_value
        
    def setInitialTime(self, initial_time):
        self.initial_time = initial_time
        
    def getInitialTime(self):
        return self.initial_time
    
    def setAngularVelocityDrive(self, angular_velocity_drive):
        self.angular_velocity_drive = angular_velocity_drive
        
    def getAngularVelocityDrive(self):
        return self.angular_velocity_drive
        
    def setAmplitudeDrive(self, amplitude_drive):
        self.amplitude_drive = amplitude_drive
        
    def getAmplitudeDrive(self):
        return self.amplitude_drive
    
    def setInitialValue(self, initial_value):
        self.initial_value = initial_value
        
    def getInitialValue(self):
        return self.initial_value
    
    def setFinalTime(self, final_time):
        self.final_time = final_time
        
    def getFinalTime(self):
        return self.final_time
    
    def setFinalValue(self, final_value):
        self.final_value = final_value
        
    def getFinalValue(self):
        return self.final_value
    

class MBDynGiNaC:
    
    def __init__(self, symbol, expression):
        
        self.symbol = symbol
        self.expression - expression
        
    def setSymbol(self, symbol):
        self.symbol = symbol
        
    def getSymbol(self):
        return self.symbol
    
    def setExpression(self, expression):
        self.expression = expression
        
    def getExpression(self, expression):
        return self.expression
    
    
class MBDynLinearDrive:
    
    def __init__(self, const_coef, slope_coef):
        
        self.const_coef = const_coef
        self.slope_coef = slope_coef
        
    def setConstCoef(self, const_coef):
        self.const_coef = const_coef
        
    def getConstCoef(self):
        return self.const_coef
    
    def setSlopeCoef(self, slope_coef):
        self.slope_coef = slope_coef
        
    def getSlopeCoef(self):
        return self.slope_coef
    
    def writeDrive(self):
        drive_line = "linear, {}, {}".format(self.const_coef, self.slope_coef)
        return drive_line
    
    
class MBDynMeterDrive:
    
    def __init__(self, initial_time, final_time, steps):
        
        self.initial_time = initial_time
        self.final_time = final_time
        self.steps_between_spikes = steps
        
    def setInitialTime(self, initial_time):
        self.initial_time = initial_time
        
    def getInitialTime(self):
        return self.initial_time
    
    def setFinalTime(self, final_time):
        self.final_time = final_time
        
    def getFinalTime(self):
        return self.final_time
    
    def setStepsBetweenSpikes(self, steps):
        self.steps_between_spikes = steps
        
    def getStepsBetweenSpikes(self):
        return self.steps_between_spikes


class MBDynMultDrive:
    
    def __init__(self, drive1, drive2):
        
        self.drive1 = drive1
        self.drive2 = drive2
        
    def setDrive1(self, drive1):
        self.drive1 = drive1
        
    def getDrive1(self):
        return self.drive1
    
    def setDrive2(self, drive2):
        self.drive2 = drive2
        
    def getDrive2(self):
        return self.drive2
    
    def writeDrive(self):
        drive_line = "mult, {}, {}".format(self.drive1.writeDrive(), self.drive2.writeDrive())
        return drive_line
    
    
class MBDynNodeDrive:
    
    def __init__(self, label, typ, name, index, func_drive):
        
        self.label = label
        self.type = typ
        self.name = name
        self.index = index
        self.func_drive
        
    def setLabel(self, label):
        self.label = label
        
    def getLabel(self):
        return self.label
    
    def setType(self, typ):
        self.type = typ
        
    def getType(self):
        return self.type
    
    def setName(self, name):
        self.name = name
        
    def getName(self):
        return self.name
    
    def setIndex(self, index):
        self.index = index
        
    def getIndex(self):
        return self.index
    
    def setFuncDrive(self, func_drive):
        self.func_drive = func_drive
        
    def getFuncDrive(self):
        return self.func_drive
    
    
class MBDynNullDrive:
    
    def __init__(self):
        
        self.drive_caller = 'null'
        
    def writeDrive(self):
        drive_line = "null"
        return drive_line
        

class MBDynParabolic:
    
    def __init__(self, const_coef, linear_coef, parabolic_coef):
        
        self.const_coef = const_coef
        self.linear_coef = linear_coef
        self.parabolic_coef = parabolic_coef
        
    def setConstCoef(self, const_coef):
        self.const_coef = const_coef
        
    def getConstCoef(self):
        return self.const_coef
    
    def setLinearCoef(self, linear_coef):
        self.linear_coef = linear_coef
        
    def getLinearCoef(self):
        return self.linear_coef
    
    def setParabolicCoef(self, parabolic_coef):
        self.parabolic_coef = parabolic_coef
        
    def getParabolicCoef(self):
        return self.parabolic_coef
    
    def writeDrive(self):
        drive_line = "cubic, {}, {}, {}".format(self.const_coef, self.linear_coef, self.parabolic_coef)
        return drive_line
    


class MBDynPeriodicDrive:
    
    def __init__(self, initial_time, period, func_drive):
        
        self.initial_time = initial_time
        self.period = period
        self.func_drive = func_drive
        
    def setInitialTime(self, initial_time):
        self.initial_time = initial_time
        
    def getInitialTime(self):
        return self.initial_time
    
    def setPeriod(self, period):
        self.period = period
        
    def getPeriod(self):
        return self.period
    
    def setFuncDrive(self, func_drive):
        self.func_drive = func_drive
        
    def getFuncDrive(self):
        return self.func_drive
    
    def writeDrive(self):
        drive_line = "periodic, {}, {}, {}".format(self.initial_time, self.period, self.func_drive.writeDrive())
        return drive_line
    
class MBDynPiecewiseLinearDrive:
    
    def __init__(self, num_points, *args):
        
        self.num_points = num_points
        self.args = list(args)
        
    def setNumPoints(self, num_points):
        self.num_points = num_points
      
    def getNumPoints(self):
        return self.num_points
    
    def addPointandValue(self, point, value):
        self.args.extend([point, value])
        
    def removePoint(self, point):
        self.args.remove(point)
    
    def removeValue(self, value):
        self.args.remove(value)
        
    def writeDrive(self):
        drive_line = "piecewise linear"
        for k in self.args:
            drive_line = drive_line + ", " + k
            
        return drive_line
    


class MBDynPostponedDrive:
    
    def __init__(self, label):
        
        self.label = label
        
    def setLabel(self, label):
        self.label = label
        
    def getLabel(self):
        return self.label
    
    def writeDrive(self):
        drive_line = "postponed, {}".format(self.label)
            
        return drive_line
    
    
class MBDynRampDrive:
    
    def __init__(self, slope, initial_time, final_time, initial_value):
        
        self.slope = slope
        self.initial_time = initial_time
        self.final_time = final_time
        self.initial_value = initial_value
        
    def setSlope(self, slope):
        self.slope = slope
        
    def getSlope(self):
        return self.slope
    
    def setInitialTime(self, initial_time):
        self.initial_time = initial_time
        
    def getInitialTime(self):
        return self.initial_time
    
    def setFinalTime(self, final_time):
        self.final_time = final_time
        
    def getFinalTime(self):
        return self.final_time
    
    def setInitialValue(self, initial_value):
        self.initial_value = initial_value
        
    def getInitialValue(self):
        return self.initial_value
    
    def writeDrive(self):
        drive_line = "ramp, {}, {}, {}, {}".format(self.slope, self.initial_time, self.final_time, self.initial_value)
            
        return drive_line
    
    

class MBDynRandomDrive:
    
    def __init__(self, amplitude_value, mean_value, initial_time, final_time, steps, seed_value):
        
        self.amplitude_value = amplitude_value
        self.mean_value = mean_value
        self.initial_time = initial_time
        self.final_time = final_time
        self.steps = steps
        self.seed_value = seed_value
        
    def setAmplitudeValue(self, value):
        self.amplitude_value = value
        
    def getAmplitudeValue(self):
        return self.amplitude_value
    
    def setMeanValue(self, value):
        self.mean_value = value
        
    def getMeanValue(self):
        return self.mean_value
    
    def setInitialTime(self, initial_time):
        self.initial_time = initial_time
        
    def getInitialTime(self):
        return self.initial_time
    
    def setFinalTime(self, final_time):
        self.final_time = final_time
        
    def getFinalTime(self):
        return self.final_time
    
    def setStepsToHoldValue(self, steps):
        self.steps = steps
        
    def getStepsToHoldValue(self):
        return self.steps
    
    def setSeedValue(self, seed_value):
        self.seed_value = seed_value
        
    def getSeedValue(self):
        return self.seed_value
    
    
class MBDynSampleAndHoldDrive:
    
    def __init__(self, function, trigger, initial_value):
        
        self.function = function
        self.trigger = trigger
        self.initial_value = initial_value
        
    def setFunction(self, function):
        self.function = function
        
    def getFunction(self):
        return self.function
    
    def setTrigger(self, trigger):
        self.trigger = trigger
        
    def getTrigger(self):
        return self.trigger
    
    def setInitialValue(self, initial_value):
        self.initial_value = initial_value
        
    def getInitialValue(self):
        return self.initial_value
    
    

class MBDynScalarFunctionDrive:
    
    def __init__(self, name, definition):
        
        self.scalar_function_name = name
        self.scalar_function_definition = definition
        
    def setScalarFunctionName(self, name):
        self.scalar_function_name = name
        
    def getScalarFunctionName(self):
        return self.scalar_function_name
    
    def setScalarFunctionDefinition(self, definition):
        self.scalar_function_definition = definition
        
    def getScalarFunctionDefinition(self):
        return self.scalar_function_definition
    
    

class MBDynSineDrive:
    
    def __init__(self, initial_time, angular_velocity, amplitude, number_of_cycles, initial_value):
        
        self.initial_time = initial_time
        self.angular_velocity = angular_velocity
        self.amplitude = amplitude
        self.number_of_cycles = number_of_cycles
        self.initial_value = initial_value
     
    def setInitialTime(self, initial_time):
        self.initial_time = initial_time
        
    def getInitialTime(self):
        return self.initial_time
    
    def setAngularVelocity(self, angular_velocity):
        self.angular_velocity = angular_velocity
        
    def getAngularVelocity(self):
        return self.angular_velocity
    
    def setAmplitude(self, amplitude):
        self.amplitude = amplitude
        
    def getAmplitude(self):
        return self.amplitude
    
    def setNumberOfCycles(self, number):
        self.number_of_cycles = number
        
    def getNumberOfCycles(self):
        return self.number_of_cycles
    
    def setInitialValue(self, initial_value):
        self.initial_value = initial_value
        
    def getInitialValue(self):
        return self.initial_value
    
    def writeDrive(self):
        drive_line = "sine, {}, {}, {}, {}, {}".format(self.initial_time, self.angular_velocity, self.amplitude, 
                                                       self.number_of_cycles, self.initial_value)
        return drive_line
    
    
    
class MBDynStepDrive:
    
    def __init__(self, initial_time, step_value, initial_value):
        
        self.initial_time = initial_time
        self.step_value = step_value
        self.initial_value = initial_value
        
    def setInitialTime(self, initial_time):
        self.initial_time = initial_time
        
    def getInitialTime(self):
        return self.initial_time
    
    def setStepValue(self, step_value):
        self.step_value = step_value
        
    def getStepValue(self):
        return self.step_value
    
    def setInitialValue(self, initial_value):
        self.initial_value = initial_value
        
    def getInitialValue(self):
        return self.initial_value
    
    def writeDrive(self):
        drive_line = "step, {}, {}, {}".format(self.initial_time, self.step_value, self.initial_value)
        return drive_line
    
    
class MBDynStringDrive:
    
    def __init__(self, expression):
        
        self.expression_string = expression
        
    def setExpressionString(self, expression):
        self.expression_string = expression
        
    def getExpressionString(self):
        return self.expression_string
    
    def writeDrive(self):
        drive_line = 'string, "{}"'.format(self.exression_string)
        return drive_line


class MBDynTanhDrive:
    
    def __init__(self, initial_time, amplitude, slope, initial_value):
        
        self.initial_time = initial_time
        self.amplitude = amplitude
        self.slope = slope
        self.initial_value = initial_value
     
    def setInitialTime(self, initial_time):
        self.initial_time = initial_time
        
    def getInitialTime(self):
        return self.initial_time
    
    def setAmplitude(self, amplitude):
        self.amplitude = amplitude
        
    def getAmplitude(self):
        return self.amplitude
    
    def setSlope(self, slope):
        self.slope = slope
        
    def getSlope(self):
        return self.slope
    
    def setInitialValue(self, initial_value):
        self.initial_value = initial_value
        
    def getInitialValue(self):
        return self.initial_value
    
    def writeDrive(self):
        drive_line = "tanh, {}, {}, {}, {}".format(self.initial_time, self.amplitude, self.slope, self.initial_value)
        return drive_line
        
    
    
    
class MBDynTimeDrive:
    
    def __init__(self):
        self.drive_caller = "time"
        
    def writeDrive(self):
        drive_line = "time"
        return drive_line
        

class MBDynTimestepDrive:
    
    def __init__(self):
        self.drive_caller = "timestep"
        
    def writeDrive(self):
        drive_line = "timestep"
        return drive_line
   
     
class MBDynUnitDrive:
    
    def __init__(self):
        self.drive_caller = "unit"
        
    def writeDrive(self):
        drive_line = "unit"
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
                    
        

    
    






        
        
class MBDynDriverFixedStep:
    
    def __init__(self, count, columns_number, initial_time, time_step, file_name, interpolation = "linear", pad_zeros = None, bailout = None):
        
        self.count = count                                                          #int
        self.columns_number = columns_number                                        #int                                  
        self.initial_time = initial_time                                            #float
        self.time_step = time_step                                                  #float
        self.file_name = file_name                                                  #string
        self.interpolation = interpolation                                          #string = linear|const
        self.pad_zeros = pad_zeros                                                  #string = yes|no
        self.bailout = bailout                                                      #string = none|upper|lower|any
        
    def setCount(self, count):
        self.count = count
        
    def getCount(self):
        return self.count
    
    def setColumnsNunmber(self, columns_number):
        self.columns_number = columns_number
        
    def getColumnsNumber(self):
        return self.columns_number
    
    def setInitialTime(self, initial_time):
        self.initial_time = initial_time
        
    def getInitialTime(self):
        return self.initial_time
    
    def setTimeStep(self, time_step):
        self.time_step = time_step
        
    def getTimeStep(self):
        return self.time_step
    
    def setFileName(self, file_name):
        self.file_name = file_name
        
    def getFileName(self):
        return self.file_name
    
    def setInterpolation(self, interpolation):
        self.interpolation = interpolation
        
    def getInterpolation(self):
        return self.interpolation
    
    def setPadZeros(self, pad_zeros):
        self.pad_zeros = pad_zeros
        
    def getPadZeros(self):
        return self.pad_zeros
    
    def setBailout(self, bailout):
        self.bailout = bailout
        
    def getBailout(self):
        return self.bailout
        
class MBDynVariableStep:
    
    def __init__(self, channels_number, file_name, interpolation = "linear", pad_zeros = None, bailout = None):
        
        self.channels_number = channels_number
        self.interpolation = interpolation
        self.pad_zeros = pad_zeros
        self.bailout = bailout
        
    def setChannelsNumber(self, channel_number):
        self.channel_number = channel_number
        
    def getChannelNumber(self):
        return self.channel_number
    
    def setFileName(self, file_name):
        self.file_name = file_name
        
    def getFileName(self):
        return self.file_name
    
    def setInterpolation(self, interpolation):
        self.interpolation = interpolation
        
    def getInterpolation(self):
        return self.interpolation
    
    def setPadZeros(self, pad_zeros):
        self.pad_zeros = pad_zeros
        
    def getPadZeros(self):
        return self.pad_zeros
    
    def setBailout(self, bailout):
        self.bailout = bailout
        
    def getBailout(self):
        return self.bailout
    

class MBDynDriverSocket:
    
    def __init__(self, columns_number, initial_values, file_name, port_number = 9011):
        
        self.columns_number = columns_number
        self.initial_values = initial_values
        self.file_name = file_name
        self.port_number = port_number
        
    def setColumnsNumber(self, columns_number):
        self.columns_number = columns_number
        
    def getColumnsNumber(self):
        return self.columns_number
    
    def setInitialValues(self, initial_values):
        self.initial_values = initial_values
        
    def getInitialValues(self):
        return self.initial_values
    
    def setFileName(self, file_name):
        self.file_name = file_name
        
    def getFileName(self):
        return self.file_name
    
    def setPortNumber(self, port_number):
        self.port_number = port_number
        
    def getPortNumber(self):
        return self.port_number
    

class MBDynDriverRTAIMailbox:
    
    def __init__(self, stream_name, create_flag, host_name, blocking_flag, columns_number):
        
        self.stream_name = stream_name
        self.create_flag = create_flag                                              #yes|no
        self.host_name = host_name
        self.blocking_flag = blocking_flag
        self.columns_number = columns_number
        
    def setStreamName(self, stream_name):
        self.stream_name = stream_name
        
    def getStreamNome(self):
        return self.stream_name
    
    def setCreateFlag(self, flag):
        self.create_flag = flag
        
    def getCreateFlag(self):
        return self.create_flag
    
    def setHostName(self, host_name):
        self.host_name = host_name
        
    def getHostName(self):
        return self.host_name
    
    def setBlockingFlag(self, blocking_flag):
        self.blocking_flag = blocking_flag
        
    def getBlockingFlag(self):
        return self.blocking_flag
    
    def setColumnsNumber(self, columns_number):
        self.columns_number = columns_number
        
    def getColumnsNumber(self):
        return self.columns_number
    
    
class MBDynDriverStream:
    
    def __init__(self, stream_name, create_flag, path, port_number, host_name, socket_type,
                 signal_flag, blocking_flag, steps, rf_flag, timeout, echo_file_name, precision, shift,
                 columns_number, initial_values, content_modifier, user_defined):
        
        self.stream_name = stream_name
        self.create_flag = create_flag
        
        self.path = path
        self.port_number = port_number
        self.host_name = host_name
        
        self.socket_type = socket_type                                         #default = tcp
        self.signal_flag = signal_flag
        self.blocking_flag = blocking_flag
        
        self.steps = steps
        self.rf_flag = rf_flag
        self.timeout = timeout
        self.echo_file_name = echo_file_name
        
        self.precision = precision
        self.shift = shift
        self.columns_number = columns_number
        self.initial_values = initial_values
        self.content_modifier = content_modifier                               #object of class ContentModifier
        self.user_defined = user_defined
        
    def setStreamName(self, stream_name):
        self.stream_name = stream_name
        
    def getStreamName(self):
        return self.stream_name
    
    def setCreateFlag(self, flag):
        self.create_flag = flag
        
    def getCreateFlag(self):
        return self.create_flag
    
    def setPath(self, path):
        self.path = path
        
    def getPath(self):
        return self.path
    
    def setPortNumber(self, port_number):
        self.port_number = port_number
        
    def getPortNumber(self):
        return self.port_number
    
    def setHostName(self, host_name):
        self.host_name = host_name
        
    def getHostName(self):
        return self.host_name
    
    def setSocketType(self, socket_type):
        self.socket_type = socket_type
        
    def getSocketType(self):
        return self.socket_type
    
    def setSignalFlag(self, flag):
        self.signal_flag = flag
        
    def getSignalFlag(self):
        return self.signal_flag
    
    def setBlockingFlag(self, blocking_flag):
        self.blocking_flag = blocking_flag
        
    def getBlockingFlag(self):
        return self.blocking_flag
    
    def setSteps(self, steps):
        self.steps = steps
        
    def getSteps(self):
        return self.steps
    
    def setReceiveFirstFlag(self, flag):
        self.rf_flag = flag
        
    def getReceiveFirstFlag(self):
        return self.rf_flag
    
    def setTimeout(self, timeout):
        self.timeout = timeout
        
    def getTimeout(self):
        return self.timeout
    
    def setEchoFileName(self, name):
        self.echo_file_name = name
        
    def getEchoFileName(self):
        return self.echo_file_name
    
    def setPrecision(self, precision):
        self.precision = precision
        
    def getPrecision(self):
        return self.precision
    
    def setShift(self, shift):
        self.shift = shift
        
    def getShift(self):
        return self.shift
    
    def setColumnsNumber(self, columns_number):
        self.columns_number = columns_number
        
    def getColumnsNumber(self):
        return self.columns_number
    
    def setInitialValues(self, initial_values):
        self.initial_values = initial_values
        
    def getInitialValues(self):
        return self.initial_values
    
    def setContentModifier(self, content_modifier):
        self.content_modifier = content_modifier
        
    def getContentModifier(self):
        return self.content_modifier
    
    def setUserDefined(self, user_defined):
        self.user_defined = user_defined
        
    def getUserDefined(self):
        return self.user_defined
    
    
class ContentModifier:
    
    def __init__(self, copy, cast_type, swap, all_flag, all_cast, buffer_size):
        
        self.copy = copy
        self.cast_type = cast_type
        self.swap = swap                                                        #yes|no|swap
        self.all_flag = all_flag                                                #yes|no
        self.all_cast = all_cast                                                #cast_type|one_cast(object of class OneCast)
        self.buffer_size = buffer_size
        
    def setCastType(self, cast_type):
        self.cast_type = cast_type
        
    def getCastType(self):
        return self.cast_type
    
    def setSwap(self, swap):
        self.swap = swap
        
    def getSwap(self):
        return self.swap
    
    def setAllFlag(self, all_flag):
        self.all_flag = all_flag
        
    def getAllFlag(self):
        return self.all_flag
    
    def setAllCast(self, cast):
        self.all_cast = cast
        
    def getAllCast(self):
        return self.all_cast
        
    def setBufferSize(self, buffer_size):
        self.buffer_size = buffer_size
        
    def getBufferSize(self):
        return self.buffer_size
    
    
    
    

class MBDynStructuralNode:
    
    def __init__(self, label, struct_type, position, orientation, abs_vel, abs_ang_vel, 
                 orientation_des = None, pos_initial_stiffness = None, vel_initial_stiffness = None, bool_omega_rotates = None):
        
        self.label = label
        self.struct_type = struct_type
        self.position = position                                                #object of class vec
        self.orientation = orientation                                          #onject of class orientationMatrix
        self.orientation_des = orientation_des
        self.abs_vel = abs_vel                                                  #object of class vec
        self.abs_ang_vel = abs_ang_vel                                          #object of class vec
        self.pos_initial_stiffness = pos_initial_stiffness
        self.vel_initial_stiffness = vel_initial_stiffness
        self.bool_omega_rotates = bool_omega_rotates                            #yes|no|bool
        
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
    
    def writeStructuralNode(self):
        line = ("        structural: {}, {},\n"
                "                {},\n"
                "                {},\n"
                "                {},\n"
                "                {};\n").format(self.label, self.struct_type, self.position.writeVector(), self.orientation.writeMatrix(),
                                                                      self.abs_vel.writeVector(), self.abs_ang_vel.writeVector())
        return line
    
    
class MBDynRigidBody:
    
    def __init__(self, label, node_label, mass, com_offset, inertia_matrix):
        
        self.label = label
        self.node_label = node_label
        self.mass = mass
        self.com_offset = com_offset                                             #object of class vec
        self.inertia_matrix = inertia_matrix                                     #object of class matrix
        
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
        
    def writeRigidBody(self):
        line = ("        body: {}, {},\n"
                "                {},\n"
                "                {},\n"
                "                {};\n").format(self.label, self.node_label, self.mass, self.com_offset.writeVector(), self.inertia_matrix.writeMatrix())
        return line
    



class MBDynGravity:
      
    def __init__(self, field_type, *args):
        
        self.field_type = field_type
        
        if self.field_type == "uniform":
            self.gravity_vector = args[0]                                          #object of class vec
            if isinstance(args[1], int) or isinstance(args[1], float):
                self.gravity_value = args[1]
                self.gravity_acc = MBDynTemplateDrive("single", self.gravity_vector, MBDynConstDrive(self.gravity_value))                      
            else:
                self.gravity_acc = MBDynTemplateDrive("single", self.gravity_vector, args[1])
        
        elif self.field_type == "central":
            self.abs_origin = args[0]                                              #object of class Vec
            self.cg_field_mass = args[1]
            self.gravity_constant = args[2]
        
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
        if self.field_type == "uniform":
            gravity_line = "        gravity: uniform, {};\n".format(self.gravity_acc.writeDrive())
            
        elif self.field_type == "central":
            gravity_line = "        gravity: central, origin, {}, mass, {}, G, {};\n".format(self.abs_origin.writeVector(), self.cg_field_mass, self.gravity_constant)
            
        return gravity_line
        
        
 
  
      


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
    
    def __init__(self, initial_time = None, final_time = None, time_step = None,
                 max_iterations = None, tolerance = None, 
                 method = None, derivatives_tolerance = None, 
                 output = None, output_meter = None):
        
        self.initial_time = initial_time                                        #Non-negetive number
        self.final_time = final_time                                            #Positive number
        self.time_step = time_step                                              #Positive number
        self.max_iterations = max_iterations                                    #Positive integer
        self.tolerance = tolerance                                              #Positive number
        self.derivatives_tolerance = derivatives_tolerance                      #Positive number
        self.method = method                                                    #Object of a subclass of MBDynIntegrationMethod
        self.output = output                                                    #Object of class MBDynOutputData
        self.output_meter = output_meter                                        #drivecaller
        
        
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
        line_iv = ""
        if self.initial_time != None:
            line1 = "        initial time: {};\n".format(self.initial_time)
            line_iv = line_iv + line1
        if self.final_time != None:
            line2 = "        final time: {};\n".format(self.final_time)
            line_iv = line_iv + line2
        if self.time_step != None:
            line3 = "        time step: {};\n".format(self.time_step)
            line_iv = line_iv + line3
        if self.tolerance != None:
            line4 = "        tolerance: {};\n".format(self.tolerance)
            line_iv = line_iv + line4
        if self.max_iterations != None:
            line5 = "        max iterations: {};\n".format(self.max_iterations)
            line_iv = line_iv + line5
        if self.method != None:
            line6 = "        method: {};\n".format(self.method.writeMethod())
            line_iv = line_iv + line6
        if self.derivatives_tolerance != None:
            line7 = "        derivatives tolerance: {};\n".format(self.derivatives_tolerance)
            line_iv = line_iv + line7        
        if self.output != None:
            line8 = self.output.write()
            line_iv = line_iv + line8
            
        if self.output_meter != None:
            line9 = "        output meter: {};\n".format(self.output_meter.writeDrive())
            line_iv = line_iv + line9
       
        return line_iv

              
class MBDynControlData:
    
    def __init__(self, nodes, elements):
        self.structural_nodes = len(nodes.nodes)                                             #int
        self.rigid_bodies = len(elements.bodies)                                             #int
        self.joints = len(elements.joints)                                                   #int
        self.forces = len(elements.forces)                                                   #int
        self.gravity = len(elements.gravity)                                                 #Yes|No
        self.use = []
        self.default_output = []
        
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
        if self.structural_nodes != 0:
            line1 = "        structural nodes: {};\n".format(self.structural_nodes)
            cd_line = cd_line + line1
        if self.rigid_bodies != 0:
            line2 = "        rigid bodies: {};\n".format(self.rigid_bodies)
            cd_line = cd_line + line2
        if self.forces != 0:
             line3 = "        forces: {};\n".format(self.forces)
             cd_line = cd_line + line3
        if self.joints != 0:
            line4 = "        joints: {};\n".format(self.joints)
            cd_line = cd_line + line4
        if self.gravity != 0:
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



    
    
            
        
        
    
    
        
    
        


            
            
        
