"""
Product table used to list all products
"""
__author__ = 'Tom Yan'

import os
from PyQt4 import QtCore, QtGui
from gui.widgets.table import Table
from utilities.io import json_load

class ProductTableItem(QtGui.QTableWidgetItem):
    """
    Product table item
    """
    def __init__(self, text='', editable=True):
        super(ProductTableItem, self).__init__(text)
        if not editable:
            self.setFlags(self.flags() ^ QtCore.Qt.ItemIsEditable)

class ProductTable(Table):
    """
    Product table
    """
    NAME = 'Name'
    BRAND = 'Brand'
    STORE_LINK = 'Store/Link'
    PURCHASE_PRICE = 'Purchase Price ($)'
    PROMO_PRICE = 'Promotion Price ($)'
    SHIPPING = 'Shipping ($)'
    SOLD_PRICE = 'Sold Price ($)'
    TB_PRICE = 'TB Price ($)'
    TM_PRICE = 'TM Price ($)'
    JD_PRICE = 'JD Price ($)'
    PROFIT = 'Profit'
    HEADERS = [NAME, BRAND, STORE_LINK, PURCHASE_PRICE, PROMO_PRICE, SHIPPING, SOLD_PRICE, TB_PRICE, TM_PRICE, JD_PRICE, PROFIT]
    COL_NAME = HEADERS.index(NAME)
    COL_BRAND = HEADERS.index(BRAND)
    COL_STORE_LINK = HEADERS.index(STORE_LINK)
    COL_PURCHASE_PRICE = HEADERS.index(PURCHASE_PRICE)
    COL_PROMO_PRICE = HEADERS.index(PROMO_PRICE)
    COL_SHIPPING = HEADERS.index(SHIPPING)
    COL_SOLD_PRICE = HEADERS.index(SOLD_PRICE)
    COL_TB_PRICE = HEADERS.index(TB_PRICE)
    COL_TM_PRICE = HEADERS.index(TM_PRICE)
    COL_JD_PRICE = HEADERS.index(JD_PRICE)
    COL_PROFIT = HEADERS.index(PROFIT)

    PATH_ROLE = QtCore.Qt.UserRole + 1
    INFO_ROLE = QtCore.Qt.UserRole + 2

    def __init__(self, product_dir=None, des_widget=None, parent=None):
        super(ProductTable, self).__init__(parent)
        self.product_dir = product_dir
        self.des_widget = des_widget
        self.setColumnCount(len(ProductTable.HEADERS))
        self.setHorizontalHeaderLabels(ProductTable.HEADERS)
        self.load_product_list(self.product_dir)

        # always have a new row for use to add new product
        cur_row = self.rowCount()
        self.insertRow(cur_row)

        self.itemClicked.connect(self.on_item_clicked)

        if self.rowCount() > 2:
            cur_item = self.item(0, ProductTable.COL_NAME)
            self.setCurrentItem(cur_item)
            self.on_item_clicked(cur_item)

    def load_product_list(self, product_dir):
        """
        Load product list
        :param product_dir:
        :return:
        """
        if not product_dir or not os.path.exists(product_dir):
            return

        product_folders = os.listdir(product_dir)
        if not product_folders:
            return

        for folder_name in product_folders:
            product_folder = os.path.join(product_dir, folder_name)
            if os.path.isfile(product_folder):
                continue

            cur_row = self.rowCount()
            self.insertRow(cur_row)
            info_file = os.path.join(product_folder, 'info.txt')
            if not os.path.exists(info_file):
                continue

            file_dict = json_load(info_file)
            info = file_dict.get('Info')
            if not info:
                continue

            # name
            name_item = self.add_item(cur_row, ProductTable.COL_NAME, info.get(ProductTable.NAME, folder_name))
            name_item.setData(ProductTable.PATH_ROLE, product_folder)
            name_item.setData(ProductTable.INFO_ROLE, info)

            # brand
            self.add_item(cur_row, ProductTable.COL_BRAND, info.get(ProductTable.BRAND))

            # store/link
            self.add_item(cur_row, ProductTable.COL_STORE_LINK, info.get(ProductTable.STORE_LINK))

            # purchase price
            self.add_item(cur_row, ProductTable.COL_PURCHASE_PRICE, info.get(ProductTable.PURCHASE_PRICE))

            # promotion price
            self.add_item(cur_row, ProductTable.COL_PROMO_PRICE, info.get(ProductTable.PROMO_PRICE))

            # shipping fee
            self.add_item(cur_row, ProductTable.COL_SHIPPING, info.get(ProductTable.SHIPPING))

            # sold price
            self.add_item(cur_row, ProductTable.COL_SOLD_PRICE, info.get(ProductTable.SOLD_PRICE))

            # taobao price
            tb_price = info.get(ProductTable.TB_PRICE)
            if tb_price:
                self.add_item(cur_row, ProductTable.COL_TB_PRICE, tb_price.get('Price'))

            # tianmao price
            tm_price = info.get(ProductTable.TM_PRICE)
            if tm_price:
                self.add_item(cur_row, ProductTable.COL_TM_PRICE, tm_price.get('Price'))

            # JD price
            jd_price = info.get(ProductTable.JD_PRICE)
            if jd_price:
                self.add_item(cur_row, ProductTable.COL_JD_PRICE, jd_price.get('Price'))

            # profit
            self.add_item(cur_row, ProductTable.COL_PROFIT, info.get(ProductTable.PROFIT))

    def add_item(self, row, col, text, editable=True):
        """
        Add item
        :param row:
        :param col:
        :param text:
        :return:
        """
        if not text:
            return

        item = ProductTableItem(str(text), editable)
        self.setItem(row, col, item)
        return item

    def on_item_clicked(self, item):
        """
        Slot: item clicked
        :param item:
        :return:
        """
        name_item = self.item(item.row(), ProductTable.COL_NAME)
        product_folder = name_item.data(ProductTable.PATH_ROLE)
        info = name_item.data(ProductTable.INFO_ROLE)
        if self.des_widget:
            self.des_widget.load_description(product_folder, info)




