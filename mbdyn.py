class MBDynModel:
    
    #Container for data block
    def data(self):
        data = dict(problem = 'initial value')
        return data
        
    #Container for initial value block
    def initialvalue(self):
        initialvalue = dict(initial_time = 0,
                                 final_time = 10.,
                                 strategy = [],
                                 min_time_step = [],
                                 max_time_step = [],
                                 time_step = '1.e-3',
                                 tolerance = '1.e-6',
                                 max_iterations = 10,
                                 derivatives_tolerance = '1e-4',
                                 method = 'ms, .6',
                                 linear_solver = 'naive, colamd')
        return initialvalue
    
        
    #Container for control data block
    def controldata(self):
        controldata = dict(structural_nodes = '2',
                                beams = '',
                                rigid_bodies = '2',
                                gravity = True,
                                joints = '',
                                forces = '',
                                adprint = 'equation description',
                                )
        return controldata
    
        
    #container for structural nodes
    def structnodes(self):    
        structnodes = self.createStructuralNodes(self.structuralNode('MASS',
                                                                          'dynamic',
                                                                          'reference', 'global', 'null',
                                                                          'reference', 'global', 'eye',
                                                                          '10.0, 0.0, 0.0',
                                                                          'null'),
                                                 self.structuralNode('MASS+1',
                                                                          'dynamic',
                                                                          'reference', 'global', '1.0, 0.0, 0.0',
                                                                          'reference', 'global', 'eye',
                                                                          'null',
                                                                          'null'))
        return structnodes
    
    
    #container for rigid bodies        
    def rigbodies(self):
        rigbodies = self.createRigidBodies(self.rigidBody('BODY',
                                                'MASS',
                                                'M',
                                                'reference, node, null',
                                                'diag, 10.0, 20.0, 30.0'),
                                           self.rigidBody('BODY+1',
                                                'MASS+1',
                                                'M',
                                                'reference, node, null',
                                                'diag, 10.0, 20.0, 30.0'))
        return rigbodies


    #container for beams3
    def beams3(self):
        beams3 = self.createBeam3()
        return beams3
    
    def beams2(self):
        beams2 = self.createBeam2()
        return beams2
        
    
    #container for joints(self):
    def joints(self):
        joints = self.createJoints()
        return joints
    
    #container for gravity
    def g(self):
        g = self.gravity('uniform', '0.0, 0.0, -1.0', 'const', '9.81')
        return g
        
   
    
    
    #set constants
    def constintegers(self):
        constintegers = self.setConstinteger(MASS = 1, BODY = 100)
        return constintegers
    
    def ints(self):
        ints = self.setIntegers()
        return ints
    
    def reals(self):
        reals = self.setReals(M = 36.0)
        return reals
        
        
        
    #returns a list of structural nodes defined by structuralNode()
    def createStructuralNodes(self, *structural_list):
        return structural_list
        
    #definition of structural node: returns a string of values required for definition
    #of a structural
    def structuralNode(self, label,
                      structype,
                      pos1, pos2, pos3,
                      orient1, orient2, orient3,
                      velocity,
                      angvel):
        
        structural_node = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(label,
                                                                          structype,
                                                                          pos1, pos2, pos3,
                                                                          orient1, orient2, orient3,
                                                                          velocity,
                                                                          angvel)
        
        return structural_node
    
    
    
    
  
    
    #creates rigid bodies from rigidBody()
    def createRigidBodies(self, *rbodies):
        return rbodies

    #definition of rigidbody: returns a string with values of a rigidbody definition 
    def rigidBody(self, label,
                 label_node,
                 mass,
                 offset_node,
                 inertensor):
        
        rBody = "{}, {}, {}, {}, {}".format(label,
                                            label_node,
                                            mass,
                                            offset_node,
                                            inertensor)
        
        return rBody



    #create beam3 elements from beam3() and beam3pzactuator()
    def createBeam3(self, *beams3):
        return beams3

    #definition of beam3
    def beam3(self, label,
              node1, relative_offset1,
              node2, relative_offset2,
              node3, relative_offset3,
              orientation1,
              constitutive_law1,
              orientation2,
              constitutive_law2):

        beam3 = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(label,
                                                                    node1, relative_offset1,
                                                                    node2, relative_offset2,
                                                                    node3, relative_offset3,
                                                                    orientation1,
                                                                    constitutive_law1,
                                                                    orientation2,
                                                                    constitutive_law2)
        return beam3
                                                        
    
    def beam3pzactuator(self, label,
                        node1, relative_offset1,
                        node2, relative_offset2,
                        node3, relative_offset3,
                        orientation1,
                        constitutive_law1,
                        orientation2,
                        constitutive_law2,
                        electrodes_no,
                        abs_node_labels,
                        piezo_matrix1,
                        piezo_matrix2):
        
        beam3pzactuator = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, piezoelectric actuator, {}, {}, {}, {}".format(label,
                                                                                                                      node1, relative_offset1,
                                                                                                                      node2, relative_offset2,
                                                                                                                      node3, relative_offset3,
                                                                                                                      orientation1,
                                                                                                                      constitutive_law1,
                                                                                                                      orientation2,
                                                                                                                      constitutive_law2,
                                                                                                                      electrodes_no,
                                                                                                                      abs_node_labels,
                                                                                                                      piezo_matrix1,
                                                                                                                      piezo_matrix2)
        return beam3pzactuator
    
    
    
    
    #definition of beam2
    def createBeam2(self, *beam2):
        return beam2
    
    def beam2(self, label,
              node1, relative_offset1,
              node2, relative_offset2,
              orientation1,
              constitutive_law1,
              electrodes_no,
              abs_node_labels,
              piezo_matrix1):
        
        beam2 = "{}, {}, {}, {}, {}, {}, {}, piezoelectric actuator, {}, {}, {}".format(label,
                                                                                        node1, relative_offset1,
                                                                                        node2, relative_offset2,
                                                                                        orientation1,
                                                                                        constitutive_law1,
                                                                                        electrodes_no,
                                                                                        abs_node_labels,
                                                                                        piezo_matrix1)
        return beam2
    
        


    #create a tuple of joints using the following functions
    def createJoints(self, *joints):
        return joints
    
    #joint_type := angular acceleratin | angular velocity
    def joint_angular(self, label,
                      joint_type,
                      node_label,
                      relative_direction,
                      acc_vel):
        
        jointang = "{}, {}, {}, {}, {}".format(label,
                                                joint_type,
                                                node_label,
                                                relative_direction,
                                                acc_vel)
        return jointang

    #joint_type = cardano pin
    def joint_cardanopin(self, label,
                         #joint_type,
                         node_label,
                         relative_offset,
                         relative_orientation_matrix,
                         absolute_pin_position,
                         absolute_pin_orientation):
        
        cardanopin = "{}, cardano pin, {}, position, {}, orientation, {}, position, {}, orientation, {}".format(label,
                                                                                                       #joint_type,
                                                                                                       node_label,
                                                                                                       relative_offset,
                                                                                                       relative_orientation_matrix,
                                                                                                       absolute_pin_position,
                                                                                                       absolute_pin_orientation)
        return cardanopin
    
    #joint_type = cardano rotation
    def cardano_rotation(self, label,
                         #joint_type,
                         node1_label,
                         relative_orientation1,
                         node2_label,
                         relative_orientation2):
        
        cardanorot = "{}, cardano rotation, {}, orientation, {}, {}, orientation, {}".format(label,
                                                                                             #joint_type,
                                                                                             node1_label,
                                                                                             relative_orientation1,
                                                                                             node2_label,
                                                                                             relative_orientation2)
        return cardanorot
    
    #joint_type = distance
    def distance(self, label,
                 #joint_type,
                 node1_label,
                 relative_offset1,
                 node2_label,
                 relative_offset2,
                 distance):
        
        dist = "{}, distance, {}, position, {}, {}, position, {}, {}".format(label,
                                                                             #joint_type,
                                                                             node1_label,
                                                                             relative_offset1,
                                                                             node2_label,
                                                                             relative_offset2,
                                                                             distance)
        return dist
    
    #joint_type = revolute rotation | spherical hinge
    def revolute_rotation(self, label,
                          joint_type,
                          node1_label, offset1, orientation1,
                          node2_label, offset2, orientation2):
        revrot = "{}, {}, {}, position, {}, orientation, {}, {}, position, {}, orientation, {}".format(label,
                                                                                                                      joint_type,
                                                                                                                      node1_label, offset1, orientation1,
                                                                                                                      node2_label, offset2, orientation2)
        return revrot
    #joint_type = revolute pin
    def revolute_pin(self, label,
                     #joint_type,
                     node_label, offset, orientation,
                     abs_pin_position, abs_pin_orientation,
                     initial_theta):
        revpin = "{}, revolute pin, {}, position, {}, orientation, {}, position, {}, orientation, {}, {}".format(label,
                                                                                                                 #joint_type,
                                                                                                                 node_label, offset, orientation,
                                                                                                                 abs_pin_position, abs_pin_orientation,
                                                                                                                 initial_theta)
        return revpin
    
    #joint_type = spherical pin
    def spherical_pin(self, label,
                     #joint_type,
                     node_label, offset, orientation,
                     abs_pin_position,
                     abs_orientation):
        sphericalpin = "{}, spherical pin, {}, position, {}, orientation, {}, position, {}, orientation, {}".format(label,
                                                                                                                    #joint_type,
                                                                                                                    node_label, offset, orientation,
                                                                                                                    abs_pin_position,
                                                                                                                    abs_orientation)
        return sphericalpin
    

    #gravity element
    def gravity(self, uniform,
                direction,
                const,
                value):
        
        grav = "{}, {}, {}, {}".format(uniform,
                                               direction,
                                               const,
                                               value)
        
        return grav
    
    
    
    
    
    #set values
    def setConstinteger(self, **constants):
        return constants
    
    def setReals(self, **reals):
        return reals
    
    def setIntegers(self, **integers):
        return integers
    
   
    
    
