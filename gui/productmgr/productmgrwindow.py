__author__ = 'Tom Yan'

from PyQt4.QtGui import QMainWindow, QTableWidget, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QDockWidget, QIcon
from PyQt4.QtCore import Qt
from descriptionwnd import DescriptionWidget
from producttable import ProductTable
from productnav import ProductNavigator

class ProductMgrWnd(QWidget):
    """
    Pro window
    """
    def __init__(self, parent=None):
        super(ProductMgrWnd, self).__init__(parent)
        self.main_wnd = QMainWindow(self)
        self.main_wnd.setWindowFlags(Qt.Widget)
        self.product_table = ProductTable(self)
        self.main_wnd.setCentralWidget(self.product_table)

        self.des_widget = DescriptionWidget(self)
        self.des_dock = QDockWidget(self.main_wnd)
        self.des_dock.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.main_wnd.addDockWidget(Qt.BottomDockWidgetArea, self.des_dock)
        self.des_dock.setWidget(self.des_widget)

        self.navigator = ProductNavigator(self)

        self.setup_ui()

    def setup_ui(self):
        """
        Setup ui
        :return:
        """
        layout = QHBoxLayout(self)
        layout.addWidget(self.navigator)
        layout.addWidget(self.main_wnd)

