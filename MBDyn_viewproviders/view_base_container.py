import FreeCAD as App

from six import string_types
import os

import MBDyn_locator
MBDwbPath = os.path.dirname(MBDyn_locator.__file__)
MBDwb_icons_path = os.path.join(MBDwbPath, 'icons')


class ViewProviderBaseContainer:
    """Proxy View Provider for FEM DocumentObjectGroupPython Base."""

    def __init__(self, vobj):
        vobj.Proxy = self

    # needs to be overwritten, if no standard icon name is used
    # see constraint body heat source as an example
    def getIcon(self):
        # https://forum.freecadweb.org/viewtopic.php?f=18&t=44009
        if not hasattr(self.Object, "Proxy"):
            App.Console.PrintMessage("{}, has no Proxy.\n".format(self.Object.Name))
            return ""
        if not hasattr(self.Object.Proxy, "Type"):
            App.Console.PrintMessage(
                "{}: Proxy does has not have attribte Type.\n"
                .format(self.Object.Name)
            )
            return ""
        if (
            isinstance(self.Object.Proxy.Type, string_types)
            and self.Object.Proxy.Type.startswith("MBDyn::")
        ):
            icon_path = "{}/{}.svg".format(MBDwb_icons_path, self.Object.Proxy.Type.replace("MBDyn::", "MBDyn_"))
            App.Console.PrintLog("{} --> {}\n".format(self.Object.Name, icon_path))
            return icon_path
        else:
            App.Console.PrintError("No icon returned for {}\n".format(self.Object.Name))
            App.Console.PrintMessage("{}\n".format(self.Object.Proxy.Type))
            return ""

    def attach(self, vobj):
        '''Setup the scene sub-graph of the view provider, this method is mandatory'''
        self.Object = vobj.Object
        self.ViewObject = vobj

    def doubleClicked(self, vobj):
        # Do nothing to avoid renaming of the container
        return True

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Flat Lines"

    # they are needed, see:
    # https://forum.freecadweb.org/viewtopic.php?f=18&t=44021
    # https://forum.freecadweb.org/viewtopic.php?f=18&t=44009
    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None

    def canDragObjects(self):
        return False

    def canDragObject(self):
        return False

    def canDopObjects(self):
        return False

    def canDopObject(self):
        return False