"""
List widget used in the project
"""
__author__ = 'Tom Yan'

from PyQt4 import QtGui
from PyQt4.QtGui import QListWidget, QListWidgetItem, QFrame, QSizePolicy, QAbstractItemView, QFontMetrics, QIcon
from PyQt4.QtCore import Qt, pyqtSignal, QSize

class List(QListWidget):  #pylint: disable=R0904
    """
    list widget
    """
    sig_item_checkstate_changed = pyqtSignal(QListWidgetItem)

    def __init__(self, parent=None, use_default_style=False):
        """
        constructor
        """
        super(List, self).__init__(parent)
        self.enable_right_click = False
        self.enable_shortcut = False
        self.right_context_menu = None
        self.setFrameStyle(QFrame.NoFrame)
        self._parent = parent
        self.use_default_style = use_default_style
        size_policy = QSizePolicy(QSizePolicy.Fixed,
                                  QSizePolicy.Preferred)
        self.setSizePolicy(size_policy)
        self.setFixedWidth(150)
        style_sheet = """
            QListView{
                background-color: transparent;
              }
            QScrollBar:vertical {
            border: 1px solid transparent;
            border-radius: 9px;
            background-color: transparent;
            width:15px;
            }
        """
        non_freeze = """
            QListView::item:hover {
                background-color: moccasin;
            }
            QListView::item:selected {
                background-color: CornflowerBlue;
            }
        """
        freeze = """
            QListView::item {
                background-color: lightGray;
            }
        """
        self.non_freeze_style = style_sheet + non_freeze
        self.freeze_style = style_sheet + freeze
        if not self.use_default_style:
            self.setStyleSheet(self.non_freeze_style)

        self.selection_mode = QAbstractItemView.SingleSelection
        self.setSelectionMode(self.selection_mode)
        self.setMaximumWidth(1000)
        self.setMinimumWidth(5)
        # self.setMaximumHeight(2000)
        # self.setMinimumHeight(32)

        # clicked connection
        self.itemChanged.connect(self.sig_item_checkstate_changed)
        #self.itemChanged.connect(self.setCurrentItem)

        font_metrics = QFontMetrics(self.font())
        self.font_height = font_metrics.height()
        self.row_height = self.font_height * 2.2

    def addItem(self, item):  #pylint: disable=C0103
        """
        control the new added item size
        """
        item.setSizeHint(QSize(item.sizeHint().width(), self.row_height))
        super(List, self).addItem(item)

    def insertItem(self, index, item):  #pylint: disable=C0103
        """
        control the new added item size
        """
        item.setSizeHint(QSize(item.sizeHint().width(), self.row_height))
        super(List, self).insertItem(index, item)

    def slot_select_all(self):
        """
        select all items
        """
        count = self.count()
        for row in range(count):
            item = self.item(row)
            item.setCheckState(Qt.Checked)

    def slot_deselect_all(self):
        """
        deselect all items
        """
        count = self.count()
        for row in range(count):
            item = self.item(row)
            item.setCheckState(Qt.Unchecked)

    def set_freeze(self, b_freeze):
        """
        freeze the list or not
        """
        if b_freeze:
            self.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
            if not self.use_default_style:
                self.setStyleSheet(self.freeze_style)
        else:
            self.setSelectionMode(self.selection_mode)
            if not self.use_default_style:
                self.setStyleSheet(self.non_freeze_style)

    # def sizeHint(self): #pylint: disable=C0103,R0201
    #     """
    #     the proper size
    #     """
    #     list_column_width = self.size().width()
    #     list_column_height = self.sizeHintForRow(0)*self.count() + 2 * self.frameWidth()
    #     return QSize(list_column_width, list_column_height)

    def upper_list_label(self, upper_case=True):
        """
        Upper each item label.
        """
        for item_index in xrange(self.count()):
            item_text = str(self.item(item_index).text())
            if upper_case:
                item_text = item_text.upper()
            else:
                item_text = item_text.lower()
            self.item(item_index).setText(item_text)

    def set_list(self, input_item_list, \
                 check_mode=2, check_map=None, selected_index=0):
        """
        set list
        """
        if len(input_item_list) == 0:
            return
        self.clear()

        list_items = []
        for item in input_item_list:
            list_items.append(QtGui.QListWidgetItem(item))

        for type_item in range(len(list_items)):
            list_items[type_item].setFlags( \
                QtGui.QListWidgetItem().flags() | Qt.ItemIsUserCheckable)
            # item_name = unicode(list_items[type_item].text())

            if check_map != None:
                item_name = input_item_list[type_item]
                check_mode = check_map[item_name]

            list_items[type_item].setCheckState(check_mode)
            self.insertItem(type_item, list_items[type_item])

        #set the item 0 to be the default selective item
        self.setCurrentItem(list_items[selected_index], \
                            QtGui.QItemSelectionModel.Select)

    def add_item(self, item_name):
        """
        """
        new_item = QtGui.QListWidgetItem(item_name)
        new_item.setFlags(QtGui.QListWidgetItem().flags() | Qt.ItemIsUserCheckable)
        new_item.setCheckState(Qt.Unchecked)
        self.insertItem(self.count(), new_item)

    def del_item(self, item_name):
        """
        """
        count = self.count()
        for row in xrange(count):
            item = self.item(row)
            if item.text() == item_name:
                self.takeItem(row)
                break

    def set_list_with_icon(self, input_item_list, icon=None, set_default_selection=True):
        """
        set list
        """
        if input_item_list is None or len(input_item_list) < 1:
            return
        list_items = []

        self.clear()
        for item in input_item_list:
            list_items.append(QtGui.QListWidgetItem(item))

        for type_item in range(len(list_items)):
            if icon is None:
                list_items[type_item].setIcon(QIcon( \
                    ":/res/check.png"))
            else:
                list_items[type_item].setIcon(icon)
            self.insertItem(type_item, list_items[type_item])

        #set the item 0 to be the default selective item
        if set_default_selection:
            self.setCurrentItem(list_items[0], QtGui.QItemSelectionModel.Select)

    def get_unchecked_labels(self):
        """
        Return unchecked items label in [].
        """
        unchecked_labels = []
        item_count = self.count()
        if item_count < 1:
            return unchecked_labels

        for item_index in xrange(item_count):
            item = self.item(item_index)
            if item is None or item.checkState() != Qt.Unchecked:
                continue
            unchecked_labels.append(str(item.text()))
        return unchecked_labels

    def get_checked_labels(self):
        """
        Return checked items label in [].
        """
        checked_labels = []
        item_count = self.count()
        if item_count < 1:
            return checked_labels

        for item_index in xrange(item_count):
            item = self.item(item_index)
            if item is None or item.checkState() == Qt.Unchecked:
                continue
            checked_labels.append(str(item.text()))
        return checked_labels

    def get_labels(self):
        """
        Get all items
        """
        labels = []
        item_count = self.count()
        if item_count < 1:
            return labels

        for item_index in xrange(item_count):
            item = self.item(item_index)
            if item is None:
                continue
            labels.append(str(item.text()))
        return labels

    def get_checked_status_list(self):
        """
        Get checked status list in order.
        """
        checked_status_list = []
        for item_index in xrange(self.count()):
            item = self.item(item_index)
            if not item is None:
                checked_status_list.append(item.checkState())
        return checked_status_list

    def get_checked_status_map(self):
        """
        Get checked status for each device type.
        """
        checked_status = {}  # {'BJT':True, ...}
        for item_index in xrange(self.count()):
            item = self.item(item_index)
            if item is None:
                continue
            item_text = str(item.text())
            if item.checkState() != Qt.Checked:
                checked_status[item_text] = False
            else:
                checked_status[item_text] = True
        return checked_status

    def get_item_by_label(self, label=''):
        '''Get specified list item by given label, return None if not found.'''
        if not label or len(label) < 1:
            return None

        _item = None
        for item_index in xrange(self.count()):
            item = self.item(item_index)
            if item is None:
                continue
            if str(item.text()).lower() == label.lower():
                _item = item
                break
        return _item

    def enable_right_click_menu(self, enable=True):
        """
        Enable right click to rename or not
        """
        self.enable_right_click = enable

    def set_right_context_menu(self, menu):
        """
        Set right-click context menu
        """
        self.right_context_menu = menu

    def enable_shortcut_key(self, enable=True):
        """
        Enable right click to rename or not
        """
        self.enable_shortcut = enable

    def get_height(self):
        """
        Get list height
        """
        row_height = self.sizeHintForRow(0)
        return row_height * self.count() + 2 * self.frameWidth()

    def mousePressEvent(self, event):
        """
        Mouse press event
        """
        super(List, self).mousePressEvent(event)
        if event.button() == Qt.RightButton:
            if self.enable_right_click:
                last_item = self.item(self.count()-1)
                if self.visualItemRect(last_item).bottom() < event.pos().y():
                    return
                elif self.right_context_menu is not None:
                    self.right_context_menu.cur_pos = event.pos
                    self.right_context_menu.exec_(self.mapToGlobal(event.pos()))

    def keyPressEvent(self, event): #pylint: disable=C0103
        """
        Key press event
        """
        if self.enable_shortcut and self._parent != None:
            if event.matches(QtGui.QKeySequence.Copy):
                if hasattr(self._parent, 'on_copy'):
                    self._parent.on_copy()
            elif event.matches(QtGui.QKeySequence.Paste):
                if hasattr(self._parent, 'on_paste'):
                    self._parent.on_paste()
            elif event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_D:
                if hasattr(self._parent, 'on_duplicate'):
                    self._parent.on_duplicate()

