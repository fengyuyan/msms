__author__ = 'Tom Yan'

APP_NAME = 'Merchandise Sales Management System'
APP_VERSION = '2016.1'
APP_DIR_NAME = '.msms'
APP_WSP_FILENAME = 'msms.wsp'

import os

def get_home_dir():
    try:
        path1 = os.path.expanduser('~')
    except:
        path1 = ''
    try:
        path2 = os.environ["HOME"]
    except:
        path2 = ''

    if os.path.exists(path1) and os.access(path1, os.W_OK):
        return path1
    elif os.path.exists(path2) and os.access(path2, os.W_OK):
        return path2
    else:
        return None

def get_msms_user_dir():
    """
    get or create the nde directory in home dir
    """
    home_dir = get_home_dir()
    if home_dir:
        msms_dir = os.path.join(home_dir, APP_DIR_NAME)

        if not os.path.exists(msms_dir):
            msms_dir = os.path.join(home_dir, APP_DIR_NAME)
            os.makedirs(msms_dir)
    else:
        cwd = os.getcwd()
        if os.access(cwd, os.W_OK):
            msms_dir = cwd
        else:
            msms_dir = None

    return msms_dir

def get_msms_wsp_file():
    """
    Get msms workspace file
    :return:
    """
    wsp_file = os.path.join(get_msms_user_dir(), APP_WSP_FILENAME)
    if os.path.exists(wsp_file):
        return wsp_file
    else:
        return None