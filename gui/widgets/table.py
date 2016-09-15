__author__ = 'Tom Yan'
from PyQt4 import QtGui
from PyQt4 import QtCore
from dialog import Dialog
from list import List
from search import SearchLineEdit
from collections import OrderedDict
from functools import partial

def get_proper_table_height(table, show_only=False):
    """
    Get proper table height, so that we can set a right table height
    :param table:
    :return: proper table height
    """
    if not table:
        return -1

    height = 0

    # check if the header has multiple lines
    for col in range(0, table.columnCount()):
        header = str(table.model().headerData(col, QtCore.Qt.Horizontal))
        if header.find("\n") > 0:
            height += 15
            break

    if table.horizontalHeader():
        height += table.horizontalHeader().height()
    top_margin = table.contentsMargins().top()
    bottom_margin = table.contentsMargins().bottom()
    row_count = table.rowCount()
    for i in range(row_count):
        if show_only and table.isRowHidden(i):
            continue
        height += table.rowHeight(i)
    # frm_width = table.frameWidth()
    return height + top_margin + bottom_margin

def get_proper_table_width(table, show_only=False):
    """
    Get proper table width, so that we can set a right table width
    :param table:
    :return: proper table height
    """
    if not table:
        return -1

    width = 0
    if table.verticalHeader():
        width += table.verticalHeader().width()
    left_margin = table.contentsMargins().left()
    right_margin = table.contentsMargins().right()
    col_count = table.columnCount()
    for i in range(col_count):
        if show_only and table.isColumnHidden():
            continue
        width += table.columnWidth(i)
    # frm_width = table.frameWidth()
    return width + left_margin + right_margin

