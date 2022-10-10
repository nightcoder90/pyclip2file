import logging

from typing import Type, Any, List
from PySide2.QtCore import QObject
from pyclip2file.api.plugin import Plugin

logger = logging.getLogger(__name__)


class PluginRegistry(QObject):
    def __init__(self):
        super().__init__()

        # Plugin dictionary mapped by their names
        self.plugin_registry = {}
        self.plugin_availability = {}
        self.plugin_dependencies = {}
        self.plugin_dependents = {}

    def get_plugin(self, plugin_name: str) -> Plugin:
        """
        Get a reference to a plugin instance by its name.

        Parameters
        ----------
        plugin_name: str
            Name of the plugin to retreive.

        Returns
        -------
        plugin: Plugin
            The instance of the requested plugin.
        """
        if plugin_name in self.plugin_registry:
            plugin_instance = self.plugin_registry[plugin_name]
            return plugin_instance
        else:
            raise Exception(f'Plugin {plugin_name} was not found in the registry')

    def register_plugin(self, main_window: Any, PluginClass: Type[Plugin]) -> Plugin:
        """
        Register a plugin into the registry.

        Parameters
        ----------
        main_window: pyclip2file.app.mainwindow.MainWindow
            Reference to pyclip2file's main window.
        PluginClass: Type[Plugin]
            The plugin class to register and create.
            It must be one of `pyclip2file.api.plugin.Plugin

        Returns
        -------
        plugin: Plugin
            The instance of the registered plugin.
        """
        if not issubclass(PluginClass, Plugin):
            raise TypeError(f'{PluginClass} does not inherit from {Plugin}')
        instance = self._initiate_plugin(main_window, PluginClass)
        return instance

    def _initiate_plugin(self, main_window: Any, PluginClass: Type[Plugin]) -> Plugin:
        required_plugins = list(set(PluginClass.REQUIRES))
        plugin_name = PluginClass.NAME
        self._update_plugin_info(plugin_name, required_plugins)
        plugin_instance = PluginClass(main_window)
        self.plugin_registry[plugin_name] = plugin_instance
        logger.info(f'Registered {plugin_name}')
        plugin_instance.sig_plugin_ready.connect(
            lambda: self.notify_plugin_availablity(plugin_name)
        )
        plugin_instance.initialize()

        self._notify_plugin_dependencies(plugin_name)
        return plugin_instance

    def notify_plugin_availablity(self, plugin_name: str):
        """
        Notify dependent plugins of a given plugin of its availability.

        Parameters
        ----------
        plugin_name: str
            Name of the plugin that is available.
        """
        logger.info(f'Plugin {plugin_name} has finished loading sending notifications')

        self.plugin_availability[plugin_name] = True

        plugin_dependents = self.plugin_dependents.get(plugin_name, [])

        for plugin in plugin_dependents:
            if plugin in self.plugin_registry:
                logger.info(f'Notifying {plugin}._on_plugin_available({plugin_name})')
                plugin_instance = self.plugin_registry[plugin]
                plugin_instance._on_plugin_available(plugin_name)

    
    def _notify_plugin_dependencies(self, plugin_name: str) -> None:
        """Notify a plugin of its available dependencies."""
        plugin_instance = self.plugin_registry[plugin_name]
        plugin_dependencies = self.plugin_dependencies.get(plugin_name, [])

        for plugin in plugin_dependencies:
            if self.plugin_availability.get(plugin, False):
                logger.info(f'Notifying {plugin_name}._on_plugin_available({plugin})')
                plugin_instance._on_plugin_available(plugin)

    def _update_plugin_info(self, plugin_name: str, plugin_dependencies: List[str]):
        """Update the dependencies and dependents of `plugin_name`."""
        for plugin in plugin_dependencies:
            self._update_dependencies(plugin_name, plugin)
            self._update_dependents(plugin, plugin_name)

    def _update_dependencies(self, plugin: str, dependency_plugin: str):
        """Add `dependency_plugin` to the list of dependencies of `plugin`."""
        plugin_dependencies = self.plugin_dependencies.get(plugin, [])
        plugin_dependencies.append(dependency_plugin)
        self.plugin_dependencies[plugin] = plugin_dependencies

    def _update_dependents(self, plugin: str, dependent_plugin: str):
        """Add `dependent_plugin` to the list of dependents of `plugin`."""
        plugin_dependents = self.plugin_dependents.get(plugin, [])
        plugin_dependents.append(dependent_plugin)
        self.plugin_dependents[plugin] = plugin_dependents

    def __contains__(self, plugin_name: str) -> bool:
        """
        Determine if a plugin name is contained in the registry.

        Parameters
        ----------
        plugin_name: str
            Name of the plugin to seek.

        Returns
        -------
        is_contained: bool
            If True, the plugin name is contained on the registry, False otherwise.
        """
        return plugin_name in self.plugin_registry
    
    def __iter__(self):
        return iter(self.plugin_registry)


PLUGIN_REGISTRY = PluginRegistry()