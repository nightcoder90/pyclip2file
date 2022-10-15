import logging

from PySide2.QtCore import Qt, QObject, Slot
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel, QSpinBox
from pyclip2file.widgets.layoutbuilder import LayoutBuilder
from pyclip2file.plugins.transformer.basetransformer import BaseTransformer


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ScaleTransformer(BaseTransformer):
    ID = 'A.Scale'

    def __init__(self, parent: QObject=None):
        # TODO: Load Settings
        BaseTransformer.__init__(self, parent)
        self._width = 800
        self._width_edit = None

    def transform(self, pixmap: QPixmap) -> QPixmap:
        # TODO: implementation
        scaled_pixmap = pixmap.scaledToWidth(self._width, Qt.SmoothTransformation)
        return scaled_pixmap

    def add_to_layout(self, layout_builder: LayoutBuilder) -> LayoutBuilder:
        logger.debug(f'add_to_layout {layout_builder}')
        label = QLabel('Width:')
        layout_builder.add_widget(label)
        if not self._width_edit:
            self._width_edit = QSpinBox()
            self._width_edit.setSuffix('px')
            self._width_edit.setMinimum(1)
            self._width_edit.setMaximum(99999)
            self._width_edit.setValue(self._width)
            self._width_edit.editingFinished.connect(self.on_width_edited)
        layout_builder.add_widget(self._width_edit)
        label.setBuddy(self._width_edit)
        return layout_builder

    @Slot()
    def on_width_edited(self):
        self._width = self._width_edit.value()
        self.sig_updated.emit()