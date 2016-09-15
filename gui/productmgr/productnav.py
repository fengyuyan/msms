"""
Product manager window navigator
"""
__author__ = 'Tom Yan'

from gui.widgets.navigator import Navigator

class ProductNavigator(Navigator):
    """
    Product manager navigator
    """
    def __init__(self, parent=None):
        super(ProductNavigator, self).__init__(parent)
        self.add_item('Clothes', icon_pic='D:\\src\mep\\mep\\gui\\icons\\splash\\mexp_splash.png')
        self.add_item('Baby')
