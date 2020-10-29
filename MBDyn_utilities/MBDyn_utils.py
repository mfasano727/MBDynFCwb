import os
from PySide2.QtWidgets import QFileDialog

def get_active_simulation(doc=None):
    """Get the active simulation from the document doc."""
    if doc is not None:
        if hasattr(doc, "MBDyn_Workbench"):
            active_sim = getattr(doc, "MBDyn_Workbench").Proxy.activeSimulation
            return active_sim
    return None

def get_active_result(doc=None):
    """Get the active result from the document doc."""
    if doc is not None:
        if hasattr(doc, "MBDyn_Workbench"):
            active_sim = getattr(doc, "MBDyn_Workbench").Proxy.activeResult
            return active_sim
    return None

def select_directory():
    selected_dir = QFileDialog.getExistingDirectory()
    if os.sep == '\\':
        selected_dir = selected_dir.replace('/', '\\')
    return selected_dir