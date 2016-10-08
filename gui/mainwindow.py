__author__ = 'Tom Yan'

from PyQt4.QtGui import QMainWindow, QStackedWidget, QIcon, QToolBar, QLabel, QWidget, QHBoxLayout, QMovie
from PyQt4.QtCore import Qt, QSize
from productmgr.productmgrwindow import ProductMgrWnd
from gui.about import APP_NAME, APP_VERSION
from widgets.button import ToolButton
from gui.workspace import g_workspace


class Toolbar(QToolBar):
    """
    Toolbar
    """
    FUNC_PRODUCT_MGR = 'Product Management'
    FUNC_SALES_RECORDER = 'Sales Recorder'
    FUNC_STAT = 'Statistics'
    FUNC_UTILITY = 'Utilities'
    def __init__(self, parent=None):
        super(Toolbar, self).__init__(parent)
        self.function_btns = []
        self.product_mgr_btn = self.add_tool_button(Toolbar.FUNC_PRODUCT_MGR)
        self.product_mgr_btn.setChecked(True)
        self.sales_recorder_btn = self.add_tool_button(Toolbar.FUNC_SALES_RECORDER)
        self.stat_btn = self.add_tool_button(Toolbar.FUNC_STAT)
        self.utility_btn = self.add_tool_button(Toolbar.FUNC_UTILITY)
        self.icon_stack = QStackedWidget(self)

        self.birthday_label = QLabel('Every Day is Birthday!')
        font = self.birthday_label.font()
        font.setBold(True)
        self.birthday_label.setFont(font)
        self.birthday_gif = QLabel()
        gif_movie = QMovie(':res/cake.gif')
        gif_movie.start()
        gif_movie.setScaledSize(QSize(32, 32))
        self.birthday_gif.setMovie(gif_movie)

        toolbar_widget = QWidget(self)
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.addWidget(self.product_mgr_btn)
        toolbar_layout.addWidget(self.sales_recorder_btn)
        toolbar_layout.addWidget(self.stat_btn)
        toolbar_layout.addWidget(self.utility_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.birthday_label)
        toolbar_layout.addWidget(self.birthday_gif)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.icon_stack)
        self.addWidget(toolbar_widget)

    def add_tool_button(self, text, icon_src=None, checkable=True):
        """
        Add tool button
        """
        btn = ToolButton(text, icon_src, style=Qt.ToolButtonTextBesideIcon, checkable=checkable)
        btn.clicked.connect(self.on_function_btn_clicked)
        self.function_btns.append(btn)
        return btn

    def on_function_btn_clicked(self):
        """
        Slot: functional button clicked
        """
        btn = self.sender()
        if not btn.isChecked():
            return

        for func_btn in self.function_btns:
            if func_btn == btn:
                continue

            func_btn.setChecked(False)

        function_text = btn.text()
        g_workspace.main_wnd.switch_window(function_text)

    def switch_icon_bar(self, icon_bar):
        """
        Switch icon bar
        """
        if self.icon_stack.indexOf(icon_bar) < 0:
            self.icon_stack.addWidget(icon_bar)
        self.icon_stack.setCurrentWidget(icon_bar)

class MainWindow(QMainWindow):
    """
    Main window
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        g_workspace.main_wnd = self
        self.central_widget = QStackedWidget(self)
        self.setCentralWidget(self.central_widget)
        self.product_mgr_window = None
        self.toolbar = Toolbar(self)
        self.addToolBar(self.toolbar)
        self.switch_window(Toolbar.FUNC_PRODUCT_MGR)
        self.setWindowIcon(QIcon(':res/app.png'))
        self.setWindowTitle(APP_NAME + ' ' + APP_VERSION)
        self.setWindowState((self.windowState() & ~(Qt.WindowMinimized | Qt.WindowFullScreen)) |
                                Qt.WindowMaximized)

    def switch_window(self, func_text):
        """
        Switch window
        :param func_text:
        :return:
        """
        if func_text == Toolbar.FUNC_PRODUCT_MGR:
            if self.product_mgr_window is None:
                self.product_mgr_window = ProductMgrWnd(self)
                self.central_widget.addWidget(self.product_mgr_window)
            else:
                self.central_widget.setCurrentWidget(self.product_mgr_window)
            self.toolbar.switch_icon_bar(self.product_mgr_window.icon_bar)


