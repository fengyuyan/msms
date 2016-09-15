"""
Search widget
"""
__author__ = 'Tom Yan'

from PyQt4 import QtGui, QtCore

class ButtonLineEdit(QtGui.QLineEdit):
    """
    one lien edit with one icon inside
    """
    buttonClicked = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        """
        constructor
        """
        super(ButtonLineEdit, self).__init__(parent)

        self.button = QtGui.QToolButton(self)
        self.button.setObjectName('tool_button')
        clear_icon = QtGui.QIcon(":/res/images/edit_clear.png")
        self.button.setIcon(clear_icon)
        # self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        self.button.clicked.connect(self.buttonClicked.emit)

        frame_width = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        line_edit_size = self.sizeHint()

        button_height = line_edit_size.height() - frame_width * 2
        self.button_size = QtCore.QSize(button_height, button_height)
        self.button.setFixedSize(self.button_size)

        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (self.button_size.width()))

    def resizeEvent(self, event):
        """
        reset the button place
        """
        self.button.move(self.rect().right() - self.button_size.width(),
                         (self.rect().bottom() - self.button_size.height() + 1) / 2)
        super(ButtonLineEdit, self).resizeEvent(event)


class SearchLineEdit(ButtonLineEdit):
    """
    one edit line widget with one clear button
    """

    sig_text_edited = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(SearchLineEdit, self).__init__(parent)
        self.button.hide()
        self.textChanged.connect(self.__slot_show_hide_button)
        self.button.clicked.connect(self.clear)
        self.button.clicked.connect(self.button.hide)
        self.textEdited.connect(self.sig_text_edited)

    def __slot_show_hide_button(self):
        """
        show button when text edit is not empty
        """
        if str(self.text()) == "":
            self.button.hide()
        else:
            self.button.show()

    def clear(self):
        """
        clear the line text
        """
        super(SearchLineEdit, self).clear()
        self.textEdited.emit("")
