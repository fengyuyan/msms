"""
Application workspace
"""
__author__ = 'Tom Yan'

from utilities.io import json_load, json_export
from gui.about import get_msms_user_dir, get_msms_wsp_file
import sys, os

def get_bin_dir():
    """
    Return the script directory - whether we're frozen or not.
    """
    import imp

    # new py2exe or tools/freeze, can't use __file__ or sys.argv[0]
    if hasattr(sys, "frozen") or imp.is_frozen("__main__"):
        return os.path.abspath(os.path.dirname(sys.executable)), False
    return os.path.abspath(os.path.dirname(sys.argv[0])), True

class WorkSpace(object):
    """
    Workspace object
    """
    def __init__(self):
        self.bin_dir, self.debug_mode = get_bin_dir()
        self.home_dir = get_msms_user_dir()
        self.wsp_file = get_msms_wsp_file()
        self.main_wnd = None
        self.wsp_info = None
        if self.wsp_file:
            self.wsp_info = json_load(self.wsp_file)

g_workspace = WorkSpace()
