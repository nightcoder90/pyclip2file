
import logging
from PySide2.QtCore import (
    Qt, Signal, Slot, QMargins, QEvent, QPoint
)
from PySide2.QtGui import (
    QPixmap, QResizeEvent, QMouseEvent, QCursor, QPaintEvent, QPainter, QPalette,
)
from PySide2.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QLayout, QSizePolicy, QScrollArea,
    QApplication, QGraphicsOpacityEffect
)

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


class PixmapPopUp(QWidget):
    # https://stackoverflow.com/questions/18765918/how-to-create-a-draggable-borderless-and-titleless-top-level-window-in-qt
    def __init__(self, parent: QWidget=None):
        QWidget.__init__(self, parent)
        self.setWindowFlag(Qt.Window, True)

        self.setLayout(QVBoxLayout())
        self._label = QLabel()
        self.layout().addWidget(self._label)
        self.layout().setSizeConstraint(QLayout.SetNoConstraint)
        
        # self.setWindowFlag(Qt.FramelessWindowHint, True)
        self._is_entered = False
        self._start_pos = QPoint()
        self._moved = QPoint(0, 0)

    def setPixmap(self, pixmap: QPixmap):
        self._label.setPixmap(pixmap)
        self.resize(pixmap.size())

    def event(self, e: QEvent) -> bool:
        if e.type() == QEvent.Enter:
            if not self._is_entered:
                logger.debug('PixmapPopUp.Enter')
                self._is_entered = True
                QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))
        elif e.type() == QEvent.Leave:
            if self._is_entered:
                logger.debug('PixmapPopUp.Leave')
                QApplication.restoreOverrideCursor()
                self._is_entered = False
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

class PixmapSizeOverlay(QWidget):
    # Reference: https://github.com/qt-creator/qt-creator/blob/master/src/libs/utils/fadingindicator.cpp
    CENTER = 'center'
    BOTTOM_LEFT = 'bottom_left'

    def __init__(self, parent: QWidget, position=None):
        QWidget.__init__(self, parent)

        if not position:
            position = PixmapSizeOverlay.CENTER
        self._position = position

        self._effect = QGraphicsOpacityEffect(self)
        self._effect.setOpacity(0.7)
        self.setGraphicsEffect(self._effect)
        
        self._label = QLabel()
        pal = self.palette()
        pal.setColor(QPalette.WindowText, pal.color(QPalette.Window))
        self._label.setPalette(pal)
        lyt = QVBoxLayout()
        self.setLayout(lyt)
        lyt.addWidget(self._label)

    def set_text(self, text):
        self._label.setText(text)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        self.adjustSize()

    def paintEvent(self, ev: QPaintEvent) -> None:
        parent = self.parentWidget()
        if self._position == PixmapSizeOverlay.CENTER:
            pos = parent.rect().center() - self.rect().center() if parent else QPoint()
        else:
            pos = parent.rect().bottomLeft() - self.rect().bottomLeft() if parent else QPoint()
        self.move(pos)

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(self.palette().color(QPalette.WindowText))
        p.drawRect(self.rect())
        return super().paintEvent(ev)

class PixmapViewer(QWidget):
    def __init__(self, parent: QWidget=None) -> None:
        super().__init__(parent)
        self._is_entered = False
        self._pixmap = QPixmap()
        self._scaled_pixmap = QPixmap()

        lyt = QVBoxLayout(self)
        lyt.setContentsMargins(QMargins(0, 0, 0, 0))
        
        self._viewer = QLabel()
        self._popup = PixmapPopUp()
        self._popup.setWindowTitle('View')
        self._overlay = PixmapSizeOverlay(self, PixmapSizeOverlay.BOTTOM_LEFT)
        self._overlay.set_text('')
        self.scrollArea = QScrollArea()
        
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setContentsMargins(QMargins(0, 0, 0, 0))
        self.scrollArea.setViewportMargins(QMargins(0, 0, 0, 0))
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.scrollArea.setWidget(self._viewer)
        lyt.addWidget(self.scrollArea, Qt.AlignCenter)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.scrollArea.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self._viewer.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self._viewer.setAlignment(Qt.AlignCenter)

    def pixmap(self) -> QPixmap:
        return self._pixmap

    def setPixmap(self, pixmap: QPixmap) -> None:
        assert isinstance(pixmap, QPixmap)
        if self._pixmap == pixmap:
            return
        self._pixmap = pixmap
        self._scaled_pixmap = self.scaled_pixmap()
        self._viewer.setPixmap(self._scaled_pixmap)
        self._popup.setPixmap(self._pixmap)
        self.update_overlay_text()
        self.show_overlay()

    def scaled_pixmap(self) -> QPixmap:
        return self._pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def resizeEvent(self, event: QResizeEvent):
        if self._pixmap:
            self._viewer.setPixmap(self.scaled_pixmap())

    def event(self, e: QEvent) -> bool:
        if e.type() == QEvent.Enter:
            if self._pixmap:        
                if not self._is_entered:
                    logger.debug(f'PixmapViewport.Enter {self}')
                    QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))
                    self._is_entered = True
                    # self.show_overlay()
                    # self.update()
        if e.type() == QEvent.Leave:
            if self._is_entered:
                logger.debug('PixmapViewport.Leave')
                QApplication.restoreOverrideCursor()
                self._is_entered = False
                # self.hide_overlay()
                # self.update()
        return super().event(e)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if self._pixmap:
            self.on_viewer_clicked()
        return super().mouseReleaseEvent(ev)

    def on_viewer_clicked(self):
        self.show_popup()

    def show_popup(self):
        self._popup.show()
        self._popup.raise_()
        self._popup.activateWindow()

    def update_overlay_text(self):
        h = self._pixmap.height()
        w = self._pixmap.width()
        self._overlay.set_text(f'{w}×{h}')

    def show_overlay(self):
        self._overlay.show()
        self._overlay.raise_()

    def hide_overlay(self):
        self._overlay.hide()