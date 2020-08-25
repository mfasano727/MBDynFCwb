import FreeCAD as App
import MBDyn_objects.MBDynJoints
import MBDyn_objects.model_so


def calc_placement(pos, orient, orient_des):
    '''calculate FreeCAD placement from MBDyn position and orientation matrix'''
    App.Console.PrintMessage(" calc: "+str(pos))

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
        m.transpose() # local axes vectors are columns of matrix, but we put them in as rwos, because it is convenient,
                      # and then transpose it.

        # make placement out of matrix
    elif orient_des == 'euler123' or orient_des == 'euler321':  # euler angles
        eulers = orient[0]
        m_roll = App.Matrix(); m_pitch = App.Matrix(); m_yaw = App.Matrix()
        m_roll.unity(); m_pitch.unity(); m_yaw.unity();
        if orient_des == 'euler123':
            m_roll.rotateX(eulers.x)
            m_pitch.rotateY(eulers.y)
            m_yaw.rotateZ(eulers.z)
            m = m_roll.multiply(m_pitch)
            m = m.multiply(m_yaw)
        if orient_des == 'euler321':
            App.Console.PrintMessage(" calc: "+str(pos))
            m_roll.rotateX(eulers.z)
            m_pitch.rotateY(eulers.y)
            m_yaw.rotateZ(eulers.x)
            m = m_yaw.multiply(m_pitch)
            m = m.multiply(m_roll)
            App.Console.PrintMessage(" calc: "+str(m))
    pla = App.Placement(m)
    Rot = pla.Rotation
    return App.Placement(pos, Rot)


def calc_orientation(place, orient_des):
    '''calculates MBDyn orientation matrix of a given orientation description from a FreeCAD placement'''




def calc_orient_Z(zdir,odir = None):
    '''calculate MBDyn orientation matrix in the global frame. with spcified Z direction.  given x and y
    directions are optional'''
    if optimizedir != None:
        ang = zir.getAngle(odir)
        if ang < 0.0000001:
            return [odir.normalize(),App.Vector(0,0,0),  zdir.normalize()]