class TableFilterDlg(Dialog):
    """
    include search line and list widget to show available values.
    """

    signal_filter_condition_changed = QtCore.pyqtSignal(list)
    signal_sorting_changed = QtCore.pyqtSignal(int)

    SELECT_ALL = 'Select All'

    def __init__(self, parent=None):
        """
        """
        super(TableFilterDlg, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint) #$ & ~QtCore.Qt.WindowTitleHint)
        # self.setWindowTitle('Text Filter')
        self.setFixedSize(300, 400)

        self._checked_items = []

        self._search_widget = None
        self._list_widget = None

        self._init_ui()

    def _init_ui(self):
        """
        """
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        toolbar_layout = QtGui.QHBoxLayout()
        layout.addLayout(toolbar_layout)

        btn_sorting_asc = QtGui.QPushButton('A->Z')
        btn_sorting_asc.setObjectName('text_filter.sorting_ascending')
        btn_sorting_asc.clicked.connect(self.slot_sorting_ascending)
        toolbar_layout.addWidget(btn_sorting_asc)
        btn_sorting_desc = QtGui.QPushButton('Z->A')
        btn_sorting_desc.setObjectName('text_filter.sorting_descending')
        btn_sorting_desc.clicked.connect(self.slot_sorting_descending)
        toolbar_layout.addWidget(btn_sorting_desc)
        toolbar_layout.addStretch()

        self._search_widget = SearchLineEdit()
        self._search_widget.setObjectName('text_filter.search_widget')
        self._search_widget.sig_text_edited.connect(self.slot_search)
        layout.addWidget(self._search_widget)

        self._list_widget = List(use_default_style=True)
        self._list_widget.setObjectName('text_filter.list_widget')
        # self._list_widget.setSortingEnabled(True)
        self._list_widget.sig_item_checkstate_changed.connect(self.slot_list_item_state_changed)
        layout.addWidget(self._list_widget)

        action_layout = QtGui.QHBoxLayout()
        layout.addLayout(action_layout)

        btn_ok = QtGui.QPushButton('OK')
        btn_ok.setObjectName('text_filter.ok')
        btn_ok.clicked.connect(self.slot_ok)
        action_layout.addWidget(btn_ok)

        btn_cancel = QtGui.QPushButton('Cancel')
        btn_cancel.setObjectName('text_filter.cancel')
        btn_cancel.clicked.connect(self.slot_cancel)
        action_layout.addWidget(btn_cancel)

    def set_search_text(self, text):
        """
        """
        self._search_widget.setText(text)

    def slot_search(self, text):
        """
        """
        item_count = self._list_widget.count()
        if not text:
            for item_index in xrange(item_count):
                self._list_widget.setItemHidden(self._list_widget.item(item_index), False)
        else:
            text = str(text).strip().lower()
            for item_index in xrange(item_count):
                item = self._list_widget.item(item_index)
                item_text = str(item.text()).strip().lower()
                self._list_widget.setItemHidden(item, item_text.find(text) < 0)

    def _update_sel_all_state(self):
        """
        """
        if not self._list_widget or self._list_widget.count() <= 0 or str(self._list_widget.item(0).text()) != TableFilterDlg.SELECT_ALL:
            return

        total_count = self._list_widget.count() - 1
        checked_count = len(self._list_widget.get_checked_labels())
        if self._list_widget.item(0).checkState() == QtCore.Qt.Checked:
            checked_count = checked_count - 1

        if checked_count <= 0:
            sel_all_state = QtCore.Qt.Unchecked
        elif checked_count < total_count:
            sel_all_state = QtCore.Qt.PartiallyChecked
        else:
            sel_all_state = QtCore.Qt.Checked
        self._list_widget.blockSignals(True)
        self._list_widget.item(0).setCheckState(sel_all_state)
        self._list_widget.blockSignals(False)

    def set_item_state(self, item_index, state):
        """
        """
        if item_index < 0 or item_index >= self._list_widget.count():
            return

        item = self._list_widget.item(item_index)
        item.setCheckState(state)

    def slot_list_item_state_changed(self, item):
        """
        """
        self._list_widget.setCurrentItem(item)
        if str(item.text()) == TableFilterDlg.SELECT_ALL:
            self._list_widget.blockSignals(True)
            for item_index in xrange(1, self._list_widget.count()):
                self._list_widget.item(item_index).setCheckState(item.checkState())
            self._list_widget.blockSignals(False)
        else:
            self._update_sel_all_state()

    def set_items(self, all_items, checked_items):
        """
        """
        self._list_widget.set_list([TableFilterDlg.SELECT_ALL] + all_items if len(all_items) > 1 else all_items)
        self._checked_items = checked_items

        self._list_widget.blockSignals(True)
        for item_index in xrange(self._list_widget.count()):
            item = self._list_widget.item(item_index)
            item_text = str(item.text())
            if not item_text in checked_items:
                item.setCheckState(QtCore.Qt.Unchecked)
        self._list_widget.blockSignals(False)

        self._update_sel_all_state()

    def slot_ok(self):
        """
        """
        is_checked_item_changed = False
        checked_items = self._list_widget.get_checked_labels()
        if len(checked_items) != len(self._checked_items):
            is_checked_item_changed = True
        else:
            same_items = list(set(self._checked_items) & set(checked_items))
            if len(checked_items) != len(same_items):
                is_checked_item_changed = True

        if is_checked_item_changed:
            self.signal_filter_condition_changed.emit(checked_items)

        self.accept()

    def slot_cancel(self):
        """
        """
        self.reject()

    def slot_sorting_ascending(self):
        """
        """
        # self._list_widget.sortItems(Qt.AscendingOrder)
        self.signal_sorting_changed.emit(QtCore.Qt.AscendingOrder)
        self.close()

    def slot_sorting_descending(self):
        """
        """
        # self._list_widget.sortItems(Qt.DescendingOrder)
        self.signal_sorting_changed.emit(QtCore.Qt.DescendingOrder)
        self.close()

    def event(self, _event):
        """
        """
        if _event.type() in [QtCore.QEvent.FocusOut, QtCore.QEvent.WindowDeactivate]:
            is_handled = True
            self.reject()
        else:
            is_handled = super(TableFilterDlg, self).event(_event)
        return is_handled

