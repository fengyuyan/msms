__author__ = 'Tom Yan'

from PyQt4.QtGui import QMainWindow, QStackedWidget, QWidget, QIcon, QHBoxLayout, QDockWidget, QToolBar
from PyQt4.QtCore import Qt
from descriptionwnd import DescriptionWidget
from producttable import ProductTable
from productnav import ProductNavigator
from gui.widgets.search import SearchLineEdit

class ProductMgrWnd(QWidget):
    """
    Product management window
    """
    def __init__(self, parent=None):
        super(ProductMgrWnd, self).__init__(parent)
        self.main_wnd = QMainWindow(self)
        self.main_wnd.setWindowFlags(Qt.Widget)
        self.central_stack = QStackedWidget(self)
        self.main_wnd.setCentralWidget(self.central_stack)

        self.icon_bar = self.setup_icon_bar()

        self.des_stack = QStackedWidget(self)
        self.des_dock = QDockWidget(self.main_wnd)
        self.des_dock.setWindowTitle("  Product Description Window")
        self.des_dock.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.main_wnd.addDockWidget(Qt.BottomDockWidgetArea, self.des_dock)
        self.des_dock.setWidget(self.des_stack)

        self.navigator = ProductNavigator(self)
        self.navigator.item_clicked.connect(self.on_item_clicked)

        self.setup_ui()

        self.on_item_clicked(self.navigator.get_current_item())

    def setup_icon_bar(self):
        """
        Setup icon bar
        :return:
        """
        icon_bar = QToolBar(self)
        icon_bar.addAction(QIcon(':res/add.png'), 'Add')
        icon_bar.addAction(QIcon(':res/delete.png'), 'Delete')
        self.search_edit = SearchLineEdit(self)
        # self.search_edit.setFixedHeight(30)
        icon_bar.addWidget(self.search_edit)
        return icon_bar

    def setup_ui(self):
        """
        Setup ui
        :return:
        """
        layout = QHBoxLayout(self)
        layout.addWidget(self.navigator)
        layout.addWidget(self.main_wnd)

    def on_item_clicked(self, item):
        """
        Slot: product category clicked
        :param item:
        :return:
        """
        if not item:
            return

        table_widget = item.get_property(ProductNavigator.TABLE_WIDGET)
        des_widget = item.get_property(ProductNavigator.DES_WIDGET)
        if not table_widget:
            des_widget = DescriptionWidget(parent=self)
            item.set_property(ProductNavigator.DES_WIDGET, des_widget)
            table_widget = ProductTable(item.get_property(ProductNavigator.PATH), des_widget, self)
            item.set_property(ProductNavigator.TABLE_WIDGET, table_widget)
            self.central_stack.addWidget(table_widget)
            self.des_stack.addWidget(des_widget)
        self.central_stack.setCurrentWidget(table_widget)
        self.des_stack.setCurrentWidget(des_widget)


