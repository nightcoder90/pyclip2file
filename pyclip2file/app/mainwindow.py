import sys
from PySide2.QtCore import (QCoreApplication)
from PySide2.QtWidgets import (QApplication, QMainWindow, QLabel)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        label = QLabel('Hello World')
        self.setCentralWidget(label)

def main():
    app = QApplication()
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

        