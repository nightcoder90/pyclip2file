import logging
from pyclip2file.api.plugin import Plugin
from pyclip2file.plugins.editor.editorwidget import EditorWidget
from pyclip2file.plugins.editor.editorpanel import EditorPanelMixin

logger = logging.getLogger(__name__)

class EditorPlugin(Plugin):
    NAME = 'editor'

    def on_initialize(self):
        self._editor_widget = EditorWidget()
        logger.info(self._main)
        self._main.setCentralWidget(self.editor_widget)

    @property
    def editor_widget(self):
        return self._editor_widget

    def add_panel(self, panel: EditorPanelMixin):
        self._editor_widget.add_panel(panel)