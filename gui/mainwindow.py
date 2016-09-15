__author__ = 'Tom Yan'

from PyQt4.QtGui import QMainWindow, QStackedWidget, QIcon
from productmgr.productmgrwindow import ProductMgrWnd
from gui.about import APP_NAME, APP_VERSION

class MainWindow(QMainWindow):
    """
    Main window
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QStackedWidget(self)
        self.setCentralWidget(self.central_widget)
        self.product_mgr_window = ProductMgrWnd(self)
        self.central_widget.addWidget(self.product_mgr_window)
        self.setWindowIcon(QIcon(':res/images/app.png'))
        self.setWindowTitle(APP_NAME + ' ' + APP_VERSION)

