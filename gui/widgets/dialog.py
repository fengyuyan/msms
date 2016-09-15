__author__ = 'Tom Yan'

from PyQt4 import QtGui, QtCore
class Dialog(QtGui.QDialog):
    """
    Dialog with minimum, maximum and close button
    """
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowMaximizeButtonHint
                            | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)