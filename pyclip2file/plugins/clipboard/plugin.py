import logging
from PySide2.QtCore import Signal, Slot
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication
from pyclip2file.api.plugin import Plugin


logger = logging.getLogger(__name__)

class ClipboardPlugin(Plugin):
    NAME = 'clipboard'

    sig_clipboard_changed = Signal()

    def on_initialize(self):
        self._pixmap = QPixmap()
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_changed)
        self.on_clipboard_changed()

    @property
    def pixmap(self):
        return self._pixmap

    @Slot()
    def on_clipboard_changed(self):
        clipboard_pixmap: QPixmap = self.clipboard.pixmap()
        if clipboard_pixmap and self._pixmap != clipboard_pixmap:
            self._pixmap = clipboard_pixmap
            self.sig_clipboard_changed.emit()
