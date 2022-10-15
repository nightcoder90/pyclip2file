import logging
from pyclip2file.api.plugin import Plugin, Plugins
from pyclip2file.api.decorators import on_plugin_available
from pyclip2file.plugins.transformer.plugin import TransformerPlugin
from pyclip2file.plugins.scaletransformer.transformer import ScaleTransformer

logger = logging.getLogger(__name__)

class ScaleTransformerPlugin(Plugin):
    NAME = "scale_transformer"
    REQUIRES = [Plugins.Transformer]

    def on_initialize(self):
        pass

    @on_plugin_available(plugin=Plugins.Transformer)
    def on_transformer_plugin_available(self):
        logger.info(f'{__class__}.on_transformer_plugin_available')
        transformer_plugin: TransformerPlugin = self.get_plugin(Plugins.Transformer)
        transformer_plugin.register_transformer(ScaleTransformer())