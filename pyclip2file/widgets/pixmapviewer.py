
import logging
from PySide2.QtCore import (
    Qt, Signal, Slot, QMargins, QEvent, QPoint
)
from PySide2.QtGui import (
    QPixmap, QResizeEvent, QMouseEvent, QCursor
)
from PySide2.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QSizePolicy, QScrollArea,
    QApplication
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class PixmapViewport(QLabel):
    sig_clicked = Signal()

    def __init__(self):
        QLabel.__init__(self)
        self._overrided_cursor = False

    def event(self, e: QEvent) -> bool:
        if self.pixmap():
            if e.type() == QEvent.Enter:
                logger.debug('PixmapViewport.Enter')
                QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))
                self._overrided_cursor = True
        if self._overrided_cursor and e.type() == QEvent.Leave:
            logger.debug('PixmapViewport.Leave')
            QApplication.restoreOverrideCursor()
            self._overrided_cursor = False
        return super().event(e)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if self.pixmap():
            self.sig_clicked.emit()
        return super().mouseReleaseEvent(ev)

class PixmapPopUp(QLabel):
    # https://stackoverflow.com/questions/18765918/how-to-create-a-draggable-borderless-and-titleless-top-level-window-in-qt
    def __init__(self):
        QLabel.__init__(self)
        self.setWindowFlag(Qt.Window, True)
        # self.setWindowFlag(Qt.FramelessWindowHint, True)
        self._overrided_cursor = False
        self._start_pos = QPoint()
        self._moved = QPoint(0, 0)

    def event(self, e: QEvent) -> bool:
        if e.type() == QEvent.Enter:
            logger.debug('PixmapPopUp.Enter')
            self._overrided_cursor = True
            QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))
        elif self._overrided_cursor and e.type() == QEvent.Leave:
            logger.debug('PixmapPopUp.Leave')
            QApplication.restoreOverrideCursor()
            self._overrided_cursor = False
        return super().event(e)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self._start_pos = ev.globalPos()
        self._moved = QPoint(0, 0)
        return super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        delta = ev.globalPos() - self._start_pos
        self._moved.setX(self._moved.x() + abs(delta.x()))
        self._moved.setY(self._moved.y() + abs(delta.y()))
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self._start_pos = ev.globalPos()

        return super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        logging.debug(f'moved: {self._moved}')
        if self._moved.manhattanLength() > 8:
            return
        else:
            self.close()


class PixmapViewer(QWidget):
    def __init__(self, parent: QWidget=None) -> None:
        super().__init__(parent)
        self.pixmap = QPixmap()
        self.scaled_pixmap = QPixmap()

        lyt = QVBoxLayout(self)
        lyt.setContentsMargins(QMargins(0, 0, 0, 0))
        
        self.viewer = PixmapViewport()
        self.viewer.sig_clicked.connect(self.on_viewer_clicked)
        self.popup = PixmapPopUp()
        self.popup.setWindowTitle('View')
        self.scrollArea = QScrollArea()
        
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setContentsMargins(QMargins(0, 0, 0, 0))
        self.scrollArea.setViewportMargins(QMargins(0, 0, 0, 0))
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.scrollArea.setWidget(self.viewer)
        lyt.addWidget(self.scrollArea, Qt.AlignCenter)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.scrollArea.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.viewer.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.viewer.setAlignment(Qt.AlignCenter)

    def pixmap(self) -> QPixmap:
        return self.pixmap

    def setPixmap(self, pixmap: QPixmap) -> None:
        assert isinstance(pixmap, QPixmap)
        if self.pixmap == pixmap:
            return
        self.pixmap = pixmap
        self.scaled_pixmap = self.scale_pixmap()
        self.viewer.setPixmap(self.scaled_pixmap)
        self.popup.setPixmap(self.pixmap)

    def scale_pixmap(self) -> QPixmap:
        return self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def resizeEvent(self, event: QResizeEvent):
        if self.pixmap:
            self.viewer.setPixmap(self.scale_pixmap())

    @Slot()
    def on_viewer_clicked(self):
        self.popup.show()
        self.popup.raise_()
        self.popup.activateWindow()

    