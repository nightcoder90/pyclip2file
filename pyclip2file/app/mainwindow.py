import sys
import logging
from PySide2.QtWidgets import QApplication, QMainWindow
from pyclip2file.api.registry import PLUGIN_REGISTRY
from pyclip2file.app.find_plugins import find_plugins


logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setup()

    def get_plugin(self, plugin_name):
        if plugin_name in PLUGIN_REGISTRY:
            return PLUGIN_REGISTRY.get_plugin(plugin_name)
        else:
            raise Exception(f'Plugin {plugin_name} not found!')

    def setup(self):
        plugins = find_plugins()
        for plugin in list(plugins.values())[::-1]:
            logger.info(f'Registering Plugin: {plugin.NAME}')
            PLUGIN_REGISTRY.register_plugin(self, plugin)

def setup_logger():
    from logging import Formatter, StreamHandler, getLogger
    fmt = Formatter('%(asctime)s [%(levelname)s] [%(name)s] -> %(message)s')
    h = StreamHandler()
    h.setFormatter(fmt)
    logger = getLogger()
    logger.addHandler(h)
    logger.setLevel('DEBUG')

def main():
    setup_logger()
    app = QApplication()
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()