class NHeaderView(QtGui.QHeaderView):
    """
    """

    multi_col_sorting_dict = OrderedDict()

    sorting_order_flag_dict = {QtCore.Qt.AscendingOrder:'Asc', QtCore.Qt.DescendingOrder:'Des'}

    signal_filter_changed = QtCore.pyqtSignal(dict)
    signal_sorting_changed = QtCore.pyqtSignal(dict)

    def __init__(self, orientation, parent=None):
        """
        """
        super(NHeaderView, self).__init__(orientation, parent)
        self.setClickable(True)
        self.non_sortable_headers = []

        self.original_col_width_dict = {} # {col_index: original_width, ...}

        # self.filter_context_menu = None
        self.filter_section_dict = {}
        self.filter_widget = None

        self._is_data_filter_enabled = True # global options, for all the filter sections.
        self._filter_widget_dict = {}

        self.sectionClicked.connect(self.slot_section_clicked)

    def _set_col_order_flag(self, col_index, sorting_order=QtCore.Qt.AscendingOrder):
        """
        """
        model = self.model()
        if col_index < 0 or col_index >= model.columnCount():
            return

        if not self.original_col_width_dict.has_key(col_index):
            self.original_col_width_dict[col_index] = self.parent().columnWidth(col_index)
        original_col_width = self.original_col_width_dict.get(col_index)

        col_header = model.headerData(col_index, QtCore.Qt.Horizontal)
        order_flag_index = self._get_order_flag_index(col_header)
        # if col_header.find('(') > -1:
        if order_flag_index > -1:
            col_header = col_header[:order_flag_index-1]
        col_header = '{}({})'.format(col_header, NHeaderView.sorting_order_flag_dict.get(sorting_order))
        model.setHeaderData(col_index, QtCore.Qt.Horizontal, col_header, QtCore.Qt.DisplayRole)

        header_font = self.viewOptions().font
        order_flag_width = QtGui.QFontMetrics(header_font).width('(ASC)')
        table_view = self.parent()
        if table_view and table_view.parent():
            table_view.parent().update_selection_width(col_index, -1, original_col_width + order_flag_width)

    def _get_order_flag_index(self, str_with_order_flag=''):
        """
        """
        if not str_with_order_flag:
            return -1

        order_flag_index = -1
        for order_flag in NHeaderView.sorting_order_flag_dict.values():
            order_flag_index = str_with_order_flag.find(order_flag)
            if order_flag_index > -1:
                break
        return order_flag_index

    def _clear_col_order_flag(self, col_index):
        """
        """
        model = self.model()
        if col_index < 0 or col_index >= model.columnCount():
            return

        col_header = model.headerData(col_index, QtCore.Qt.Horizontal)
        order_flag_index = self._get_order_flag_index(col_header)
        if order_flag_index > -1:
            model.setHeaderData(col_index, QtCore.Qt.Horizontal, col_header[:order_flag_index-1], QtCore.Qt.DisplayRole)
            original_col_width = self.original_col_width_dict.get(col_index)
            table_view = self.parent()
            if table_view and table_view.parent():
                table_view.parent().update_selection_width(col_index, -1, original_col_width)

    def set_section_sorting_order(self, col_index, sorting_order=QtCore.Qt.AscendingOrder):
        """
        """
        table_view = self.parent()
        if not table_view or not isinstance(table_view, NTableView):
            return

        col_header = self.model().headerData(col_index, QtCore.Qt.Horizontal)
        if col_header.lower().strip() in self.non_sortable_headers:
            return

        if NHeaderView.multi_col_sorting_dict.has_key(col_index):
            del NHeaderView.multi_col_sorting_dict[col_index]

        if not table_view.is_multi_col_sorting_enabled():
            self.clear_sorting()
        NHeaderView.multi_col_sorting_dict[col_index] = sorting_order

        table_view.sortByColumn(col_index, sorting_order)
        self._set_col_order_flag(col_index, sorting_order)

    def slot_section_clicked(self, col_index):
        """
        """
        if not NHeaderView.multi_col_sorting_dict.has_key(col_index):
            new_order = QtCore.Qt.AscendingOrder
        else:
            cur_order = NHeaderView.multi_col_sorting_dict.get(col_index)
            new_order = QtCore.Qt.AscendingOrder if cur_order == QtCore.Qt.DescendingOrder else QtCore.Qt.DescendingOrder
        self.set_section_sorting_order(col_index, new_order)

    def clear_sorting(self):
        """
        """
        NHeaderView.multi_col_sorting_dict.clear()

        model = self.model()
        for col_index in xrange(model.columnCount()):
            self._clear_col_order_flag(col_index)

    def enable_data_filter(self, is_enabled=True):
        """
        """
        self._is_data_filter_enabled = is_enabled

    def is_data_filter_enabled(self):
        """
        """
        return self._is_data_filter_enabled

    def slot_view_filter(self, section_index):
        """
        """
        self.filter_widget = TableFilterDlg(self.parent())
        self.filter_widget.setObjectName('header_view.filter_dlg')
        self.filter_widget.signal_filter_condition_changed.connect(partial(self.slot_filter_values_changed, section_index))
        self.filter_widget.signal_sorting_changed.connect(partial(self.slot_sorting_changed, section_index))

        model = self.model()
        all_values = []
        if self.filter_section_dict.has_key(section_index):
            filter_values = self.filter_section_dict.get(section_index)
        else:
            filter_values = []

        for row_index in xrange(model.rowCount()):
            is_matched = True
            for filter_col_index in self.filter_section_dict.keys():
                if filter_col_index == section_index:
                    continue
                item = model.item(row_index, filter_col_index)
                if item is None:
                    continue
                filter_col_value = item.text()
                if not filter_col_value in self.filter_section_dict.get(filter_col_index):
                    is_matched = False
                    break

            if not is_matched:
                continue
            item = model.item(row_index, section_index)
            if item is None:
                continue
            item_value = str(item.text()).strip()
            if not item_value in all_values:
                all_values.append(item_value)
            if not self.parent().isRowHidden(row_index) and not item_value in filter_values:
                filter_values.append(item_value)

        # if not filter_values:
        #     filter_values = all_values
        self.filter_widget.set_items(all_values, filter_values)

        x_offset = 0
        for col_index in xrange(section_index):
            if not self.parent().isColumnHidden(col_index):
                x_offset = x_offset + self.parent().columnWidth(col_index)
        header_pos = QtCore.QPoint(x_offset, self.height())
        header_pos = self.mapToGlobal(header_pos)
        self.filter_widget.move(header_pos)
        self.filter_widget.show()

    def slot_filter_values_changed(self, col_index, filter_values=None):
        """
        """
        if col_index < 0 or col_index >= self.model().columnCount() or filter_values is None:
            return

        self.filter_section_dict[col_index] = filter_values
        self.refresh_filter()
        self.signal_filter_changed.emit(self.filter_section_dict)

    def slot_sorting_changed(self, col_index, sorting_order):
        """
        """
        if not sorting_order in [QtCore.Qt.AscendingOrder, QtCore.Qt.DescendingOrder]:
            return
        self.set_section_sorting_order(col_index, sorting_order)

    def refresh_filter(self, filter_section_dict=None):
        """
        """
        # if self.filter_section_dict == filter_section_dict:
        #     return

        if not filter_section_dict is None:
            self.filter_section_dict = filter_section_dict
        if not self.filter_section_dict:
            return

        model = self.model()
        for row_index in xrange(model.rowCount()):
            is_matched = True
            for col_index, _filter_values in self.filter_section_dict.items():
                col_value = str(model.item(row_index, col_index).text()).strip()
                if not col_value in _filter_values:
                    is_matched = False
                    break
            self.parent().setRowHidden(row_index, not is_matched)
            self.parent().parent().setRowHidden(row_index, not is_matched)

    def contextMenuEvent(self, event):
        """
        """
        section_index = self.logicalIndexAt(event.pos())
        if section_index < 0 or section_index >= self.count() or not self._is_data_filter_enabled:
            return
        self.slot_view_filter(section_index)

