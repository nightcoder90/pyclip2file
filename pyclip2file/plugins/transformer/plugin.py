import logging
from typing import Optional, List
from PySide2.QtCore import Signal, Slot
from PySide2.QtGui import QPixmap
from pyclip2file.api.plugin import Plugin, Plugins
from pyclip2file.api.decorators import on_plugin_available
from pyclip2file.plugins.editor.plugin import EditorPlugin
from pyclip2file.plugins.clipboardwatcher.plugin import ClipboardWatcherPlugin
from pyclip2file.plugins.transformer.panel import TransformerPanel
from pyclip2file.plugins.transformer.basetransformer import BaseTransformer
from pyclip2file.plugins.transformer.manager import TransformerManager
from pyclip2file.widgets.layoutbuilder import LayoutBuilder

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

class TransformerPlugin(Plugin):
    NAME = "transformer"
    REQUIRES = [Plugins.Editor, Plugins.ClipboardWatcher]


    sig_transformed_pixmap_changed = Signal()

    def on_initialize(self):
        self._panel: Optional[TransformerPanel] = None
        self._manager = TransformerManager()
        self._manager.sig_transformed_pixmap_changed.connect(self.sig_transformed_pixmap_changed)

    def before_mainwindow_visible(self):
        assert self._panel
        logger.debug(f'{__class__}.before_mainwindow_visible')
        layout_builder = LayoutBuilder()
        logger.debug(f'layout_builder: {layout_builder}')
        self._manager.add_to_layout(layout_builder=layout_builder)
        logger.debug(f'layout_builder: {layout_builder}')
        layout_builder.attach_to(self._panel)
        return super().before_mainwindow_visible()

    @on_plugin_available(plugin=Plugins.Editor)
    def on_editor_plugin_available(self):
        editor_plugin: EditorPlugin = self.get_plugin(Plugins.Editor)
        if not self._panel:
            self._panel = TransformerPanel()
        editor_plugin.add_panel(self._panel)

    @on_plugin_available(plugin=Plugins.ClipboardWatcher)
    def on_clipboard_plugin_available(self):
        logger.warn('clipboard available!')
        clipboard_plugin: ClipboardWatcherPlugin = self.get_plugin(Plugins.ClipboardWatcher)
        clipboard_plugin.sig_clipboard_changed.connect(self.on_clipboard_changed)
        self.on_clipboard_changed()

    def register_transformer(self, transformer: BaseTransformer):
        self._manager.register_transformer(transformer)


    def transformed_pixmap(self):
        return self._manager.transformed_pixmap

    @Slot()
    def on_clipboard_changed(self):
        clipboard_plugin: ClipboardWatcherPlugin = self.get_plugin(Plugins.ClipboardWatcher)
        pixmap = clipboard_plugin.pixmap
        self._manager.set_original_pixmap(pixmap)