def WriteInputFile(o):
    
    with open("file.txt", 'w') as f:
        
        #data block
        f.write("begin: data;\n")
        f.write("        problem: {};\n".format(o.data()['problem']))
        f.write("end: data;\n")
        #data block
        
        f.write("\n")
        
        #initial value block
        f.write("begin: initial value;\n")
        f.write("        initial time: {};\n".format(o.initialvalue()['initial_time']))
        f.write("        time step: {};\n".format(o.initialvalue()['time_step']))
        f.write("        final time: {};\n".format(o.initialvalue()['final_time']))
        f.write("        tolerance: {};\n".format(o.initialvalue()['tolerance']))
        f.write("        max iterations: {};\n".format(o.initialvalue()['max_iterations']))
        f.write("        derivatives tolerance: {};\n".format(o.initialvalue()['derivatives_tolerance']))
        f.write("        linear solver: {};\n".format(o.initialvalue()['linear_solver']))
        f.write("        method: {};\n".format(o.initialvalue()['method']))
        f.write("end: initial value;\n")
        #initial value block

        f.write("\n")

        #control data block
        f.write("begin: control data;\n")
        f.write("        structural nodes: {};\n".format(o.controldata()['structural_nodes']))
        f.write("        rigid bodis: {};\n".format(o.controldata()['rigid_bodies']))
        f.write("        gravity;\n")
        f.write("        print: {};\n".format(o.controldata()['adprint']))
        f.write("end: control data;\n")
        #control data block
        
        f.write("\n")

        #set values
        for k in o.constintegers():
                f.write("set: const integer {} = {};\n".format(k, o.constintegers()[k]))
        for k in o.ints():
                f.write("set: integer {} = {};\n".format(k, o.ints()[k]))
        for k in o.reals():
                f.write("set: const real {} = {};\n".format(k, o.reals()[k]))
        #set values
        
        f.write("\n")

        #nodes block
        f.write("begin: nodes;\n")
        for k in o.structnodes():
                f.write("        structural :{};\n".format(k))
        f.write("end: nodes;\n")
        #nodes block
        
        f.write("\n")
        
        #elements block
        f.write("begin: elements;\n")
        for k in o.rigbodies():
                f.write("        body :{};\n".format(k))
        for k in o.beams3():
                f.write("        beam3 :{};\n".format(k))
        for k in o.beams2():
                f.write("        beam2 :{};\n".format(k))
        for k in o.joints():
                f.write("        joint :{};\n".format(k))
        f.write("        gravity: {};\n".format(o.g()))
        f.write("end: elements;\n")
        #elements block
        
        
def main():
    test = MBDynModel()
    WriteInputFile(test)
    
if __name__ == "__main__": main()

        
        
        
        
        















        
