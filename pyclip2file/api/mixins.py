class PluginObserver:
    """
    This mixin enables a class to receive notifications when a plugin 
    is available, by registering methods using the
    :function:`pyclip2file.api.descorators.on_plugin_available`
    decorator.

    When any of the requested plugins is ready, the corresponding registered 
    method is called.
    """

    def __init__(self):
        self._plugin_listeners = {}

        for method_name in dir(self):
            method = getattr(self, method_name, None)
            if hasattr(method, '_plugin_listen'):
                plugin_listen = method._plugin_listen

                self._plugin_listeners[plugin_listen] = method_name

    def _on_plugin_available(self, plugin: str):
        if plugin in self._plugin_listeners:
            method_name = self._plugin_listeners[plugin]
            method = getattr(self, method_name)
            method()
