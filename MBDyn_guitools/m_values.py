
import os
import sys
import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')

import MBDyn_objects.model_so
from PySide2 import QtCore, QtGui, QtWidgets
import FreeCAD as App
import FreeCADGui as Gui




#class mbdyn_launchGui:

#    def Activated(self):
class Ui_mbdyngui(object):
    def setupUi(self, mbdyngui):
        mbdyngui.setObjectName("mbdyngui")
        mbdyngui.resize(359, 453)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Downloads/logo.xpm"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mbdyngui.setWindowIcon(icon)
        self.tabWidget = QtWidgets.QTabWidget(mbdyngui)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 361, 461))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.formLayoutWidget = QtWidgets.QWidget(self.tab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(40, 10, 259, 251))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.initial_time = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.initial_time.setObjectName("initial_time")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.initial_time)
        self.final_time = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.final_time.setObjectName("final_time")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.final_time)
        self.time_step = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.time_step.setObjectName("time_step")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.time_step)
        self.tolerance = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.tolerance.setObjectName("tolerance")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.tolerance)
        self.derivatives_tolerance = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.derivatives_tolerance.setEnabled(False)
        self.derivatives_tolerance.setObjectName("derivatives_tolerance")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.derivatives_tolerance)
        self.output = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.output.setEnabled(False)
        self.output.setObjectName("output")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.output)
        self.method = QtWidgets.QComboBox(self.formLayoutWidget)
        self.method.setEnabled(False)
        self.method.setObjectName("method")
        self.method.addItem("")
        self.method.addItem("")
        self.method.addItem("")
        self.method.addItem("")
        self.method.addItem("")
        self.method.addItem("")
        self.method.addItem("")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.method)
        self.checkBox = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.checkBox_3)
        self.checkBox_4 = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.checkBox_4.setObjectName("checkBox_4")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.checkBox_4)
        self.checkBox_5 = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.checkBox_5.setChecked(True)
        self.checkBox_5.setObjectName("checkBox_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.checkBox_5)
        self.checkBox_6 = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.checkBox_6.setChecked(True)
        self.checkBox_6.setObjectName("checkBox_6")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.checkBox_6)
        self.checkBox_7 = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.checkBox_7.setChecked(True)
        self.checkBox_7.setObjectName("checkBox_7")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.checkBox_7)
        self.checkBox_8 = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.checkBox_8.setChecked(True)
        self.checkBox_8.setObjectName("checkBox_8")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.checkBox_8)
        self.max_iterations = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.max_iterations.setObjectName("max_iterations")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.max_iterations)
        self.setInitialValues = QtWidgets.QPushButton(self.tab)
        self.setInitialValues.setGeometry(QtCore.QRect(110, 360, 121, 25))
        self.setInitialValues.setObjectName("setInitialValues")
        self.methods_stack = QtWidgets.QStackedWidget(self.tab)
        self.methods_stack.setEnabled(False)
        self.methods_stack.setGeometry(QtCore.QRect(110, 270, 171, 71))
        self.methods_stack.setObjectName("methods_stack")
        self.select = QtWidgets.QWidget()
        self.select.setObjectName("select")
        self.methods_stack.addWidget(self.select)
        self.cn = QtWidgets.QWidget()
        self.cn.setObjectName("cn")
        self.methods_stack.addWidget(self.cn)
        self.ms = QtWidgets.QWidget()
        self.ms.setObjectName("ms")
        self.layoutWidget = QtWidgets.QWidget(self.ms)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 0, 151, 58))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout_2 = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        self.label_9.setObjectName("label_9")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.ms_differential_radius = QtWidgets.QLineEdit(self.layoutWidget)
        self.ms_differential_radius.setObjectName("ms_differential_radius")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ms_differential_radius)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget)
        self.label_10.setObjectName("label_10")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.ms_algebraic_radius = QtWidgets.QLineEdit(self.layoutWidget)
        self.ms_algebraic_radius.setObjectName("ms_algebraic_radius")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ms_algebraic_radius)
        self.methods_stack.addWidget(self.ms)
        self.hope = QtWidgets.QWidget()
        self.hope.setObjectName("hope")
        self.layoutWidget_2 = QtWidgets.QWidget(self.hope)
        self.layoutWidget_2.setGeometry(QtCore.QRect(20, 0, 151, 58))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.formLayout_7 = QtWidgets.QFormLayout(self.layoutWidget_2)
        self.formLayout_7.setContentsMargins(0, 0, 0, 0)
        self.formLayout_7.setObjectName("formLayout_7")
        self.label_19 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_19.setObjectName("label_19")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_19)
        self.hope_differential_radius = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.hope_differential_radius.setObjectName("hope_differential_radius")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.hope_differential_radius)
        self.label_20 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_20.setObjectName("label_20")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_20)
        self.hope_algebraic_radius = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.hope_algebraic_radius.setObjectName("hope_algebraic_radius")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.hope_algebraic_radius)
        self.methods_stack.addWidget(self.hope)
        self.thirdOrder = QtWidgets.QWidget()
        self.thirdOrder.setObjectName("thirdOrder")
        self.layoutWidget_3 = QtWidgets.QWidget(self.thirdOrder)
        self.layoutWidget_3.setGeometry(QtCore.QRect(20, 0, 151, 31))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.formLayout_8 = QtWidgets.QFormLayout(self.layoutWidget_3)
        self.formLayout_8.setContentsMargins(0, 0, 0, 0)
        self.formLayout_8.setObjectName("formLayout_8")
        self.label_26 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_26.setObjectName("label_26")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_26)
        self.torder_differential_radius = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.torder_differential_radius.setObjectName("torder_differential_radius")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.torder_differential_radius)
        self.methods_stack.addWidget(self.thirdOrder)
        self.bdf = QtWidgets.QWidget()
        self.bdf.setObjectName("bdf")
        self.layoutWidget1 = QtWidgets.QWidget(self.bdf)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 0, 151, 31))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.formLayout_9 = QtWidgets.QFormLayout(self.layoutWidget1)
        self.formLayout_9.setContentsMargins(0, 0, 0, 0)
        self.formLayout_9.setObjectName("formLayout_9")
        self.bdf_order = QtWidgets.QLineEdit(self.layoutWidget1)
        self.bdf_order.setFrame(True)
        self.bdf_order.setObjectName("bdf_order")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.bdf_order)
        self.label_12 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_12.setObjectName("label_12")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.methods_stack.addWidget(self.bdf)
        self.ie = QtWidgets.QWidget()
        self.ie.setObjectName("ie")
        self.methods_stack.addWidget(self.ie)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.tab_2)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(40, 30, 160, 131))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_3 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_14 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_14.setEnabled(True)
        self.label_14.setObjectName("label_14")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.structural_nodes = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.structural_nodes.setEnabled(True)
        self.structural_nodes.setObjectName("structural_nodes")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.structural_nodes)
        self.label_16 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_16.setObjectName("label_16")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.rigid_bodies = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.rigid_bodies.setObjectName("rigid_bodies")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.rigid_bodies)
        self.label_17 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_17.setObjectName("label_17")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_17)
        self.forces = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.forces.setObjectName("forces")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.forces)
        self.label_18 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_18.setObjectName("label_18")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.joints = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.joints.setObjectName("joints")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.joints)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label = QtWidgets.QLabel(self.tab_3)
        self.label.setGeometry(QtCore.QRect(50, 50, 67, 17))
        self.label.setText("")
        self.label.setObjectName("label")
        self.add_gravity = QtWidgets.QCheckBox(self.tab_3)
        self.add_gravity.setGeometry(QtCore.QRect(40, 30, 141, 23))
        self.add_gravity.setTristate(False)
        self.add_gravity.setObjectName("add_gravity")
        self.stack_gravity = QtWidgets.QStackedWidget(self.tab_3)
        self.stack_gravity.setEnabled(False)
        self.stack_gravity.setGeometry(QtCore.QRect(50, 120, 241, 231))
        self.stack_gravity.setObjectName("stack_gravity")
        self.uniform = QtWidgets.QWidget()
        self.uniform.setObjectName("uniform")
        self.formLayoutWidget_3 = QtWidgets.QWidget(self.uniform)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 204, 31))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_4 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_13 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_13.setObjectName("label_13")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.gravity_acceleration = QtWidgets.QLineEdit(self.formLayoutWidget_3)
        self.gravity_acceleration.setObjectName("gravity_acceleration")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.gravity_acceleration)
        self.groupBox_2 = QtWidgets.QGroupBox(self.uniform)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 60, 151, 131))
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayoutWidget_6 = QtWidgets.QWidget(self.groupBox_2)
        self.formLayoutWidget_6.setGeometry(QtCore.QRect(10, 30, 130, 89))
        self.formLayoutWidget_6.setObjectName("formLayoutWidget_6")
        self.formLayout_10 = QtWidgets.QFormLayout(self.formLayoutWidget_6)
        self.formLayout_10.setContentsMargins(0, 0, 0, 0)
        self.formLayout_10.setObjectName("formLayout_10")
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget_6)
        self.label_2.setObjectName("label_2")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.ug_x = QtWidgets.QLineEdit(self.formLayoutWidget_6)
        self.ug_x.setObjectName("ug_x")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.ug_x)
        self.ug_y = QtWidgets.QLineEdit(self.formLayoutWidget_6)
        self.ug_y.setObjectName("ug_y")
        self.formLayout_10.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ug_y)
        self.ug_z = QtWidgets.QLineEdit(self.formLayoutWidget_6)
        self.ug_z.setObjectName("ug_z")
        self.formLayout_10.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.ug_z)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget_6)
        self.label_3.setObjectName("label_3")
        self.formLayout_10.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget_6)
        self.label_4.setObjectName("label_4")
        self.formLayout_10.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.stack_gravity.addWidget(self.uniform)
        self.central = QtWidgets.QWidget()
        self.central.setObjectName("central")
        self.groupBox = QtWidgets.QGroupBox(self.central)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 111, 141))
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setObjectName("groupBox")
        self.formLayoutWidget_4 = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(10, 20, 82, 121))
        self.formLayoutWidget_4.setObjectName("formLayoutWidget_4")
        self.formLayout_5 = QtWidgets.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_5.setContentsMargins(0, 0, 0, 0)
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_23 = QtWidgets.QLabel(self.formLayoutWidget_4)
        self.label_23.setObjectName("label_23")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_23)
        self.cg_x = QtWidgets.QLineEdit(self.formLayoutWidget_4)
        self.cg_x.setObjectName("cg_x")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cg_x)
        self.label_24 = QtWidgets.QLabel(self.formLayoutWidget_4)
        self.label_24.setObjectName("label_24")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_24)
        self.cg_y = QtWidgets.QLineEdit(self.formLayoutWidget_4)
        self.cg_y.setObjectName("cg_y")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cg_y)
        self.label_25 = QtWidgets.QLabel(self.formLayoutWidget_4)
        self.label_25.setObjectName("label_25")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_25)
        self.cg_z = QtWidgets.QLineEdit(self.formLayoutWidget_4)
        self.cg_z.setObjectName("cg_z")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cg_z)
        self.pickOrigin = QtWidgets.QPushButton(self.formLayoutWidget_4)
        self.pickOrigin.setObjectName("pickOrigin")
        self.formLayout_5.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.pickOrigin)
        self.formLayoutWidget_5 = QtWidgets.QWidget(self.central)
        self.formLayoutWidget_5.setGeometry(QtCore.QRect(10, 150, 178, 58))
        self.formLayoutWidget_5.setObjectName("formLayoutWidget_5")
        self.formLayout_6 = QtWidgets.QFormLayout(self.formLayoutWidget_5)
        self.formLayout_6.setContentsMargins(0, 0, 0, 0)
        self.formLayout_6.setObjectName("formLayout_6")
        self.label_21 = QtWidgets.QLabel(self.formLayoutWidget_5)
        self.label_21.setObjectName("label_21")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_21)
        self.cg_field_mass = QtWidgets.QLineEdit(self.formLayoutWidget_5)
        self.cg_field_mass.setObjectName("cg_field_mass")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cg_field_mass)
        self.label_22 = QtWidgets.QLabel(self.formLayoutWidget_5)
        self.label_22.setObjectName("label_22")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_22)
        self.grav_constant = QtWidgets.QLineEdit(self.formLayoutWidget_5)
        self.grav_constant.setObjectName("grav_constant")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.grav_constant)
        self.stack_gravity.addWidget(self.central)
        self.gravity_type = QtWidgets.QComboBox(self.tab_3)
        self.gravity_type.setEnabled(False)
        self.gravity_type.setGeometry(QtCore.QRect(60, 80, 91, 25))
        self.gravity_type.setObjectName("gravity_type")
        self.gravity_type.addItem("")
        self.gravity_type.addItem("")
        self.setGravity = QtWidgets.QPushButton(self.tab_3)
        self.setGravity.setGeometry(QtCore.QRect(130, 370, 89, 25))
        self.setGravity.setObjectName("setGravity")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")

        self.retranslateUi(mbdyngui)
        self.tabWidget.setCurrentIndex(0)
        self.methods_stack.setCurrentIndex(0)
        self.stack_gravity.setCurrentIndex(0)
        self.add_gravity.toggled['bool'].connect(self.stack_gravity.setEnabled)
        self.add_gravity.toggled['bool'].connect(self.gravity_type.setEnabled)
        self.gravity_type.currentIndexChanged['int'].connect(self.stack_gravity.setCurrentIndex)
        self.method.currentIndexChanged['int'].connect(self.methods_stack.setCurrentIndex)
        self.checkBox_8.clicked['bool'].connect(self.initial_time.setEnabled)
        self.checkBox_7.clicked['bool'].connect(self.final_time.setEnabled)
        self.checkBox_6.clicked['bool'].connect(self.time_step.setEnabled)
        self.checkBox_5.clicked['bool'].connect(self.max_iterations.setEnabled)
        self.checkBox.clicked['bool'].connect(self.tolerance.setEnabled)
        self.checkBox_2.clicked['bool'].connect(self.derivatives_tolerance.setEnabled)
        self.checkBox_3.clicked['bool'].connect(self.output.setEnabled)
        self.checkBox_4.clicked['bool'].connect(self.method.setEnabled)
        self.checkBox_4.clicked['bool'].connect(self.methods_stack.setEnabled)

        self.setInitialValues.clicked.connect(self.setupInitialValues)
        self.setGravity.clicked.connect(self.setupGravity)

        QtCore.QMetaObject.connectSlotsByName(mbdyngui)

    def retranslateUi(self, mbdyngui):
        _translate = QtCore.QCoreApplication.translate
        mbdyngui.setWindowTitle(_translate("mbdyngui", "Configure MBDyn"))
        #self.initial_time.setText(_translate("mbdyngui", "0.0"))
        self.method.setItemText(0, _translate("mbdyngui", "-select-"))
        self.method.setItemText(1, _translate("mbdyngui", "crank nicolson"))
        self.method.setItemText(2, _translate("mbdyngui", "ms"))
        self.method.setItemText(3, _translate("mbdyngui", "hope"))
        self.method.setItemText(4, _translate("mbdyngui", "third order"))
        self.method.setItemText(5, _translate("mbdyngui", "bdf"))
        self.method.setItemText(6, _translate("mbdyngui", "implicit euler"))
        self.checkBox.setText(_translate("mbdyngui", "Tolerance"))
        self.checkBox_2.setText(_translate("mbdyngui", "Der. Tolerance"))
        self.checkBox_3.setText(_translate("mbdyngui", "Output"))
        self.checkBox_4.setText(_translate("mbdyngui", "Method"))
        self.checkBox_5.setText(_translate("mbdyngui", "Max Iterations"))
        self.checkBox_6.setText(_translate("mbdyngui", "Time Step"))
        self.checkBox_7.setText(_translate("mbdyngui", "Final Time"))
        self.checkBox_8.setText(_translate("mbdyngui", "Initial Time"))
        self.setInitialValues.setText(_translate("mbdyngui", "Set Initial Values"))
        self.label_9.setText(_translate("mbdyngui", "Dif. radius:"))
        self.label_10.setText(_translate("mbdyngui", "Alg. radius:"))
        self.label_19.setText(_translate("mbdyngui", "Dif. radius:"))
        self.label_20.setText(_translate("mbdyngui", "Alg. radius:"))
        self.label_26.setText(_translate("mbdyngui", "Dif. radius:"))
        self.bdf_order.setText(_translate("mbdyngui", "2"))
        self.label_12.setText(_translate("mbdyngui", "Order:        "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("mbdyngui", "Initial Values"))
        self.label_14.setText(_translate("mbdyngui", "Struct. Nodes:"))
        self.label_16.setText(_translate("mbdyngui", "Rigid Bodies:"))
        self.label_17.setText(_translate("mbdyngui", "Forces:"))
        self.label_18.setText(_translate("mbdyngui", "Joints:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("mbdyngui", "Control Data"))
        self.add_gravity.setText(_translate("mbdyngui", "Add Gravity"))
        self.label_13.setText(_translate("mbdyngui", "Gravity Acceleration:"))
        self.groupBox_2.setTitle(_translate("mbdyngui", "Direction:"))
        self.label_2.setText(_translate("mbdyngui", "X:               "))
        self.label_3.setText(_translate("mbdyngui", "Y:"))
        self.label_4.setText(_translate("mbdyngui", "Z:"))
        self.groupBox.setTitle(_translate("mbdyngui", "Absolute Origin:"))
        self.label_23.setText(_translate("mbdyngui", "X:"))
        self.label_24.setText(_translate("mbdyngui", "Y:"))
        self.label_25.setText(_translate("mbdyngui", "Z:"))
        self.pickOrigin.setText(_translate("mbdyngui", "Pick origin"))
        self.label_21.setText(_translate("mbdyngui", "Field Mass:"))
        self.label_22.setText(_translate("mbdyngui", "Gravity constant:"))
        self.gravity_type.setItemText(0, _translate("mbdyngui", "Uniform"))
        self.gravity_type.setItemText(1, _translate("mbdyngui", "Central"))
        self.setGravity.setText(_translate("mbdyngui", "Set Gravity"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("mbdyngui", "Gravity"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("mbdyngui", "Force"))


    def setupInitialValues(self):

        App.Console.PrintMessage("hello")
        MBDynGrp  = App.ActiveDocument.addObject("App::DocumentObjectGroup","MBDyn")
        if len(App.ActiveDocument.getObjectsByLabel("integration_method")) == 0:
            integ_method = MBDynGrp.newObject("App::FeaturePython","integration_method")
            MBDyn_objects.model_so.MBDynIntegrationMethod(integ_method)
            integ_method.ViewObject.Proxy = 0
        else:
            integ_method = App.ActiveDocument.integration_method
        if len(App.ActiveDocument.getObjectsByLabel("initial_values")) == 0 :
            iv = MBDynGrp.newObject("App::FeaturePython","initial_values")
            MBDyn_objects.model_so.MBDynInitialValue(iv)
            iv.ViewObject.Proxy = 0

            referencesGrp  = MBDynGrp.newObject("App::DocumentObjectGroup","References")
            nodesGrp  =MBDynGrp.newObject("App::DocumentObjectGroup","Nodes")
            driveGrp  = MBDynGrp.newObject("App::DocumentObjectGroup","Drive_callers")
            elementsGrp  = MBDynGrp.newObject("App::DocumentObjectGroup","Elements")
            bodies_elemSubGrp = elementsGrp.newObject('App::DocumentObjectGroup', 'Bodies')
            joints_elemSubGrp = elementsGrp.newObject('App::DocumentObjectGroup', 'Joints')
            forces_elemSubGrp = elementsGrp.newObject('App::DocumentObjectGroup', 'Forces')

             # create global reference
            global_ref = referencesGrp.newObject("App::FeaturePython","global_reference")
            MBDyn_objects.model_so.MBDynReference(global_ref)
            global_ref.ViewObject.Proxy = 0
            global_ref.ref_label = 1
            global_ref.ref_name = "global"
            global_ref.refered_label = 0
            global_ref.position = App.Vector(0,0,0)
            global_ref.orientation = [App.Vector(1,0,0), App.Vector(0,1,0), App.Vector(0,0,0)]
            global_ref.orientation_des = "eye"
            global_ref.vel = App.Vector(0,0,0)
            global_ref.ang_vel = App.Vector(0,0,0)
#            referencesGrp.addObject(global_ref)
        else:
            iv = App.ActiveDocument.initial_values


        if self.checkBox_4.checkState():
            App.Console.PrintMessage("meth" + self.method.currentText())
            if self.method.currentIndex() == 0:
                integ_method.differential_radius = 0
                integ_method.algebraic_radius = 0
                integ_method.order = 0
                integ_method.Imethod = ""
            if self.method.currentIndex() == 1:
                integ_method.differential_radius = 0
                integ_method.algebraic_radius = 0
                integ_method.order = 0
                integ_method.Imethod = self.method.currentText()
            elif self.method.currentIndex() == 2:
                integ_method.differential_radius = float(self.ms_differential_radius.text())
                integ_method.algebraic_radius = float(self.ms_algebraic_radius.text())
                integ_method.order = 0
                integ_method.Imethod = self.method.currentText()
                App.Console.PrintMessage("testi")
            elif self.method.currentIndex() == 3:
                integ_method.differential_radius = float(self.hope_differential_radius.text())
                integ_method.algebraic_radius = float(self.hope_algebraic_radius.text())
                integ_method.order = 0
                integ_method.Imethod = self.method.currentText()
            elif self.method.currentIndex() == 4:
                integ_method.differential_radius = float(self.torder_differential_radius.text())
                integ_method.algebraic_radius = 0
                integ_method.order = 0
                integ_method.Imethod = self.method.currentText()
            elif self.method.currentIndex() == 5:
                integ_method.differential_radius = 0
                integ_method.algebraic_radius = 0
                integ_method.order = float(self.bdf_order.text())
                integration_method.Imethod = self.method.currentText()
            elif self.method.currentIndex() == 6:
                integ_method.differential_radius = 0
                integ_method.algebraic_radius = 0
                integ_method.order = 0
                integ_method.Imethod = self.method.currentText()

        App.Console.PrintMessage("hello2")
        iv.initial_time = float(self.initial_time.text())

        iv.final_time = float(self.final_time.text())
        iv.time_step = float(self.time_step.text())
        iv.max_iterations = int(self.max_iterations.text())
        iv.tolerance = float(self.tolerance.text())
        if self.checkBox_2.checkState():
            iv.derivatives_tolerance = float(self.derivatives_tolerance.text())
#        App.Console.PrintMessage("testi")
        App.Console.PrintMessage(iv.Proxy.writeInitialValue())
        if self.checkBox_2.checkState():
            o = MBDynModel.MBDynOutputData(self.output.text())




#        iv = App.ActiveDocument.addObject("App::FeaturePython","MBDynInitialValue")
#        model_so.MBDynInitialValue(iv)
#        iv.ViewObject.Proxy = 0
#        App.Console.PrintMessage( self.iv.initial_time)

#        self.setInitialValues.setEnabled(False)
#        App.Console.PrintMessage( Gui.activeWorkbench().iv.initial_time)
#       App.Console.PrintMessage( Gui.activeWorkbench().elements.gravity)


    def setupGravity(self):
        if len(App.ActiveDocument.getObjectsByLabel("gravity")) == 0 :
            gravity = App.ActiveDocument.MBDyn.newObject("App::FeaturePython","gravity")
            MBDyn_objects.model_so.MBDynGravity(gravity)
            gravity.ViewObject.Proxy = 0

        if self.add_gravity.checkState():
            if self.gravity_type.currentIndex() == 0:
                App.Console.PrintMessage("testg3")
                gravity.field_type = "uniform"
                g_vect = App.Vector()
                App.Console.PrintMessage("testg3" + self.ug_x.text())
                g_vect.x = float(self.ug_x.text())
                g_vect.y = float(self.ug_y.text())
                g_vect.z = float(self.ug_z.text())
                App.Console.PrintMessage("testg4" + self.ug_x.text())

                gravity.gravity_vector = g_vect
                gravity.gravity_value = float(self.gravity_acceleration.text()) * 1000.0 # times 1000 to convert to mm
#                g = MBDynModel.MBDynGravity("uniform", MBDynModel.vec(x, y, z), ga)

            else:
                App.Console.PrintMessage("testg4")
                gravity.field_type = "central"
                g_origin = App.Vector()
                g_origin.x = float(self.cg_x.text())
                g_origin.y = float(self.cg_y.text())
                g_origin.z = float(self.cg_z.text())
                gravity.gravity_origin = g_origin
                gravity.cg_field_mass = float(self.cg_field_mass.text())
                gravity.gravity_constant = float(self.grav_constant.text())
#                g = MBDynModel.MBDynGravity("central", MBDynModel.vec(x, y, z), m, gc)

#            Gui.activeWorkbench().elements.addGravity(g)
#            self.setGravity.setEnabled(False)
        App.Console.PrintMessage( Gui.activeWorkbench().elements.gravity)
        App.Console.PrintMessage( Gui.activeWorkbench().iv.initial_time)
        App.Console.PrintMessage("testg")

class mbdyn_configure(QtWidgets.QDialog, Ui_mbdyngui):
    def __init__(self):
        super(mbdyn_configure,self).__init__()
        self.setupUi(self)
#        self.show()
        import sys
#        app = QtWidgets.QApplication(sys.argv)
#        mbdyngui = QtWidgets.QWidget()
#        ui = Ui_mbdyngui()
#        ui.setupUi(mbdyngui)
#        mbdyngui.show()

#        sys.exit(mbdyngui.exec_())
    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'IVP_icon.svg'),
                'MenuText': "Set MBDyn initial values",
                'ToolTip': "input initial values parameters"}

    def Activated(self):
#        mbdyndia = mbdyn_launchGui()
        self.show()
        if len(App.ActiveDocument.getObjectsByLabel("MBDynInitialValue")) == 0 :
            self.initial_time.setText("0.0")
            self.final_time.setText("5.0")
            self.time_step.setText("0.01")
            self.max_iterations.setText("4")
            self.tolerance.setText("0.001")
        else:
#            self.initial_time.setText(str{App.ActiveDocument.getObjectsByLabel("MBDynInitialValue").initial_time}}
#            App.Console.PrintMessage(App.ActiveDocument.getObjectsByLabel("MBDynInitialValue")}
            App.Console.PrintMessage(App.ActiveDocument.MBDynInitialValue.initial_time)
            App.ActiveDocument.MBDynInitialValue.initial_time
            self.initial_time.setText(str(App.ActiveDocument.MBDynInitialValue.initial_time))
            self.final_time.setText(str(App.ActiveDocument.MBDynInitialValue.final_time))
            self.time_step.setText(str(App.ActiveDocument.MBDynInitialValue.time_step))
            self.max_iterations.setText(str(App.ActiveDocument.MBDynInitialValue.max_iterations))
            self.tolerance.setText(str(App.ActiveDocument.MBDynInitialValue.tolerance))

        if len(App.ActiveDocument.getObjectsByLabel("MBDyngravity")) != 0 :
            self.gravity_acceleration.setText(str(App.ActiveDocument.MBDyngravity.gravity_value))
            self.ug_x.setText(str(App.ActiveDocument.MBDyngravity.gravity_vector.x))
            self.ug_y.setText(str(App.ActiveDocument.MBDyngravity.gravity_vector.y))
            self.ug_z.setText(str(App.ActiveDocument.MBDyngravity.gravity_vector.z))

            self.cg_x.setText(str(App.ActiveDocument.MBDyngravity.gravity_origin.x))
            self.cg_y.setText(str(App.ActiveDocument.MBDyngravity.gravity_origin.y))
            self.cg_z.setText(str(App.ActiveDocument.MBDyngravity.gravity_origin.z))
            self.cg_field_mass.setText(str(App.ActiveDocument.MBDyngravity.cg_field_mass))
            self.grav_constant.setText(str(App.ActiveDocument.MBDyngravity.gravity_constant))
    def IsActive(self):
        if App.ActiveDocument == None:
            return False
        else:
            return True




Gui.addCommand('mbdyn_configure', mbdyn_configure())
