from PySide2.QtCore import (
    Qt, QMargins
)
from PySide2.QtGui import (
    QPixmap, QResizeEvent
)
from PySide2.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QSizePolicy, QScrollArea
)


class PixmapViewer(QWidget):
    def __init__(self, parent: QWidget=None) -> None:
        super().__init__(parent)
        self.pixmap = QPixmap()

        lyt = QVBoxLayout(self)
        lyt.setContentsMargins(QMargins(0, 0, 0, 0))
        
        self.viewer = QLabel()
        self.scrollArea = QScrollArea()
        
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setContentsMargins(QMargins(0, 0, 0, 0))
        self.scrollArea.setViewportMargins(QMargins(0, 0, 0, 0))
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.scrollArea.setWidget(self.viewer)
        lyt.addWidget(self.scrollArea)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.scrollArea.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.viewer.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

    def pixmap(self) -> QPixmap:
        return self.pixmap

    def setPixmap(self, pixmap: QPixmap) -> None:
        assert isinstance(pixmap, QPixmap)
        if self.pixmap == pixmap:
            return
        self.pixmap = pixmap
        self.viewer.setPixmap(self.scaledPixmap())

    def scaledPixmap(self) -> QPixmap:
        return self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def resizeEvent(self, event: QResizeEvent):
        if self.pixmap:
            self.viewer.setPixmap(self.scaledPixmap())