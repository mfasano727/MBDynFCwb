import FreeCAD as App

#----------------Gravity creation
def createGravity(grav_parameter):
    from MBDyn_objects.model_so import MBDynGravity
    gravity = App.ActiveDocument.Loads.newObject("App::FeaturePython", "GravityField")
    MBDynGravity(gravity, grav_parameter)
    gravity.ViewObject.Proxy = 0