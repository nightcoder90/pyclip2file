import logging
from optparse import Option
from typing import Optional, List
from PySide2.QtCore import Signal, Slot
from PySide2.QtGui import QPixmap
from pyclip2file.api.plugin import Plugin, Plugins
from pyclip2file.api.decorators import on_plugin_available
from pyclip2file.plugins.editor.plugin import EditorPlugin
from pyclip2file.plugins.fileexporter.plugin import FileExporterPlugin
from pyclip2file.plugins.postprocessor.engine import PostProcessorEngine
from pyclip2file.plugins.editor.editorpanel import GroupBoxEditorPanel
from pyclip2file.widgets.layoutbuilder import LayoutBuilder

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PostProcessorPanel(GroupBoxEditorPanel):
    def __init__(self):
        GroupBoxEditorPanel.__init__(self, 'Z2.Post-processor')
        self.setTitle('Post-process')


class PostProcessorPlugin(Plugin):
    NAME = "post_processor"
    REQUIRES = [Plugins.Editor, Plugins.FileExporter]


    sig_transformed_pixmap_changed = Signal()

    def on_initialize(self):
        self._engine: Optional[PostProcessorEngine] = PostProcessorEngine()
        self._panel: Optional[PostProcessorPanel] = None

    @on_plugin_available(plugin=Plugins.Editor)
    def on_editor_plugin_available(self):
        editor_plugin: EditorPlugin = self.get_plugin(Plugins.Editor)

        if not self._engine:
            self._engine = PostProcessorEngine()
        if not self._panel:
            self._panel = PostProcessorPanel()
            layout_builder = LayoutBuilder()
            self._engine.add_to_layout(layout_builder=layout_builder)
            layout_builder.attach_to(self._panel)
        editor_plugin.add_panel(self._panel)

    @on_plugin_available(plugin=Plugins.FileExporter)
    def on_file_exporter_plugin_available(self):
        exporter_plugin: FileExporterPlugin = self.get_plugin(Plugins.FileExporter)
        exporter_plugin.sig_exported.connect(self.on_file_exported)

    @Slot(str)
    def on_file_exported(self, path: str):
        logger.debug(f'on_file_exported({path})')
        self._engine.process(path)