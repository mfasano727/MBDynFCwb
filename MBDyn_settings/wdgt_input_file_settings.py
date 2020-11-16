#!/usr/bin/env python3
# coding: utf-8
#
# revpin_joint_cmd.py
import os
import re
import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')

from PySide2 import QtCore, QtGui, QtWidgets
import FreeCAD as App

from MBDyn_settings.ui_input_file_settings import Ui_input_file_settings
from MBDyn_utilities.constants import *
from MBDyn_utilities.MBDyn_funcs import Writer

class wdgt_input_file_settings(QtWidgets.QWidget, Ui_input_file_settings):
    """MBD input file double format
    
    TODO: sqve function, update example function"""
    
    formatChanged = QtCore.Signal()
    _format_types = {'Scientific':'e','Floating':'f'}
    
    def __init__(self):
        super(wdgt_input_file_settings, self).__init__()
        self.setupUi()

    def setupUi(self):
        super(wdgt_input_file_settings, self).setupUi(self)
        self._format_spec = "1.7e"
        self._zero_threshold = 1e-15
        
        self.input_ex_1.setText("1.23456789")
        self.input_ex_2.setText("12.3456789")
        self.input_ex_3.setText("-123.456789123")
        self.input_ex_4.setText("-1234567.89123")
        self.input_ex_5.setText("0.000000001")
        
        re_float = QtGui.QRegExpValidator(QtCore.QRegExp("[-+]?[0-9]*[\.,]?[0-9]+([eE][-+]?[0-9]+)?"))        
        self.input_ex_1.setValidator(re_float)
        self.input_ex_2.setValidator(re_float)
        self.input_ex_3.setValidator(re_float)
        self.input_ex_4.setValidator(re_float)
        self.input_ex_5.setValidator(re_float)
        re_zero_threshold = QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]*[\.,]?[0-9]+([eE][-+]?[0-9]+)?"))
        self.zero_threshold.setValidator(re_zero_threshold)
        
        
        # Connections
        self.format_type.currentTextChanged.connect(self.getFormat)
        self.decimal_number.valueChanged.connect(self.getFormat)
        self.total_width.valueChanged.connect(self.getFormat)
        self.leading_zeros.clicked.connect(self.getFormat)
        self.zero_threshold.editingFinished.connect(self.getFormat)

        self.input_ex_1.editingFinished.connect(self.updateExamples)
        self.input_ex_2.editingFinished.connect(self.updateExamples)
        self.input_ex_3.editingFinished.connect(self.updateExamples)
        self.input_ex_4.editingFinished.connect(self.updateExamples)
        self.input_ex_5.editingFinished.connect(self.updateExamples)

        self.formatChanged.connect(self.updateExamples)

    def saveSettings(self):
        """Save double format settings"""
        App.Console.PrintMessage("Saving MBDyn double format settings...")
        App.ParamGet(INPUTFILE_USER_SETTINGS).SetString("FORMAT_SPEC", self._format_spec)
        App.ParamGet(INPUTFILE_USER_SETTINGS).SetString("ZERO_THRESHOLD", "{:1.4e}".format(self._zero_threshold))        
        App.Console.PrintMessage("... MBDyn double format settings saved." + "\n")
    
    def loadSettings(self):
        """Load solver settings"""
        App.Console.PrintMessage("Loading MBDyn double format settings...")
        
        #get Actual settings
        self._format_spec = App.ParamGet(INPUTFILE_USER_SETTINGS).GetString("FORMAT_SPEC","1.7e")
        self._zero_threshold = float(App.ParamGet(INPUTFILE_USER_SETTINGS).GetString("ZERO_THRESHOLD","1e-15"))
        # update the ui
        self.updateView()

        App.Console.PrintMessage("... MBDyn double format settings loaded." + "\n")
            
    def updateView(self):
        # parse the format_spec to update each widget
        line_search = "(?P<leading_zero>0?)(?P<width>[0-9])+\.(?P<decimals>[0-9])+(?P<type>[fe])"
        
        test = re.search(line_search, self._format_spec)
        if test:
            if test.group('leading_zero') == "0":
                self.leading_zeros.setChecked(True)
            else:
                self.leading_zeros.setChecked(False)
            self.total_width.setProperty("value", int(test.group('width')))
            
            self.decimal_number.setProperty("value", int(test.group('decimals')))
            
            for key, value in self._format_types.items():
                if value == test.group('type'):
                    self.format_type.setCurrentText(key)
            self.format_spec.setText(self._format_spec)
        else:
            print("unable to read the format, default format is used (1.3e)")
            self.format_spec.setText("1.7e")
        
        
        self.zero_threshold.setText(str(self._zero_threshold))
        self.formatChanged.emit()
    
    
    def getFormat(self, *args):
        """
        Write the format string using the different user input. 
        """
        _format_spec = ""
        
        _format_type = self._format_types[str(self.format_type.currentText())]
        
        _leading_zeros = ""
        if self.leading_zeros.isChecked(): _leading_zeros = "0"
        
        _decimals = str(self.decimal_number.value())
        
        _total_width = str(self.total_width.value())
        
        
        _format_spec = "{}{}.{}{}".format(_leading_zeros,
                                         _total_width,
                                         _decimals,
                                         _format_type)
        print("new format:", _format_spec)
        self._format_spec = _format_spec
        self._zero_threshold = float(self.zero_threshold.text())
        self.format_spec.setText(_format_spec)
        self.formatChanged.emit()
        

    def updateExamples(self):
        Writer.set_format(self._format_spec)
        Writer.set_zero_threshold(self._zero_threshold)
        
        ex1 = float(self.input_ex_1.text().replace(",","."))
        ex2 = float(self.input_ex_2.text().replace(",","."))
        ex3 = float(self.input_ex_3.text().replace(",","."))
        ex4 = float(self.input_ex_4.text().replace(",","."))
        ex5 = float(self.input_ex_5.text().replace(",","."))
        self.output_ex_1.setText(Writer.float_to_string(ex1))
        self.output_ex_2.setText(Writer.float_to_string(ex2))
        self.output_ex_3.setText(Writer.float_to_string(ex3))
        self.output_ex_4.setText(Writer.float_to_string(ex4))
        self.output_ex_5.setText(Writer.float_to_string(ex5))
        

