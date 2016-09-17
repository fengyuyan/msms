"""
Product manager window navigator
"""
__author__ = 'Tom Yan'

from gui.widgets.navigator import Navigator
from gui.workspace import g_workspace
import os

class ProductNavigator(Navigator):
    """
    Product manager navigator
    """
    PATH = 'path'
    TABLE_WIDGET = 'table_widget'
    DES_WIDGET = 'des_widget'

    def __init__(self, parent=None):
        super(ProductNavigator, self).__init__(parent)
        self.product_dir = None
        if g_workspace.wsp_info:
            self.product_dir = g_workspace.wsp_info.get('Product Dir')
        if self.product_dir:
            self.load_products(self.product_dir)
        else:
            self.setVisible(False)
        self.setFixedWidth(64)

    def load_products(self, product_dir):
        """
        Load products from give directory
        :param product_dir:
        :return:
        """
        if not product_dir or not os.path.exists(product_dir):
            return

        cat_folders = os.listdir(product_dir)
        if not cat_folders:
            return

        for cat_folder in cat_folders:
            cat_name = cat_folder
            cat_folder = os.path.join(product_dir, cat_folder)
            cat_name.capitalize()
            icon_src = self.get_icon(cat_name)
            item = self.add_item(cat_name, icon_src)
            item.set_property(self.PATH, cat_folder)

        first_item = self.items[0]
        self.set_current_item(first_item)

    def get_icon(self, cat_name):
        """
        Get icon
        :param cat_name:
        :return:
        """
        if g_workspace.debug_mode:
            icon_dir = os.path.join(g_workspace.bin_dir, 'gui', 'res')
        else:
            icon_dir = os.path.join(g_workspace.bin_dir, 'res')
        lower_cat = cat_name.lower()
        if lower_cat.find('cloth') == 0:
            icon_src = os.path.join(icon_dir, 'dress.png')
        elif lower_cat.find('baby') == 0:
            icon_src = os.path.join(icon_dir,'baby.png')
        elif lower_cat.find('bag') == 0:
            icon_src = os.path.join(icon_dir, 'bag.png')
        elif lower_cat.find('health') == 0:
            icon_src = os.path.join(icon_dir, 'capsule.png')
        else:
            icon_src = None
        return icon_src
