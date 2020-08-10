def makeOrientationFromLocalAxes(ZAx, XAx = None):
    '''
    makeOrientationFromLocalAxes(ZAx, XAx): constructs App.Rotation to get into
    alignment with given local Z and X axes. Z axis is followed strictly; X axis
    is a guide and can be not strictly perpendicular to Z axis; it will be
    corrected and modified

    '''
    if XAx is None:
        XAx = App.Vector(0,0,1) #Why Z? Because I prefer local X axis to be aligned so that local XZ plane is parallel to global Z axis.
    #First, compute all three axes.
    ZAx.normalize() #just to be sure; it's important to have the matrix normalized
    YAx = ZAx.cross(XAx) # construct Y axis
    ParaConfusion = 1e-9
    if YAx.Length < ParaConfusion*10.0:
        #failed, try some other X axis direction hint
        XAx = App.Vector(0,0,1)
        YAx = ZAx.cross(XAx)
        if YAx.Length < ParaConfusion*10.0:
            #failed again. Now, we can tell, that local Z axis is along global
            # Z axis
            XAx = App.Vector(1,0,0)
            YAx = ZAx.cross(XAx)

    YAx.normalize()
    XAx = YAx.cross(ZAx) # force X perpendicular

    #hacky way of constucting rotation to a local coordinate system:
    # make matrix,
    m = App.Matrix()
    m.A = list(XAx)+[0.0]+list(YAx)+[0.0]+list(ZAx)+[0.0]+[0.0]*3+[1.0]
    m.transpose() # local axes vectors are columns of matrix, but we put them in as rwos, because it is convenient, and then transpose it.
    # make placement out of matrix,
    tmpplm = App.Placement(m)
    # and extract rotation from placement.
    ori = tmpplm.Rotation
    return ori

def makeOrientationFromLocalAxesUni(priorityString, XAx = None, YAx = None, ZAx = None):
    '''
    makeOrientationFromLocalAxesUni(priorityString, XAx = None, YAx = None, ZAx = None):
    constructs App.Rotation to get into alignment with given local axes.
    Priority string is a string like "ZXY", which defines how axes are made
    perpendicular. For example, "ZXY" means that Z is followed strictly, X is
    made to be perpendicular to Z, and Y is completely ignored (a new one will
    be computed from X and Z). The strict axis must be specified, all other are
    optional.
    '''
    # see Lattice (lattice2GeomUtils.py) for actual code, it's quite long
