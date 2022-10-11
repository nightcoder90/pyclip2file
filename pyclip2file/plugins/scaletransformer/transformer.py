from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel, QLineEdit
from pyclip2file.widgets.layoutbuilder import LayoutBuilder
from pyclip2file.plugins.transformer.basetransformer import BaseTransformer

class ScaleTransformer(BaseTransformer):
    ID = 'A.Scale'

    def transform(self, pixmap: QPixmap) -> QPixmap:
        # TODO: implementation
        return pixmap

    def add_to_layout(self, layout_builder: LayoutBuilder) -> LayoutBuilder:
        # TODO: implementation
        layout_builder.add_widget(QLabel('Width [px]'))
        layout_builder.add_widget(QLineEdit())
        return layout_builder