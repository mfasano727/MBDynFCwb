import FreeCAD as App
import FreeCADGui as Gui
import os, sys, math
import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')

try:
    from PySide import QtCore, QtGui, QtSvg
except ImportError:
    App.Console.PrintMessage("Error: Python-pyside package must be installed on your system to use the Draft module.")

try:
    if sys.version_info.major >= 3:
        _encoding = None
    else:
        _encoding = QtGui.QApplication.UnicodeUTF8
    def translate(context, text, utf8_decode=True):
        """convenience function for Qt translator
            context: str
                context is typically a class name (e.g., "MyDialog")
            text: str
                text which gets translated
            utf8_decode: bool [False]
                if set to true utf8 encoded unicode will be returned. This option does not have influence
                on python3 as for python3 we are returning utf-8 encoded unicode by default!
        """
        if sys.version_info.major >= 3:
            return QtGui.QApplication.translate(context, text, None)
        elif utf8_decode:
            return QtGui.QApplication.translate(context, text, None, _encoding)
        else:
            return QtGui.QApplication.translate(context, text, None, _encoding).encode("utf8")

except AttributeError:
    def translate(context, text, utf8_decode=False):
        """convenience function for Qt translator
            context: str
                context is typically a class name (e.g., "MyDialog")
            text: str
                text which gets translated
            utf8_decode: bool [False]
                if set to true utf8 encoded unicode will be returned. This option does not have influence
                on python3 as for python3 we are returning utf-8 encoded unicode by default!
        """
        if sys.version_info.major >= 3:
            return QtGui.QApplication.translate(context, text, None)
        elif QtCore.qVersion() > "4":
            if utf8_decode:
                return QtGui.QApplication.translate(context, text, None)
            else:
                return QtGui.QApplication.translate(context, text, None).encode("utf8")
        else:
            if utf8_decode:
                return QtGui.QApplication.translate(context, text, None, _encoding)
            else:
                return QtGui.QApplication.translate(context, text, None, _encoding).encode("utf8")

def utf8_decode(text):
    """py2: str     -> unicode
            unicode -> unicode
       py3: str     -> str
            bytes   -> str
    """
    try:
        return text.decode("utf-8")
    except AttributeError:
        return text


# in-command shortcut definitions: Shortcut / Translation / related UI control
inCommandShortcuts = {
    "Relative":   ["R",translate("draft","Relative"),             "isRelative"],
    "Continue":   ["T",translate("draft","Continue"),             "continueCmd"],
    "Close":      ["O",translate("draft","Close"),                "closeButton"],
    "Copy":       ["P",translate("draft","Copy"),                 "isCopy"],
    "Fill":       ["L",translate("draft","Fill"),                 "hasFill"],
    "Exit":       ["A",translate("draft","Exit"),                 "finishButton"],
    "Snap":       ["S",translate("draft","Snap On/Off"),          None],
    "Increase":   ["[",translate("draft","Increase snap radius"), None],
    "Decrease":   ["]",translate("draft","Decrease snap radius"), None],
    "RestrictX":  ["X",translate("draft","Restrict X"),           None],
    "RestrictY":  ["Y",translate("draft","Restrict Y"),           None],
    "RestrictZ":  ["Z",translate("draft","Restrict Z"),           None],
    "SelectEdge": ["E",translate("draft","Select edge"),          "selectButton"],
    "AddHold":    ["Q",translate("draft","Add custom snap point"),None],
    "Length":     ["H",translate("draft","Length mode"),          "lengthValue"],
    "Wipe":       ["W",translate("draft","Wipe"),                 "wipeButton"],
    "SetWP":      ["U",translate("draft","Set Working Plane"), "orientWPButton"],
    "CycleSnap":  ["`",translate("draft","Cycle snap object"), None]
}



#---------------------------------------------------------------------------
# Customized widgets
#---------------------------------------------------------------------------

class MbdynBaseWidget(QtGui.QWidget):
    def __init__(self,parent = None):
        QtGui.QWidget.__init__(self,parent)
    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.KeyPress and event.text().upper()==inCommandShortcuts["CycleSnap"][0]:
            if hasattr(Gui,"Snapper"):
                Gui.Snapper.cycleSnapObject()
            return True
        return QtGui.QWidget.eventFilter(self, widget, event)
                        
