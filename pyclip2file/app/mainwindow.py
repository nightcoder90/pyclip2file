import sys
import logging
from PySide2.QtWidgets import QApplication, QMainWindow
from pyclip2file.api.registry import PLUGIN_REGISTRY
from pyclip2file.api.plugin import Plugin
from pyclip2file.app.find_plugins import find_plugins


logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('pyclip2file')
        self.setup()

    def get_plugin(self, plugin_name: str) -> Plugin:
        if plugin_name in PLUGIN_REGISTRY:
            return PLUGIN_REGISTRY.get_plugin(plugin_name)
        else:
            raise Exception(f'Plugin {plugin_name} not found!')

    def setup(self) -> None:
        plugins = find_plugins()
        for plugin in list(plugins.values())[::-1]:
            logger.info(f'Registering Plugin: {plugin.NAME}')
            PLUGIN_REGISTRY.register_plugin(self, plugin)

    def pre_visible_setup(self):
        logger.info('Setting up window...')
        for plugin_name in PLUGIN_REGISTRY:
            plugin_instance = PLUGIN_REGISTRY.get_plugin(plugin_name)
            try:
                plugin_instance.before_mainwindow_visible()
            except AttributeError:
                pass

def setup_logger():
    from logging import Formatter, StreamHandler, getLogger
    fmt = Formatter('%(asctime)s [%(levelname)s] [%(name)s] -> %(message)s')
    h = StreamHandler()
    h.setFormatter(fmt)
    logger = getLogger()
    logger.addHandler(h)
    logger.setLevel(logging.WARN)

def main():
    setup_logger()
    app = QApplication()
    mainwindow = MainWindow()
    mainwindow.pre_visible_setup()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()