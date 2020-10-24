Other widgets can be added here for the workbench settings
To appear on the wb_gui, the constant SETTING_WIDGETS (in wb_settings_cmd.py) need do be modified
    add a tuple (str::setting_name, class)
All new widget need to have the methods:
 loadSettings
 saveSettings

loadSettings is call each time the preference gui is opened
saveSettings is call when the ok/apply button is clicked

all widget should be independants
user parameter should be only change in the saveSettings method.


Setting tab can be added directly using ui file and predefine widget, GUI:Pref...

to do if necessary:
    - Simulation settings
    - PostProc settings
