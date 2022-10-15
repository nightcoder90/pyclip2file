import logging
from typing import List
from PySide2.QtWidgets import QWidget, QGridLayout, QLayoutItem


logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

class SpecialTypes:
    Break = 'break'

class LayoutItem:
    def __init__(self, widget: QWidget=None, layout: QLayoutItem=None, 
                 special_type: str='', span: int=1):
        self._widget = widget
        self._layout = layout
        self._special_type = special_type
        self._span = span
        
    @property
    def widget(self):
        return self._widget

    @property
    def layout(self):
        return self._layout

    @property
    def special_type(self):
        return self._special_type

    @property
    def span(self):
        return self._span


class LayoutBuilder:
    def __init__(self):
        self.items: List[LayoutItem] = list()

    def add_item(self, item: LayoutItem):
        self.items.append(item)
        return self

    def add_widget(self, widget: QWidget, span: int=1):
        self.add_item(LayoutItem(widget=widget, span=span))
        return self

    def finish_row(self):
        self.add_item(LayoutItem(special_type=SpecialTypes.Break))
        return self

    def attach_to(self, w: QWidget) -> None:
        logger.info(f'{__class__}.attach_to')
        self._do_layout(w)

    def _do_layout(self, w: QWidget) -> None:
        logger.info(f'{__class__}._do_layout')
        layout = QGridLayout()
        w.setLayout(layout)

        self._do_layout_helper(layout, self.items)

    def _do_layout_helper(self, grid_layout: QGridLayout, items: List[LayoutItem]):
        logger.info(f'{__class__}._do_layout_helper')
        current_row = 0
        current_column = 0
        logger.info(f'{__class__}.items: {items}')
        for item in items:
            if item.special_type == SpecialTypes.Break:
                logger.info(f'{__class__}.addBreak')
                if current_column != 0:
                    current_row += 1
                    current_column = 0
            elif item.widget:
                logger.info(f'{__class__}.addWidget')
                grid_layout.addWidget(item.widget, current_row, current_column, 1, item.span)
            elif item.layout:
                logger.info(f'{__class__}.addLayout')
                grid_layout.addLayout(item.layout, current_row, current_column, 1, item.span)
            current_column += item.span
            
                
        
