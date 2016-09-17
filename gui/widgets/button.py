"""
Buttons
"""
__author__ = 'Tom Yan'

from PyQt4.QtGui import QToolButton, QIcon

class ToolButton(QToolButton):
    """
    Tool Button
    """
    def __init__(self, text, icon_src=None, checkable=False, style=None, parent=None):
        super(ToolButton, self).__init__(parent)
        self.setText(text)
        if icon_src:
            self.setIcon(QIcon(icon_src))
        if style:
            self.setToolButtonStyle(style)
        if checkable:
            self.setCheckable(True)
