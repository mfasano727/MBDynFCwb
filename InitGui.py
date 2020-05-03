import os
import sys
import FreeCAD as App
import FreeCADGui as Gui

import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')
class MbdynGui(Workbench):
    
    def __init__(self):
        self.__class__.Icon = """
            /* XPM */
            static char *_857_5567c986d2e71b01ca23671d10617805d3f636aef74fac3a0f42400b43825347[] = {
            /* columns rows colors chars-per-pixel */
            "16 16 6 1 ",
            "  c red",
            ". c #808000",
            "X c yellow",
            "o c #808080",
            "O c #C0C0C0",
            "+ c white",
            /* pixels */
            "++++++++++++++++",
            "++++++++++++++++",
            "++++++++++++++++",
            "++++++++++++++++",
            "++++++++++++++++",
            "++++++++++++++++",
            "+++++XXOO+++XXOO",
            "++++OXX  ++OXX  ",
            "oo++ .+O ++ .+++",
            "O O  +++XO  ++++",
            "+O  ++++O  +++++",
            "++++++++++++++++",
            "++++++++++++++++",
            "++++++++++++++++",
            "++++++++++++++++",
            "++++++++++++++++"
            };
            """
        self.__class__.MenuText = "MBDyn"
        self.__class__.ToolTip = "Model for Mbdyn simulation"

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        import MBDyn_guitools.m_values
        import MBDyn_guitools.MBDynFreeCAD
        import MBDyn_guitools.body_AS4_cmd
        import MBDyn_guitools.ref_cmd
        import MBDyn_guitools.struct_node_cmd
        import MBDyn_guitools.revpin_joint_AS4_2_cmd
        import MBDyn_guitools.hinge_joint_AS4_cmd
        import MBDyn_guitools.postproc_AS4_cmd
        self.list = ["mbdyn_configure", "mbdyn_launchGui", "body_sel_cmd",
                     "ref_cmd", "struct_node_cmd", "revpin_joint_cmd","hinge_joint_cmd", "postproc_cmd"]
        self.appendToolbar("Mbdyn_comands", self.list)
        self.appendMenu("Mbdyn_menu", self.list)

        Log("Loading MyModule... done\n")

    def Activated(self):
#        import MBDyn_objects.model_so
#        self.model = model_so.MBDynModel
#        iv = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","MBDynInitialValue")
#        model_so.MBDynInitialValue(iv)        
#        self.nodes = model_so.MBDynNodes()
#        self.elements = model_so.MBDynElements()
        
        App.Console.PrintMessage("test")
        

    def Deactivated(self):
        Msg("MyWorkbench.Deactivated()\n")

Gui.addWorkbench(MbdynGui)
