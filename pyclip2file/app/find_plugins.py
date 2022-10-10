import logging
import pkg_resources
import importlib


logger = logging.getLogger(__name__)

def find_plugins():
    """
    Find plugins based on setuptools entry points.
    """
    logger.info('find_plugins')

    entry_points = list(pkg_resources.iter_entry_points('pyclip2file.plugins'))
    logger.info(f'entry_points: {entry_points}')

    plugins = {}

    for entry_point in entry_points:
        name = entry_point.name
        class_name = entry_point.attrs[0]
        mod = importlib.import_module(entry_point.module_name)
        plugin_class = getattr(mod, class_name, None)
        plugins[name] = plugin_class
    
    return plugins