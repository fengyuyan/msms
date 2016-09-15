"""
Navigator implementation
"""
__author__ = 'Tom Yan'

from PyQt4 import QtCore, QtGui

class NavigatorItem(QtGui.QWidget):
    """
    Navigator Item
    """
    def __init__(self, text, icon_size=None, icon_pic=None, parent=None):
        super(NavigatorItem, self).__init__(parent)
        self.text_label = QtGui.QLabel(text)
        font = self.text_label.font()
        font.setBold(True)
        self.text_label.setFont(font)

        if icon_size:
            self.icon_size = icon_size
        else:
            self.icon_size = [32, 32]

        self.pixmap = None
        self.icon_label = QtGui.QLabel()
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
        self.setFixedSize(64, 50)

class Navigator(QtGui.QWidget):
    """
    Navigator
    """
    def __init__(self, parent=None):
        super(Navigator, self).__init__(parent)
        self.items = []
        self._layout = QtGui.QVBoxLayout(self)
        self._layout.setAlignment(QtCore.Qt.AlignTop)

    def add_item(self, text, icon_size=None, icon_pic=None):
        """
        Add item
        :param text:
        :param icon_size:
        :param icon_pic:
        :return:
        """
        item = NavigatorItem(text, icon_size, icon_pic)
        self._layout.addWidget(item)
        return item
