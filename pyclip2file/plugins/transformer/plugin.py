import logging
from typing import Optional, List
from PySide2.QtCore import Signal
from pyclip2file.api.plugin import Plugin, Plugins
from pyclip2file.api.decorators import on_plugin_available
from pyclip2file.plugins.editor.plugin import EditorPlugin
from pyclip2file.plugins.transformer.panel import TransformerPanel
from pyclip2file.plugins.transformer.basetransformer import BaseTransformer
from pyclip2file.widgets.layoutbuilder import LayoutBuilder

logger = logging.getLogger(__name__)


class TransformerPlugin(Plugin):
    NAME = "transformer"
    REQUIRES = [Plugins.Editor]

    sig_pixmap_changed = Signal()

    def on_initialize(self):
        self._panel: Optional[TransformerPanel] = None
        self._transformers: List[BaseTransformer] = []

    def before_mainwindow_visible(self):
        assert self._panel
        logger.info(f'{__class__}.before_mainwindow_visible')
        layout_builder = LayoutBuilder()
        self._transformers.sort(key=lambda tf: tf.ID)
        logger.info(f'self._transformers: {self._transformers}')
        for transformer in self._transformers:
            transformer.add_to_layout(layout_builder=layout_builder.finish_row())
        layout_builder.attach_to(self._panel)
        return super().before_mainwindow_visible()

    @on_plugin_available(plugin=Plugins.Editor)
    def on_editor_plugin_available(self):
        editor_plugin: EditorPlugin = self.get_plugin(Plugins.Editor)
        if not self._panel:
            self._panel = TransformerPanel()
        editor_plugin.add_panel(self._panel)

    def add_transformer(self, transformer: BaseTransformer):
        self._transformers.append(transformer)
