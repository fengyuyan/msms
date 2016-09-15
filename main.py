__author__ = 'Fengyu Yan'

import sys
import sip
from PyQt4 import QtGui
from gui.mainwindow import MainWindow
from gui.about import APP_NAME, APP_VERSION
from gui import res_rc
# API_NAMES = ["QDate", "QDateTime", "QString",
#              "QTextStream", "QTime", "QUrl",
#              "QVariant"]
# API_VERSION = 2
# for name in API_NAMES:
#     sip.setapi(name, API_VERSION)

import time
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('Tom')
    app.setApplicationName(APP_NAME + ' ' + APP_VERSION)

    main_wnd = MainWindow()
    main_wnd.show()
    sys.exit(app.exec_())