class NTableView(QtGui.QTableView):
    """
    """

    def __init__(self, parent=None):
        """
        """
        super(NTableView, self).__init__(parent)
        self.h_header_view = NHeaderView(QtCore.Qt.Horizontal, self)
        self.h_header_view.setObjectName('h_header_view')
        self.setHorizontalHeader(self.h_header_view)
        self.enable_right_click_menu = False
        self.right_click_menu = None

        self.multi_col_sorting_enabled = False

    def enable_multi_col_sorting(self, enabled=True):
        """
        """
        self.multi_col_sorting_enabled = enabled
        self.horizontalHeader().clear_sorting()
        # self.setSortingEnabled(not enabled)

    def is_multi_col_sorting_enabled(self):
        """
        """
        return self.multi_col_sorting_enabled

    def set_non_sortable_headers(self, headers):
        """
        Set non-sortable headers
        """
        self.h_header_view.non_sortable_headers = []
        for i in xrange(len(headers)):
            lower_header = str(headers[i]).lower()
            self.h_header_view.non_sortable_headers.append(lower_header)

    def get_col_values(self, col_index, only_visible=False):
        """
        """
        model = self.model()
        if not model or col_index < 0 or col_index >= model.columnCount():
            return []

        col_values = []
        for row_index in xrange(model.rowCount()):
            item = model.item(row_index, col_index)
            if not item or (only_visible and self.isRowHidden(row_index)):
                continue
            col_values.append(item.text())
        return col_values

    def slot_horizontal_scroll_bar_value_changed(self, value):
        """
        :param value:
        :return:
        """
        if value <= 0:
            return
        self.horizontalScrollBar().setValue(0)

    def mousePressEvent(self, event): #pylint: disable=C0103
        """
        Mouse press event
        """
        super(NTableView, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.RightButton:
            cur_index = self.currentIndex()
            if not self.enable_right_click_menu or self.visualRect(cur_index).bottom() < event.pos().y():
                return

            elif self.right_click_menu is not None:
                pos = event.pos()
                pos.setY(event.pos().y() + 24)
                self.right_click_menu.exec_(self.mapToGlobal(pos))

class NFreezeTableWidgetItem(QtGui.QStandardItem):
    """
    Freeze table item
    """
    def __init__(self, text='', editable=False):
        super(NFreezeTableWidgetItem, self).__init__(text)
        self.color = None
        if not editable:
            self.setFlags(self.flags() ^ QtCore.Qt.ItemIsEditable)

class FreezeTable(QtGui.QTableView):
    """
    Frozen table widget
    """

    ROLE_SPAN = QtCore.Qt.UserRole + 1

    cellChanged = QtCore.pyqtSignal(int, int)
    signal_filter_changed = QtCore.pyqtSignal(dict)

    def __init__(self, model, parent=None):
        super(FreezeTable, self).__init__(parent)
        font_metrics = QtGui.QFontMetrics(self.font())
        font_height = font_metrics.height()
        self.row_height = font_height * 1.8

        # to improve performance
        # ATTENTION: table.model().headerData() has big performance issue
        self.horizontal_headers = []
        self.horizontal_header_col_map = {}

        self.m_model = model
        if model is None:
            self.m_model = QtGui.QStandardItemModel()
            self.m_model.setObjectName('model')
        self.setModel(self.m_model)
        self.frozen_columns = []
        self.frozen_table_view = NTableView(self) # QtGui.QTableView(self)
        self.frozen_table_view.setObjectName('frozen_table_view')
        # self.frozen_table_view.setSortingEnabled(True)
        self.vertical_header_width = 0

        self.setup_ui()

        # connect the headers and scrollbars of both tableviews together
        self.horizontalHeader().sectionResized.connect(self.update_selection_width)
        self.verticalHeader().sectionResized.connect(self.update_selection_height)
        self.frozen_table_view.verticalScrollBar().valueChanged.connect(self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(self.frozen_table_view.verticalScrollBar().setValue)
        self.frozen_table_view.horizontalHeader().signal_filter_changed.connect(self.signal_filter_changed)

    def setup_ui(self):
        """
        Setup UI
        """
        self.frozen_table_view.setModel(self.model())
        self.frozen_table_view.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frozen_table_view.verticalHeader().hide()
        self.frozen_table_view.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.viewport().stackUnder(self.frozen_table_view)

        self.frozen_table_view.setStyleSheet("QTableView { border: none; background-color: lightGray;}")
        self.frozen_table_view.setSelectionMode(self.selectionMode())
        for col in xrange(len(self.frozen_columns), self.model().columnCount()):
            self.frozen_table_view.setColumnHidden(col, True)

        for i in xrange(len(self.frozen_columns)):
            col = self.frozen_columns[i]
            self.frozen_table_view.setColumnWidth(col, self.columnWidth(col))

        self.frozen_table_view.horizontalScrollBar().valueChanged.connect(self.frozen_table_view.slot_horizontal_scroll_bar_value_changed)
        self.frozen_table_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.frozen_table_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        if len(self.frozen_columns) > 0:
            self.frozen_table_view.show()
        else:
            self.frozen_table_view.hide()

        self.update_frozen_table_geometry()

        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.frozen_table_view.setVerticalScrollMode(self.ScrollPerPixel)

    def enable_frozen_view_r_click_menu(self, enable):
        """
        Enable frozen view right click menu
        :param enable:
        :return:
        """
        self.frozen_table_view.enable_right_click_menu = enable

    def set_frozen_view_r_click_menu(self, menu):
        """
        Set frozen view right click menu
        :param menu:
        :return:
        """
        self.frozen_table_view.right_click_menu = menu

    def click_col_header(self, col_header):
        """
        :param col_header:
        :return:
        """
        model = self.frozen_table_view.model()
        for col_index in xrange(model.columnCount()):
            _col_header = model.headerData(col_index, QtCore.Qt.Horizontal)
            if _col_header == col_header:
                self.frozen_table_view.horizontalHeader().sectionClicked.emit(col_index)
                break

    def right_click_col_header(self, col_header):
        """
        :param col_header:
        :return:
        """
        filter_dlg = None

        model = self.frozen_table_view.model()
        for col_index in xrange(model.columnCount()):
            _col_header = model.headerData(col_index, QtCore.Qt.Horizontal)
            if _col_header.find('(') > -1:
                _col_header = _col_header[:_col_header.index('(')]
            if col_header == _col_header:
                header_view = self.frozen_table_view.horizontalHeader()
                header_view.slot_view_filter(col_index)
                filter_dlg = header_view.filter_widget
                break
        return filter_dlg

    def export(self, file_path):
        """
        :param file_path:
        :return:
        """
        if not file_path or not file_path.endswith('.csv') or not self.model():
            return

        visible_col_names, visible_col_indexes = [], []
        for col_header in self.horizontal_headers:
            col_index = self.horizontal_header_col_map.get(col_header)
            if col_index is None or self.isColumnHidden(col_index):
                continue
            visible_col_names.append(col_header.replace('\n', ''))
            visible_col_indexes.append(col_index)
        if not visible_col_names or not visible_col_indexes:
            return

        line_values = []
        for row_index in xrange(self.model().rowCount()):
            line = []
            for _index, col_index in enumerate(visible_col_indexes):
                item = self.item(row_index, col_index)
                if item:
                    item_text = str(item.text())
                elif line_values: # for the span table cell
                    item_text = line_values[-1][_index]
                else:
                    item_text = ''
                line.append(item_text)
            line_values.append(line)

        from utilities.io import export_csv
        export_csv(file_path, [visible_col_names] + line_values)

    def update_frozen_table_geometry(self):
        """
        Update frozen table geometry
        """
        if len(self.frozen_columns) == 0:
            return

        self.frozen_table_view.horizontalHeader().setFixedHeight(self.horizontalHeader().height())

        # calculate right width
        width = 0
        for col in self.frozen_columns:
            width += self.columnWidth(col)

        ver_header_width = self.verticalHeader().sizeHint().width()
        if ver_header_width == 0:
            ver_header_width = self.vertical_header_width
        self.frozen_table_view.setGeometry(ver_header_width + self.frameWidth(),
                                           self.frameWidth(), width,
                                           self.viewport().height() + self.horizontalHeader().height())

    def update_selection_width(self, logical_id, old_size, new_size):
        """
        Update selection width
        """
        # if logical_id in self.frozen_columns:
        self.frozen_table_view.setColumnWidth(logical_id, new_size)
        self.setColumnWidth(logical_id, new_size)
        self.update_frozen_table_geometry()

    def update_selection_height(self, logical_id, old_size, new_size):
        """
        Update selection height
        """
        self.frozen_table_view.setRowHeight(logical_id, new_size)

    def set_frozen_columns(self, columns):
        """
        Set frozen columns
        """
        self.frozen_columns = columns
        if len(columns) > 0:
            for col in xrange(len(self.frozen_columns), self.model().columnCount()):
                self.frozen_table_view.setColumnHidden(col, True)

            for i in xrange(len(self.frozen_columns)):
                col = self.frozen_columns[i]
                self.frozen_table_view.setColumnWidth(col, self.columnWidth(col))
                self.frozen_table_view.setColumnHidden(col, False)
            self.update_frozen_table_geometry()
            self.frozen_table_view.show()
        else:
            self.frozen_table_view.hide()

    def set_non_sortable_headers(self, headers):
        """
        Set non-sortable headers
        :param headers:
        :return:
        """
        self.frozen_table_view.set_non_sortable_headers(headers)

    def setSpan(self, row, col, row_span_count, col_span_count):
        """
        set span
        """
        # super(FreezeTable, self).setSpan(row, col, row_span_count, col_span_count)
        self.frozen_table_view.setSpan(row, col, row_span_count, col_span_count)

        model = self.model()
        if model:
            display_value = model.data(model.index(row, col))
            display_value = '' if display_value is None else display_value
            span_key = 'span_{}_{}'.format(display_value, row)
            for row_index in xrange(row, row+row_span_count):
                model.setData(model.index(row_index, col), span_key, FreezeTable.ROLE_SPAN)

    def resizeEvent(self, event):
        """
        Resize event
        """
        super(FreezeTable, self).resizeEvent(event)
        self.update_frozen_table_geometry()
        self.vertical_header_width = self.verticalHeader().width()

    def moveCursor(self, cursor_action, modifiers):
        """
        Move cursor function
        """
        current = super(FreezeTable, self).moveCursor(cursor_action, modifiers)

        frozen_col_num = len(self.frozen_columns)
        if frozen_col_num == 0:
            return current

        frozen_col_width = 0
        for col in self.frozen_columns:
            frozen_col_width += self.frozen_table_view.columnWidth(col)

        if frozen_col_num > 0 and cursor_action == self.MoveLeft and \
            current.column() > 0 and \
            self.visualRect(current).topLeft().x() < frozen_col_width:
            new_value = self.horizontalScrollBar().value() + self.visualRect(current).topLeft().x() - frozen_col_width
            self.horizontalScrollBar().setValue(new_value)
        return current

    def scrollTo(self, index, hint):
        """
        Scroll to
        """
        if index.column() > 0:
            super(FreezeTable, self).scrollTo(index, hint)


    def on_item_changed(self, item):
        """
        Slot: item change
        :param item:
        :return:
        """
        self.cellChanged.emit(item.row(), item.column())

    def hideColumn(self, col):
        """
        """
        super(FreezeTable, self).hideColumn(col)
        if self.frozen_table_view:
            self.frozen_table_view.hideColumn(col)

    def showColumn(self, col):
        """
        """
        super(FreezeTable, self).showColumn(col)
        if self.frozen_table_view:
            self.frozen_table_view.showColumn(col)

    def nextVisibleRow(self, start_row_index=0):
        """
        :param start_row_index:
        :return:
        """
        row_count = self.rowCount()
        if start_row_index >= row_count:
            return -1

        row = start_row_index
        while row < row_count:
            if not self.isRowHidden(row):
                break
            row = row + 1
        return row if row < row_count else -1

    def nextVisibleColumn(self, start_col_index=0):
        """
        """
        col_count = self.columnCount()
        if start_col_index >= col_count:
            return -1

        col = start_col_index
        while col < col_count:
            if not self.isColumnHidden(col):
                break
            col = col + 1
        return col if col < col_count else -1

    def horizontalHeaderItem(self, col): #pylint: disable=C0103
        """
        Horizontal header
        :param col:
        :return:
        """
        return self.m_model.horizontalHeaderItem(col)

    def item(self, row, col):
        """
        Get item in row, col
        :param row:
        :param col:
        :return:
        """
        return self.m_model.item(row, col)

    def setItem(self, row, col, item):
        """
        Set item
        :param row:
        :param col:
        :return:
        """
        return self.m_model.setItem(row, col, item)

    def currentItem(self):
        """
        Current item
        :return:
        """
        return self.m_model.itemFromIndex(self.currentIndex())

    def selectedItems(self):
        """
        Selected items
        :return:
        """
        selected_items = []
        selected_index = self.selectedIndexes()
        count = len(selected_index)
        for i in range(0, count):
            item = self.m_model.itemFromIndex(selected_index[i])
            selected_items.append(item)
        return selected_items

    def setColumnCount(self, col_count):
        """
        Set colummn count
        :return:
        """
        return self.m_model.setColumnCount(col_count)

    def columnCount(self):
        """
        Column count
        :return:
        """
        return self.m_model.columnCount()

    def rowCount(self):
        """
        Row count
        :return:
        """
        return self.m_model.rowCount()

    def setRowCount(self, row_count):
        """
        Set row count
        :return:
        """
        self.m_model.setRowCount(row_count)

    def setRowHidden(self, row, hidden):
        """
        Set row hidden
        :param row:
        :param hidden:
        :return:
        """
        super(FreezeTable, self).setRowHidden(row, hidden)
        self.frozen_table_view.setRowHidden(row, hidden)
        # self.update_frozen_table_geometry()

    def select_item(self, row_index, col_index, is_selected=True):
        """
        :param row_index:
        :param col_index:
        :param is_selected:
        :return:
        """
        model = self.model()
        if row_index < 0 or row_index >= model.rowCount() or col_index < 0 or col_index >= model.columnCount():
            return

        model_index = model.index(row_index, col_index)
        self.setSelection(self.visualRect(model_index), QtGui.QItemSelectionModel.Select if is_selected else QtGui.QItemSelectionModel.Deselect)

    def slot_multi_col_sorting_changed(self, state):
        """
        """
        self.frozen_table_view.enable_multi_col_sorting(state == QtCore.Qt.Checked)

    def set_row_height(self, height=None):
        """
        Set row height
        :param height:
        :return:
        """
        row_height = height
        if row_height is None:
            row_height = self.row_height
        for i in xrange(self.rowCount()):
            self.setRowHeight(i, row_height)

    def insertRow(self, p_int): #pylint: disable=C0103
        """
        Insert row: override function
        """
        self.m_model.insertRow(p_int)
        self.setRowHeight(p_int, self.row_height)

    def setHorizontalHeaderLabels(self, labels): #pylint: disable=C0103
        """
        Set horizontal header labels
        :param labels:
        :return:
        """
        self.m_model.setHorizontalHeaderLabels(labels)
        self.horizontal_headers = labels
        for i in xrange(len(labels)-1, -1, -1):
            label = labels[i]
            self.horizontal_header_col_map[label] = i

    def get_horizontal_header(self, col_index):
        """
        Get horizontal header
        :param col_index:
        :return:
        """
        return self.horizontal_headers[col_index]

    def add_columns(self, col_headers):
        """
        Add columns based on given headers
        :param col_headers:
        :return:
        """
        if col_headers is None or len(col_headers) == 0:
            return

        for i in xrange(len(col_headers)):
            header = col_headers[i]
            self.horizontal_header_col_map[header] = len(self.horizontal_headers)
            self.horizontal_headers.append(header)
            cur_col = self.columnCount()
            self.m_model.insertColumn(cur_col)
            self.m_model.setHorizontalHeaderItem(cur_col, QtGui.QStandardItem(header))

    def find_column(self, header_name):
        """
        Find column named with header_name
        :param header_name:
        :return:
        """
        return self.horizontal_header_col_map.get(header_name)

class Table(QtGui.QTableWidget):
    """
    Unified table widget
    """
    def __init__(self, parent=None, watermark=False):
        super(Table, self).__init__(parent)
        if watermark:
            pass

    def get_vertical_headers(self):
        """
        :return:
        """
        vertical_headers = []
        for row_index in xrange(self.rowCount()):
            vertical_headers.append(self.verticalHeaderItem(row_index).text())
        return vertical_headers

    def get_horizontal_headers(self):
        """
        :return:
        """
        horizontal_header = []
        for col_index in xrange(self.columnCount()):
            horizontal_header.append(self.horizontalHeaderItem(col_index).text())
        return horizontal_header

if __name__ == "__main__":
    app = QtGui.QApplication([])
    dlg = QtGui.QDialog()
    # table = Table(dlg)
    # table.setRowCount(10)
    # table.setColumnCount(5)
    # layout = QtGui.QVBoxLayout(dlg)
    # layout.addWidget(table)
    # g = ['c', 'b']
    # g_v = [[2, 1, 3], [5, 4], ['TT', 'SS', 'FF']]
    # import itertools
    # p = itertools.product(*g_v)
    # for i, p_i in enumerate(p):
    #     print i
    #     print list(p_i)

    layout = QtGui.QVBoxLayout(dlg)
    # tw = QtGui.QTableWidget(dlg)
    # tw.setHorizontalHeaderLabels(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n'])
    # tw.show()
    # layout.addWidget(tw)
    model = QtGui.QStandardItemModel()
    model.setColumnCount(13)
    model.setRowCount(100)
    model.setHorizontalHeaderLabels(['a', 'b', 'c', 'd', 'e', 'f\ntest', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n'])
    for row in xrange(100):
        for col in xrange(13):
            new_item = QtGui.QStandardItem("text_%d_%d" % (row, col))
            model.setItem(row, col, new_item)
    view = FreezeTable(model, dlg)
    view.set_frozen_columns([0, 1, 2])
    # view = QtGui.QTableView(dlg)
    # view.setModel(model)
    view.setWindowTitle('frozen table example')
    layout.addWidget(view)
    dlg.resize(560, 680)
    # view.show()
    dlg.show()
    app.exec_()