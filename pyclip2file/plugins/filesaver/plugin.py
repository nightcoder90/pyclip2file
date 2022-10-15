import logging
from typing import Optional

from PySide2.QtCore import Slot
from PySide2.QtGui import QPixmap
from pyclip2file.api.plugin import Plugin
from pyclip2file.api.decorators import on_plugin_available
from pyclip2file.api.plugin import Plugins
from pyclip2file.plugins.transformer.plugin import TransformerPlugin
from pyclip2file.plugins.editor.plugin import EditorPlugin
from pyclip2file.plugins.filesaver.panel import FileSaverPanel
from pyclip2file.plugins.filesaver.macroexpander import MacroExpander, datetime_expander

logger = logging.getLogger(__name__)


class FileSaverPlugin(Plugin):
    NAME = 'file_saver'
    REQUIRES = [Plugins.Transformer, Plugins.Editor]

    def create_panel(self):
        panel = FileSaverPanel()
        panel.sig_save_requested.connect(self.on_save_requested)
        return panel

    def on_initialize(self):
        self._panel: Optional[FileSaverPanel] = None
        self._pixmap: Optional[QPixmap] = None
        self._macro_expander = MacroExpander()
        self._macro_expander.register_variable('%{DATETIME}', 'datetime', datetime_expander)

    @on_plugin_available(plugin=Plugins.Editor)
    def on_editor_plugin_available(self):
        editor_plugin: EditorPlugin = self.get_plugin(Plugins.Editor)

        if not self._panel:
            self._panel = self.create_panel()
        if self._pixmap:
            self._panel.save_enable(True)
        editor_plugin.add_panel(self._panel)

    @on_plugin_available(plugin=Plugins.Transformer)
    def on_clipboard_plugin_available(self):
        logger.warn('clipboard available!')
        transformer_plugin: TransformerPlugin = self.get_plugin(Plugins.Transformer)
        transformer_plugin.sig_transformed_pixmap_changed.connect(self.on_pixmap_changed)
        self.on_pixmap_changed()

    @Slot()
    def on_pixmap_changed(self):
        transformer_plugin: TransformerPlugin = self.get_plugin(Plugins.Transformer)
        if self._pixmap == transformer_plugin.transformed_pixmap():
            return
        self._pixmap = transformer_plugin.transformed_pixmap()
        if  self._pixmap and self._panel:
            self._panel.save_enable(True)

    @Slot(str)
    def on_save_requested(self, path: str):
        if not path:
            logger.warn('Null path')
        if not self._pixmap:
            logger.warn('Null pixmap')
        expanded_path = self._macro_expander.expand(path)
        logger.warn(f'Saving...{expanded_path}')
        self._pixmap.save(expanded_path)
