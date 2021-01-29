

import os
import platform
import time
from PySide2 import QtCore, QtWidgets, QtGui
import FreeCAD as App
import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')
from MBDyn_utilities.MBDyn_funcs import *
from MBDyn_utilities.constants import *
from MBDyn_utilities.Settings_funcs import string_to_list
from MBDyn_utilities.MBDyn_utils import get_active_simulation
from MBDyn_utilities.MBDyn_utils import select_directory


from MBDyn_guitools.External_Ui.dia_launcher import Ui_dia_launcher


class mbdyn_launchGui(QtWidgets.QDialog,  Ui_dia_launcher):
    msgSignal = QtCore.Signal()
    def __init__(self):
        super(mbdyn_launchGui, self).__init__()
        self.setupUi()

        self._decode_frmt = "CP437" #format for windows machine (terminal)
        self._font_name = "Monospac821 BT"
        self._font_size = 8

        # modification of the log editor font
        self.font = QtGui.QFont()
        self.font.setFamily(self._font_name)
        self.font.setPointSize(self._font_size)
        self.editor.setFont(self.font)
        
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        
        self.default_solver = ""
        self.binaries_list = []
        self.use_WSL = False
        self.editor_binary = ""
        self.is_editor_defined = False  # indicate if the file exist
        self.use_cstm_dir = False
        self.keep_res = True
        self.is_edited = False  # Tell the run button to use existing file or write a new one
        self.clear_onsole = False # To know if the console has to be clear before any new command


        self.process = QtCore.QProcess()
        self.process.readyReadStandardError.connect(self.onReadyReadStandardError)
        self.process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)
        self.process.finished.connect(self.runFinished)

        self.msgSignal.connect(self.ConsoleMessage)
        self.console_message = ""
        self.print_time = True  # boolean to decide if the time have to be added to the msg

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

    def getGeneralSettings(self):
        self.use_cstm_dir = App.ParamGet(GENERAL_USER_SETTINGS).GetBool("UseCustomDirectory", 0)
        self.keep_res = App.ParamGet(GENERAL_USER_SETTINGS).GetBool("KeepResultsOnReRun", 1)
        self.editor_binary = App.ParamGet(GENERAL_USER_SETTINGS).GetString("EditorBinaryPath", "")

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

        if not self.use_cstm_dir:
            self.out_location.setReadOnly(True)
            self.fp_outfile.setEnabled(False)
        #Load Sim Name / working Path
        self.out_filename.setText(active_sim.Label) # check if result exist.
        self.out_location.setText(active_sim.WorkingDirectory)

    def checkAviableResults(self):
        pass

    def newLine(self, raw_message, color="#000000"):
        """ This function add nw entry to the editor"""
        spacer=""
        for i in range(7):
            spacer+= "&nbsp;"
 
        results = raw_message.split('\n')

        res = results[0]
        for car in res:
                if car == " ":
                    res = res.replace(" ","&nbsp;")
                else:
                    break
        if len(results) > 1:
            message = res + "<br>"
            for i,res in enumerate(results[1::]):
                for car in res:
                    if car == " ":
                        res = res.replace(" ","&nbsp;")
                    else:
                        break
                message += spacer + res + "<br>" #only if 
        else:
            message = res

        msg_html = '<font color="{0}">{1}</font>'.format(color, message)

        if self.print_time:
            self.console_message = self.console_message + (
                '<font color="#0000FF">{0:05.1f}:</font> {1}'
                .format(time.time() - self.Start, msg_html))

        self.msgSignal.emit()

    def fromatTexttoHtml(self, raw_message, color="#000000"):
        """ This function adapt the raw text from the windows terminal to a html text format.
            Result has to be test on Linux"""
        remove_time_next_line = False
        spacer=""
        for i in range(7):
            spacer+= "&nbsp;"
            
        results = raw_message.split('\r\n')

        res = results[0]
        for car in res:
                if car == " ":
                    res = res.replace(" ","&nbsp;")
                else:
                    break
        if len(results) > 1:
            message = res + "<br>"
            for i,res in enumerate(results[1:-1]):
                for car in res:
                    if car == " ":
                        res = res.replace(" ","&nbsp;")
                    else:
                        break
                message += spacer + res + "<br>" #only if \n is present.
            
            if results[-1] != "":
                res = results[-1]
                for car in res:
                    if car == " ":
                        res = res.replace(" ","&nbsp;")
                    else:
                        break
                message += spacer + res
                remove_time_next_line = True
                
        else:
            message = res
            remove_time_next_line = True
            
        msg_html = '<font color="{0}">{1}</font>'.format(color, message)

        if self.print_time:
            self.console_message = self.console_message + (
                '<font color="#0000FF">{0:05.1f}:</font> {1}'
                .format(time.time() - self.Start, msg_html))
        else:
            self.console_message = self.console_message + (
                '{1}'
                .format(time.time() - self.Start, msg_html))
            
        if remove_time_next_line:
            self.print_time = False
        else:
            self.print_time = True
        self.msgSignal.emit()
    
    # Dialog Slots---------------------------------------
    def setOutputPath(self):
        outlocation = select_directory()
        self.out_location.setText(outlocation)
 
    def writeInputFile(self):
        if self.clear_onsole:
            self.fem_console_message = ""
            self.editor.clear()
            self.clear_onsole = False
        self.Start = time.time()
        self.newLine('{:*^50}\n'.format("Start writing Input file..."))
        doc = App.ActiveDocument
        active_sim = get_active_simulation(doc)
        full_file_name = self.fullFileName()
        if full_file_name:
            writeInputFile(active_sim, full_file_name)
        self.newLine('{:*^50}\n'.format("Finished writing Input file..."))
        self.newLine("Elapsed time: {:1.2f}s\n".format(time.time()-self.Start))        

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
        """Command to run the simulation"""
        import os

        active_solver = self.active_solver.currentText()
        solver_path = App.ParamGet(SOLVERS_USER_SETTINGS).GetString(active_solver, "")

        working_directory = self.out_location.text()

        full_file_name = self.fullFileName()
        # check here for existing results/input
        if not self.is_edited:
            self.Start = time.time()
            self.newLine('{:*^50}\n'.format("Start writing Input file..."))
            if full_file_name:
                doc = App.ActiveDocument
                active_sim = get_active_simulation(doc)
                writeInputFile(active_sim, full_file_name)
            self.newLine('{:*^50}\n'.format("Finished writing Input file..."))
            self.newLine("Elapsed time: {:1.2f}s\n".format(time.time()-self.Start)) 
        self.Start = time.time()
        args= [solver_path, full_file_name]
        cwd = working_directory
        self.m_log_file = os.path.join(working_directory, "_console.log")

        # clear previous text
        if self.clear_onsole:
            self.fem_console_message = ""
            self.editor.clear()
            self.clear_console = False
        
        App.Console.PrintMessage("Simulation Started... \n")
        self.newLine('{:*^50}\n'.format("Simulation Started..."))
        
        self.process.setWorkingDirectory(cwd)
        self.process.start(args[0], [args[1]])

        self.runSim.setEnabled(False)
        self.stopSim.setEnabled(True)
        self.viewStatus.setEnabled(True)

    def stopSimulation(self):
        #self.p.terminate()
        self.process.kill()
        self.stopSim.setEnabled(False)
        self.viewStatus.setEnabled(True)

    def ConsoleMessage(self):
        self.editor.setText(self.console_message)
        self.editor.moveCursor(QtGui.QTextCursor.End)

    def onReadyReadStandardError(self):
        """Capture the standard error"""
        result = self.process.readAllStandardError().data().decode(self._decode_frmt)
        color = "#FF0000"
        self.fromatTexttoHtml(result,color)

    def onReadyReadStandardOutput(self):
        """Capture the standard output"""
        result = self.process.readAllStandardOutput().data().decode(self._decode_frmt)
        self.fromatTexttoHtml(result)

    def runFinished(self):
        self.clear_onsole = True
        self.newLine('{:*^50}\n'.format("Simulation finished..."))
        self.newLine("Elapsed time: {:1.2f}s\n".format(time.time()-self.Start))        
        self.log_file = open(self.m_log_file, 'w')
        self.log_file.write(self.editor.toPlainText())
        self.log_file.close()
        #reset interface

    def outputMessage(self):
        import subprocess
        args = [self.editor_binary, self.m_log_file]
        proc = subprocess.Popen(args)
        outs, errs = proc.communicate()

    # End of Dialog Slots---------------------------------------

