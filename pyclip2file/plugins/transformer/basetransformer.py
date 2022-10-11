from PySide2.QtGui import QPixmap
from pyclip2file.widgets.layoutbuilder import LayoutBuilder

class BaseTransformer:
    ID = None

    def __init__(self):
        pass

    def transform(self, pixmap: QPixmap) -> QPixmap:
        raise NotImplementedError()

    def add_to_layout(self, layout_builder: LayoutBuilder) -> LayoutBuilder:
        raise NotImplementedError()