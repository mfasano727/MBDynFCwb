
import os
from PySide2 import QtWidgets
import FreeCAD as App
import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')


from MBDyn_objects.MBDynObjectFactory.LoadsCreation import createGravity
from MBDyn_guitools.External_Ui.dia_gravity_field import Ui_dia_gravity_field

class GravityField(QtWidgets.QDialog,  Ui_dia_gravity_field):
    def __init__(self, gravObj=None):
        super(GravityField, self).__init__()
        self.gravObj = gravObj
        self.setupUi()

    def setupUi(self):
        super(GravityField, self).setupUi(self)
        if self.gravObj:
            self.loadParameters()

    def accept(self):
        grav_parameters = self.getParameters()
        if self.gravObj:
            self.gravObj.Proxy.setParameters(grav_parameters)
        else:
            createGravity(grav_parameters)
        self.done(1)

    def loadParameters(self):

        #all_items = [self.cbGravityType.itemText(i) for i in range(self.cbGravityType.count())]
        self.cbGravityType.setCurrentText(self.gravObj.FieldType)  # all_items.index())

        self.leGravAcceleration.setText(str(self.gravObj.GravityAcceleration))
        self.leUniformVx.setText(str(self.gravObj.GravityVector[0]))
        self.leUniformVy.setText(str(self.gravObj.GravityVector[1]))
        self.leUniformVz.setText(str(self.gravObj.GravityVector[2]))

        self.leCgFieldMass.setText(str(self.gravObj.CgFieldMass))
        self.leGravConstant.setText(str(self.gravObj.GravityConstant))
        self.leCentralOx.setText(str(self.gravObj.GravityOrigin[0]))
        self.leCentralOy.setText(str(self.gravObj.GravityOrigin[0]))
        self.leCentralOz.setText(str(self.gravObj.GravityOrigin[0]))

    def getParameters(self):
        res = {}
        res["FieldType"] = self.cbGravityType.currentText()

        res["GravityAcceleration"] = 0
        if not "" == self.leGravAcceleration.text():
            res["GravityAcceleration"] = float(self.leGravAcceleration.text())

        g_vect = App.Vector()
        if not "" == self.leUniformVx.text():
            g_vect.x = float(self.leUniformVx.text())
        if not "" == self.leUniformVy.text():
            g_vect.y = float(self.leUniformVy.text())
        if not "" == self.leUniformVz.text():
            g_vect.z = float(self.leUniformVz.text())
        res["GravityVector"] = g_vect

        res["CgFieldMass"] = 0
        if not "" == self.leCgFieldMass.text():
            res["CgFieldMass"] = float(self.leCgFieldMass.text())

        res["GravityConstant"] = 0
        if not "" == self.leGravConstant.text():
            res["GravityConstant"] = float(self.leGravConstant.text())

        g_origin = App.Vector()
        if not "" == self.leCentralOx.text():
            g_origin.x = float(self.leCentralOx.text())
        if not "" == self.leCentralOy.text():
            g_origin.y = float(self.leCentralOy.text())
        if not "" == self.leCentralOz.text():
            g_origin.z = float(self.leCentralOz.text())
        res["GravityOrigin"] = g_origin

        return res