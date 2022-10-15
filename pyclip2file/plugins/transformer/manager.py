import logging
from typing import List
from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtGui import QPixmap
from pyclip2file.widgets.layoutbuilder import LayoutBuilder
from pyclip2file.plugins.transformer.basetransformer import BaseTransformer


logger = logging.getLogger(__name__)


class TransformerManager(QObject):
    sig_transformed_pixmap_changed = Signal()

    def __init__(self, parent: QObject=None):
        QObject.__init__(self, parent)
        self._pixmap: QPixmap = QPixmap()
        self._transformed_pixmap: QPixmap = QPixmap()
        self._transformers: List[BaseTransformer] = list()

    def set_original_pixmap(self, pixmap: QPixmap) -> None:
        self._pixmap = pixmap
        self.transform()

    @property
    def transformed_pixmap(self) -> QPixmap:
        return self._transformed_pixmap

    def register_transformer(self, transformer: BaseTransformer) -> None:
        self._transformers.append(transformer)
        self._transformers.sort(key=lambda tf: tf.ID)
        transformer.sig_updated.connect(self.on_transformer_updated)
        self.transform()

    def add_to_layout(self, layout_builder: LayoutBuilder) -> None:
        for transformer in self._transformers:
            transformer.add_to_layout(layout_builder=layout_builder.finish_row())

    def transform(self) -> None:
        if not self._pixmap:
            logger.warn(f'pixmap is invalid')
            return
        pixmap = self._pixmap
        for tr in self._transformers:
            pixmap = tr.transform(pixmap=pixmap)
        self._transformed_pixmap = pixmap
        self.sig_transformed_pixmap_changed.emit()

    @Slot()
    def on_transformer_updated(self) -> None:
        self.transform()