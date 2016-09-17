__author__ = 'Tom Yan'

import sip
API_NAMES = ["QDate", "QDateTime", "QString",
             "QTextStream", "QTime", "QUrl",
             "QVariant"]
API_VERSION = 2
for name in API_NAMES:
    sip.setapi(name, API_VERSION)

import sys
from PyQt4 import QtGui
from gui.about import APP_NAME, APP_VERSION
from gui.workspace import g_workspace
from gui import res_rc



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('Tom')
    app.setApplicationName(APP_NAME + ' ' + APP_VERSION)

    from gui.mainwindow import MainWindow
    main_wnd = MainWindow()
    main_wnd.show()
    sys.exit(app.exec_())
