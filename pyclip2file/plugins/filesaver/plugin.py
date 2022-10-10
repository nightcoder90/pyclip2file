import logging
from typing import Optional

from PySide2.QtCore import Slot
from PySide2.QtGui import QPixmap
from pyclip2file.api.plugin import Plugin
from pyclip2file.api.decorators import on_plugin_available
from pyclip2file.api.plugin import Plugins
from pyclip2file.plugins.clipboard.plugin import ClipboardPlugin
from pyclip2file.plugins.editor.plugin import EditorPlugin
from pyclip2file.plugins.filesaver.panel import FileSaverPanel

logger = logging.getLogger(__name__)


class FileSaverPlugin(Plugin):
    NAME = 'file_saver'
    REQUIRES = [Plugins.Clipboard, Plugins.Editor]

    def create_panel(self):
        panel = FileSaverPanel()
        panel.sig_save_requested.connect(self.on_save_requested)
        return panel

    def on_initialize(self):
        self._panel: Optional[FileSaverPanel] = None
        self._pixmap: Optional[QPixmap] = None

    @on_plugin_available(plugin=Plugins.Editor)
    def on_editor_plugin_available(self):
        editor_plugin: EditorPlugin = self.get_plugin(Plugins.Editor)

        if not self._panel:
            self._panel = self.create_panel()
        if self._pixmap:
            self._panel.save_enable(True)
        editor_plugin.add_panel(self._panel)

    @on_plugin_available(plugin=Plugins.Clipboard)
    def on_clipboard_plugin_available(self):
        logger.warn('clipboard available!')
        clipboard_plugin: ClipboardPlugin = self.get_plugin(Plugins.Clipboard)
        clipboard_plugin.sig_clipboard_changed.connect(self.on_clipboard_changed)
        self.on_clipboard_changed()

    @Slot()
    def on_clipboard_changed(self):
        clipboard_plugin: ClipboardPlugin = self.get_plugin(Plugins.Clipboard)
        if self._pixmap == clipboard_plugin.pixmap:
            return
        self._pixmap = clipboard_plugin.pixmap
        if  self._pixmap and self._panel:
            self._panel.save_enable(True)

    @Slot(str)
    def on_save_requested(self, path: str):
        if not self._pixmap:
            logger.warn('Null pixmap')
        self._pixmap.save(path)
