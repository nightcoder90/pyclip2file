from re import S
from typing import Optional
from pyclip2file.api.plugin import Plugin, Plugins
from pyclip2file.api.decorators import on_plugin_available
from pyclip2file.plugins.editor.plugin import EditorPlugin
from pyclip2file.plugins.scaler.panel import ScalerPanel


class ScalerPlugin(Plugin):
    NAME = "scaler"
    REQUIRES = [Plugins.Editor]

    def on_initialize(self):
        self._panel: Optional[ScalerPanel] = None

    @on_plugin_available(plugin=Plugins.Editor)
    def on_editor_plugin_available(self):
        editor_plugin: EditorPlugin = self.get_plugin(Plugins.Editor)
        if not self._panel:
            self._panel = ScalerPanel()
        editor_plugin.add_panel(self._panel)