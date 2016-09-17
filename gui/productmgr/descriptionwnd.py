"""
Description window, it has two parts: description chart and description notes
"""
__author__ = 'Tom Yan'

import os
from PyQt4 import QtCore, QtGui

class DescriptionChart(QtGui.QScrollArea):
    """
    Description chart widget
    """
    IMAGE_EXT = ['.jpg', '.png', '.jpeg', '.bmp', '.gif']

    def __init__(self, parent=None):
        super(DescriptionChart, self).__init__(parent)
        self.cur_image_folder = None
        self.image_widgets = {}
        self.main_widget = QtGui.QWidget(self)
        self._layout = QtGui.QHBoxLayout(self.main_widget)
        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)

    def load_images(self, image_folder):
        """
        Load images from folder
        """
        if self.cur_image_folder == image_folder:
            return

        self.clear_images()

        if not image_folder or not os.path.exists(image_folder):
            return

        files = os.listdir(image_folder)
        if not files:
            return

        for image_file in files:
            image_file = os.path.join(image_folder, image_file)
            if not os.path.isfile(image_file) or not DescriptionChart.is_image_file(image_file):
                continue

            self.add_image(image_file)

    @staticmethod
    def is_image_file(filename):
        """
        Check if the file is image file
        """
        _, extension = os.path.splitext(filename)
        return str(extension).lower() in DescriptionChart.IMAGE_EXT

    def clear_images(self):
        """
        Clear images
        """
        while self._layout.count():
            child = self._layout.takeAt(0)
            widget = child.widget()
            if widget:
                self._layout.removeWidget(widget)
                widget.setParent(None)

    def add_image(self, image_file):
        """
        Add image
        """
        image_label = self.image_widgets.get(image_file)
        if not image_label:
            image_label = QtGui.QLabel(self.main_widget)
            pixmap = QtGui.QPixmap(image_file)
            image_label.setPixmap(pixmap)
            self.image_widgets[image_file] = image_label
        self._layout.addWidget(image_label)

class DescriptionNotesWidget(QtGui.QWidget):
    """
    Description notes widget
    """
    HOLDER_TEXT = 'Add description here'
    def __init__(self, parent=None):
        super(DescriptionNotesWidget, self).__init__(parent)
        self.notes = {}
        self.cur_note_folder = None
        self.cur_info = None
        self.text_editor = QtGui.QTextEdit(self)
        self.text_editor.setText(DescriptionNotesWidget.HOLDER_TEXT)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.text_editor)
        layout.setContentsMargins(0, 0, 0, 0)

    def load_notes(self, product_folder, info):
        """
        Load notes
        """
        if not product_folder or not os.path.exists(product_folder) or self.cur_note_folder == product_folder:
            return

        # save current notes firstly if it's modified
        if self.cur_note_folder and self.text_editor.document().isModified():
            cur_text = self.text_editor.toPlainText()
            if DescriptionNotesWidget.HOLDER_TEXT != cur_text:
                self.notes[self.cur_note_folder] = cur_text

        note = self.notes.get(product_folder)
        if note:
            self.text_editor.setText(note)
        elif info:
            note = info.get('Description', '')
            self.text_editor.setText(note)
            self.notes[product_folder] = note
        self.cur_info = info
        self.cur_note_folder = product_folder


class DescriptionWidget(QtGui.QSplitter):
    """
    Description widget
    """
    def __init__(self, parent=None):
        super(DescriptionWidget, self).__init__(parent)
        self.chart_widget = DescriptionChart(parent=self)
        self.notes_widget = DescriptionNotesWidget(self)
        self.addWidget(self.chart_widget)
        self.addWidget(self.notes_widget)

    def load_description(self, product_folder, info):
        """
        Load description
        :param product_folder:
        :return:
        """
        self.chart_widget.load_images(product_folder)
        self.notes_widget.load_notes(product_folder, info)



