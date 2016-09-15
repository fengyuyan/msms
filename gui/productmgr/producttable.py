"""
Product table used to list all products
"""
__author__ = 'Tom Yan'

from PyQt4 import QtCore, QtGui
from gui.widgets.table import Table

class ProductTable(Table):
    """
    Product table
    """
    def __init__(self, parent=None):
        super(ProductTable, self).__init__(parent)