class DraftLineEdit(QtGui.QLineEdit):
    "custom QLineEdit widget that has the power to catch Escape keypress"
    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.emit(QtCore.SIGNAL("escaped()"))
        elif event.key() == QtCore.Qt.Key_Up:
            self.emit(QtCore.SIGNAL("up()"))
        elif event.key() == QtCore.Qt.Key_Down:
            self.emit(QtCore.SIGNAL("down()"))
        else:
            QtGui.QLineEdit.keyPressEvent(self, event)

class MbdynPlayButton(QtGui.QToolButton):
    " custom QToolbutton widget that change icon depending on this check state"
    def __init__(self, parent=None):
        super(MbdynPlayButton,self).__init__(parent)
        self.setObjectName("PlayButton")
        self._pauseIcon = os.path.join(MBDwb_icons_path,"MBDyn_postPause.svg")
        self._playIcon = os.path.join(MBDwb_icons_path,"MBDyn_postPlay.svg")

        self.setIcons()

        self.setCheckable(True)
        self.setChecked(False)

    def setIcons(self):
        ico = QtGui.QIcon()
        ico.addPixmap(QtGui.QPixmap(self._pauseIcon),QtGui.QIcon.Normal,QtGui.QIcon.On);
        ico.addPixmap(QtGui.QPixmap(self._playIcon),QtGui.QIcon.Normal,QtGui.QIcon.Off);
        
        p = App.ParamGet("User parameter:BaseApp/Preferences/General")
        bsize = p.GetInt("ToolbarIconSize",24)
        isize = p.GetInt("ToolbarIconSize",24)
        
        self.setIcon(ico)
        self.setIconSize(QtCore.QSize(isize, isize))
    
    def IsActive(self):
        return False


