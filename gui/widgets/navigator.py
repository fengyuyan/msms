"""
Navigator implementation
"""
__author__ = 'Tom Yan'

from PyQt4 import QtCore, QtGui
from functools import partial

class NavigatorItem(QtGui.QFrame):
    """
    Navigator Item
    """
    clicked = QtCore.pyqtSignal()
    def __init__(self, text, icon_size=None, icon_pic=None, parent=None):
        super(NavigatorItem, self).__init__(parent)
        self.properties = {}
        self.text_label = QtGui.QLabel(text)
        font = self.text_label.font()
        font.setBold(True)
        self.text_label.setFont(font)

        if icon_size:
            self.icon_size = icon_size
        else:
            self.icon_size = [32, 32]

        self.pixmap = None
        self.icon_label = QtGui.QLabel(self)
        if icon_pic:
            self.pixmap = QtGui.QPixmap(icon_pic)
            self.pixmap = self.pixmap.scaled(QtCore.QSize(self.icon_size[0], self.icon_size[1]))
            self.icon_label.setPixmap(self.pixmap)
            self.icon_label.setVisible(True)
        else:
            self.icon_label.setVisible(False)

        layout = QtGui.QVBoxLayout(self)
        icon_layout = QtGui.QHBoxLayout()
        icon_layout.setAlignment(QtCore.Qt.AlignCenter)
        icon_layout.addWidget(self.icon_label)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(icon_layout)
        layout.addWidget(self.text_label)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        if icon_pic:
            self.setFixedSize(64, 64)
        else:
            self.setFixedSize(64, 32)

        self.setStyleSheet("background-color: transparent; border: 1px solid transparent; border-radius: 5px;")

    def set_property(self, property_type, property_val):
        """
        Set property
        """
        self.properties[property_type] = property_val

    def get_property(self, property_type):
        """
        Get property
        """
        return self.properties.get(property_type)

    def set_background_color(self, color_str):
        """
        Set item background color
        """
        self.cur_background_color = color_str
        style_sheet = self.styleSheet() + "background: " + color_str + ";"
        self.setStyleSheet(style_sheet)

    def mousePressEvent(self, event): #pylint: disable=C0103
        """
        Override mouse press event
        """
        super(NavigatorItem, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()

class Navigator(QtGui.QWidget):
    """
    Navigator
    """
    item_clicked = QtCore.pyqtSignal(object)
    HIGHLIGHT_COLOR = "#2B60DE"
    NORMAL_COLOR = "transparent"

    def __init__(self, parent=None):
        super(Navigator, self).__init__(parent)
        self.cur_item = None
        self.items = []
        self._layout = QtGui.QVBoxLayout(self)
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(20)

    def add_item(self, text, icon_pic=None, icon_size=None, ):
        """
        Add item
        :param text:
        :param icon_size:
        :param icon_pic:
        :return:
        """
        item = NavigatorItem(text, icon_size, icon_pic, self)
        item.clicked.connect(partial(self.on_item_clicked, item))
        self._layout.addWidget(item)
        self.items.append(item)
        return item

    def on_item_clicked(self, item):
        """
        Slot: item clicked
        :param item:
        :return:
        """
        self.set_current_item(item)

        # emit signal to client
        self.item_clicked.emit(item)

    def get_current_item(self):
        """
        Get current item
        :return:
        """
        return self.cur_item

    def set_current_item(self, item):
        """
        set current item
        :return:
        """
        if self.cur_item == item:
            return

        # change background
        for nav_item in self.items:
            if nav_item == item:
                nav_item.set_background_color(self.HIGHLIGHT_COLOR)
                nav_item.highlighted = True
            else:
                nav_item.set_background_color(self.NORMAL_COLOR)
                nav_item.highlighted = False

        self.cur_item = item
