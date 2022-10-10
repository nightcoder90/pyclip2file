from typing import Callable, Optional
import functools

def on_plugin_available(func: Callable = None,
                        plugin: Optional[str] = None):
    """
    Method decorator used to handle plugin availability.

    The methods that use this decorator must have the folowing signature:
    `def method(self)` when observing a single plugin or
    `def method(self, plugin): ...` when observing mutiple plugins or
    all plugins that were listed as dependencies.

    Parameters
    ----------
    func: Callable
        Method to decorate. Given by default when applying the decorator.
    plugin: Optional[str]
        Name of the requested plugin whose availability triggers the method.

    Returns
    -------
    func: Callable
        The same method that was given as input.
    """
    if func is None:
        return functools.partial(on_plugin_available, plugin=plugin)
    
    if plugin is None:
        plugin = '__all'

    func._plugin_listen = plugin
    return func