class MbdynAnimationToolBar:
    "main draft Toolbar"
    def __init__(self):
       
        self.baseWidget = MbdynBaseWidget()
        self.tray = QtGui.QToolBar(None)
        self.tray.setObjectName("Mbdyn Animation tray")
        self.tray.setWindowTitle("Mbdyn Animation tray")
        self.toptray = self.tray
        self.setupTray()
        mw = Gui.getMainWindow()
        mw.addToolBar(self.tray)
        self.tray.setParent(mw)
        self.tray.hide()

        self.retranslateUi(self.baseWidget)

    def _toolbutton (self,name, layout, hide=True, icon=None, checkable=False):
        p = App.ParamGet("User parameter:BaseApp/Preferences/General")
        bsize = p.GetInt("ToolbarIconSize",24)
        isize = p.GetInt("ToolbarIconSize",24)
        button = QtGui.QToolButton(self.baseWidget)
        button.setObjectName(name)

        if hide:
            button.hide()
        if icon:
            if icon.endswith(".svg"):
                button.setIcon(QtGui.QIcon(icon))
            else:
                button.setIcon(QtGui.QIcon.fromTheme(icon, QtGui.QIcon(':/icons/'+icon+'.svg')))
            button.setIconSize(QtCore.QSize(isize, isize))
        if checkable:
            button.setCheckable(True)
            button.setChecked(False)
        layout.addWidget(button)
        return button

    def _playbutton (self, layout):
        button = MbdynPlayButton(self.baseWidget)
        layout.addWidget(button)
        return button

    def _lineedit (self,name, layout, width=None):
        p = App.ParamGet("User parameter:BaseApp/Preferences/General")
        bsize = p.GetInt("ToolbarIconSize",24)
        lineedit = DraftLineEdit(self.baseWidget)
        lineedit.setObjectName(name)
        #if not width: width = 800
        if not width: width = 75
        lineedit.setMaximumSize(QtCore.QSize(width,bsize))
        layout.addWidget(lineedit)
        return lineedit

    def _combo (self,name,layout):
        p = App.ParamGet("User parameter:BaseApp/Preferences/General")
        bsize = p.GetInt("ToolbarIconSize",24)
        cb = QtGui.QComboBox(self.baseWidget)
        cb.setObjectName(name)

        cb.setMaximumHeight(bsize)
        layout.addWidget(cb)
        return cb

    def setupTray(self,task=False):
        """sets draft tray buttons up"""

        iconPath = os.path.join(MBDwb_icons_path,"MBDyn_postPrev.svg")
        self.prevButton = self._toolbutton("prev", self.toptray, icon=iconPath,hide=False)
        
        self.playButton = self._playbutton(self.toptray)

        iconPath = os.path.join(MBDwb_icons_path,"MBDyn_postNext.svg")
        self.nextButton = self._toolbutton("next", self.toptray, icon=iconPath,hide=False)

        iconPath = os.path.join(MBDwb_icons_path,"MBDyn_postStop.svg")
        self.stopButton = self._toolbutton("stop", self.toptray, icon=iconPath,hide=False)
        
        self.animType = self._combo("animType",self.toptray)
        self.animType.addItems(["nb frame/anim step"])
        
        t = self._lineedit("Input", self.toptray, width=75)

        self.advOptButton = self._toolbutton("applyButton", self.toptray, hide=False, icon='Draft_Apply')

        QtCore.QObject.connect(self.playButton,QtCore.SIGNAL("toggled(bool)"),self.btnPlayPressed)
        QtCore.QObject.connect(self.stopButton,QtCore.SIGNAL("pressed()"),self.btnStopPressed)
        QtCore.QObject.connect(self.prevButton,QtCore.SIGNAL("pressed()"),self.btnPrevPressed)
        QtCore.QObject.connect(self.nextButton,QtCore.SIGNAL("pressed()"),self.btnNextPressed)
        QtCore.QObject.connect(self.advOptButton,QtCore.SIGNAL("pressed()"),self.btnAdvOptPressed)
        
        #QtCore.QObject.connect(self.colorButton,QtCore.SIGNAL("pressed()"),self.getcol)
        #QtCore.QObject.connect(self.facecolorButton,QtCore.SIGNAL("pressed()"),self.getfacecol)
        #QtCore.QObject.connect(self.widthButton,QtCore.SIGNAL("valueChanged(int)"),self.setwidth)
        #QtCore.QObject.connect(self.fontsizeButton,QtCore.SIGNAL("valueChanged(double)"),self.setfontsize)
        #QtCore.QObject.connect(self.applyButton,QtCore.SIGNAL("pressed()"),self.apply)
        #QtCore.QObject.connect(self.constrButton,QtCore.SIGNAL("toggled(bool)"),self.toggleConstrMode)
        #QtCore.QObject.connect(self.autoGroupButton,QtCore.SIGNAL("pressed()"),self.runAutoGroup)
        #
        #QtCore.QTimer.singleShot(2000,self.retranslateTray) # delay so translations get a chance to load

#---------------------------------------------------------------------------
# language tools
#---------------------------------------------------------------------------
				
    def retranslateUi(self, widget=None):
        #self.promptlabel.setText(translate("draft", "active command:"))
        #self.cmdlabel.setText(translate("draft", "None"))
        #self.cmdlabel.setToolTip(translate("draft", "Active Draft command"))
        pass

