import os
import sys
from PySide2 import QtCore, QtGui, QtWidgets
import FreeCADGui as Gui
import FreeCAD as App
import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 20, 91, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 41, 17))
        self.label_2.setObjectName("label_2")
        self.install_path = QtWidgets.QLineEdit(Form)
        self.install_path.setGeometry(QtCore.QRect(80, 50, 191, 25))
        self.install_path.setObjectName("install_path")
        self.fpInstallpath = QtWidgets.QPushButton(Form)
        self.fpInstallpath.setGeometry(QtCore.QRect(270, 50, 89, 25))
        self.fpInstallpath.setObjectName("fpInstallpath")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(30, 100, 91, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(30, 130, 51, 17))
        self.label_4.setObjectName("label_4")
        self.out_filename = QtWidgets.QLineEdit(Form)
        self.out_filename.setGeometry(QtCore.QRect(80, 130, 191, 25))
        self.out_filename.setObjectName("out_filename")
        self.fp_outfile = QtWidgets.QPushButton(Form)
        self.fp_outfile.setGeometry(QtCore.QRect(270, 160, 89, 25))
        self.fp_outfile.setObjectName("fp_outfile")
        self.out_location = QtWidgets.QLineEdit(Form)
        self.out_location.setGeometry(QtCore.QRect(80, 160, 191, 25))
        self.out_location.setObjectName("out_location")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(30, 160, 41, 17))
        self.label_5.setObjectName("label_5")
        self.runSim = QtWidgets.QPushButton(Form)
        self.runSim.setGeometry(QtCore.QRect(40, 200, 291, 25))
        self.runSim.setObjectName("runSim")
        self.stopSim = QtWidgets.QPushButton(Form)
        self.stopSim.setGeometry(QtCore.QRect(40, 230, 291, 25))
        self.stopSim.setObjectName("stopSim")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(140, 260, 101, 25))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


        self.fpInstallpath.clicked.connect(self.setinstallpath)
        self.fp_outfile.clicked.connect(self.setoutputpath)
        self.runSim.clicked.connect(self.runSimulation)
        self.stopSim.clicked.connect(self.stopSimulation)
        self.pushButton.clicked.connect(self.outputMessage)
        

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Run Simulation"))
        self.label.setText(_translate("Form", "MBDyn Path:"))
        self.label_2.setText(_translate("Form", "Path:"))
        self.fpInstallpath.setText(_translate("Form", "Browse..."))
        self.label_3.setText(_translate("Form", "Output file:"))
        self.label_4.setText(_translate("Form", "Name:"))
        self.fp_outfile.setText(_translate("Form", "Browse..."))
        self.label_5.setText(_translate("Form", "Path:"))
        self.runSim.setText(_translate("Form", "Run Simulation"))
        self.stopSim.setText(_translate("Form", "Stop Simulation"))
        self.pushButton.setText(_translate("Form", "View status"))
        self.stopSim.setEnabled(False)
        self.pushButton.setEnabled(False)
	
	

    def setinstallpath(self):
        mbdyninstallpath = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.install_path.setText(mbdyninstallpath)

    def setoutputpath(self):
        outlocation = QtWidgets.QFileDialog.getExistingDirectory()
        self.out_location.setText(outlocation)

    def runSimulation(self):
        import os
        import subprocess
        mbdyn = os.path.realpath(self.install_path.text())
        outfile = os.path.realpath(self.out_location.text() + "/" + self.out_filename.text())

##        Change the file path here
        infile = os.path.realpath('/home/adityabhagat/Documents/projects/long')
        self.outlogfile = self.out_location.text() + "/" + "out_msg.log"
        self.ol = open(self.outlogfile, 'w')
        args = [mbdyn, '-f', infile, '-o', outfile]
        self.p = subprocess.Popen(args, \
                  #env=env_vars, \
                  stdout = self.ol, \
                  stderr = subprocess.STDOUT,
                  universal_newlines=True)
        self.runSim.setEnabled(False)
        self.stopSim.setEnabled(True)
        self.pushButton.setEnabled(True)
        
    def stopSimulation(self):
        self.p.terminate()
        self.stopSim.setEnabled(False)
        self.pushButton.setEnabled(True)
	
    def outputMessage(self):
        self.ol.close()
        self.olr = open(self.outlogfile, 'r')
        outmessage = self.olr.read()
        popupdlg = QtWidgets.QMessageBox.information(Form, 'output message', outmessage)
	
	
	
class mbdyn_launchGui(QtWidgets.QDialog,  Ui_Form):	
    def __init__(self):
        super(mbdyn_launchGui, self).__init__()
        self.setupUi(self)
    def GetResources(self):
        return {'Pixmap': os.path.join(MBDwb_icons_path, 'MBDform_icon.svg'),
                'MenuText': "MBD launch",
                'ToolTip': "start MBDyn dialog"}
    def Activated(self):
        """Do something here"""
        App.Console.PrintMessage( Gui.activeWorkbench().iv.initial_time)
        self.show()
        
Gui.addCommand('mbdyn_launchGui', mbdyn_launchGui())	
'''

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    
    sys.exit(app.exec_())
'''
