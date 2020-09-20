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
        def QT_TRANSLATE_NOOP(context, text):
            return text
            
        import os
        import FreeCAD as App
        import FreeCADGui as Gui
        import MBDyn_locator
        MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
        MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')
        MBDwb_setting_ui_path = os.path.join(MBDwbPath, 'resources','wb_settings_widgets')
        import MBDyn_guitools.MBDynFreeCAD
        import MBDyn_guitools.body_AS4_cmd
        import MBDyn_guitools.ref_cmd
        import MBDyn_guitools.struct_node_cmd
        import MBDyn_guitools.revpin_joint_AS4_2_cmd
        import MBDyn_guitools.hinge_joint_AS4_cmd
        import MBDyn_guitools.postproc_AS4_cmd
        import MBDyn_guitools.total_joint_cmd
        import MBDyn_guitools.total_pinjoint_cmd
        import MBDyn_guitools.ramp_drive_cmd
        import MBDyn_guitools.axial_rot_joint_AS4_cmd
        import MBDyn_commands.sim_cmd
        import MBDyn_commands.layout_cmd
        import MBDyn_commands.analyze_cmd
        import MBDyn_commands.gravity_cmd
        
  
        from MBDyn_settings.wdgt_solver_settings import wdgt_solver_settings
  
        self.list = ["CommandTreeLayout","CommandAddSimulation", "mbdyn_launchGui", "CommandAddGravity","body_sel_cmd", "ref_cmd", "struct_node_cmd", "revpin_joint_cmd",
                    "hinge_joint_cmd", "total_joint_cmd", "total_pinjoint_cmd",
                    "axial_rot_joint_cmd", "ramp_drive_cmd", "postproc_cmd"]

        self.appendToolbar("Mbdyn comands", self.list)     
        self.appendMenu("&MBDyn", self.list)

        import MBDyn_commands.postprocessing_cmd # Call in last to have the post processing tool bar after the others
        Log("Loading MyModule... done\n")
        # Add preferences page on the main window toolbar: Edit/ preferences.../mbdyn
        general_setting_ui = os.path.join(MBDwb_setting_ui_path, 'ui_general_settings.ui')
        Gui.addPreferencePage(general_setting_ui, "MBDyn")
        Gui.addPreferencePage(wdgt_solver_settings, "MBDyn")
        img_path = os.path.join(MBDwb_icons_path, 'preferences-MBDyn.svg')
        # The commande Gui.addIcon gives me the following warning (on freecad 0.19):
        # <string>:86: DeprecationWarning: PY_SSIZE_T_CLEAN will be required for '#' formats
        Gui.addIcon("preferences-mbdyn", img_path)

    def Activated(self):
        App.Console.PrintMessage("MBDyn Workbench Activated")
        if hasattr(Gui,"mbdynAnimationToolBar"):
            Gui.mbdynAnimationToolBar.Activated()

    def Deactivated(self):
        Msg("MyWorkbench.Deactivated()\n")
        if hasattr(Gui,"mbdynAnimationToolBar"):
            Gui.mbdynAnimationToolBar.Deactivated()

Gui.addWorkbench(MbdynGui)