#---------------------------------------------------------------------------
# Processing functions
#---------------------------------------------------------------------------        
    def btnStopPressed(self):
        """Stop Animation"""
        print("Stop Method: ", self.playButton.isChecked())
        if self.playButton.isChecked:
            self.playButton.toggle() # change the state of the plat button
        # return to the first step.

    def btnPlayPressed(self,isChecked):
        """Play/Pause Animation"""
        print("Play/Pause Method: ", self.playButton.isChecked())
        pass

    def btnNextPressed(self):
        """Show Animation Step"""
        pass
    def btnPrevPressed(self):
        """Show Animation Step"""
        pass
    def btnAdvOptPressed(self):
        """Show advance postprocessing option"""
        pass

    def validateSNumeric(self):
        ''' send valid numeric parameters to ShapeString '''
        if self.sourceCmd: 
            if (self.labelSSize.isVisible()):
                try:
                    SSize=float(self.SSize)
                except ValueError:
                    App.Console.PrintMessage(translate("draft", "Invalid Size value. Using 200.0."))                     
                    self.sourceCmd.numericSSize(200.0)
                else:
                    self.sourceCmd.numericSSize(SSize)
            elif (self.labelSTrack.isVisible()):
                try:
                    track=int(self.STrack)
                except ValueError:
                    App.Console.PrintMessage(translate("draft", "Invalid Tracking value. Using 0."))                     
                    self.sourceCmd.numericSTrack(0)
                else:
                    self.sourceCmd.numericSTrack(track)

    def finish(self):
        "finish button action"
        if self.sourceCmd:
            self.sourceCmd.finish(False)
        if self.cancel:
            self.cancel()
            self.cancel = None
        if Gui.ActiveDocument:
            Gui.ActiveDocument.resetEdit()

    def escape(self):
        "escapes the current command"
        self.continueMode = False
        if not self.taskmode:
            self.continueCmd.setChecked(False)
        self.finish()

                    
    def updateSnapper(self):
        "updates the snapper track line if applicable"
        if hasattr(Gui,"Snapper"):
            if Gui.Snapper.trackLine:
                if Gui.Snapper.trackLine.Visible:
                    last = App.Vector(0,0,0)
                    if not self.xValue.isVisible():
                        return
                    if self.isRelative.isChecked():
                        if self.sourceCmd:
                            if hasattr(self.sourceCmd,"node"):
                                if self.sourceCmd.node:
                                    last = self.sourceCmd.node[-1]
                    delta = App.DraftWorkingPlane.getGlobalCoords(App.Vector(self.x,self.y,self.z))
                    Gui.Snapper.trackLine.p2(last.add(delta))

    def storeCurrentText(self,qstr):
        self.currEditText = self.textValue.text()

    def setCurrentText(self,tstr):
        if (not self.taskmode) or (self.taskmode and self.isTaskOn):
            self.textValue.setText(tstr)

    def sendText(self):
        '''
        this function sends the entered text to the active draft command
        if enter has been pressed twice. Otherwise it blanks the line.
        '''
        if self.textline == len(self.textbuffer):
            if self.textline:
                if not self.currEditText:
                    self.sourceCmd.text=self.textbuffer
                    self.sourceCmd.createObject()
            self.textbuffer.append(self.currEditText)
            self.textline += 1
            self.setCurrentText('')
        elif self.textline < len(self.textbuffer):
            self.textbuffer[self.textline] = self.currEditText
            self.textline += 1
            if self.textline < len(self.textbuffer):
                self.setCurrentText(self.textbuffer[self.textline])
            else:
                self.setCurrentText('')

    def show(self):
        if not self.taskmode:
            self.mbdynWidget.setVisible(True)

    def hide(self):
        if not self.taskmode:
            self.mbdynWidget.setVisible(False)

#---------------------------------------------------------------------------
# TaskView operations
#---------------------------------------------------------------------------

    def setWatchers(self):
        class DraftCreateWatcher:
            def __init__(self):
                self.commands = ["Draft_Line","Draft_Wire",
                                 "Draft_Rectangle","Draft_Arc",
                                 "Draft_Circle","Draft_BSpline",
                                 "Draft_Text","Draft_Dimension",
                                 "Draft_ShapeString","Draft_BezCurve"]
                self.title = "Create objects"
            def shouldShow(self):
                return (App.ActiveDocument != None) and (not Gui.Selection.getSelection())

        class DraftModifyWatcher:
            def __init__(self):
                self.commands = ["Draft_Move","Draft_Rotate",
                                 "Draft_Scale","Draft_Offset",
                                 "Draft_Trimex","Draft_Upgrade",
                                 "Draft_Downgrade","Draft_Edit",
                                 "Draft_Drawing"]
                self.title = "Modify objects"
            def shouldShow(self):
                return (App.ActiveDocument != None) and (Gui.Selection.getSelection() != [])

        Gui.Control.addTaskWatcher([DraftCreateWatcher(),DraftModifyWatcher()])

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.LanguageChange:
            #print("Language changed!")
            self.ui.retranslateUi(self)

    def Activated(self):
        if hasattr(self,"tray"):
            self.tray.show()

    def Deactivated(self):
        if hasattr(self,"tray"):
            self.tray.hide()

    def IsActive(self):
        if App.ActiveDocument == None:
            self.tray.setEnabled(False)
        else:
            self.tray.setEnabled(True)

#Add the toolbar on the global variable of the Gui
if not hasattr(Gui,"mbdynAnimationToolBar"):
    Gui.mbdynAnimationToolBar = MbdynAnimationToolBar()
