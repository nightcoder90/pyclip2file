import logging
from typing import Optional

from PySide2.QtCore import Slot
from PySide2.QtGui import QPixmap
from pyclip2file.api.plugin import Plugin
from pyclip2file.api.decorators import on_plugin_available
from pyclip2file.api.plugin import Plugins
from pyclip2file.plugins.clipboard.plugin import ClipboardPlugin
from pyclip2file.plugins.editor.plugin import EditorPlugin
from pyclip2file.plugins.preview.panel import PreviewPanel

logger = logging.getLogger(__name__)


class PreviewPlugin(Plugin):
    NAME = 'preview'
    REQUIRES = [Plugins.Clipboard, Plugins.Editor]

    def on_initialize(self):
        self._pixmap: Optional[QPixmap] = None
        self._viewer: Optional[PreviewPanel] = None

    @on_plugin_available(plugin=Plugins.Editor)
    def on_editor_plugin_available(self):
        logger.warn('editor available!')
        editor_plugin: EditorPlugin = self.get_plugin(Plugins.Editor)

        if not self._viewer:
            self._viewer = PreviewPanel()
        if self._pixmap:
            self._viewer.setPixmap(self._pixmap)
        editor_plugin.add_panel(self._viewer)

    @on_plugin_available(plugin=Plugins.Clipboard)
    def on_clipboard_plugin_available(self):
        logger.warn('clipboard available!')
        clipboard_plugin: ClipboardPlugin = self.get_plugin(Plugins.Clipboard)
        clipboard_plugin.sig_clipboard_changed.connect(self.on_clipboard_changed)
        self.on_clipboard_changed()

    @Slot()
    def on_clipboard_changed(self):
        clipboard_plugin: ClipboardPlugin = self.get_plugin(Plugins.Clipboard)
        self._pixmap = clipboard_plugin.pixmap
        if self._pixmap and self._viewer:
            self._viewer.setPixmap(self._pixmap)