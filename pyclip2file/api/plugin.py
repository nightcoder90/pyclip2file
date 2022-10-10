from PySide2.QtCore import QObject, Signal, Slot
from pyclip2file.api.mixins import PluginObserver


class Plugins:
    """
    Convenience class for accessing internal plugins.
    """
    Clipboard = 'clipboard'
    Editor = 'editor'
    FileSaver = 'file_saver'
    Preview = 'preview'
    Scaler = 'scaler'


class Plugin(QObject, PluginObserver):
    """
    A plugin to extend functionality.
    """

    # Name of the plugin that will be used to refer to it.
    # This name must be unique and will only be loaded once.
    NAME = None

    # List of required plugin dependencies.
    # Example: [Plugins.Editor, Plugins.Preview, ...].
    # These values are defined in the `Plugins` class present in this file.
    # If a plugin is using a widget from another plugin, that other
    # must be declared as a required dependency.
    REQUIRES = []


    sig_plugin_ready = Signal()
    """
    This signal can be emitted to reflect that the plugin was initialized.
    """

    def __init__(self, parent):
        QObject.__init__(self, parent)
        PluginObserver.__init__(self)
        self._main = parent

    def get_plugin(self, plugin_name):
        requires = set(self.REQUIRES)

        if plugin_name in requires:
            try:
                return self._main.get_plugin(plugin_name)
            except Exception as e:
                raise e
        else:
            raise Exception(f'Plugin {plugin_name} not part of REQUIRES!')

    def initialize(self):
        self.on_initialize()
        self.sig_plugin_ready.emit()
        
    def on_initialize(self):
        raise NotImplementedError(
            f'The plugin {type(self)} is missing an implementation of on_initialize'
        )