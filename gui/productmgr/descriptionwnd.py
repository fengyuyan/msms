"""
Description window, it has two parts: description chart and description notes
"""
__author__ = 'Tom Yan'

from PyQt4 import QtCore, QtGui

class DescriptionChart(QtGui.QWidget):
    """
    Description chart widget
    """
    def __init__(self, parent=None):
        super(DescriptionChart, self).__init__(parent)

class DescriptionNotesWidget(QtGui.QWidget):
    """
    Description notes widget
    """
    def __init__(self, parent=None):
        super(DescriptionNotesWidget, self).__init__(parent)
        self.text_editor = QtGui.QTextEdit(self)
        self.text_editor.setText('Add description here')
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.text_editor)

class DescriptionWidget(QtGui.QSplitter):
    """
    Description widget
    """
    def __init__(self, parent=None):
        super(DescriptionWidget, self).__init__(parent)
        self.chart_widget = DescriptionChart(self)
        self.notes_widget = DescriptionNotesWidget(self)
        self.addWidget(self.chart_widget)
        self.addWidget(self.notes_widget)


