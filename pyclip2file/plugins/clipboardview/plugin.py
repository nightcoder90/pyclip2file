import logging
from typing import Optional

from PySide2.QtCore import Slot
from PySide2.QtGui import QPixmap
from pyclip2file.api.plugin import Plugin
from pyclip2file.api.decorators import on_plugin_available
from pyclip2file.api.plugin import Plugins
from pyclip2file.plugins.clipboardwatcher.plugin import ClipboardWatcherPlugin
from pyclip2file.plugins.editor.plugin import EditorPlugin
from pyclip2file.plugins.clipboardview.panel import ClipboardViewPanel

logger = logging.getLogger(__name__)


class ClipboardViewPlugin(Plugin):
    NAME = 'clipboard_view'
    REQUIRES = [Plugins.ClipboardWatcher, Plugins.Editor]

    def on_initialize(self):
        self._pixmap: Optional[QPixmap] = None
        self._viewer: Optional[ClipboardViewPanel] = None

    @on_plugin_available(plugin=Plugins.Editor)
    def on_editor_plugin_available(self):
        editor_plugin: EditorPlugin = self.get_plugin(Plugins.Editor)

        if not self._viewer:
            self._viewer = ClipboardViewPanel()
        if self._pixmap:
            self._viewer.setPixmap(self._pixmap)
        editor_plugin.add_panel(self._viewer)

    @on_plugin_available(plugin=Plugins.ClipboardWatcher)
    def on_clipboard_plugin_available(self):
        clipboard_plugin: ClipboardWatcherPlugin = self.get_plugin(Plugins.ClipboardWatcher)
        clipboard_plugin.sig_clipboard_changed.connect(self.on_clipboard_changed)
        self.on_clipboard_changed()

    @Slot()
    def on_clipboard_changed(self):
        clipboard_plugin: ClipboardWatcherPlugin = self.get_plugin(Plugins.ClipboardWatcher)
        self._pixmap = clipboard_plugin.pixmap
        if self._pixmap and self._viewer:
            self._viewer.setPixmap(self._pixmap)