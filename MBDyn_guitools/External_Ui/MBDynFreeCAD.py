

import os
from PySide2 import QtCore, QtWidgets
import FreeCAD as App
import MBDyn_locator
import platform
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')
from MBDyn_utilities.MBDyn_funcs import *
from MBDyn_utilities.constants import *
from MBDyn_utilities.Settings_funcs import string_to_list
from MBDyn_utilities.MBDyn_utils import get_active_simulation
from MBDyn_utilities.MBDyn_utils import select_directory


from MBDyn_guitools.External_Ui.dia_launcher import Ui_dia_launcher


class mbdyn_launchGui(QtWidgets.QDialog,  Ui_dia_launcher):
    def __init__(self):
        super(mbdyn_launchGui, self).__init__()
        self.setupUi()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.default_solver = ""
        self.binaries_list = []
        self.use_WSL = False
        self.is_edited = False
        self.editor_binary = ""
        self.is_editor_defined = False  # indicate if the file exist
        self.is_edited = False  # Tell the run button to use existing file or write a new one

    def setupUi(self):
        super(mbdyn_launchGui, self).setupUi(self)

        # define connections for dialog widgets
        self.fp_outfile.clicked.connect(self.setOutputPath)
        self.runSim.clicked.connect(self.runSimulation)
        self.stopSim.clicked.connect(self.stopSimulation)
        self.viewStatus.clicked.connect(self.outputMessage)
        self.writeIF.clicked.connect(self.writeInputFile) # function from MBDyn_utilities.MBDyn_funcs
        QtCore.QObject.connect(self.writeIF, QtCore.SIGNAL("clicked(bool)"), self.editIF.setDisabled)
        #self.writeIF.clicked.connect(lambda x=True: self.editIF.setEnabled(x))
        self.editIF.clicked.connect(self.editInputFile)
        

        self.stopSim.setEnabled(False)
        self.viewStatus.setEnabled(False)

    def getWorkbenchSettings(self):
        self.getSolverSettings()
        self.getGeneralSettings()

    def getSolverSettings(self):
        self.default_solver = App.ParamGet(SOLVERS_USER_SETTINGS).GetString("DEFAULT_SOLVER", "")
        self.binaries_list = string_to_list(App.ParamGet(SOLVERS_USER_SETTINGS).GetString("BINARIES_LIST", ""), SEP)
        self.use_WSL = App.ParamGet(SOLVERS_USER_SETTINGS).GetBool("USE_WSL", False)

    def updateView(self):
        doc = App.ActiveDocument
        active_sim = get_active_simulation(doc)

        if self.editor_binary:
            self.is_editor_defined = True
        self.editIF.setEnabled(False)

        # Fill combobox Data
        self.active_solver.clear()
        self.active_solver.addItems(self.binaries_list)
        #set default item
        self.active_solver.setCurrentIndex(self.binaries_list.index(self.default_solver))

        if platform.system() == "Windows":
            self.useWSL.setChecked(self.use_WSL)
        else:
            self.useWSL.setEnabled(False)

        #Load Sim Name / working Path
        self.out_filename.setText(active_sim.Label) # check if result exist.
        self.out_location.setText(active_sim.WorkingDirectory)

    def getGeneralSettings(self):
        self.editor_binary = App.ParamGet(GENERAL_USER_SETTINGS).GetString("EditorBinaryPath", "")

    # Dialog Slots---------------------------------------
    def setOutputPath(self):
        outlocation = select_directory()
        self.out_location.setText(outlocation)
 
    def writeInputFile(self):
        doc = App.ActiveDocument
        active_sim = get_active_simulation(doc)
        full_file_name = self.fullFileName()
        if full_file_name:
            writeInputFile(active_sim, full_file_name)
            
    def editInputFile(self):
        import subprocess
        full_file_name = self.fullFileName()
        if full_file_name:
            args = [self.editor_binary, full_file_name]
            proc = subprocess.Popen(args)
            outs, errs = proc.communicate()
            self.is_edited = True

    def fullFileName(self):
        import os
        working_directory = self.out_location.text()
        file_name = self.out_filename.text()
        #  Check the file extension, mandatory but allow to use highlitght syntax in atom
        if not file_name.endswith(tuple(MBDYN_EXTENSIONS)):
            file_name += MBDYN_EXTENSIONS[0]
        if os.path.isdir(working_directory):
            full_file_name = os.path.join(working_directory, file_name)
            App.Console.PrintMessage("Filename: " + full_file_name + "\n")
            return full_file_name
        else:
            App.Console.PrintMessage("Filename" + working_directory + " not a dir\n")  
            return ""

    def runSimulation(self):
        App.Console.PrintMessage("Simulation Started..... \n")
        import os
        import subprocess

        active_solver = self.active_solver.currentText()
        solver_path = App.ParamGet(SOLVERS_USER_SETTINGS).GetString(active_solver, "")

        working_directory = self.out_location.text()

        full_file_name = self.fullFileName()
        if not self.is_edited:
            if full_file_name:
                doc = App.ActiveDocument
                active_sim = get_active_simulation(doc)
                writeInputFile(active_sim, full_file_name)

        args= [solver_path, full_file_name]
        cwd = "D:\\Garnier\\Documents\\01_programmation\\01_Python\\mbdyn_FreeCAD\\_SOLVERS_\\mbdyn-1.7.2-win32\\"
        m_log_file = os.path.join(working_directory, "_console.log")
        self.log_file = open(m_log_file, 'w')

        #subprocess.PIPE
        self.p = subprocess.Popen(args, shell=True, cwd=cwd, stdout=self.log_file, stderr=subprocess.STDOUT) #
        App.Console.PrintMessage("Start Now")

        self.runSim.setEnabled(False)
        self.stopSim.setEnabled(True)
        self.viewStatus.setEnabled(True)

    def stopSimulation(self):
        #self.p.terminate()
        self.p.kill()
        print(self.p)
        self.stopSim.setEnabled(False)
        self.viewStatus.setEnabled(True)

    def outputMessage(self):
        import subprocess
        log_file_name = self.log_file.name
        self.log_file.close()
        args = [self.editor_binary, log_file_name]
        proc = subprocess.Popen(args)
        outs, errs = proc.communicate()

    # End of Dialog Slots---------------------------------------

